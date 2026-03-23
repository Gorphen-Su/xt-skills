## 新增需求

### 需求:系统必须采集当前 session 的 token 消耗数据

在归档变更时，系统必须调用 `ccusage` 工具获取当前项目 session 的 token 消耗统计。

#### 场景:成功获取 token 数据
- **当** `ccusage` 已安装且当前 session 有数据
- **那么** 系统获取 input_tokens、output_tokens、cache_create_tokens、cache_read_tokens、total_tokens、cost 和 models 字段

#### 场景:ccusage 未安装
- **当** `ccusage` 命令不存在
- **那么** 系统提示用户"当前环境未安装 ccusage 工具，是否安装？"
- **当** 用户确认安装
- **那么** 系统执行 `npm install -g ccusage` 安装工具，安装成功后继续采集
- **当** 用户拒绝安装
- **那么** 系统打印提示信息，token 相关字段写入空值

#### 场景:ccusage 安装失败
- **当** `npm install -g ccusage` 执行失败
- **那么** 系统打印错误信息，token 相关字段写入空值

#### 场景:ccusage 执行失败
- **当** `ccusage session --json` 返回非零退出码
- **那么** 系统打印错误信息，token 相关字段写入空值

#### 场景:session 无匹配数据
- **当** 当前项目路径在 `ccusage` 输出中找不到匹配的 session
- **那么** 系统打印提示信息，token 相关字段写入空值

### 需求:系统必须支持多模型数据聚合

当 session 使用多个模型时，系统必须聚合所有模型的 token 数据。

#### 场景:多模型聚合
- **当** session 使用 glm-5 和 qwen3-coder-next 两个模型
- **那么** input_tokens 为两模型 input_tokens 之和，models 字段为 "glm-5,qwen3-coder-next"