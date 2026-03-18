---
name: "XT: 批量归档"
description: 批量归档多个已完成的 OpenSpec 变更（ xt 封装层）
category: 工作流
tags: [workflow, archive]
---

批量归档实验性工作流中已完成的变更。

**输入**：可选择指定多个变更名称或使用通配符。

**步骤**

1. **获取变更列表**
   ```bash
   openspec-cn list --json
   ```

2. **筛选已完成的变更**
3. **批量归档**

**护栏**
- 逐个检查完成状态
- 显示归档摘要
