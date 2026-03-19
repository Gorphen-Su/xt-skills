# CLAUDE.md - 项目上下文

## 项目概述

**xt-skills** - 一个基于 OpenSpec 的变更管理工具项目，提供 `xt:*` 和 `opsx:*` 命令集。

## 重要规则

### Git 提交规则
- ✅ 可以修改代码文件
- ✅ 可以使用 `git add` 暂存文件
- ❌ **禁止主动执行 `git commit`**
- ❌ **禁止自动提交到远程仓库**

所有 git 提交操作必须等待用户明确授权。

### OpenSpec 变更流程

项目使用 OpenSpec 进行变更管理，主命令为 `xt:*` 系列：

| 命令 | 描述 |
|------|------|
| `xt:new` | 启动新变更 |
| `xt:propose` | 快速提案新变更并生成所有产出物 |
| `xt:apply` | 实现变更中的任务 |
| `xt:archive` | 归档已完成的变更（含代码变更统计） |
| `xt:continue` | 继续创建产出物 |
| `xt:bulk-archive` | 批量归档多个变更 |
| `xt:sync` | 同步增量规范到主规范 |
| `xt:verify` | 验证实现是否与产出物匹配 |
| `xt:explore` | 探索模式，构思想法和澄清需求 |

### archive_with_stats 脚本

`scripts/archive_with_stats.py` 用于在归档时收集代码变更统计：

**CSV 格式**：
```
id,author,timestamp,additions,deletions,changed_files,changed_functions,total_lines,project_name
```

已移除的字段：
- `branch` - 分支名称
- `repository` - 仓库名称

## 目录结构

```
..
├── .claude/
│   ├── commands/     # xt:* 和 opsx:* 命令定义
│   ├── skills/       # Claude 技能定义
│   └── settings.local.json
├── cursor/           # Cursor IDE 同步的命令和技能
├── openspec/
│   ├── changes/      # 变更目录
│   │   ├── archive/  # 归档的变更
│   │   └── <change-name>/
│   └── ai.summary.csv
└── scripts/
    └── archive_with_stats.py
```

## 技术栈

- Python 3 (用于脚本)
- Markdown (配置和文档)
- Git (版本控制)
