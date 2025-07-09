#!/usr/bin/env node

/**
 * プロジェクト構造整理システム
 * ファイル・フォルダの整理、重複削除、構造最適化を実行
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class ProjectOrganizer {
    constructor() {
        this.rootPath = path.join(__dirname, '..');
        this.organizationPlan = {
            duplicateFiles: [],
            obsoleteFiles: [],
            restructureNeeded: [],
            namingIssues: []
        };
        
        this.newStructure = {
            '01_プロジェクト管理': {
                '記録': ['01_プロジェクト記録'],
                '計画': ['整理計画', '戦略'],
                'ディスカッション': ['第14回ディスカッション準備.md']
            },
            '02_研究成果': {
                '論文・発表': ['research/reports', 'research/analysis/analysis_reports'],
                '実験結果': ['research/experiments', 'research/analysis'],
                '分析レポート': ['research/analysis/results'],
                'グラフ・可視化': ['research/graphs', 'auto-graphs']
            },
            '03_システム実装': {
                'core': ['04_システム実装/system'],
                'api': ['scripts/mcp-*.js'],
                'ui': ['02_ウェブサイト/public']
            },
            '04_ウェブサイト': {
                'public': ['public', '02_ウェブサイト/public'],
                'assets': ['統一デザインシステム.css'],
                'deploy': ['vercel.json', 'VERCEL_URL.txt']
            },
            '05_自動化ツール': {
                'mcp': ['scripts/mcp-*.js'],
                'deploy': ['scripts/*vercel*.js', 'scripts/*deploy*.js'],
                'maintenance': ['05_ツール/tools/maintenance'],
                'research': ['scripts/research-*.js']
            },
            '06_開発環境': {
                'config': ['.devcontainer', '.mcp.json', '.env'],
                'scripts': ['scripts/*.sh', 'package.json'],
                'docs': ['*.md']
            }
        };
    }

    async analyzeDuplicateFiles() {
        console.log('🔍 重複ファイル分析中...');
        
        const duplicates = [
            {
                files: [
                    'index.html',
                    '02_ウェブサイト/index.html'
                ],
                action: 'merge',
                priority: 'high'
            },
            {
                files: [
                    'vercel.json',
                    '02_ウェブサイト/vercel.json'
                ],
                action: 'merge',
                priority: 'high'
            },
            {
                files: [
                    'unified_design_system.css',
                    '02_ウェブサイト/統一デザインシステム.css'
                ],
                action: 'merge',
                priority: 'high'
            },
            {
                files: [
                    'public/',
                    '02_ウェブサイト/public/'
                ],
                action: 'merge_directories',
                priority: 'high'
            }
        ];

        this.organizationPlan.duplicateFiles = duplicates;
        console.log(`✅ ${duplicates.length}件の重複ファイル/ディレクトリを検出`);
    }

    async findObsoleteFiles() {
        console.log('🗑️ 不要ファイル検出中...');
        
        const obsoletePatterns = [
            'public/discussion-site/index_old.html',
            'public/experiment_timeline/index_original.html',
            'public/experiment_timeline/test.html',
            '03_研究資料/research/analysis/early_development/',
            '**/*_old.*',
            '**/*_backup.*',
            '**/*_temp.*'
        ];

        const obsoleteFiles = [];
        
        for (const pattern of obsoletePatterns) {
            const filePath = path.join(this.rootPath, pattern);
            if (fs.existsSync(filePath)) {
                obsoleteFiles.push({
                    path: pattern,
                    size: this.getFileSize(filePath),
                    lastModified: this.getLastModified(filePath)
                });
            }
        }

        this.organizationPlan.obsoleteFiles = obsoleteFiles;
        console.log(`✅ ${obsoleteFiles.length}件の不要ファイルを検出`);
    }

    async analyzeMCPFiles() {
        console.log('🔧 MCPファイル分析中...');
        
        const scriptsDir = path.join(this.rootPath, 'scripts');
        const mcpFiles = fs.readdirSync(scriptsDir)
            .filter(file => file.startsWith('mcp-'))
            .map(file => ({
                name: file,
                category: this.categorizeMCPFile(file),
                path: path.join('scripts', file)
            }));

        const mcpCategories = {
            research: mcpFiles.filter(f => f.category === 'research'),
            vercel: mcpFiles.filter(f => f.category === 'vercel'),
            integration: mcpFiles.filter(f => f.category === 'integration')
        };

        console.log(`✅ MCP関連ファイル分析完了:`);
        console.log(`   - 研究系: ${mcpCategories.research.length}件`);
        console.log(`   - Vercel系: ${mcpCategories.vercel.length}件`);
        console.log(`   - 統合系: ${mcpCategories.integration.length}件`);

        return mcpCategories;
    }

    categorizeMCPFile(filename) {
        if (filename.includes('research')) return 'research';
        if (filename.includes('vercel')) return 'vercel';
        if (filename.includes('integration')) return 'integration';
        return 'other';
    }

    async executeDuplicateCleanup() {
        console.log('🧹 重複ファイル整理実行中...');
        
        for (const duplicate of this.organizationPlan.duplicateFiles) {
            try {
                await this.handleDuplicateFile(duplicate);
            } catch (error) {
                console.error(`⚠️ 重複ファイル処理エラー: ${duplicate.files[0]}`, error.message);
            }
        }
        
        console.log('✅ 重複ファイル整理完了');
    }

    async handleDuplicateFile(duplicate) {
        if (duplicate.action === 'merge') {
            const primaryFile = path.join(this.rootPath, duplicate.files[0]);
            const secondaryFile = path.join(this.rootPath, duplicate.files[1]);
            
            if (fs.existsSync(secondaryFile)) {
                // 内容比較
                const primaryContent = fs.readFileSync(primaryFile, 'utf8');
                const secondaryContent = fs.readFileSync(secondaryFile, 'utf8');
                
                if (primaryContent !== secondaryContent) {
                    console.log(`⚠️ 内容が異なるファイル: ${duplicate.files[0]}`);
                    // より新しいファイルを保持
                    const primaryStat = fs.statSync(primaryFile);
                    const secondaryStat = fs.statSync(secondaryFile);
                    
                    if (secondaryStat.mtime > primaryStat.mtime) {
                        fs.copyFileSync(secondaryFile, primaryFile);
                        console.log(`📄 新しいファイルをコピー: ${duplicate.files[1]} → ${duplicate.files[0]}`);
                    }
                }
                
                // 重複ファイルを削除
                fs.unlinkSync(secondaryFile);
                console.log(`🗑️ 重複ファイル削除: ${duplicate.files[1]}`);
            }
        } else if (duplicate.action === 'merge_directories') {
            await this.mergeDirectories(duplicate.files[0], duplicate.files[1]);
        }
    }

    async mergeDirectories(primaryDir, secondaryDir) {
        const primaryPath = path.join(this.rootPath, primaryDir);
        const secondaryPath = path.join(this.rootPath, secondaryDir);
        
        if (!fs.existsSync(secondaryPath)) return;
        
        const files = fs.readdirSync(secondaryPath);
        
        for (const file of files) {
            const sourcePath = path.join(secondaryPath, file);
            const targetPath = path.join(primaryPath, file);
            
            if (fs.statSync(sourcePath).isDirectory()) {
                if (!fs.existsSync(targetPath)) {
                    fs.mkdirSync(targetPath, { recursive: true });
                }
                await this.mergeDirectories(
                    path.join(primaryDir, file),
                    path.join(secondaryDir, file)
                );
            } else {
                if (!fs.existsSync(targetPath)) {
                    fs.copyFileSync(sourcePath, targetPath);
                    console.log(`📄 ファイルコピー: ${sourcePath} → ${targetPath}`);
                }
            }
        }
    }

    async removeObsoleteFiles() {
        console.log('🗑️ 不要ファイル削除中...');
        
        let removedCount = 0;
        
        for (const obsoleteFile of this.organizationPlan.obsoleteFiles) {
            const filePath = path.join(this.rootPath, obsoleteFile.path);
            
            try {
                if (fs.existsSync(filePath)) {
                    if (fs.statSync(filePath).isDirectory()) {
                        fs.rmSync(filePath, { recursive: true, force: true });
                    } else {
                        fs.unlinkSync(filePath);
                    }
                    console.log(`🗑️ 削除: ${obsoleteFile.path}`);
                    removedCount++;
                }
            } catch (error) {
                console.error(`⚠️ 削除エラー: ${obsoleteFile.path}`, error.message);
            }
        }
        
        console.log(`✅ ${removedCount}件の不要ファイルを削除`);
    }

    async reorganizeMCPFiles() {
        console.log('🔄 MCPファイル再構成中...');
        
        const mcpCategories = await this.analyzeMCPFiles();
        
        // 新しいディレクトリ構造を作成
        const mcpBaseDir = path.join(this.rootPath, '05_自動化ツール');
        const mcpDirs = {
            research: path.join(mcpBaseDir, 'research'),
            vercel: path.join(mcpBaseDir, 'vercel'),
            integration: path.join(mcpBaseDir, 'integration')
        };
        
        // ディレクトリ作成
        for (const dir of Object.values(mcpDirs)) {
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
            }
        }
        
        // ファイル移動
        for (const [category, files] of Object.entries(mcpCategories)) {
            for (const file of files) {
                const sourcePath = path.join(this.rootPath, file.path);
                const targetPath = path.join(mcpDirs[category], file.name);
                
                if (fs.existsSync(sourcePath)) {
                    fs.copyFileSync(sourcePath, targetPath);
                    console.log(`📄 移動: ${file.path} → ${targetPath}`);
                }
            }
        }
        
        console.log('✅ MCPファイル再構成完了');
    }

    async updatePackageJsonPaths() {
        console.log('📦 package.json パス更新中...');
        
        const packageJsonPath = path.join(this.rootPath, 'package.json');
        const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
        
        // scripts のパスを更新
        const newScripts = {};
        for (const [key, value] of Object.entries(packageJson.scripts)) {
            if (value.includes('scripts/mcp-research')) {
                newScripts[key] = value.replace('scripts/', '05_自動化ツール/research/');
            } else if (value.includes('scripts/mcp-vercel')) {
                newScripts[key] = value.replace('scripts/', '05_自動化ツール/vercel/');
            } else if (value.includes('scripts/research-vercel-integration')) {
                newScripts[key] = value.replace('scripts/', '05_自動化ツール/integration/');
            } else {
                newScripts[key] = value;
            }
        }
        
        packageJson.scripts = newScripts;
        
        fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
        console.log('✅ package.json パス更新完了');
    }

    async createProjectStructureDoc() {
        console.log('📋 プロジェクト構造ドキュメント生成中...');
        
        const docContent = `# プロジェクト構造ドキュメント

## 📁 ディレクトリ構造

\`\`\`
/workspaces/Research/
├── 01_プロジェクト管理/          # プロジェクト記録・計画
│   ├── 記録/                    # 日次記録、完了報告
│   ├── 計画/                    # 整理計画、戦略
│   └── ディスカッション/        # 議論記録
├── 02_研究成果/                 # 研究結果・分析
│   ├── 論文・発表/              # 研究報告書、プレゼン
│   ├── 実験結果/                # 実験データ、結果
│   ├── 分析レポート/            # 分析結果、統計
│   └── グラフ・可視化/          # 生成グラフ、ダッシュボード
├── 03_システム実装/             # システム開発
│   ├── core/                    # コアシステム
│   ├── api/                     # API実装
│   └── ui/                      # ユーザーインターフェース
├── 04_ウェブサイト/             # Web公開用
│   ├── public/                  # 公開ファイル
│   ├── assets/                  # 静的リソース
│   └── deploy/                  # デプロイ設定
├── 05_自動化ツール/             # 自動化システム
│   ├── research/                # 研究自動化
│   ├── vercel/                  # Vercelデプロイ
│   ├── integration/             # 統合システム
│   └── maintenance/             # メンテナンス
└── 06_開発環境/                 # 開発設定
    ├── config/                  # 設定ファイル
    ├── scripts/                 # 開発スクリプト
    └── docs/                    # ドキュメント
\`\`\`

## 🔧 主要ファイル

### 自動化システム
- **研究自動化**: \`05_自動化ツール/research/\`
- **Vercelデプロイ**: \`05_自動化ツール/vercel/\`
- **統合システム**: \`05_自動化ツール/integration/\`

### ウェブサイト
- **メインサイト**: \`04_ウェブサイト/public/\`
- **デプロイ設定**: \`04_ウェブサイト/deploy/vercel.json\`

### 研究成果
- **実験結果**: \`02_研究成果/実験結果/\`
- **分析レポート**: \`02_研究成果/分析レポート/\`
- **グラフ**: \`02_研究成果/グラフ・可視化/\`

## 📋 使用方法

### 研究自動化
\`\`\`bash
npm run research-full          # 研究プロセス全体
npm run research-deploy        # 研究→Vercelデプロイ
\`\`\`

### Vercelデプロイ
\`\`\`bash
npm run deploy-full           # フルデプロイ
npm run deploy-monitor        # 監視付きデプロイ
\`\`\`

## 🔄 整理完了日時
${new Date().toLocaleString()}

## 📊 整理結果サマリー
- 重複ファイル: ${this.organizationPlan.duplicateFiles.length}件処理
- 不要ファイル: ${this.organizationPlan.obsoleteFiles.length}件削除
- MCPファイル: 機能別に再構成
- 構造: 6つの主要カテゴリに整理
`;

        const docPath = path.join(this.rootPath, 'PROJECT_STRUCTURE.md');
        fs.writeFileSync(docPath, docContent);
        
        console.log('✅ プロジェクト構造ドキュメント生成完了');
    }

    // ユーティリティメソッド
    getFileSize(filePath) {
        try {
            return fs.statSync(filePath).size;
        } catch {
            return 0;
        }
    }

    getLastModified(filePath) {
        try {
            return fs.statSync(filePath).mtime;
        } catch {
            return new Date();
        }
    }

    async runCompleteOrganization() {
        console.log('🎯 プロジェクト完全整理開始');
        console.log('=' * 60);
        
        try {
            // 1. 分析フェーズ
            await this.analyzeDuplicateFiles();
            await this.findObsoleteFiles();
            
            // 2. 整理フェーズ
            await this.executeDuplicateCleanup();
            await this.removeObsoleteFiles();
            
            // 3. 再構成フェーズ
            await this.reorganizeMCPFiles();
            await this.updatePackageJsonPaths();
            
            // 4. ドキュメント生成
            await this.createProjectStructureDoc();
            
            console.log('\n' + '=' * 60);
            console.log('🎉 プロジェクト整理完了!');
            console.log('📋 新しい構造でプロジェクトが整理されました');
            console.log('📄 詳細は PROJECT_STRUCTURE.md を参照');
            console.log('=' * 60);
            
        } catch (error) {
            console.error('❌ プロジェクト整理エラー:', error.message);
            throw error;
        }
    }
}

// 実行
if (require.main === module) {
    const organizer = new ProjectOrganizer();
    organizer.runCompleteOrganization().catch(error => {
        console.error('❌ 実行エラー:', error);
        process.exit(1);
    });
}

module.exports = ProjectOrganizer;