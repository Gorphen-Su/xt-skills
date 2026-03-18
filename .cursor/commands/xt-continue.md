---
name: "XT: 继续"
description: 继续创建 OpenSpec 变更的产出物（ xt 封装层）
category: 工作流
tags: [workflow, artifacts]
---

通过创建下一个产出物继续处理 OpenSpec 变更。

**输入**：可选择指定变更名称（例如，`/xt:continue add-auth`）。如果省略，检查是否可以从对话上下文中推断出来。

**步骤**

1. **选择变更**
   - 如果提供了名称，使用它
   - 否则从上下文推断或让用户选择

2. **获取下一个产出物的指令**
   ```bash
   openspec-cn instructions next --change "<name>"
   ```

3. **创建产出物**
   - 阅读模板和上下文
   - 创建产出物
   - 更新状态

**护栏**
- 始终确认产出物创建成功
- 使用正确的产出物模板
- 保持产出物格式一致
