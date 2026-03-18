---
name: "XT: OpenSpec 项目封装"
description: 项目级别的 OpenSpec 变更管理封装层，提供 xt:* 命令集。作为 opsx:* 命令的转发层，避免内容重复和兼容性问题。当用户需要使用xt命令封装时使用。
---

# XT: OpenSpec 项目封装

## 设计原则

此封装层采用**转发模式**而非复制模式：

- **`commands/xt/*.md`**：仅包含命令元数据和转发说明
- **`commands/opsx/*.md`**：包含完整的命令实现逻辑

这样做的好处：
1. **避免内容重复**：单一数据源
2. **兼容性保证**：opsx 升级时 xt 自动继承
3. **维护简单**：不需要同步两份代码

## 命令映射

| XT 命令 | 原始 OPX 命令 | 转发文件 |
|---------|--------------|----------|
| `xt:new` | `opsx:new` | `.claude/commands/opsx/new.md` |
| `xt:continue` | `opsx:continue` | `.claude/commands/opsx/continue.md` |
| `xt:apply` | `opsx:apply` | `.claude/commands/opsx/apply.md` |
| `xt:archive` | `opsx:archive` | `.claude/commands/opsx/archive.md` |
| `xt:bulk-archive` | `opsx:bulk-archive` | `.claude/commands/opsx/bulk-archive.md` |
| `xt:sync` | `opsx:sync` | `.claude/commands/opsx/sync.md` |
| `xt:verify` | `opsx:verify` | `.claude/commands/opsx/verify.md` |
| `xt:explore` | `opsx:explore` | `.claude/commands/opsx/explore.md` |
| `xt:propose` | `opsx:propose` | `.claude/commands/opsx/propose.md` |
| `xt:onboard` | `opsx:onboard` | `.claude/commands/opsx/onboard.md` |
| `xt:ff` | `opsx:ff` | `.claude/commands/opsx/ff.md` |

## 项目自定义扩展

此 skill 作为项目级封装，可以在以下位置添加自定义内容：

- **`scripts/`**：自定义脚本（如钩子、工具函数）
- **`references/`**：项目特定文档（如工作流、模板）
- **`assets/`**：项目特定资源（如模板、图标）

## 底层依赖

所有命令底层调用 `openspec-cn` CLI 工具。
