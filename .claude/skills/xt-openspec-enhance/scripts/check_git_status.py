#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查并等待 Git 状态干净

用于在启动 OpenSpec 变更前确保工作区处于提交状态
"""

import subprocess
import sys
import os
import io

# 设置 stdout 编码为 UTF-8，解决 Windows 控制台编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# ============ Git 工具函数 ============

def run_cmd(cmd, shell=False):
    """跨平台运行命令"""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return "", 1


def get_git_root():
    """获取 git 仓库根目录"""
    stdout, _ = run_cmd(["git", "rev-parse", "--show-toplevel"])
    return stdout if stdout else os.getcwd()


def get_git_status():
    """获取 git status 输出"""
    stdout, _ = run_cmd(["git", "status"])
    return stdout


# ============ 检查逻辑 ============


def is_git_clean():
    """检查 git 工作区是否干净（无未提交变更）"""
    repo_root = get_git_root()
    os.chdir(repo_root)

    # 检查工作区是否有未提交的变更
    stdout, _ = run_cmd(["git", "status", "--porcelain"])

    if stdout:
        return False

    # 检查是否有暂存区的变更（未提交的 commit）
    # 通过检查是否有提交来确认
    stdout, _ = run_cmd(["git", "log", "-1"])
    if not stdout:
        # 仓库没有提交，视为不干净
        return False

    return True


def main():
    """主函数：检查 git 状态"""
    repo_root = get_git_root()
    os.chdir(repo_root)

    if not os.path.exists(os.path.join(repo_root, ".git")):
        print("错误：当前目录不是 git 仓库")
        sys.exit(1)

    if is_git_clean():
        print("✓ Git 状态干净，可以继续操作")
        sys.exit(0)
    else:
        print("✗ Git 状态不干净，存在未提交的变更")
        print("\n当前状态：")
        print("-" * 60)
        print(get_git_status())
        print("-" * 60)
        print("\n提示：请先提交或暂存您的变更，然后输入 '继续' 或 '继续' 来重试")
        sys.exit(1)


if __name__ == "__main__":
    main()
