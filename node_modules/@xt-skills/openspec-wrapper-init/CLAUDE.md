# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## 项目概述

**@xt-skills/openspec-wrapper-init** - OpenSpec 变更管理工具的 xt 封装层初始化脚本。

## 核心功能

此包提供 `xt-openspec-wrapper-init` 命令，在 npm install 时自动执行（通过 `postinstall` 钩子），完成以下初始化工作：

1. **安装依赖**：
   - `@fission-ai/openspec` - OpenSpec 主工具
   - `@studyzy/openspec-cn` - OpenSpec 中文支持

2. **复制文件**到 `.claude/` 目录：
   - `commands/xt/*.md` - 11 个 xt 命令文件（new, apply, archive, continue, bulk-archive, sync, verify, explore, propose, onboard, ff）
   - `skills/xt-openspec-wrapper/SKILL.md` - Skill 定义
   - `skills/xt-openspec-wrapper/scripts/` - Python 统计脚本

3. **创建配置**：
   - `.claude/settings.local.json` - 包含禁止自动 git commit 的权限规则

## 项目结构

```
init-cli/xt-openspec-wrapper-init/
├── bin/
│   └── xt-openspec-wrapper-init.js   # Node.js 初始化脚本
├── lib/
│   ├── commands/                     # 源命令文件（复制到 .claude/commands/xt/）
│   ├── skills/                       # 源 skill 文件
│   └── scripts/                      # Python 统计脚本
└── package.json
```

## 工作机制

**初始化流程** (`bin/xt-openspec-wrapper-init.js`)：

1. 检查并安装 `openspec` 和 `openspec-cn`（如未安装）
2. 创建目标目录结构
3. 复制命令和 skill 文件
4. 生成/更新 `settings.local.json`

## 定期检查依赖

初始化脚本会检查以下命令是否已安装，未安装则自动安装：

```bash
npm install -g @fission-ai/openspec@latest
npm install -g @studyzy/openspec-cn@latest
```

## 配置说明

生成的 `settings.local.json` 默认包含：

```json
{
  "permissions": {
    "deny": [
      "Bash(git commit*)"
    ]
  }
}
```

## 相关资源

- 主项目：`D:\workspaces\private-workspaces\xt-skills\CLAUDE.md`
- 初始化后使用：`/xt:explore`, `/xt:new`, `/xt:apply`, `/xt:archive` 等命令
