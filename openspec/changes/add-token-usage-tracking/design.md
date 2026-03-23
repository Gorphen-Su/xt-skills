## 上下文

当前 `archive_with_stats.py` 脚本在归档变更时收集代码行数统计，写入 `openspec/ai.summary.csv`。现有 CSV 字段：`id`, `author`, `timestamp`, `additions`, `deletions`, `total_lines`, `project_name`。

用户使用 `ccusage` 命令行工具可以查看 token 消耗统计。`ccusage session --json` 提供 JSON 格式输出，包含完整的 token 数据。

约束：
- 必须向后兼容现有 CSV 文件
- 新字段写入前需检查并添加表头
- `ccusage` 可能未安装，需要优雅降级处理

## 目标 / 非目标

**目标：**
- 在归档时自动采集当前 session 的 token 消耗数据
- 将 token 数据与代码行数统计一并记录到 CSV
- 支持 `ccusage` 未安装时的降级处理

**非目标：**
- 不追踪历史 token 消耗趋势
- 不提供 token 消耗可视化
- 不修改 `ccusage` 工具本身

## 决策

### 1. 数据获取方式
**选择**: 调用 `ccusage session --json --id <session-id>` 获取当前 session 数据
**理由**: `ccusage` 已提供结构化 JSON 输出，无需重复解析原始日志
**替代方案**:
- 解析 Claude Code 日志文件 → 复杂且易受版本影响
- 使用 ccusage MCP 工具 → 增加依赖复杂度

### 2. Session ID 识别
**选择**: 基于项目目录路径生成 session ID（`ccusage` 使用路径的 base64 或类似格式）
**理由**: 与 `ccusage` 内部 session ID 格式保持一致
**实现**: 从 `ccusage session --json` 输出中匹配当前项目路径

### 3. CSV 字段扩展
**选择**: 新增 7 个字段追加到现有表头后
**字段**: `input_tokens`, `output_tokens`, `cache_create_tokens`, `cache_read_tokens`, `total_tokens`, `cost`, `models`
**理由**: 与 `ccusage` 输出字段一一对应，便于数据对齐

### 4. ccusage 安装策略
**选择**: 检测到 `ccusage` 未安装时，提示用户并询问是否安装
**理由**: 确保数据采集完整，而不是简单地跳过 token 统计
**实现**: 调用 `npm install -g ccusage` 全局安装

## 风险 / 权衡

| 风险 | 缓解措施 |
|------|----------|
| `ccusage` 未安装 | 提示用户是否安装，确认后执行 `npm install -g ccusage` |
| 用户拒绝安装 | token 字段写入空值，继续执行代码统计 |
| 安装失败 | 打印错误信息，token 字段写入空值 |
| Session ID 不匹配 | 使用项目路径模糊匹配，优先精确匹配 |
| CSV 格式变更 | 检测旧格式文件，自动补充新表头 |
| JSON 解析失败 | try-catch 包装，失败时使用空值 |