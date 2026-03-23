## 修改需求

### 需求:CSV 文件必须包含 token 消耗字段

`ai.summary.csv` 文件必须支持新增的 token 消耗统计字段。

**原有字段**: `id`, `author`, `timestamp`, `additions`, `deletions`, `total_lines`, `project_name`

**新增字段**: `input_tokens`, `output_tokens`, `cache_create_tokens`, `cache_read_tokens`, `total_tokens`, `cost`, `models`

#### 场景:新建 CSV 文件
- **当** CSV 文件不存在
- **那么** 系统创建包含所有字段的 CSV 文件（包括新增的 token 字段）

#### 场景:现有 CSV 文件无 token 字段
- **当** 现有 CSV 文件仅有旧字段
- **那么** 系统自动追加新字段表头，现有记录的新字段留空

#### 场景:写入统计记录
- **当** 收集完代码统计和 token 数据
- **那么** 系统将所有字段写入 CSV 文件的新行