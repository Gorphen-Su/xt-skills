---
name: "XT: 批量归档"
description: 批量归档多个已完成的 OpenSpec 变更（ xt 封装层，包含代码变更统计）
category: 工作流
tags: [workflow, archive]
---

转发到 `opsx:bulk-archive` 命令，并在每个变更归档完成后自动收集代码变更统计。

**输入**：可选择指定多个变更名称或使用通配符。

**扩展功能**
- 每个变更归档完成后自动执行 `scripts/archive_with_stats.py` 脚本
- 将代码变更统计追加到 `openspec/ai.summary.csv` 文件

详见：`.claude/commands/opsx/bulk-archive.md`
