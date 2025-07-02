#!/usr/bin/env node
/**
 * AI文章チェックスクリプト
 * textlint-rule-preset-ai-writingを使用して文章の品質をチェック
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// チェック対象のファイルパターン
const FILE_PATTERNS = [
  'sessions/*.md',
  '*.md',
  'docs/*.md',
  'COLAB_USAGE.md',
  'VERCEL_*.md'
];

// 除外するファイル
const EXCLUDE_PATTERNS = [
  'node_modules',
  '.git',
  'dist',
  'build',
  '.vercel'
];

// カラー出力用のANSIコード
const colors = {
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m'
};

// ヘルプメッセージ
function showHelp() {
  console.log(`
${colors.blue}📝 AI文章チェックツール${colors.reset}

使用方法:
  node scripts/check-writing.js [オプション] [ファイルパス]

オプション:
  --fix, -f      自動修正を適用
  --sessions     セッションファイルのみチェック
  --docs         ドキュメントファイルのみチェック
  --all          すべてのマークダウンファイルをチェック
  --help, -h     このヘルプを表示

例:
  node scripts/check-writing.js                    # デフォルトのファイルをチェック
  node scripts/check-writing.js --fix             # 自動修正を適用
  node scripts/check-writing.js README.md         # 特定のファイルをチェック
  node scripts/check-writing.js --sessions --fix  # セッションファイルを自動修正

${colors.yellow}検出されるパターン:${colors.reset}
  • AI生成特有のリストフォーマット
  • 過度に誇張された表現
  • 機械的な強調パターン
  • 技術文書のベストプラクティス違反
`);
}

// textlintが利用可能かチェック
function checkTextlintInstalled() {
  try {
    execSync('npx textlint --version', { stdio: 'ignore' });
    return true;
  } catch (error) {
    return false;
  }
}

// textlintを実行
function runTextlint(files, fix = false) {
  const command = fix 
    ? `npx textlint --fix ${files}`
    : `npx textlint ${files}`;
  
  try {
    const output = execSync(command, { encoding: 'utf-8' });
    return { success: true, output };
  } catch (error) {
    return { success: false, output: error.stdout || error.message };
  }
}

// 結果を整形して表示
function displayResults(result, fix) {
  if (result.success) {
    console.log(`${colors.green}✅ 文章チェック完了！問題は見つかりませんでした。${colors.reset}`);
  } else {
    console.log(`${colors.red}❌ 文章に改善可能な箇所が見つかりました:${colors.reset}\n`);
    console.log(result.output);
    
    if (!fix) {
      console.log(`\n${colors.yellow}💡 ヒント: --fix オプションで自動修正できます${colors.reset}`);
    }
  }
}

// メイン処理
function main() {
  const args = process.argv.slice(2);
  
  // ヘルプ表示
  if (args.includes('--help') || args.includes('-h')) {
    showHelp();
    return;
  }
  
  // textlintインストールチェック
  if (!checkTextlintInstalled()) {
    console.error(`${colors.red}❌ textlintがインストールされていません。${colors.reset}`);
    console.log(`${colors.yellow}以下のコマンドでインストールしてください:${colors.reset}`);
    console.log('npm install');
    process.exit(1);
  }
  
  // オプション解析
  const fix = args.includes('--fix') || args.includes('-f');
  const sessionsOnly = args.includes('--sessions');
  const docsOnly = args.includes('--docs');
  const all = args.includes('--all');
  
  // ファイル指定
  let targetFiles;
  const nonOptionArgs = args.filter(arg => !arg.startsWith('--') && !arg.startsWith('-'));
  
  if (nonOptionArgs.length > 0) {
    // 特定のファイルが指定された場合
    targetFiles = nonOptionArgs.join(' ');
  } else if (sessionsOnly) {
    targetFiles = 'sessions/*.md';
  } else if (docsOnly) {
    targetFiles = '*.md docs/*.md';
  } else if (all) {
    targetFiles = '**/*.md';
  } else {
    // デフォルト
    targetFiles = FILE_PATTERNS.join(' ');
  }
  
  console.log(`${colors.blue}🔍 文章チェックを開始します...${colors.reset}`);
  console.log(`対象: ${targetFiles}`);
  
  if (fix) {
    console.log(`${colors.yellow}🔧 自動修正モードが有効です${colors.reset}`);
  }
  
  console.log('');
  
  // textlint実行
  const result = runTextlint(targetFiles, fix);
  displayResults(result, fix);
  
  // 統計情報の表示
  if (!result.success) {
    try {
      const stats = execSync(`npx textlint ${targetFiles} --format json`, { encoding: 'utf-8' });
      const data = JSON.parse(stats);
      let totalErrors = 0;
      let totalWarnings = 0;
      
      data.forEach(file => {
        totalErrors += file.messages.filter(m => m.severity === 2).length;
        totalWarnings += file.messages.filter(m => m.severity === 1).length;
      });
      
      console.log(`\n${colors.blue}📊 統計:${colors.reset}`);
      console.log(`  エラー: ${totalErrors}`);
      console.log(`  警告: ${totalWarnings}`);
      console.log(`  チェックしたファイル数: ${data.length}`);
    } catch (e) {
      // JSON形式での取得に失敗した場合は無視
    }
  }
  
  // 終了コード
  process.exit(result.success ? 0 : 1);
}

// 実行
if (require.main === module) {
  main();
}