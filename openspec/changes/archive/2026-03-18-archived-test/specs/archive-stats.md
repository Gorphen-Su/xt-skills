## 新增需求

### 需求:归档完成后自动收集代码变更统计
在执行 `xt:archive` 或 `xt:bulk-archive` 命令完成归档后，系统必须自动执行统计脚本，收集代码变更信息并追加到 `openspec/ai.summary.csv` 文件中。

#### 场景:归档完成后统计
- **当** 用户执行 `/xt:archive <change-name>` 命令
- **当** 归档操作成功完成
- **那么** 系统自动执行 `scripts/archive_with_stats.py` 脚本
- **那么** 统计信息追加到 `openspec/ai.summary.csv` 文件
- **那么** 统计信息包含：id、author、timestamp、additions、deletions、changed_files、changed_functions、total_lines、project_name、branch、repository

#### 场景:脚本执行失败
- **当** 统计脚本执行失败
- **那么** 归档操作不回滚
- **那么** 显示警告信息但不阻塞归档完成

### 需求:代码变更统计字段
统计脚本必须收集并输出以下字段：

| 字段 | 说明 |
|------|------|
| id | 随机 UUID |
| author | 当前 git 操作人 |
| timestamp | 处理时间（日期时分秒） |
| additions | 新增行数 |
| deletions | 删除行数 |
| changed_files | 变更文件数 |
| changed_functions | 变更函数列表（分号分隔） |
| total_lines | 总行数 |
| project_name | 所属项目名称 |
| branch | 当前分支 |
| repository | 仓库名称 |

#### 场景:统计信息收集
- **当** 统计脚本执行
- **当** 项目有 package.json 文件
- **那么** project_name 从 package.json 的 name 字段获取
- **当** 项目无 package.json 文件
- **那么** project_name 使用仓库根目录名

## 修改需求

## 移除需求
