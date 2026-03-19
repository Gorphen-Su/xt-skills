## Context

`archive_with_stats.py` 脚本在归档操作后收集代码变更统计信息，当前实现了完整的 git 环境信息收集，包括分支名、仓库名等。这些信息在某些场景下有用，但增加了逻辑复杂度。

## Goals / Non-Goals

**Goals:**
- 简化 `archive_with_stats.py` 脚本，移除 `branch` 和 `repository` 字段
- 保持 CSV 文件格式一致性（移除对应列）
- 更新相关文档以反映变更

**Non-Goals:**
- 不修改其他统计字段的收集逻辑
- 不改变 CSV 文件的存储位置和追加行为

## Decisions

1. **移除字段而非禁用**：直接删除 `branch` 和 `repository` 相关代码，而非添加配置开关。理由：简化代码逻辑，降低维护成本。

2. **分支信息移除**：`get_current_branch()` 函数将不再调用，相关代码可选择删除或保留作为潜在复用（但当前不返回该值）。

3. **仓库名称移除**：`repository` 字段（从 git root 提取的 basename）一并移除，理由：项目名称（`project_name`）已足够标识来源。

## Risks / Trade-offs

- [旧 CSV 数据兼容性] legacy CSV 文件包含 `branch` 和 `repository` 列，新脚本输出将少两列。 → 缓解：这是预期的BREAKING变更，通过归档完成时的文档更新说明。
