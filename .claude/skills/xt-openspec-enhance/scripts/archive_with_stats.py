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
import yaml
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


def is_spec_markdown(file_path):
    """判断文件是否为 openspec 目录下的 markdown 文件"""
    # 统一路径分隔符
    normalized_path = file_path.replace('\\', '/').lower()
    # 检查是否在 openspec/ 目录下且以 .md 结尾
    return normalized_path.startswith('openspec/') and normalized_path.endswith('.md')


def collect_spec_stats(repo_root):
    """独立统计 openspec 目录下 markdown 文件的数量和行数"""
    openspec_dir = os.path.join(repo_root, "openspec")
    if not os.path.exists(openspec_dir):
        return {"spec_files": 0, "spec_lines": 0}

    spec_files = 0
    spec_lines = 0

    for root, dirs, files in os.walk(openspec_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                spec_files += 1
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        spec_lines += len(f.readlines())
                except:
                    pass

    return {"spec_files": spec_files, "spec_lines": spec_lines}


# ============ ccusage 工具函数 ============

def check_ccusage_installed():
    """检测 ccusage 是否已安装"""
    # Windows 下需要使用 shell=True 来找到 npm 全局安装的命令
    stdout, returncode = run_cmd(["ccusage", "--version"], shell=True)
    return returncode == 0


def install_ccusage():
    """安装 ccusage 工具"""
    print("正在安装 ccusage...")
    stdout, returncode = run_cmd(["npm", "install", "-g", "ccusage"], shell=True)
    if returncode == 0:
        print("ccusage 安装成功")
        return True
    else:
        print(f"ccusage 安装失败: {stdout}")
        return False


def prompt_install_ccusage():
    """提示用户是否安装 ccusage"""
    print("\n当前环境未安装 ccusage 工具。")
    print("ccusage 用于采集 token 消耗统计，建议安装以确保数据完整。")
    try:
        response = input("是否安装 ccusage？(y/n): ").strip().lower()
        return response == 'y' or response == 'yes'
    except EOFError:
        # 非交互模式，默认跳过
        print("检测到非交互模式，跳过安装。")
        return False


def read_baseline_tokens(change_dir):
    """从 .openspec.yaml 读取基准 token"""
    yaml_path = os.path.join(change_dir, ".openspec.yaml")
    if not os.path.exists(yaml_path):
        return None

    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
            return data.get("baseline_tokens")
    except Exception as e:
        print(f"警告: 读取基准 token 失败: {e}")
        return None


def calculate_token_diff(current, baseline):
    """计算 token 差值"""
    if not baseline:
        return current

    return {
        "input_tokens": current.get("input_tokens", 0) - baseline.get("input", 0),
        "output_tokens": current.get("output_tokens", 0) - baseline.get("output", 0),
        "cache_create_tokens": current.get("cache_create_tokens", 0) - baseline.get("cache_create", 0),
        "cache_read_tokens": current.get("cache_read_tokens", 0) - baseline.get("cache_read", 0),
        "total_tokens": current.get("total_tokens", 0) - baseline.get("total", 0),
        "cost": current.get("cost", 0),
        "models": current.get("models", "")
    }


def get_token_stats(repo_root, change_dir=None):
    """获取当前项目的 token 消耗统计

    Args:
        repo_root: Git 仓库根目录
        change_dir: 变更目录路径（用于读取基准 token）

    Returns:
        dict: token 统计数据（差值或当前值）
    """
    # 检查 ccusage 是否已安装
    if not check_ccusage_installed():
        if prompt_install_ccusage():
            if not install_ccusage():
                return None
        else:
            print("跳过 token 统计采集")
            return None

    # 获取所有 session 数据
    stdout, returncode = run_cmd(["ccusage", "session", "--json"], shell=True)
    if returncode != 0 or not stdout:
        print("警告: 无法获取 ccusage 数据")
        return None

    try:
        data = json.loads(stdout)
        sessions = data.get("sessions", [])

        if not sessions:
            print("提示: 没有找到 session 数据")
            return None

        # 获取项目路径用于匹配
        repo_path = repo_root.replace("\\", "/").replace("/", "-").lower()
        repo_basename = os.path.basename(repo_root)

        # 尝试匹配当前项目的 session
        matched_session = None
        for session in sessions:
            session_id = session.get("sessionId", "")
            # 匹配策略：session ID 包含项目路径或项目名称
            if repo_basename.lower() in session_id.lower() or repo_path in session_id.lower():
                matched_session = session
                break

        # 如果没有精确匹配，使用最新的 session
        if not matched_session:
            # 按最后活动时间排序，获取最新的
            matched_session = max(sessions, key=lambda s: s.get("lastActivity", ""))
            print(f"提示: 未精确匹配 session，使用最新 session")

        # 聚合多模型数据
        model_breakdowns = matched_session.get("modelBreakdowns", [])

        input_tokens = sum(m.get("inputTokens", 0) for m in model_breakdowns)
        output_tokens = sum(m.get("outputTokens", 0) for m in model_breakdowns)
        cache_create_tokens = sum(m.get("cacheCreationTokens", 0) for m in model_breakdowns)
        cache_read_tokens = sum(m.get("cacheReadTokens", 0) for m in model_breakdowns)
        total_tokens = matched_session.get("totalTokens", 0)
        cost = matched_session.get("totalCost", 0)
        models = ",".join(matched_session.get("modelsUsed", []))

        current_tokens = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cache_create_tokens": cache_create_tokens,
            "cache_read_tokens": cache_read_tokens,
            "total_tokens": total_tokens,
            "cost": round(cost, 4),
            "models": models
        }

        # 读取基准 token 并计算差值
        baseline = None
        if change_dir:
            baseline = read_baseline_tokens(change_dir)

        if baseline:
            # 计算差值
            diff_tokens = calculate_token_diff(current_tokens, baseline)
            print(f"Token 差值计算: 总计 {diff_tokens['total_tokens']:,} (当前 {current_tokens['total_tokens']:,} - 基准 {baseline.get('total', 0):,})")
            return diff_tokens
        else:
            # 无基准，使用当前值并打印警告
            print("警告: 无基准 token，使用累计值（变更可能在新功能实现前创建）")
            return current_tokens

    except json.JSONDecodeError as e:
        print(f"警告: 解析 ccusage JSON 失败: {e}")
        return None
    except Exception as e:
        print(f"警告: 获取 token 统计失败: {e}")
        return None


# ============ CSV 统计逻辑 ============


# CSV 文件路径常量
CSV_HEADERS = ["id", "author", "timestamp", "additions", "deletions", "total_lines", "project_name",
               "input_tokens", "output_tokens", "cache_create_tokens", "cache_read_tokens",
               "total_tokens", "cost", "models", "spec_files", "spec_lines"]


def collect_stats(change_dir=None):
    """收集代码变更统计

    Args:
        change_dir: 归档的变更目录路径（用于读取基准 token）
    """
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
        # 排除 openspec 目录下的 markdown 文件
        if is_spec_markdown(file):
            continue
        additions, deletions = get_file_changes(file)
        total_additions += additions
        total_deletions += deletions

    total_lines = total_additions + total_deletions

    stats = {
        "id": str(uuid.uuid4()),
        "author": author,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "additions": total_additions,
        "deletions": total_deletions,
        "total_lines": total_lines,
        "project_name": project_name
    }

    # 获取 token 统计（传入变更目录以读取基准）
    token_stats = get_token_stats(repo_root, change_dir)
    if token_stats:
        stats.update(token_stats)
    else:
        # 填充空值
        stats.update({
            "input_tokens": "",
            "output_tokens": "",
            "cache_create_tokens": "",
            "cache_read_tokens": "",
            "total_tokens": "",
            "cost": "",
            "models": ""
        })

    # 获取规范文档统计
    spec_stats = collect_spec_stats(repo_root)
    stats.update(spec_stats)

    return stats


def ensure_csv_exists(csv_path):
    """确保 CSV 文件存在并有表头"""
    if not os.path.exists(csv_path):
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)
        print(f"已创建 CSV 文件: {csv_path}")


def migrate_csv_headers(csv_path):
    """为旧 CSV 文件追加新表头"""
    if not os.path.exists(csv_path):
        return

    with open(csv_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader, [])
        rows = list(reader)

    # 检查是否需要迁移
    if len(headers) >= len(CSV_HEADERS):
        return  # 已经是新格式

    # 计算需要添加的新字段
    new_fields = CSV_HEADERS[len(headers):]
    if not new_fields:
        return

    print(f"检测到旧 CSV 格式，正在迁移，添加字段: {new_fields}")

    # 重写文件
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADERS)
        for row in rows:
            # 为旧行填充空值
            extended_row = row + [''] * len(new_fields)
            writer.writerow(extended_row)

    print(f"CSV 迁移完成，新增 {len(new_fields)} 个字段")


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
            stats["project_name"],
            stats.get("input_tokens", ""),
            stats.get("output_tokens", ""),
            stats.get("cache_create_tokens", ""),
            stats.get("cache_read_tokens", ""),
            stats.get("total_tokens", ""),
            stats.get("cost", ""),
            stats.get("models", ""),
            stats.get("spec_files", 0),
            stats.get("spec_lines", 0)
        ])
    print(f"已追加记录到: {csv_path}")


def find_recent_archived_change(repo_root):
    """找到最近归档的变更目录

    Returns:
        str: 最近归档的变更目录路径，如果没有则返回 None
    """
    archive_dir = os.path.join(repo_root, "openspec", "changes", "archive")
    if not os.path.exists(archive_dir):
        return None

    # 获取所有归档目录
    archived_changes = []
    for name in os.listdir(archive_dir):
        change_path = os.path.join(archive_dir, name)
        if os.path.isdir(change_path):
            # 获取修改时间
            mtime = os.path.getmtime(change_path)
            archived_changes.append((change_path, mtime))

    if not archived_changes:
        return None

    # 按修改时间排序，返回最新的
    archived_changes.sort(key=lambda x: x[1], reverse=True)
    return archived_changes[0][0]


def main():
    repo_root = get_git_root()
    openspec_dir = os.path.join(repo_root, "openspec")
    csv_path = os.path.join(openspec_dir, "ai.summary.csv")

    # 确保 openspec 目录存在
    if not os.path.exists(openspec_dir):
        os.makedirs(openspec_dir)

    # 确保 CSV 文件存在
    ensure_csv_exists(csv_path)

    # 迁移旧 CSV 格式
    migrate_csv_headers(csv_path)

    # 查找最近归档的变更目录（用于读取基准 token）
    change_dir = find_recent_archived_change(repo_root)
    if change_dir:
        print(f"检测到归档变更: {os.path.basename(change_dir)}")

    # 收集统计信息
    stats = collect_stats(change_dir)

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

    # 输出 token 统计
    if stats.get("total_tokens"):
        print("\nToken 消耗统计:")
        print(f"  输入: {stats['input_tokens']:,}")
        print(f"  输出: {stats['output_tokens']:,}")
        print(f"  缓存创建: {stats['cache_create_tokens']:,}")
        print(f"  缓存读取: {stats['cache_read_tokens']:,}")
        print(f"  总计: {stats['total_tokens']:,}")
        print(f"  成本: ${stats['cost']}")
        print(f"  模型: {stats['models']}")

    # 输出规范文档统计
    if stats.get("spec_files", 0) > 0:
        print("\n规范文档统计:")
        print(f"  文件数: {stats['spec_files']}")
        print(f"  总行数: {stats['spec_lines']}")


if __name__ == "__main__":
    main()
