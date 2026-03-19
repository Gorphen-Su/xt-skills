## Why

`xt-openspec-wrapper-init` 的使用依赖于 `openspec` 和 `openspec-cn` 工具，但当前实现没有检查这些依赖是否已安装。用户需要手动安装这些依赖，这增加了使用门槛。

## What Changes

- 在 `xt-openspec-wrapper-init` 脚本中添加依赖检查逻辑
- 如果 `openspec` 或 `openspec-cn` 未安装，自动安装它们
- 如果已安装，运行 `openspec init` 和 `openspec-cn init` 初始化项目配置
- 初始化时默认选择 Cursor 和 Claude Code 两个工具

## Capabilities

### New Capabilities
- `auto-dependency-install`: 自动检查和安装 openspec/openspec-cn 依赖

### Modified Capabilities
None

## Impact

- `init-cli/xt-openspec-wrapper-init/bin/xt-openspec-wrapper-init.js` - 添加依赖检查和安装逻辑
- `init-cli/xt-openspec-wrapper-init/lib/scripts/` - 可能需要新增 Python 辅助脚本
