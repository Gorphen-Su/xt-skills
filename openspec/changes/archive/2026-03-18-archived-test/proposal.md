## 为什么

本次变更旨在测试 `xt:archive` 命令的完整工作流程，包括归档完成后自动收集代码变更统计的功能。

## 变更内容

- 测试 `xt:archive` 命令归档流程
- 验证 `scripts/archive_with_stats.py` 脚本在归档完成后自动执行
- 验证代码变更统计正确写入 `openspec/ai.summary.csv`

## 功能 (Capabilities)

### 新增功能
- `archive-stats`: 封装 `xt:archive` 和 `xt:bulk-archive` 命令，增加归档完成后自动收集代码变更统计的功能

### 修改功能
无

## 影响

- 新增脚本：`scripts/collect_git_stats.py` - 基础统计脚本
- 新增脚本：`scripts/archive_with_stats.py` - 归档统计脚本
- 新增目录：`scripts/` - 存放统计脚本
