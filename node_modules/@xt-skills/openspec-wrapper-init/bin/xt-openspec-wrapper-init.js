#!/usr/bin/env node

/**
 * xt-openspec-wrapper-init
 * 初始化 xt-openspec-wrapper 到当前项目
 */

const fs = require('fs');
const path = require('path');
const { execSync, spawnSync } = require('child_process');

// 配置
// 使用 process.cwd() 作为项目根目录（npm install 的目标项目）
// 使用 __filename 获取当前文件绝对路径，从而定位依赖包内的 lib 目录
const PROJECT_ROOT = process.cwd();
const CURRENT_FILE_DIR = path.dirname(__filename);
const PACKAGE_DIR = path.dirname(CURRENT_FILE_DIR); // __filename 返回 bin 目录，需取上一级
const SOURCE_DIR = path.join(PACKAGE_DIR, 'lib');

// 目标目录（基于项目根目录的绝对路径）
const TARGET_CLAUDE_DIR = path.join(PROJECT_ROOT, '.claude');
const TARGET_CMD_DIR = path.join(PROJECT_ROOT, '.claude', 'commands', 'xt');
const TARGET_SKILL_DIR = path.join(PROJECT_ROOT, '.claude', 'skills', 'xt-openspec-wrapper');


console.error('PROJECT_ROOT', PROJECT_ROOT)
console.error('CURRENT_FILE_DIR', CURRENT_FILE_DIR)
console.error('PACKAGE_DIR', PACKAGE_DIR)
console.error('SOURCE_DIR', SOURCE_DIR)
console.error('TARGET_CLAUDE_DIR', TARGET_CLAUDE_DIR)
console.error('TARGET_CMD_DIR', TARGET_CMD_DIR)
console.error('TARGET_SKILL_DIR', TARGET_SKILL_DIR)


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

/**
 * 检查命令是否已安装
 * @param {string} command - 命令名称
 * @returns {boolean} - 是否已安装
 */
function checkCommandInstalled(command) {
  try {
    const result = spawnSync(command, ['--version'], {
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'ignore']
    });
    return result.status === 0;
  } catch (e) {
    return false;
  }
}

/**
 * 安装全局 npm 包
 * @param {string} packageName - 包名称
 * @param {string} displayName - 显示名称
 * @returns {boolean} - 是否安装成功
 */
function installGlobal(packageName, displayName) {
  console.log(`   安装 ${displayName}...`);
  try {
    execSync(`npm install -g ${packageName}`, {
      stdio: ['pipe', process.stdout, process.stderr],
      encoding: 'utf-8'
    });
    console.log(`   ✓ ${displayName} 安装完成`);
    return true;
  } catch (e) {
    console.log(`   ✗ ${displayName} 安装失败`);
    console.log('   错误: 请手动运行以下命令安装:');
    console.log(`     npm install -g ${packageName}`);
    return false;
  }
}

/**
 * 运行命令初始化
 * @param {string} command - 命令名称
 * @param {string} args - 命令参数
 * @param {string} displayName - 显示名称
 */
function runInit(command, args, displayName) {
  console.log(`   初始化 ${displayName}...`);
  try {
    execSync(`${command} ${args}`, {
      stdio: ['pipe', process.stdout, process.stderr],
      encoding: 'utf-8'
    });
    console.log(`   ✓ ${displayName} 初始化完成`);
  } catch (e) {
    console.log(`   ✗ ${displayName} 初始化失败`);
    console.log(`   错误: 请手动运行 "${command} ${args}" 初始化`);
  }
}

/**
 * 检查和安装依赖
 * - 检查 openspec 和 openspec-cn 是否安装
 * - 如未安装则自动安装
 * - 如已安装则运行初始化
 */
function checkAndInstallDependencies() {
  console.log('正在检查依赖...');

  // 检查 openspec
  const openspecInstalled = checkCommandInstalled('openspec');
  if (!openspecInstalled) {
    console.log('   未检测到 openspec，正在安装...');
    installGlobal('@fission-ai/openspec@latest', 'openspec');
  } else {
    console.log('   ✓ openspec 已安装');
    runInit('openspec init --tools claude,cursor', '', 'openspec');
  }

  // 检查 openspec-cn
  const openspecCnInstalled = checkCommandInstalled('openspec-cn');
  if (!openspecCnInstalled) {
    console.log('   未检测到 openspec-cn，正在安装...');
    installGlobal('@studyzy/openspec-cn@latest', 'openspec-cn');
  } else {
    console.log('   ✓ openspec-cn 已安装');
    runInit('openspec-cn init --tools claude,cursor', '', 'openspec-cn');
  }
}

function main() {
  console.log('正在初始化 xt-openspec-wrapper...\n');

  // 0. 检查和安装依赖
  console.log('0. 检查和安装依赖...');
  checkAndInstallDependencies();
  console.log();

  // 1. 创建目录结构
  console.log('1. 创建目录结构...');
  ensureDirectory(TARGET_CMD_DIR);
  ensureDirectory(TARGET_SKILL_DIR);
  ensureDirectory(path.join(TARGET_SKILL_DIR, 'scripts'));
  ensureDirectory(path.join(TARGET_SKILL_DIR, 'references'));
  ensureDirectory(path.join(TARGET_SKILL_DIR, 'assets'));
  console.log('   ✓ 目录创建完成\n');

  // 2. 复制命令文件
  console.log('2. 复制命令文件...');
  COMMAND_FILES.forEach(file => {
    const sourceFile = path.join(SOURCE_DIR, 'commands', file);
    const targetFile = path.join(TARGET_CMD_DIR, file);
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
    const targetFile = path.join(TARGET_SKILL_DIR, file);
    if (fs.existsSync(sourceFile)) {
      fs.copyFileSync(sourceFile, targetFile);
      console.log(`   ✓ ${file}`);
    }
  });

  // 复制脚本文件
  const scriptFiles = ['archive_with_stats.py', 'collect_git_stats.py'];
  scriptFiles.forEach(file => {
    const sourceFile = path.join(SOURCE_DIR, 'scripts', file);
    const targetFile = path.join(TARGET_SKILL_DIR, 'scripts', file);
    if (fs.existsSync(sourceFile)) {
      fs.copyFileSync(sourceFile, targetFile);
      console.log(`   ✓ ${file}`);
    }
  });
  console.log();

  // 4. 更新 settings.local.json
  console.log('4. 检查 settings.local.json 配置...');
  const settingsPath = path.join(TARGET_CLAUDE_DIR, 'settings.local.json');

  // 默认配置
  const defaultSettings = {
    permissions: {
      allow: [],
      deny: [
        'Bash(git commit*)'
      ]
    }
  };

  if (fs.existsSync(settingsPath)) {
    // 合并现有配置
    console.log('   ✓ settings.local.json 已存在，合并配置...');
    try {
      const existingSettings = JSON.parse(fs.readFileSync(settingsPath, 'utf-8'));
      // 合并权限配置：合并 allow 列表，保留 deny 列表
      const mergedSettings = {
        ...existingSettings,
        permissions: {
          allow: [...(existingSettings.permissions?.allow || []), ...defaultSettings.permissions.allow],
          deny: [...(existingSettings.permissions?.deny || []), ...defaultSettings.permissions.deny]
        }
      };
      // 去重
      mergedSettings.permissions.allow = [...new Set(mergedSettings.permissions.allow)];
      mergedSettings.permissions.deny = [...new Set(mergedSettings.permissions.deny)];

      fs.writeFileSync(
        settingsPath,
        JSON.stringify(mergedSettings, null, 2) + '\n',
        'utf-8'
      );
      console.log('   ✓ 配置已合并');
    } catch (e) {
      console.log(`   ✗ 合并配置失败: ${e.message}`);
    }
  } else {
    // 创建新的 settings.local.json
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
