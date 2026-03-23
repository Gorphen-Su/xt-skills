## 为什么

当前 token 统计记录的是整个 session 的累计值（91M），而不是单个变更周期的实际消耗（20.5M/天）。这导致统计数据无法准确反映每个变更的真实 token 成本。需要在变更开始时记录基准 token，归档时计算差值，才能得到准确的变更级别 token 统计。

## 变更内容

- **新增**: 在 `opsx:new` / `opsx:propose` 时记录基准 token 到 `.openspec.yaml`
- **修改**: 在 `opsx:archive` 时计算 token 差值（当前 - 基准）
- **新增**: `.openspec.yaml` 中增加 `baseline_tokens` 字段存储基准值

## 功能 (Capabilities)

### 新增功能
- `baseline-token-tracking`: 在变更开始时记录 token 基准，归档时计算实际消耗

### 修改功能
- `token-tracking`: 修改 token 统计逻辑，从累计值改为增量值计算

## 影响

- `.openspec.yaml` 文件格式（新增 `baseline_tokens` 字段）
- `archive_with_stats.py` 脚本（计算 token 差值）
- 可能需要修改 opsx 命令的 skill 文件以在变更创建时记录基准