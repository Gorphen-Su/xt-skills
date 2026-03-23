## 1. 基准记录脚本

- [x] 1.1 创建 `record_baseline.py` 脚本，获取当前 session token 并写入 `.openspec.yaml`
- [x] 1.2 实现 `read_baseline_tokens()` 函数，从 `.openspec.yaml` 读取基准
- [x] 1.3 实现 `write_baseline_tokens()` 函数，将基准写入 `.openspec.yaml`

## 2. 归档脚本修改

- [x] 2.1 修改 `get_token_stats()` 函数，读取基准并计算差值
- [x] 2.2 添加无基准时的警告输出
- [x] 2.3 同步脚本到 xt-openspec-wrapper 和 init-cli 目录

## 3. opsx 命令修改

- [x] 3.1 修改 `opsx:new` skill 文件，在创建变更后调用 `record_baseline.py`
- [x] 3.2 修改 `opsx:propose` skill 文件，在创建变更后调用 `record_baseline.py`

## 4. 测试验证

- [ ] 4.1 手动测试 opsx:new 流程，验证基准记录
- [ ] 4.2 手动测试 opsx:archive 流程，验证差值计算