#!/usr/bin/env python3
"""
测试 commit_after_archive.py 脚本
"""

import subprocess
import sys
import os

# 设置测试输入（跳过提交）
test_input = "n\n"

# 运行脚本并传入测试输入
script_path = "D:/workspaces/private-workspaces/xt-skills/.claude/skills/xt-openspec-enhance/scripts/commit_after_archive.py"

# 使用 UTF-8 编码运行
process = subprocess.Popen(
    [sys.executable, script_path],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    encoding='utf-8',
    errors='replace',
    cwd="D:/workspaces/private-workspaces/xt-skills"
)

stdout, stderr = process.communicate(input=test_input)

# 输出到文件而不是控制台，避免 Windows gbk 编码问题
with open('test_output.txt', 'w', encoding='utf-8') as f:
    f.write("=== 脚本输出 ===\n")
    f.write(stdout)
    if stderr:
        f.write("\n=== 错误输出 ===\n")
        f.write(stderr)
    f.write(f"\n=== 返回码: {process.returncode} ===\n")

print(f"测试完成，输出已保存到 test_output.txt")
print(f"返回码: {process.returncode}")
