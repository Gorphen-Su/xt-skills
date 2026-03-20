#!/usr/bin/env python3
"""
收集 Git 代码变更统计并追加到 CSV

增强版：简化字段，移除 changed_files 和 changed_functions
"""

import subprocess
import json
import sys
import os
import csv
from datetime import datetime
import uuid


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


def get_author():
    """获取当前 git 用户名"""
    stdout, _ = run_cmd(["git", "config", "user.name"])
    return stdout if stdout else "unknown"


def get_project_name(repo_root):
    """获取项目名称"""
    package_json = os.path.join(repo_root, "package.json")
    if os.path.exists(package_json):
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "name" in data:
                    return data["name"]
        except:
            pass
    return os.path.basename(repo_root)


def get_changed_files():
    """获取变更的文件列表"""
    stdout1, _ = run_cmd(["git", "diff", "--name-only", "HEAD"])
    stdout2, _ = run_cmd(["git", "diff", "--name-only", "--cached", "HEAD"])

    files = set()
    for line in stdout1.split('\n'):
        if line:
            files.add(line)
    for line in stdout2.split('\n'):
        if line:
            files.add(line)
    return list(files)


def get_file_changes(file_path):
    """获取单个文件的变更详情"""
    stdout, _ = run_cmd(["git", "diff", "-U0", "HEAD", "--", file_path])

    additions = 0
    deletions = 0

    for line in stdout.split('\n'):
        if line.startswith('+') and not line.startswith('+++'):
            additions += 1
        elif line.startswith('-') and not line.startswith('---'):
            deletions += 1

    return additions, deletions


# ============ CSV 统计逻辑 ============


# CSV 文件路径常量
CSV_HEADERS = ["id", "author", "timestamp", "additions", "deletions", "total_lines", "project_name"]


def collect_stats():
    """收集代码变更统计"""
    repo_root = get_git_root()
    os.chdir(repo_root)

    if not os.path.exists(os.path.join(repo_root, ".git")):
        return {
            "error": "当前目录不是 git 仓库"
        }

    author = get_author()
    project_name = get_project_name(repo_root)
    changed_files = get_changed_files()

    total_additions = 0
    total_deletions = 0

    for file in changed_files:
        additions, deletions = get_file_changes(file)
        total_additions += additions
        total_deletions += deletions

    total_lines = total_additions + total_deletions

    return {
        "id": str(uuid.uuid4()),
        "author": author,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "additions": total_additions,
        "deletions": total_deletions,
        "total_lines": total_lines,
        "project_name": project_name
    }


def ensure_csv_exists(csv_path):
    """确保 CSV 文件存在并有表头"""
    if not os.path.exists(csv_path):
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)
        print(f"已创建 CSV 文件: {csv_path}")


def append_to_csv(csv_path, stats):
    """追加记录到 CSV"""
    with open(csv_path, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            stats["id"],
            stats["author"],
            stats["timestamp"],
            stats["additions"],
            stats["deletions"],
            stats["total_lines"],
            stats["project_name"]
        ])
    print(f"已追加记录到: {csv_path}")


def main():
    repo_root = get_git_root()
    openspec_dir = os.path.join(repo_root, "openspec")
    csv_path = os.path.join(openspec_dir, "ai.summary.csv")

    # 确保 openspec 目录存在
    if not os.path.exists(openspec_dir):
        os.makedirs(openspec_dir)

    # 确保 CSV 文件存在
    ensure_csv_exists(csv_path)

    # 收集统计信息
    stats = collect_stats()

    if "error" in stats:
        print(f"错误: {stats['error']}")
        sys.exit(1)

    # 追加到 CSV
    append_to_csv(csv_path, stats)

    # 输出摘要
    print("\n代码变更统计已记录:")
    print(f"  ID: {stats['id']}")
    print(f"  作者: {stats['author']}")
    print(f"  新增: +{stats['additions']} 行")
    print(f"  删除: -{stats['deletions']} 行")
    print(f"  总变更: {stats['total_lines']} 行")


if __name__ == "__main__":
    main()
