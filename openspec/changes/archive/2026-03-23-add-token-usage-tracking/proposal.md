## 为什么

当前 `xt-openspec-enhance` 工具在归档变更时仅收集代码行数统计（additions、deletions、total_lines），缺少对 AI 辅助开发过程中 token 消耗的追踪。随着 AI 编码工具的普及，token 消耗已成为衡量开发成本的重要指标，需要在代码采集过程中一并记录，以便进行成本分析和效率评估。

## 变更内容

- **新增功能**: 在 `archive_with_stats.py` 脚本中集成 `ccusage` 工具，采集当前 session 的 token 消耗数据
- **扩展 CSV 字段**: 在 `ai.summary.csv` 中增加 token 相关字段：
  - `input_tokens` - 输入 token 数
  - `output_tokens` - 输出 token 数
  - `cache_create_tokens` - 缓存创建 token 数
  - `cache_read_tokens` - 缓存读取 token 数
  - `total_tokens` - 总 token 数
  - `cost` - 估算成本（美元）
  - `models` - 使用的模型列表（逗号分隔）

## 功能 (Capabilities)

### 新增功能
- `token-tracking`: 在归档时自动采集并记录当前 session 的 token 消耗统计

### 修改功能
- `code-stats`: 扩展现有代码统计功能，增加 token 消耗相关字段

## 影响

- `scripts/archive_with_stats.py` - 核心统计脚本
- `openspec/ai.summary.csv` - 统计数据存储格式变更
- 依赖 `ccusage` 命令行工具（需确保已安装）