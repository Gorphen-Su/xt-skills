---
name: "XT: OpenSpec 增强版"
description: 基于 OpenSpec 的变更管理增强层，提供 Git 状态检查和代码变更统计功能
---

# XT: OpenSpec 增强版

## 设计原则

此增强层通过独立 skill 实现，与 `xt-openspec-wrapper` 完全隔离：

1. **Git 状态检查**：在启动变更前强制检查 git 状态是否干净
2. **代码变更统计**：归档时自动统计代码变更并写入 CSV
3. **归档后 Commit 提示**：归档完成后提示用户提交代码
4. **主动初始化**：用户执行 init 命令后才启用增强功能
5. **升级兼容**：opsx 升级后可重新初始化恢复增强功能

## 初始化命令

### 启用增强功能

```
/xt-openspec-enhance:init
```

执行后启用以下增强：

**Git 状态检查**（创建变更前）：
- `/opsx:new` - 启动新变更
- `/opsx:propose` - 快速提案
- `/opsx:ff` - 快速完成

**归档增强**（归档成功后）：
- `/opsx:archive` - 代码变更统计 + Commit 提示
- `/opsx:bulk-archive` - 代码变更统计 + Commit 提示

### 恢复原始状态

```
/xt-openspec-enhance:restore
```

移除所有增强功能，恢复 opsx 命令到原始状态。

## Git 状态检查

### 检查时机

当用户执行以下命令时，**必须先检查 Git 状态**：
- `/opsx:new` - 启动新变更
- `/opsx:propose` - 快速提案
- `/opsx:ff` - 快速完成

### 检查流程

```bash
python .claude/skills/xt-openspec-enhance/scripts/check_git_status.py
```

**循环检查逻辑**：
1. 运行检查脚本
2. 如果返回码 `0`：Git 干净，继续正常流程
3. 如果返回码 `1`：
   - 显示 `git status` 的详细输出
   - 提示："当前 Git 状态不干净，有未提交信息，请先处理后点击确认或者输入 '继续' 确认"
   - 等待用户处理并输入 "继续"
   - 重新运行检查脚本
   - 循环直到 Git 干净

### 用户提示示例

```
✗ Git 状态不干净，存在未提交的变更

当前状态：
------------------------------------------------------------
M   src/app.ts
??  docs/changes.md
------------------------------------------------------------

提示：当前 Git 状态不干净，有未提交信息，
请先处理后点击确认或者输入 '继续' 确认
```

## 代码变更统计

### 启用方式

通过 `/xt-openspec-enhance:init` 命令注入到 opsx 归档命令中。

### 统计时机

当用户执行以下命令且归档成功后，**自动执行统计**：
- `/opsx:archive` - 归档变更
- `/opsx:bulk-archive` - 批量归档

### 统计流程

```bash
python .claude/skills/xt-openspec-enhance/scripts/archive_with_stats.py
```

脚本自动完成：
1. 计算自上次提交以来的代码变更
2. 追加记录到 `openspec/ai.summary.csv`
3. 输出统计摘要

### CSV 字段

| 字段 | 说明 |
|------|------|
| `id` | 随机 UUID |
| `author` | 当前 Git 操作人 |
| `timestamp` | 处理时间（日期时分秒） |
| `additions` | 新增行数 |
| `deletions` | 删除行数 |
| `total_lines` | 总变更行数（additions + deletions） |
| `project_name` | 项目名称 |

### CSV 输出示例

```csv
id,author,timestamp,additions,deletions,total_lines,project_name
"abc123...","John Doe","2024-03-18 15:30:00",150,25,175,"my-project"
```

## 命令映射（原始逻辑）

以下命令由 `xt-openspec-wrapper` 提供，保持原样不变：

| XT 命令 | 原始 OPX 命令 | 描述 |
|---------|--------------|------|
| `xt:new` | `opsx:new` | 启动新变更 |
| `xt:propose` | `opsx:propose` | 快速提案 |
| `xt:ff` | `opsx:ff` | 快速完成 |
| `xt:archive` | `opsx:archive` | 归档变更 |
| `xt:apply` | `opsx:apply` | 实现任务 |
| `xt:continue` | `opsx:continue` | 继续产出物 |
| `xt:explore` | `opsx:explore` | 探索模式 |
| `xt:sync` | `opsx:sync` | 同步规范 |
| `xt:verify` | `opsx:verify` | 验证实现 |
| `xt:bulk-archive` | `opsx:bulk-archive` | 批量归档 |
| `xt:onboard` | `opsx:onboard` | 引导入门 |

## 归档后 Commit 提示

### 启用方式

通过 `/xt-openspec-enhance:init` 命令注入到 opsx 归档命令中。

### 提示时机

当用户执行以下命令且归档成功后，**提示用户提交代码**：
- `/opsx:archive` - 归档变更
- `/opsx:bulk-archive` - 批量归档

### 提示流程

1. **读取变更信息**
   - 从 `openspec/changes/archive/YYYY-MM-DD-<name>/` 读取变更目录
   - 读取 `proposal.md` 获取功能简述
   - 读取 `design.md` 获取实现细节（可选）
   - 获取变更涉及的文件列表

2. **生成 Commit 信息**
   ```
   <变更名称>: <功能简述>

   - 实现内容：<功能描述>
   - 归档时间：<timestamp>
   - 作者：<author>
   ```

3. **显示变更摘要**
   ```
   ## 归档完成

   **变更：** <change-name>
   **功能：** <功能简述>
   **归档至：** openspec/changes/archive/YYYY-MM-DD-<name>/
   **涉及文件：** <文件列表>

   Commit 信息：
   <变更名称>: <功能简述>
   ```

4. **询问用户确认**
   > "是否执行 git commit 提交本次变更？输入 '是' 或 '提交' 确认，或其他内容跳过"

5. **执行提交**
   - 用户确认：执行 `git add . && git commit -m "<生成的commit信息>"`
   - 用户跳过：提示用户后续手动提交

### 用户提示示例

```
## 归档完成

**变更：** add-user-auth
**功能：** 添加用户认证功能
**归档至：** openspec/changes/archive/2024-03-20-add-user-auth/
**涉及文件：** src/auth.ts, src/user.ts, docs/auth.md

Commit 信息：
add-user-auth: 添加用户认证功能

是否执行 git commit 提交本次变更？
输入 '是' 或 '提交' 确认，或其他内容跳过
```

## 文件结构

```
.claude/
├── commands/
│   └── xt-openspec-enhance/
│       ├── init.md              # 初始化增强功能
│       └── restore.md           # 恢复原始状态
└── skills/
    └── xt-openspec-enhance/
        ├── SKILL.md             # 本文件 - 定义增强规则
        └── scripts/
            ├── git_utils.py     # 共享工具函数
            ├── check_git_status.py  # Git 状态检查脚本
            ├── archive_with_stats.py # CSV 统计脚本
            └── commit_after_archive.py # 归档后 Commit 提示脚本
```

## 与 xt-openspec-wrapper 的关系

| 特性 | xt-openspec-wrapper | xt-openspec-enhance |
|------|---------------------|---------------------|
| 目录 | `.claude/skills/xt-openspec-wrapper/` | `.claude/skills/xt-openspec-enhance/` |
| 职责 | 纯转发层到 openspec-cn | 增强：Git 检查 + CSV 统计 |
| 初始化 | 无需初始化 | 需执行 `/xt-openspec-enhance:init` |
| 命令文件 | `.claude/commands/opsx/*.md` | init 时修改 opsx 文件 |

## 使用要求

**权限要求**（在 settings.json 中）：
```json
{
  "permissions": {
    "allow": [
      "Bash(python:*)",
      "Bash(python3:*)"
    ]
  }
}
```

**依赖**：
- Python 3.6+
- Git（已安装）

## 核心优势

1. **用户主动控制**
   - 通过 init/restore 命令控制增强功能的启用/禁用
   - 明确的操作流程，用户完全知情

2. **升级兼容**
   - opsx 升级后可重新执行 init 恢复增强功能
   - restore 命令可随时恢复原始状态

3. **集中管理**
   - 所有增强规则在 SKILL.md 中定义
   - init/restore 命令位于 `.claude/commands/xt-openspec-enhance/`
