---
name: "XT: OpenSpec 增强初始化"
description: 初始化 OpenSpec 增强功能，为 opsx 命令添加 Git 状态检查和归档增强
category: 工具
tags: [setup, git, enhance]
---

初始化 OpenSpec 增强功能，为 opsx 命令添加增强功能。

## 功能说明

执行此命令后将启用以下增强：

### 1. Git 状态检查（创建变更前）

| 命令 | 检查时机 |
|------|----------|
| `/opsx:new` | 创建变更前 |
| `/opsx:propose` | 创建变更前 |
| `/opsx:ff` | 创建变更前 |

### 2. 归档增强（归档成功后）

| 命令 | 增强内容 |
|------|----------|
| `/opsx:archive` | 代码变更统计 + Commit 提示 |
| `/opsx:bulk-archive` | 代码变更统计 + Commit 提示 |

## 步骤

1. **检查是否已初始化**

   读取 `.claude/commands/opsx/new.md`，检查是否包含 `步骤 0：检查 Git 状态`。

   - 如果已包含：提示"增强功能已初始化，无需重复操作"
   - 如果未包含：继续下一步

2. **注入 Git 检查代码（创建变更命令）**

   在以下文件的 `**步骤**` 后、`1. **如果没有提供输入` 前，插入检查代码：

   - `.claude/commands/opsx/new.md`
   - `.claude/commands/opsx/propose.md`
   - `.claude/commands/opsx/ff.md`

   **注入内容**：
   ```markdown

   0. **检查 Git 状态**

      运行 Git 状态检查脚本：
      ```bash
      python .claude/skills/xt-openspec-enhance/scripts/check_git_status.py
      ```

      - 返回码 `0`：Git 干净，继续下一步
      - 返回码 `1`：显示 git 状态，等待用户处理并输入"继续"后再重试

   ```

3. **注入归档增强代码（归档命令）**

   在以下文件的 `**防护措施**` 前添加新步骤：

   - `.claude/commands/opsx/archive.md`
   - `.claude/commands/opsx/bulk-archive.md`

   **注入内容**（在步骤 6 "显示摘要" 后添加）：
   ```markdown

   7. **代码变更统计**

      运行统计脚本：
      ```bash
      python .claude/skills/xt-openspec-enhance/scripts/archive_with_stats.py
      ```

      脚本自动完成：
      - 计算自上次提交以来的代码变更
      - 追加记录到 `openspec/ai.summary.csv`
      - 输出统计摘要

   8. **Commit 提示**

      显示变更摘要并询问用户是否提交：

      ```
      ## 归档增强

      **变更统计**：
      - 新增行数：<additions>
      - 删除行数：<deletions>
      - 变更文件：<changed_files>

      是否执行 git commit 提交本次变更？
      输入 '是' 或 '提交' 确认，或其他内容跳过
      ```

      - 用户确认：执行 `git add . && git commit -m "<change-name>: <description>"`
      - 用户跳过：提示用户后续手动提交

   ```

4. **更新步骤编号**

   将原命令中的后续步骤编号顺延。

5. **显示完成信息**

   ```
   ## 初始化完成

   已为以下命令添加增强功能：

   **Git 状态检查**：
   - /opsx:new
   - /opsx:propose
   - /opsx:ff

   **归档增强**：
   - /opsx:archive
   - /opsx:bulk-archive
   ```

## 恢复原始状态

如需恢复 opsx 命令到原始状态，运行 `/xt-openspec-enhance:restore`。

## 注意事项

- opsx 升级后可能覆盖修改，需要重新运行此命令
- 建议在每次 opsx 升级后检查增强功能是否生效