---
name: "XT: 归档"
description: 归档已完成的 OpenSpec 变更（ xt 封装层，包含代码变更统计）
category: 工作流
tags: [workflow, archive]
---

转发到 `opsx:archive` 命令，并在归档完成后自动收集代码变更统计。

**输入**：可选择在 `/xt:archive` 后指定变更名称。

**扩展功能**
- 归档完成后自动执行 `scripts/archive_with_stats.py` 脚本
- 将代码变更统计追加到 `openspec/ai.summary.csv` 文件

**统计字段**
- `id`: 随机 UUID
- `author`: 当前 git 操作人
- `timestamp`: 处理时间（日期时分秒）
- `additions`: 新增行数
- `deletions`: 删除行数
- `changed_files`: 变更文件数
- `changed_functions`: 变更函数列表（分号分隔）
- `total_lines`: 总行数
- `project_name`: 所属项目名称
- `branch`: 当前分支
- `repository`: 仓库名称

详见：`.claude/commands/opsx/archive.md`
