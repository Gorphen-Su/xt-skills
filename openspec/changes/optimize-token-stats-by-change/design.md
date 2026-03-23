## 上下文

当前 token 统计问题：
- `ccusage session` 返回的是 session 累计 token（可能跨越多天）
- 归档时记录的是累计值，而非变更周期的实际消耗
- 无法准确统计每个变更的真实 token 成本

现有架构：
- `opsx:new` / `opsx:propose` 创建变更，生成 `.openspec.yaml`
- `opsx:archive` 归档变更，调用 `archive_with_stats.py` 收集统计
- `archive_with_stats.py` 调用 `ccusage session --json` 获取 token 数据

约束：
- 需要修改 opsx 命令的 skill 文件
- `.openspec.yaml` 格式变更需要向后兼容
- 基准 token 可能不存在（旧变更），需要优雅降级

## 目标 / 非目标

**目标：**
- 在变更创建时记录 token 基准
- 在归档时计算 token 差值
- 旧变更（无基准）保持现有行为

**非目标：**
- 不修改 ccusage 工具
- 不追踪历史变更的 token（只对新变更生效）

## 决策

### 1. 基准存储位置
**选择**: 存储在 `.openspec.yaml` 中
**理由**: 变更元数据与变更目录共存，便于管理
**格式**:
```yaml
schema: spec-driven
created: 2026-03-23
baseline_tokens:
  input: 88000000
  output: 180000
  cache_create: 0
  cache_read: 3500000
  total: 91600000
```

### 2. 基准记录时机
**选择**: 在 `opsx:new` 和 `opsx:propose` 执行时记录
**理由**: 这两个命令是变更的入口点
**实现**: 修改对应的 skill 文件，在创建变更后调用 Python 脚本记录基准

### 3. 差值计算方式
**选择**: 归档时 `archive_with_stats.py` 读取基准并计算差值
**理由**: 复用现有脚本，逻辑集中
**降级**: 如果 `.openspec.yaml` 中无 `baseline_tokens`，使用当前值（保持向后兼容）

## 风险 / 权衡

| 风险 | 缓解措施 |
|------|----------|
| 旧变更无基准 | 检测并使用当前值，打印警告 |
| ccusage 未安装 | 基准字段留空，归档时跳过 token 差值计算 |
| 多项目并发 | session ID 匹配当前项目，确保数据准确 |

## 迁移计划

1. 修改 `archive_with_stats.py` 支持读取基准和计算差值
2. 创建 `record_baseline.py` 脚本供 opsx 命令调用
3. 修改 `opsx:new` 和 `opsx:propose` skill 文件
4. 现有变更无需处理，归档时按旧逻辑运行