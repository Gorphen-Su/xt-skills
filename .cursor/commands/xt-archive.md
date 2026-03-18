---
name: "XT: 归档"
description: 归档已完成的 OpenSpec 变更（ xt 封装层）
category: 工作流
tags: [workflow, archive]
---

归档实验性工作流中已完成的变更。

**输入**：可选择在 `/xt:archive` 后指定变更名称。

**步骤**

1. **如果没有提供变更名称，提示选择**
2. **检查产出物完成状态**
3. **检查任务完成状态**
4. **执行归档**
   ```bash
   mv openspec/changes/<name> openspec/changes/archive/YYYY-MM-DD-<name>
   ```

**护栏**
- 确认所有产出物已完成
- 显示警告信息（如有未完成项）
- 确保归档目录不重复
