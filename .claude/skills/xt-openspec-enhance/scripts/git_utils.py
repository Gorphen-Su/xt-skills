#!/usr/bin/env python3
"""
Git 工具函数共享模块
"""

import subprocess
import json
import os


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
