## 修改需求

### 需求:系统必须采集当前 session 的 token 消耗数据

在归档变更时，系统必须调用 `ccusage` 工具获取当前项目 session 的 token 消耗统计。

**原有行为**: 获取 session 累计 token 值并直接记录

**新增行为**:
1. 检查 `.openspec.yaml` 中是否存在 `baseline_tokens`
2. 如果存在，计算差值并记录
3. 如果不存在，使用当前值并打印警告

#### 场景:成功获取 token 数据（有基准）
- **当** `ccusage` 已安装且当前 session 有数据，且存在 `baseline_tokens`
- **那么** 系统计算 token 差值（当前 - 基准），记录差值到 CSV

#### 场景:成功获取 token 数据（无基准）
- **当** `ccusage` 已安装且当前 session 有数据，但无 `baseline_tokens`
- **那么** 系统使用当前 token 值，打印"警告: 无基准 token，使用累计值"

#### 场景:ccusage 未安装
- **当** `ccusage` 命令不存在
- **那么** 系统提示用户是否安装，token 相关字段写入空值