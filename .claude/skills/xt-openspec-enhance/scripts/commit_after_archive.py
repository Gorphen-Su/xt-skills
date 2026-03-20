#!/usr/bin/env python3
"""
归档后 Commit 提示脚本

在归档完成后提示用户执行 git commit
"""

import subprocess
import json
import sys
import os
from datetime import datetime


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


def get_author():
    """获取当前 git 用户名"""
    stdout, _ = run_cmd(["git", "config", "user.name"])
    return stdout if stdout else "unknown"


def read_proposal(archive_path):
    """读取 proposal.md 获取功能简述"""
    proposal_file = os.path.join(archive_path, "proposal.md")
    if not os.path.exists(proposal_file):
        return "无功能描述"

    try:
        with open(proposal_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取第一行作为简述（通常是标题）
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        return lines[0] if lines else "无功能描述"
    except:
        return "无法读取功能描述"


def get_changed_files(repo_root, archive_path):
    """获取变更涉及的文件列表"""
    # 检查是否有 git diff 变更
    stdout, _ = run_cmd(["git", "diff", "--name-only", "HEAD"])
    files = set()
    for line in stdout.split('\n'):
        if line:
            files.add(line)

    return list(files)[:20]  # 限制显示前20个文件


def generate_commit_message(change_name, proposal_text, author):
    """生成 commit 信息"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    msg = f"""{change_name}: {proposal_text}

- 归档时间：{timestamp}
- 作者：{author}"""
    return msg


def get_archived_changes():
    """获取归档的变更列表"""
    repo_root = get_git_root()
    archive_dir = os.path.join(repo_root, "openspec", "changes", "archive")

    if not os.path.exists(archive_dir):
        return []

    changes = []
    for item in os.listdir(archive_dir):
        item_path = os.path.join(archive_dir, item)
        if os.path.isdir(item_path):
            # 解析 YYYY-MM-DD-name 格式
            parts = item.split('-', 3)
            if len(parts) >= 4:
                date = '-'.join(parts[:3])
                name = parts[3]
                changes.append({
                    "full_name": item,
                    "date": date,
                    "name": name,
                    "path": item_path
                })

    # 按时间倒序
    changes.sort(key=lambda x: x["full_name"], reverse=True)
    return changes


def main():
    repo_root = get_git_root()
    os.chdir(repo_root)

    if not os.path.exists(os.path.join(repo_root, ".git")):
        print("错误：当前目录不是 git 仓库")
        sys.exit(1)

    # 检查是否有未提交的变更
    stdout, _ = run_cmd(["git", "status", "--porcelain"])
    if not stdout:
        print("提示：当前没有未提交的变更，无需执行 git commit")
        sys.exit(0)

    # 显示当前状态
    print("-" * 60)
    run_cmd(["git", "status"])
    print("-" * 60)

    # 询问用户是否提交
    print("\n检测到未提交的变更。")
    print("是否执行 git commit 提交本次变更？")
    print("输入 '是' 或 '提交' 确认，或其他内容跳过")

    try:
        user_input = input("> ").strip()
    except EOFError:
        user_input = ""

    if user_input.lower() in ['是', '提交', 'yes', 'y', 'commit']:
        # 执行 git commit
        print("\n正在执行 git commit...")

        # 读取最新归档的变更信息（如果有）
        changes = get_archived_changes()
        change_info = changes[0] if changes else {"name": "unknown-change", "path": ""}

        # 读取 proposal
        proposal_text = "无功能描述"
        if change_info["path"]:
            proposal_text = read_proposal(change_info["path"])

        author = get_author()
        commit_msg = generate_commit_message(
            change_info["name"],
            proposal_text,
            author
        )

        # 执行 git add 和 commit
        run_cmd(["git", "add", "."])
        run_cmd(["git", "commit", "-m", commit_msg])

        print(f"\n✓ Git commit 已执行")
        print(f"提交信息：\n{commit_msg}")
    else:
        print("\n跳过 git commit。请稍后手动提交变更。")


if __name__ == "__main__":
    main()
