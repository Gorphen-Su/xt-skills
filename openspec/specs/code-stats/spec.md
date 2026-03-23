## 修改需求

### 需求:CSV 文件必须包含 token 消耗字段

`ai.summary.csv` 文件必须支持新增的 token 消耗统计字段。

**原有字段**: `id`, `author`, `timestamp`, `additions`, `deletions`, `total_lines`, `project_name`

**新增字段**: `input_tokens`, `output_tokens`, `cache_create_tokens`, `cache_read_tokens`, `total_tokens`, `cost`, `models`, `spec_files`, `spec_lines`

#### 场景:新建 CSV 文件
- **当** CSV 文件不存在
- **那么** 系统创建包含所有字段的 CSV 文件（包括新增的 token 和 spec 字段）

#### 场景:现有 CSV 文件无 token 字段
- **当** 现有 CSV 文件仅有旧字段
- **那么** 系统自动追加新字段表头，现有记录的新字段留空

#### 场景:写入统计记录
- **当** 收集完代码统计和 token 数据
- **那么** 系统将所有字段写入 CSV 文件的新行

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