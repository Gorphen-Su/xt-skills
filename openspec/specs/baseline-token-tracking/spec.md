## 新增需求

### 需求:系统必须在变更创建时记录 token 基准

当使用 `opsx:new` 或 `opsx:propose` 创建新变更时，系统必须记录当前 session 的 token 消耗作为基准值。

#### 场景:记录基准 token
- **当** 用户执行 `opsx:new` 或 `opsx:propose` 创建变更
- **那么** 系统获取当前 session token 数据并写入 `.openspec.yaml` 的 `baseline_tokens` 字段

#### 场景:ccusage 未安装
- **当** ccusage 未安装
- **那么** `baseline_tokens` 字段留空，打印警告信息

#### 场景:基准字段格式
- **当** 记录基准 token
- **那么** `.openspec.yaml` 包含以下字段：`input`、`output`、`cache_create`、`cache_read`、`total`

### 需求:系统必须在归档时计算 token 差值

归档时系统必须读取基准 token，计算当前值与基准的差值，记录到 CSV。

#### 场景:计算 token 差值
- **当** 变更归档且存在 `baseline_tokens`
- **那么** 系统 计算差值 = 当前 token - 基准 token，记录差值到 CSV

#### 场景:无基准 token
- **当** 变更归档但 `.openspec.yaml` 中无 `baseline_tokens`
- **那么** 系统使用当前 token 值（向后兼容），打印警告信息