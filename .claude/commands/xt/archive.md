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

详见：[`.claude/commands/opsx/archive.md`](./opsx/archive.md)
