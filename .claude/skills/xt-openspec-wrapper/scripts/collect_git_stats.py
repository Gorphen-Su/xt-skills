#!/usr/bin/env python3
"""
收集 Git 代码变更统计信息（跨平台兼容）
输出 JSON 格式：id, author, timestamp, additions, deletions, changed_files, total_lines, project_name
"""

import subprocess
import json
import sys
import os
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

def get_current_branch():
    """获取当前分支名"""
    stdout, _ = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    return stdout if stdout else "unknown"

def get_author():
    """获取当前 git 用户名"""
    stdout, _ = run_cmd(["git", "config", "user.name"])
    return stdout if stdout else "unknown"

def get_project_name(repo_root):
    """获取项目名称"""
    # 1. package.json 中的 name
    package_json = os.path.join(repo_root, "package.json")
    if os.path.exists(package_json):
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "name" in data:
                    return data["name"]
        except:
            pass

    # 2. 使用仓库根目录名
    return os.path.basename(repo_root)

def get_changed_files():
    """获取变更的文件列表"""
    # 获取未暂存和已暂存的变更文件
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
    # 获取文件的增删行数
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
    # 匹配函数定义行（多种语言）
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

    return list(functions)[:20]  # 最多返回20个函数

def collect_stats():
    """收集代码变更统计"""
    repo_root = get_git_root()
    os.chdir(repo_root)

    # 检查是否在 git 仓库中
    if not os.path.exists(os.path.join(repo_root, ".git")):
        return {
            "error": "当前目录不是 git 仓库"
        }

    # 获取基本信息
    author = get_author()
    project_name = get_project_name(repo_root)
    branch = get_current_branch()

    # 获取变更文件列表
    changed_files = get_changed_files()

    # 统计行数变化
    total_additions = 0
    total_deletions = 0
    all_diff_output = ""

    for file in changed_files:
        additions, deletions = get_file_changes(file)
        total_additions += additions
        total_deletions += deletions
        stdout, _ = run_cmd(["git", "diff", "-U0", "HEAD", "--", file])
        all_diff_output += stdout + "\n"

    # 获取变更的函数
    changed_functions = get_changed_functions(all_diff_output)

    # 总行数（新增 + 删除 + 未变更的文件行数估算）
    total_lines = total_additions + total_deletions

    return {
        "id": str(uuid.uuid4()),
        "author": author,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "additions": total_additions,
        "deletions": total_deletions,
        "changed_files": len(changed_files),
        "changed_functions": changed_functions,
        "total_lines": total_lines,
        "project_name": project_name,
        "branch": branch,
        "repository": os.path.basename(repo_root)
    }

def main():
    output_format = "text"
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        output_format = "json"

    stats = collect_stats()

    if output_format == "json":
        print(json.dumps(stats, indent=2, ensure_ascii=False))
    else:
        print("=" * 50)
        print("代码变更统计")
        print("=" * 50)
        print(f"ID: {stats.get('id', 'N/A')}")
        print(f"代码处理人: {stats.get('author', 'N/A')}")
        print(f"处理时间: {stats.get('timestamp', 'N/A')}")
        print(f"新增行数: {stats.get('additions', 0)}")
        print(f"删除行数: {stats.get('deletions', 0)}")
        print(f"变更文件数: {stats.get('changed_files', 0)}")
        print(f"变更函数: {', '.join(stats.get('changed_functions', []))}")
        print(f"总行数: {stats.get('total_lines', 0)}")
        print(f"所属项目: {stats.get('project_name', 'N/A')}")
        print(f"分支: {stats.get('branch', 'N/A')}")
        print("=" * 50)

if __name__ == "__main__":
    main()
