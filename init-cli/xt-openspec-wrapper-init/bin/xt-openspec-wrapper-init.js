#!/usr/bin/env node

/**
 * xt-openspec-wrapper-init
 * 初始化 xt-openspec-wrapper 到当前项目
 */

const fs = require('fs');
const path = require('path');

// 配置
const SOURCE_DIR = path.join(__dirname, 'lib');
const TARGET_CLAUDE_DIR = '.claude';
const TARGET_CMD_DIR = path.join(TARGET_CLAUDE_DIR, 'commands', 'xt');
const TARGET_SKILL_DIR = path.join(TARGET_CLAUDE_DIR, 'skills', 'xt-openspec-wrapper');

// 命令文件列表
const COMMAND_FILES = [
  'new.md',
  'apply.md',
  'archive.md',
  'continue.md',
  'bulk-archive.md',
  'sync.md',
  'verify.md',
  'explore.md',
  'propose.md',
  'onboard.md',
  'ff.md'
];

function main() {
  const cwd = process.cwd();
  const targetClaudeDir = path.join(cwd, TARGET_CLAUDE_DIR);
  const targetCmdDir = path.join(cwd, TARGET_CMD_DIR);
  const targetSkillDir = path.join(cwd, TARGET_SKILL_DIR);

  console.log('正在初始化 xt-openspec-wrapper...\n');

  // 1. 创建目录结构
  console.log('1. 创建目录结构...');
  ensureDirectory(targetCmdDir);
  ensureDirectory(targetSkillDir);
  ensureDirectory(path.join(targetSkillDir, 'scripts'));
  ensureDirectory(path.join(targetSkillDir, 'references'));
  ensureDirectory(path.join(targetSkillDir, 'assets'));
  console.log('   ✓ 目录创建完成\n');

  // 2. 复制命令文件
  console.log('2. 复制命令文件...');
  COMMAND_FILES.forEach(file => {
    const sourceFile = path.join(SOURCE_DIR, 'commands', file);
    const targetFile = path.join(targetCmdDir, file);
    if (fs.existsSync(sourceFile)) {
      fs.copyFileSync(sourceFile, targetFile);
      console.log(`   ✓ ${file}`);
    } else {
      console.log(`   ⚠ ${file} (未找到源文件)`);
    }
  });
  console.log();

  // 3. 复制 skill 文件
  console.log('3. 复制 skill 文件...');
  const skillFiles = ['SKILL.md'];
  skillFiles.forEach(file => {
    const sourceFile = path.join(SOURCE_DIR, 'skills', file);
    const targetFile = path.join(targetSkillDir, file);
    if (fs.existsSync(sourceFile)) {
      fs.copyFileSync(sourceFile, targetFile);
      console.log(`   ✓ ${file}`);
    }
  });

  // 复制脚本文件
  const scriptFiles = ['archive_with_stats.py', 'collect_git_stats.py'];
  scriptFiles.forEach(file => {
    const sourceFile = path.join(SOURCE_DIR, 'scripts', file);
    const targetFile = path.join(targetSkillDir, 'scripts', file);
    if (fs.existsSync(sourceFile)) {
      fs.copyFileSync(sourceFile, targetFile);
      console.log(`   ✓ ${file}`);
    }
  });
  console.log();

  // 4. 更新 settings.local.json
  console.log('4. 检查 settings.local.json 配置...');
  const settingsPath = path.join(cwd, TARGET_CLAUDE_DIR, 'settings.local.json');

  if (fs.existsSync(settingsPath)) {
    console.log('   ✓ settings.local.json 已存在');
    console.log('   ⚠ 请手动添加必要的权限规则（见 README）');
  } else {
    // 创建新的 settings.local.json
    const defaultSettings = {
      permissions: {
        allow: [],
        deny: [
          'Bash(git commit*)'
        ]
      }
    };
    fs.writeFileSync(
      settingsPath,
      JSON.stringify(defaultSettings, null, 2) + '\n',
      'utf-8'
    );
    console.log('   ✓ settings.local.json 已创建（包含 deny 规则）');
  }
  console.log();

  // 5. 显示完成信息
  console.log('==========================================');
  console.log('xt-openspec-wrapper 初始化完成！');
  console.log('==========================================\n');

  console.log('已安装的文件:');
  console.log(`  - .claude/commands/xt/ (${COMMAND_FILES.length} 个命令文件)`);
  console.log(`  - .claude/skills/xt-openspec-wrapper/`);
  console.log(`    - SKILL.md`);
  console.log(`    - scripts/ (Python 脚本)\n`);

  console.log('下一步操作:');
  console.log('1. 检查并更新 .claude/settings.local.json');
  console.log('2. 运行 `git add .` 暂存新文件');
  console.log('3. 提交到版本控制（如果你希望团队使用）\n');

  console.log('使用说明:');
  console.log('  - /xt:explore    - 探索模式');
  console.log('  - /xt:new        - 创建新变更');
  console.log('  - /xt:apply      - 实现变更任务');
  console.log('  - /xt:archive    - 归档完成的变更\n');
}

function ensureDirectory(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

main();
