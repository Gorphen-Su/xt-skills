## 为什么

当前代码统计将 `openspec/` 目录下的所有文件变更都计入代码行数，但实际上该目录中的 markdown 文件（如 proposal.md、design.md、tasks.md、spec.md 等）是 AI 辅助开发过程的产物，不属于真正的代码内容。这导致代码统计不准确，无法区分"实际代码"和"规范文档"。需要将规范文档统计分离为独立维度，以便更准确地评估代码产出。

## 变更内容

- **修改**: 代码统计逻辑，排除 `openspec/` 目录下的 markdown 文件
- **新增**: 规范文档统计维度，包括 `spec_files`（文件总数）和 `spec_lines`（总行数）
- **扩展**: CSV 输出格式，增加两个新列

## 功能 (Capabilities)

### 新增功能
- `spec-stats`: 独立统计规范文档（openspec/ 目录下的 markdown 文件）的数量和行数

### 修改功能
- `code-stats`: 代码统计排除 openspec/ 目录下的 markdown 文件，仅统计真正的代码文件

## 影响

- `archive_with_stats.py` - 核心统计脚本
- `openspec/ai.summary.csv` - 新增 `spec_files` 和 `spec_lines` 字段
- 现有代码统计数据可能需要重新理解（排除规范文档后数值会变小）