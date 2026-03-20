---
name: "XT: OpenSpec 增强恢复"
description: 恢复 opsx 命令到原始状态，移除所有增强功能
category: 工具
tags: [setup, git, enhance]
---

恢复 opsx 命令到原始状态，移除所有增强功能。

## 移除的增强功能

### 1. Git 状态检查

从以下命令移除步骤 0：
- `/opsx:new`
- `/opsx:propose`
- `/opsx:ff`

### 2. 归档增强

从以下命令移除步骤 7 和步骤 8：
- `/opsx:archive`
- `/opsx:bulk-archive`

## 步骤

1. **检查是否已初始化**

   读取 `.claude/commands/opsx/new.md`，检查是否包含 `步骤 0：检查 Git 状态`。

   - 如果未包含：提示"增强功能未初始化，无需恢复"
   - 如果已包含：继续下一步

2. **移除 Git 检查代码**

   从以下文件中移除注入的检查代码：

   - `.claude/commands/opsx/new.md`
   - `.claude/commands/opsx/propose.md`
   - `.claude/commands/opsx/ff.md`

   移除的内容模式：
   ```markdown

   0. **检查 Git 状态**

      ...（整个步骤 0 的内容）

   ```

3. **移除归档增强代码**

   从以下文件中移除注入的归档增强步骤：

   - `.claude/commands/opsx/archive.md`
   - `.claude/commands/opsx/bulk-archive.md`

   移除的内容：
   - 步骤 7：代码变更统计
   - 步骤 8：Commit 提示

4. **恢复步骤编号**

   将原命令中的步骤编号恢复到原始顺序。

5. **显示完成信息**

   ```
   ## 恢复完成

   已从以下命令移除增强功能：

   **Git 状态检查**：
   - /opsx:new
   - /opsx:propose
   - /opsx:ff

   **归档增强**：
   - /opsx:archive
   - /opsx:bulk-archive

   opsx 命令已恢复到原始状态。
   ```

## 重新启用

如需重新启用增强功能，运行 `/xt-openspec-enhance:init`。