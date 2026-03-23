## 新增需求

### 需求:系统必须独立统计规范文档

系统必须独立统计 `openspec/` 目录下所有 markdown 文件的数量和行数。

#### 场景:统计规范文档
- **当** 存在 `openspec/changes/xxx/proposal.md`、`openspec/specs/xxx/spec.md` 等 markdown 文件
- **那么** 系统统计文件总数（`spec_files`）和总行数（`spec_lines`）

#### 场景:无规范文档
- **当** `openspec/` 目录下没有 markdown 文件
- **那么** `spec_files` 为 0，`spec_lines` 为 0

#### 场景:排除归档目录
- **当** 存在 `openspec/changes/archive/` 目录下的 markdown 文件
- **那么** 这些文件也计入规范统计（归档的规范也是规范）