## 1. 代码统计优化

- [x] 1.1 添加 `is_spec_markdown()` 函数，判断文件是否为 openspec 目录下的 markdown 文件
- [x] 1.2 修改 `collect_stats()` 函数，排除 openspec markdown 文件的代码统计
- [x] 1.3 添加 `collect_spec_stats()` 函数，独立统计 openspec markdown 文件

## 2. CSV 扩展

- [x] 2.1 更新 `CSV_HEADERS` 常量，新增 `spec_files` 和 `spec_lines` 字段
- [x] 2.2 更新 `migrate_csv_headers()` 函数，支持新字段迁移
- [x] 2.3 更新 `append_to_csv()` 函数，写入规范统计字段

## 3. 输出更新

- [x] 3.1 更新 `main()` 函数输出，显示规范文档统计信息
- [x] 3.2 同步脚本到 xt-openspec-wrapper 和 init-cli 目录

## 4. 测试验证

- [x] 4.1 手动测试完整流程，验证排除逻辑和统计准确性