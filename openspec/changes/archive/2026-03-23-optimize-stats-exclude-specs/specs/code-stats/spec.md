## 修改需求

### 需求:代码统计必须排除规范文档

代码行数统计必须排除 `openspec/` 目录下的 markdown 文件，仅统计真正的代码文件变更。

#### 场景:排除 openspec 目录的 markdown 文件
- **当** 变更文件包括 `openspec/changes/xxx/proposal.md` 和 `src/index.py`
- **那么** 代码统计仅计算 `src/index.py` 的行数，排除 markdown 文件

#### 场景:保留其他目录的 markdown 文件
- **当** 变更文件包括 `README.md` 和 `docs/guide.md`
- **那么** 这些文件仍然计入代码统计（不在 openspec/ 目录下）

#### 场景:openspec 目录下的非 markdown 文件
- **当** 变更文件包括 `openspec/ai.summary.csv`
- **那么** 该文件计入代码统计（不是 markdown 文件）