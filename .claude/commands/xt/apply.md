---
name: "XT: 应用"
description: 实现 OpenSpec 变更中的任务（ xt 封装层）
category: 工作流
tags: [workflow, tasks]
---

此命令是 `opsx:apply` 的封装层，用于项目定制。

**当前版本**：仅转发到 `opsx:apply` 命令。

**重要规则**：
- ✅ 可以修改代码文件
- ✅ 可以使用 `git add` 暂存文件
- ❌ **禁止主动执行 `git commit`**
- ❌ **禁止自动提交到远程仓库**

所有 git 提交操作必须等待用户明确授权。

详见：[`.claude/commands/opsx/apply.md`](../opsx/apply.md)
