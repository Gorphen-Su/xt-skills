## 1. 数据采集模块

- [x] 1.1 添加 `get_token_stats()` 函数，调用 `ccusage session --json` 获取 token 数据
- [x] 1.2 实现 session ID 匹配逻辑，根据当前项目路径定位对应 session
- [x] 1.3 实现多模型数据聚合逻辑（累加 tokens，拼接 models）

## 2. CSV 扩展

- [x] 2.1 更新 `CSV_HEADERS` 常量，新增 7 个 token 相关字段
- [x] 2.2 修改 `ensure_csv_exists()` 函数，创建时包含新字段
- [x] 2.3 添加 `migrate_csv_headers()` 函数，为旧 CSV 文件追加新表头
- [x] 2.4 更新 `append_to_csv()` 函数，写入 token 字段数据

## 3. ccusage 安装与错误处理

- [x] 3.1 添加 `check_ccusage_installed()` 函数，检测 ccusage 是否已安装
- [x] 3.2 添加 `install_ccusage()` 函数，执行 `npm install -g ccusage` 并处理安装结果
- [x] 3.3 实现用户确认交互：提示未安装并询问是否安装
- [x] 3.4 添加 `ccusage` 执行失败的异常捕获
- [x] 3.5 添加 session 无匹配数据的处理逻辑

## 4. 集成与测试

- [x] 4.1 修改 `collect_stats()` 函数，整合 token 数据采集
- [x] 4.2 更新 `main()` 函数输出，显示 token 统计信息
- [x] 4.3 手动测试完整流程