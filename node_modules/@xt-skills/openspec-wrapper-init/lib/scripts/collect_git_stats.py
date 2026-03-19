#!/usr/bin/env python3
"""
收集 git 代码变更统计
"""

import subprocess
import json
import sys
import os
import csv
import re
from datetime import datetime
import uuid

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

def get_changed_functions(diff_output):
    """从 diff 中提取变更的函数名"""
    functions = set()
    func_patterns = [
        r'^[+\-]\s*(?:public|private|const|let|var)?\s*(?:function|fn|def)?\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*[\(\{]',
        r'^[+\-]\s*(\w+)\s*=\s*(?:\(|function|func|def)',
    ]

    for line in diff_output.split('\n'):
        if line.startswith('+') or line.startswith('-'):
            for pattern in func_patterns:
                match = re.match(pattern, line)
                if match:
                    functions.add(match.group(1))

    return list(functions)[:20]

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
    all_diff_output = ""

    for file in changed_files:
        additions, deletions = get_file_changes(file)
        total_additions += additions
        total_deletions += deletions
        stdout, _ = run_cmd(["git", "diff", "-U0", "HEAD", "--", file])
        all_diff_output += stdout + "\n"

    changed_functions = get_changed_functions(all_diff_output)
    total_lines = total_additions + total_deletions

    return {
        "id": str(uuid.uuid4()),
        "author": author,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "additions": total_additions,
        "deletions": total_deletions,
        "changed_files": len(changed_files),
        "changed_functions": ";".join(changed_functions),
        "total_lines": total_lines,
        "project_name": project_name
    }

def main():
    repo_root = get_git_root()
    openspec_dir = os.path.join(repo_root, "openspec")
    csv_path = os.path.join(openspec_dir, "ai.summary.csv")

    # 确保 openspec 目录存在
    if not os.path.exists(openspec_dir):
        os.makedirs(openspec_dir)

    # 收集统计信息
    stats = collect_stats()

    if "error" in stats:
        print(f"错误: {stats['error']}")
        sys.exit(1)

    # 写入 CSV（覆盖模式，每次完整写入）
    mode = 'w' if not os.path.exists(csv_path) else 'a'
    with open(csv_path, mode, encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if mode == 'w':
            writer.writerow([
                "id", "author", "timestamp", "additions", "deletions",
                "changed_files", "changed_functions", "total_lines",
                "project_name"
            ])
        writer.writerow([
            stats["id"],
            stats["author"],
            stats["timestamp"],
            stats["additions"],
            stats["deletions"],
            stats["changed_files"],
            stats["changed_functions"],
            stats["total_lines"],
            stats["project_name"]
        ])
    print(f"统计已写入: {csv_path}")

    # 输出摘要
    print("\n代码变更统计:")
    print(f"  ID: {stats['id']}")
    print(f"  作者: {stats['author']}")
    print(f"  新增: +{stats['additions']} 行")
    print(f"  删除: -{stats['deletions']} 行")
    print(f"  文件: {stats['changed_files']} 个")
    print(f"  总行数: {stats['total_lines']}")

if __name__ == "__main__":
    main()
