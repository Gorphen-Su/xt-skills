# @xt-skills/openspec-wrapper-init

OpenSpec 变更管理工具的 xt 封装层初始化脚本。

## 说明

此包提供了 `xt-openspec-wrapper-init` 命令，用于将 xt-openspec-wrapper 初始化到当前项目中。

## 安装

### 自动安装（推荐）

将此包添加到你的 `package.json` 作为依赖，npm 会在安装完成后自动执行初始化：

```json
{
  "devDependencies": {
    "@xt-skills/openspec-wrapper-init": "^1.0.0"
  }
}
```

然后运行：

```bash
npm install
```

`postinstall` 钩子会自动执行 `xt-openspec-wrapper-init`，将文件复制到 `.claude/` 目录。

### 手动安装

```bash
npm install -D @xt-skills/openspec-wrapper-init
npx xt-openspec-wrapper-init
```

或使用 npx：

```bash
npx -p @xt-skills/openspec-wrapper-init xt-openspec-wrapper-init
```

### Git 安装

你也可以使用 Git 安装：

```bash
npm install -D git+https://github.com/your-org/xt-skills.git#subdirectory=init-cli/xt-openspec-wrapper-init
```

## 初始化内容

运行 `xt-openspec-wrapper-init` 会：

1. 创建目录结构：
   - `.claude/commands/xt/` - xt 命令文件
   - `.claude/skills/xt-openspec-wrapper/` - skill 文件
   - `.claude/skills/xt-openspec-wrapper/scripts/` - Python 脚本

2. 复制文件：
   - 11 个 xt 命令文件
   - SKILL.md
   - Python 脚本（archive_with_stats.py, collect_git_stats.py）

3. 创建/更新 `.claude/settings.local.json`（添加 `deny: [Bash(git commit*)]`）

## 后续步骤

初始化完成后：

1. **检查并更新 `.claude/settings.local.json`**

   确保权限配置正确，可能需要添加本地路径到 allow 列表：

   ```json
   {
     "permissions": {
       "allow": [
         "Bash(mkdir -p \"C:/Users/GorphenSu/.claude/skills/openspec-wrapper\")",
         "Bash(mkdir -p \"C:/Users/GorphenSu/.claude/skills/openspec-wrapper/scripts\")",
         "Bash(mkdir -p \"C:/Users/GorphenSu/.claude/skills/openspec-wrapper/references\")",
         "Bash(mkdir -p \"C:/Users/GorphenSu/.claude/skills/openspec-wrapper/assets\")"
       ],
       "deny": [
         "Bash(git commit*)"
       ]
     }
   }
   ```

2. **暂存并提交文件**（可选，用于团队共享）：

   ```bash
   git add .
   ```

## 可用命令

初始化后，你可以使用以下 xt 命令：

| 命令 | 描述 |
|------|------|
| `/xt:explore` | 探索模式，构思想法和澄清需求 |
| `/xt:new` | 启动新 OpenSpec 变更 |
| `/xt:propose` | 快速提案新变更并生成所有产出物 |
| `/xt:apply` | 实现 OpenSpec 变更中的任务 |
| `/xt:continue` | 继续创建 OpenSpec 变更的产出物 |
| `/xt:archive` | 归档已完成的 OpenSpec 变更（含代码变更统计） |
| `/xt:bulk-archive` | 批量归档多个已完成的 OpenSpec 变更 |
| `/xt:sync` | 同步增量规范到主规范 |
| `/xt:verify` | 验证实现是否与变更产出物匹配 |
| `/xt:onboard` | OpenSpec 引导式入门 |

## 相关项目

- [OpenSpec](https://github.com/your-org/openspec) - OpenSpec 变更管理系统
- [xt-skills](https://github.com/your-org/xt-skills) - xt 封装层项目

## 许可证

MIT
