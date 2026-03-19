## Context

当前 `xt-openspec-wrapper-init` 依赖 `openspec` 和 `openspec-cn` 工具，但：
1. 没有检查这些工具是否已安装
2. 用户需要手动安装：`npm install -g @fission-ai/openspec@latest` 和 `npm install -g @studyzy/openspec-cn@latest`
3. 安装后还需要运行 `openspec init` 和 `openspec-cn init` 初始化项目
4. 这个过程对新用户不友好，增加了使用门槛

## Goals / Non-Goals

**Goals:**
- 自动检查 `openspec` 和 `openspec-cn` 是否已安装
- 如果未安装，自动运行 `npm install -g` 安装它们
- 如果已安装，运行 `openspec init` 和 `openspec-cn init` 初始化项目配置
- 初始化时默认选择 Cursor 和 Claude Code 两个工具

**Non-Goals:**
- 不改变现有的 `xt-openspec-wrapper-init` 文件复制逻辑
- 不处理 openspec/openspec-cn 的版本管理（始终使用 latest）
- 不修改全局安装的包，只在需要时安装

## Decisions

### 决策1：使用 Node.js child_process 执行命令
- **原因**：当前脚本是 Node.js，方便执行 shell 命令
- **实现**：使用 `child_process.exec()` 或 `spawn()` 执行 `--version` 和 `npm install` 命令

### 决策2：安装到全局 vs 本地
- **选择**：全局安装 (`-g`)
- **原因**：openspec/openspec-cn 是 CLI 工具，需要在任意目录运行；用户可能在不同项目间切换

### 决策3：初始化配置默认选择 Cursor 和 Claude Code
- **原因**：这两个是主要的 IDE/编辑器集成场景
- **实现**：通过 `openspec init --tool cursor` 和 `openspec-cn init --tool claude`（需要确认具体参数）

### 决策4：错误处理策略
- 如果命令执行失败，显示友好的错误信息
- 如果用户没有安装 Node.js/npm，提示用户手动安装

## Risks / Trade-offs

- [如果 `npm install -g` 需要管理员权限] → 用户可能遇到权限错误，需要提示用户以管理员身份运行或使用 `--userconfig` 参数
- [如果网络不稳定导致安装失败] → 可能需要重试机制，但首次实现保持简单
- [openspec/openspec-cn init 的参数未知] → 需要先确认它们支持的参数，可能需要交互式配置
