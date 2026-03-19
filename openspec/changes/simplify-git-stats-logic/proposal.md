## Why

`archive_with_stats.py` 脚本在统计 git 代码变更时收集了 `branch`（分支）和 `repository`（仓库名称）字段，但这些信息在当前使用场景中并非必需，反而增加了不必要的复杂度。简化统计逻辑，移除这两个字段，使脚本更专注地收集核心代码变更指标。

## What Changes

- 移除 `archive_with_stats.py` 中的 `branch` 和 `repository` 字段收集逻辑
- 更新 CSV 表头，移除 `branch` 和 `repository` 列
- 更新 `archive-stats.md` 规范中字段定义

## Capabilities

### New Capabilities
- `simplified-git-stats`: 简化 git 代码变更统计，仅保留核心字段（id、author、timestamp、additions、deletions、changed_files、changed_functions、total_lines、project_name）

### Modified Capabilities
None

## Impact

- `scripts/archive_with_stats.py`: 移除 `get_current_branch()` 和 `get_project_name()` 中的 repository 提取逻辑，简化 `collect_stats()` 返回值
- `openspec/specs/archive-stats.md`: 更新字段定义文档
- `openspec/ai.summary.csv`: 表格结构变更（移除最后两列）
