---
name: "XT: 应用"
description: 实现 OpenSpec 变更中的任务（ xt 封装层）
category: 工作流
tags: [workflow, tasks]
---

实现 OpenSpec 变更中的任务。

**输入**：可选择指定变更名称（例如，`/xt:apply add-auth`）。如果省略，检查是否可以从对话上下文中推断出来。

**步骤**

1. **选择变更**
   - 如果提供了名称，使用它
   - 否则从上下文推断或让用户选择

2. **获取应用指令**
   ```bash
   openspec-cn instructions apply --change "<name>"
   ```

3. **实现任务**
   - 阅读上下文文件
   - 逐个实现任务
   - 更新任务状态为完成

4. **完成检查**
   - 检查所有任务是否完成
   - 提示用户后续操作

**护栏**
- 保持更改最小化
- 实现过程中如果不清楚立即暂停
- 更新任务复选框状态
