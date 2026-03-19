---
name: "XT: 归档"
description: 归档已完成的 OpenSpec 变更（ xt 封装层，包含代码变更统计）
category: 工作流
tags: [workflow, archive]
---

此命令是 `opsx:archive` 的封装层，用于项目定制。

**扩展功能**：
- 在归档完成后自动执行 `scripts/archive_with_stats.py` 脚本
- 将代码变更统计追加到 `openspec/ai.summary.csv` 文件

**重要规则**：
- ✅ 归档是文件系统操作（移动目录）
- ✅ 可以使用 `git add` 暂存变更
- ❌ **禁止主动执行 `git commit`**
- ❌ **禁止自动提交到远程仓库**

详见：[`.claude/commands/opsx/archive.md`](./opsx/archive.md)
