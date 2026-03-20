#!/usr/bin/env python3
"""
检查并等待 Git 状态干净

用于在启动 OpenSpec 变更前确保工作区处于提交状态
"""

import sys
import os

from .git_utils import run_cmd, get_git_root, get_git_status


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
