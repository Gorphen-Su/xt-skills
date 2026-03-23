#!/usr/bin/env python3
"""
记录变更的 token 基准到 .openspec.yaml

在 opsx:new 或 opsx:propose 时调用，记录当前 session 的 token 作为基准。
归档时计算差值，得到变更周期的实际 token 消耗。
"""

import subprocess
import json
import sys
import os
import yaml


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


def check_ccusage_installed():
    """检测 ccusage 是否已安装"""
    stdout, returncode = run_cmd(["ccusage", "--version"], shell=True)
    return returncode == 0


def get_current_tokens(repo_root):
    """获取当前 session 的 token 数据"""
    if not check_ccusage_installed():
        print("警告: ccusage 未安装，无法记录 token 基准")
        return None

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
        repo_basename = os.path.basename(repo_root)

        # 尝试匹配当前项目的 session
        matched_session = None
        for session in sessions:
            session_id = session.get("sessionId", "")
            if repo_basename.lower() in session_id.lower():
                matched_session = session
                break

        # 如果没有精确匹配，使用最新的 session
        if not matched_session:
            matched_session = max(sessions, key=lambda s: s.get("lastActivity", ""))

        # 聚合多模型数据
        model_breakdowns = matched_session.get("modelBreakdowns", [])

        return {
            "input": sum(m.get("inputTokens", 0) for m in model_breakdowns),
            "output": sum(m.get("outputTokens", 0) for m in model_breakdowns),
            "cache_create": sum(m.get("cacheCreationTokens", 0) for m in model_breakdowns),
            "cache_read": sum(m.get("cacheReadTokens", 0) for m in model_breakdowns),
            "total": matched_session.get("totalTokens", 0)
        }

    except Exception as e:
        print(f"警告: 获取 token 数据失败: {e}")
        return None


def read_openspec_yaml(change_dir):
    """读取 .openspec.yaml 文件"""
    yaml_path = os.path.join(change_dir, ".openspec.yaml")
    if not os.path.exists(yaml_path):
        return {}

    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"警告: 读取 .openspec.yaml 失败: {e}")
        return {}


def write_baseline_tokens(change_dir, tokens):
    """将基准 token 写入 .openspec.yaml"""
    yaml_path = os.path.join(change_dir, ".openspec.yaml")

    # 读取现有内容
    data = read_openspec_yaml(change_dir)

    # 添加基准 token
    data["baseline_tokens"] = tokens

    try:
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        print(f"已记录 token 基准到: {yaml_path}")
        return True
    except Exception as e:
        print(f"错误: 写入 .openspec.yaml 失败: {e}")
        return False


def record_baseline(change_name):
    """记录指定变更的 token 基准"""
    repo_root = get_git_root()
    change_dir = os.path.join(repo_root, "openspec", "changes", change_name)

    if not os.path.exists(change_dir):
        print(f"错误: 变更目录不存在: {change_dir}")
        return False

    # 获取当前 token
    tokens = get_current_tokens(repo_root)

    if tokens:
        # 写入基准
        success = write_baseline_tokens(change_dir, tokens)
        if success:
            print(f"基准 token: input={tokens['input']:,}, output={tokens['output']:,}, total={tokens['total']:,}")
        return success
    else:
        # 写入空基准
        write_baseline_tokens(change_dir, {})
        return False


def main():
    if len(sys.argv) < 2:
        print("用法: python record_baseline.py <change-name>")
        sys.exit(1)

    change_name = sys.argv[1]
    record_baseline(change_name)


if __name__ == "__main__":
    main()