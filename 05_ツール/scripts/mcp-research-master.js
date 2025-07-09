#!/usr/bin/env node

/**
 * MCP統合研究自動化マスターシステム
 * 研究作業の全プロセスを自動化（データ収集、実験、分析、レポート作成）
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

class MCPResearchMaster {
    constructor() {
        this.env = this.loadEnv();
        this.mcpPlaywrightUrl = 'http://localhost:9222';
        this.mcpFigmaUrl = 'http://localhost:9223';
        this.researchConfig = {
            dataPath: path.join(__dirname, '..', '03_研究資料'),
            experimentsPath: path.join(__dirname, '..', '03_研究資料', 'research', 'experiments'),
            reportsPath: path.join(__dirname, '..', '03_研究資料', 'research', 'reports'),
            graphsPath: path.join(__dirname, '..', '03_研究資料', 'research', 'graphs'),
            websitePath: path.join(__dirname, '..', '02_ウェブサイト'),
            systemPath: path.join(__dirname, '..', '04_システム実装')
        };
        
        this.researchSession = {
            id: Date.now(),
            startTime: new Date().toISOString(),
            tasks: [],
            results: {},
            experiments: [],
            reports: [],
            success: false
        };
    }

    loadEnv() {
        const envPath = path.join(__dirname, '..', '.env');
        const envContent = fs.readFileSync(envPath, 'utf8');
        const env = {};
        
        envContent.split('\n').forEach(line => {
            const [key, value] = line.split('=');
            if (key && value) {
                env[key] = value.trim();
            }
        });
        
        return env;
    }

    async sendMCPCommand(command, server = 'playwright') {
        const url = server === 'playwright' ? this.mcpPlaywrightUrl : this.mcpFigmaUrl;
        
        try {
            const response = await fetch(`${url}/mcp`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    id: Date.now(),
                    method: 'tools/call',
                    params: {
                        name: server === 'playwright' ? 'playwright_action' : 'figma_action',
                        arguments: command
                    }
                })
            });

            if (response.ok) {
                return await response.json();
            } else {
                throw new Error(`MCP通信エラー: ${response.status}`);
            }
        } catch (error) {
            console.error(`❌ MCP通信失敗 (${server}):`, error.message);
            throw error;
        }
    }

    async initializeResearchEnvironment() {
        console.log('🔬 研究環境初期化中...');
        
        // 必要なディレクトリを作成
        const requiredDirs = [
            'research-automation',
            'research-reports',
            'experiment-results',
            'auto-graphs',
            'research-presentations'
        ];
        
        requiredDirs.forEach(dir => {
            const dirPath = path.join(__dirname, '..', dir);
            if (!fs.existsSync(dirPath)) {
                fs.mkdirSync(dirPath, { recursive: true });
                console.log(`📁 ディレクトリ作成: ${dir}`);
            }
        });
        
        // Playwright初期化
        const playwrightInit = {
            action: 'launch_browser',
            options: {
                headless: true,
                args: ['--no-sandbox', '--disable-setuid-sandbox']
            }
        };
        
        await this.sendMCPCommand(playwrightInit);
        console.log('✅ 研究環境初期化完了');
    }

    async autoDataCollection() {
        console.log('📊 自動データ収集開始...');
        
        const dataTask = {
            name: 'データ収集',
            startTime: new Date().toISOString(),
            results: []
        };
        
        try {
            // 研究資料フォルダからデータを収集
            const researchFiles = this.scanResearchDirectory();
            dataTask.results.push({
                type: 'file_scan',
                count: researchFiles.length,
                files: researchFiles
            });
            
            // 実験データを収集
            const experimentData = await this.collectExperimentData();
            dataTask.results.push({
                type: 'experiment_data',
                experiments: experimentData
            });
            
            // ウェブサイトからデータを収集
            const websiteData = await this.collectWebsiteData();
            dataTask.results.push({
                type: 'website_data',
                data: websiteData
            });
            
            dataTask.status = 'completed';
            dataTask.endTime = new Date().toISOString();
            
            this.researchSession.tasks.push(dataTask);
            console.log('✅ データ収集完了');
            
            return dataTask;
            
        } catch (error) {
            dataTask.status = 'failed';
            dataTask.error = error.message;
            console.error('❌ データ収集失敗:', error.message);
            throw error;
        }
    }

    scanResearchDirectory() {
        const files = [];
        
        const scanDir = (dirPath) => {
            if (!fs.existsSync(dirPath)) return;
            
            const items = fs.readdirSync(dirPath);
            items.forEach(item => {
                const itemPath = path.join(dirPath, item);
                const stat = fs.statSync(itemPath);
                
                if (stat.isDirectory()) {
                    scanDir(itemPath);
                } else if (item.endsWith('.py') || item.endsWith('.json') || item.endsWith('.md')) {
                    files.push({
                        path: itemPath,
                        name: item,
                        size: stat.size,
                        modified: stat.mtime
                    });
                }
            });
        };
        
        scanDir(this.researchConfig.dataPath);
        return files;
    }

    async collectExperimentData() {
        console.log('🧪 実験データ収集中...');
        
        const experiments = [];
        
        // Pythonスクリプトを自動実行
        const pythonFiles = fs.readdirSync(this.researchConfig.experimentsPath)
            .filter(file => file.endsWith('.py'));
        
        for (const pythonFile of pythonFiles) {
            try {
                const filePath = path.join(this.researchConfig.experimentsPath, pythonFile);
                console.log(`🐍 実行中: ${pythonFile}`);
                
                const result = execSync(`python3 "${filePath}"`, { 
                    encoding: 'utf8',
                    timeout: 60000
                });
                
                experiments.push({
                    name: pythonFile,
                    status: 'success',
                    output: result,
                    timestamp: new Date().toISOString()
                });
                
            } catch (error) {
                experiments.push({
                    name: pythonFile,
                    status: 'failed',
                    error: error.message,
                    timestamp: new Date().toISOString()
                });
            }
        }
        
        return experiments;
    }

    async collectWebsiteData() {
        console.log('🌐 ウェブサイトデータ収集中...');
        
        const websiteCommand = {
            action: 'navigate',
            url: 'https://study-research-final.vercel.app'
        };
        
        try {
            await this.sendMCPCommand(websiteCommand);
            
            const performanceCommand = {
                action: 'evaluate',
                expression: `
                    const perfData = performance.getEntriesByType('navigation')[0];
                    const resources = performance.getEntriesByType('resource');
                    
                    return {
                        loadTime: perfData.loadEventEnd - perfData.navigationStart,
                        resourceCount: resources.length,
                        pageTitle: document.title,
                        lastModified: document.lastModified,
                        links: Array.from(document.querySelectorAll('a')).map(a => a.href).slice(0, 10)
                    };
                `
            };
            
            const websiteData = await this.sendMCPCommand(performanceCommand);
            return websiteData;
            
        } catch (error) {
            console.error('⚠️ ウェブサイトデータ収集失敗:', error.message);
            return { error: error.message };
        }
    }

    async autoExperimentExecution() {
        console.log('🔬 自動実験実行開始...');
        
        const experimentTask = {
            name: '実験実行',
            startTime: new Date().toISOString(),
            experiments: []
        };
        
        try {
            // 最小単位実験システムの実行
            const minimalExperiment = await this.runMinimalExperiment();
            experimentTask.experiments.push(minimalExperiment);
            
            // パフォーマンス実験の実行
            const performanceExperiment = await this.runPerformanceExperiment();
            experimentTask.experiments.push(performanceExperiment);
            
            // 自動グラフ生成
            const graphGeneration = await this.autoGenerateGraphs();
            experimentTask.experiments.push(graphGeneration);
            
            experimentTask.status = 'completed';
            experimentTask.endTime = new Date().toISOString();
            
            this.researchSession.tasks.push(experimentTask);
            console.log('✅ 実験実行完了');
            
            return experimentTask;
            
        } catch (error) {
            experimentTask.status = 'failed';
            experimentTask.error = error.message;
            console.error('❌ 実験実行失敗:', error.message);
            throw error;
        }
    }

    async runMinimalExperiment() {
        console.log('🧪 最小単位実験実行中...');
        
        try {
            const experimentScript = path.join(this.researchConfig.dataPath, '実験方針', 'minimal_experiment_template.py');
            
            if (fs.existsSync(experimentScript)) {
                const result = execSync(`python3 "${experimentScript}"`, { 
                    encoding: 'utf8',
                    timeout: 120000
                });
                
                return {
                    name: '最小単位実験',
                    status: 'success',
                    output: result,
                    timestamp: new Date().toISOString()
                };
            } else {
                return {
                    name: '最小単位実験',
                    status: 'skipped',
                    reason: 'スクリプトファイルが見つかりません',
                    timestamp: new Date().toISOString()
                };
            }
            
        } catch (error) {
            return {
                name: '最小単位実験',
                status: 'failed',
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    async runPerformanceExperiment() {
        console.log('⚡ パフォーマンス実験実行中...');
        
        try {
            const performanceScript = path.join(this.researchConfig.experimentsPath, 'performance_optimization_experiment.py');
            
            if (fs.existsSync(performanceScript)) {
                const result = execSync(`python3 "${performanceScript}"`, { 
                    encoding: 'utf8',
                    timeout: 120000
                });
                
                return {
                    name: 'パフォーマンス実験',
                    status: 'success',
                    output: result,
                    timestamp: new Date().toISOString()
                };
            } else {
                return {
                    name: 'パフォーマンス実験',
                    status: 'skipped',
                    reason: 'スクリプトファイルが見つかりません',
                    timestamp: new Date().toISOString()
                };
            }
            
        } catch (error) {
            return {
                name: 'パフォーマンス実験',
                status: 'failed',
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    async autoGenerateGraphs() {
        console.log('📈 自動グラフ生成中...');
        
        try {
            const graphScript = path.join(this.researchConfig.experimentsPath, 'html_experiment_graphs.py');
            
            if (fs.existsSync(graphScript)) {
                const result = execSync(`python3 "${graphScript}"`, { 
                    encoding: 'utf8',
                    timeout: 120000
                });
                
                // 生成されたグラフファイルを確認
                const graphFiles = fs.readdirSync(this.researchConfig.graphsPath)
                    .filter(file => file.endsWith('.html'))
                    .map(file => ({
                        name: file,
                        path: path.join(this.researchConfig.graphsPath, file),
                        created: fs.statSync(path.join(this.researchConfig.graphsPath, file)).mtime
                    }));
                
                return {
                    name: '自動グラフ生成',
                    status: 'success',
                    output: result,
                    generatedFiles: graphFiles,
                    timestamp: new Date().toISOString()
                };
            } else {
                return {
                    name: '自動グラフ生成',
                    status: 'skipped',
                    reason: 'グラフ生成スクリプトが見つかりません',
                    timestamp: new Date().toISOString()
                };
            }
            
        } catch (error) {
            return {
                name: '自動グラフ生成',
                status: 'failed',
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    async autoReportGeneration() {
        console.log('📝 自動レポート生成開始...');
        
        const reportTask = {
            name: 'レポート生成',
            startTime: new Date().toISOString(),
            reports: []
        };
        
        try {
            // 研究進捗レポート生成
            const progressReport = await this.generateProgressReport();
            reportTask.reports.push(progressReport);
            
            // 実験結果レポート生成
            const experimentReport = await this.generateExperimentReport();
            reportTask.reports.push(experimentReport);
            
            // HTMLプレゼンテーション生成
            const presentationReport = await this.generatePresentation();
            reportTask.reports.push(presentationReport);
            
            reportTask.status = 'completed';
            reportTask.endTime = new Date().toISOString();
            
            this.researchSession.tasks.push(reportTask);
            console.log('✅ レポート生成完了');
            
            return reportTask;
            
        } catch (error) {
            reportTask.status = 'failed';
            reportTask.error = error.message;
            console.error('❌ レポート生成失敗:', error.message);
            throw error;
        }
    }

    async generateProgressReport() {
        console.log('📊 研究進捗レポート生成中...');
        
        const progressData = {
            sessionId: this.researchSession.id,
            timestamp: new Date().toISOString(),
            tasks: this.researchSession.tasks,
            experiments: this.researchSession.experiments,
            summary: {
                totalTasks: this.researchSession.tasks.length,
                completedTasks: this.researchSession.tasks.filter(t => t.status === 'completed').length,
                failedTasks: this.researchSession.tasks.filter(t => t.status === 'failed').length
            }
        };
        
        const reportPath = path.join(__dirname, '..', 'research-reports', `progress-report-${Date.now()}.json`);
        fs.writeFileSync(reportPath, JSON.stringify(progressData, null, 2));
        
        return {
            name: '研究進捗レポート',
            status: 'success',
            path: reportPath,
            timestamp: new Date().toISOString()
        };
    }

    async generateExperimentReport() {
        console.log('🔬 実験結果レポート生成中...');
        
        const experimentData = this.researchSession.tasks
            .filter(task => task.name === '実験実行')
            .map(task => task.experiments)
            .flat();
        
        const htmlReport = `
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>研究実験結果レポート</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f0f8ff; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .experiment { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .success { background: #d4edda; }
        .failed { background: #f8d7da; }
        .skipped { background: #fff3cd; }
        .output { background: #f8f9fa; padding: 10px; border-radius: 3px; font-family: monospace; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔬 研究実験結果レポート</h1>
        <p>生成日時: ${new Date().toLocaleString()}</p>
        <p>実験数: ${experimentData.length}</p>
    </div>
    
    ${experimentData.map(exp => `
        <div class="experiment ${exp.status}">
            <h3>${exp.name}</h3>
            <p><strong>ステータス:</strong> ${exp.status}</p>
            <p><strong>実行時刻:</strong> ${new Date(exp.timestamp).toLocaleString()}</p>
            
            ${exp.output ? `<div class="output">${exp.output}</div>` : ''}
            ${exp.error ? `<p><strong>エラー:</strong> ${exp.error}</p>` : ''}
            ${exp.generatedFiles ? `
                <div>
                    <strong>生成ファイル:</strong>
                    <ul>
                        ${exp.generatedFiles.map(file => `<li>${file.name}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        </div>
    `).join('')}
</body>
</html>
        `;
        
        const reportPath = path.join(__dirname, '..', 'research-reports', `experiment-report-${Date.now()}.html`);
        fs.writeFileSync(reportPath, htmlReport);
        
        return {
            name: '実験結果レポート',
            status: 'success',
            path: reportPath,
            timestamp: new Date().toISOString()
        };
    }

    async generatePresentation() {
        console.log('📊 プレゼンテーション生成中...');
        
        const presentationHTML = `
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>研究成果プレゼンテーション</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .slide { background: white; padding: 40px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .slide h1 { color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }
        .slide h2 { color: #666; }
        .highlight { background: #e7f3ff; padding: 15px; border-left: 4px solid #007bff; margin: 15px 0; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .metric { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }
    </style>
</head>
<body>
    <div class="slide">
        <h1>🎯 研究成果自動化システム</h1>
        <h2>MCP統合による研究プロセス最適化</h2>
        <p>実行日時: ${new Date().toLocaleString()}</p>
        
        <div class="highlight">
            <h3>📊 システム概要</h3>
            <p>Playwright MCP と Figma MCP を活用した研究作業の完全自動化</p>
        </div>
    </div>
    
    <div class="slide">
        <h1>📈 実行結果</h1>
        
        <div class="metrics">
            <div class="metric">
                <h3>${this.researchSession.tasks.length}</h3>
                <p>実行タスク数</p>
            </div>
            <div class="metric">
                <h3>${this.researchSession.tasks.filter(t => t.status === 'completed').length}</h3>
                <p>完了タスク数</p>
            </div>
            <div class="metric">
                <h3>${this.researchSession.experiments.length}</h3>
                <p>実行実験数</p>
            </div>
        </div>
    </div>
    
    <div class="slide">
        <h1>🔬 実験結果</h1>
        ${this.researchSession.tasks.map(task => `
            <div class="highlight">
                <h3>${task.name}</h3>
                <p><strong>ステータス:</strong> ${task.status}</p>
                <p><strong>実行時間:</strong> ${task.startTime} - ${task.endTime}</p>
            </div>
        `).join('')}
    </div>
    
    <div class="slide">
        <h1>🎉 今後の展開</h1>
        <div class="highlight">
            <h3>✅ 達成項目</h3>
            <ul>
                <li>研究プロセスの完全自動化</li>
                <li>リアルタイム実験実行</li>
                <li>自動レポート生成</li>
                <li>MCP統合システム構築</li>
            </ul>
        </div>
        
        <div class="highlight">
            <h3>🚀 次期展開</h3>
            <ul>
                <li>AI駆動型実験設計</li>
                <li>クラウド統合拡張</li>
                <li>リアルタイム協調研究</li>
            </ul>
        </div>
    </div>
</body>
</html>
        `;
        
        const presentationPath = path.join(__dirname, '..', 'research-presentations', `presentation-${Date.now()}.html`);
        fs.writeFileSync(presentationPath, presentationHTML);
        
        return {
            name: '研究プレゼンテーション',
            status: 'success',
            path: presentationPath,
            timestamp: new Date().toISOString()
        };
    }

    async autoWebsiteUpdate() {
        console.log('🌐 ウェブサイト自動更新開始...');
        
        try {
            // 実験結果をウェブサイトに反映
            const experimentTimelinePath = path.join(this.researchConfig.websitePath, 'public', 'experiment_timeline', 'index.html');
            
            if (fs.existsSync(experimentTimelinePath)) {
                // 最新の実験結果を取得
                const latestExperiments = this.researchSession.tasks
                    .filter(task => task.name === '実験実行')
                    .map(task => task.experiments)
                    .flat()
                    .slice(-5); // 最新5件
                
                // HTMLを更新（簡易版）
                let html = fs.readFileSync(experimentTimelinePath, 'utf8');
                
                const updateComment = `<!-- 自動更新: ${new Date().toLocaleString()} -->`;
                html = html.replace('<!-- 自動更新:', updateComment);
                
                fs.writeFileSync(experimentTimelinePath, html);
                
                console.log('✅ ウェブサイト更新完了');
                
                return {
                    name: 'ウェブサイト更新',
                    status: 'success',
                    timestamp: new Date().toISOString()
                };
            }
            
        } catch (error) {
            console.error('❌ ウェブサイト更新失敗:', error.message);
            return {
                name: 'ウェブサイト更新',
                status: 'failed',
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    async cleanup() {
        console.log('🧹 研究環境クリーンアップ中...');
        
        try {
            await this.sendMCPCommand({ action: 'close_browser' });
            console.log('✅ クリーンアップ完了');
        } catch (error) {
            console.error('⚠️ クリーンアップエラー:', error.message);
        }
    }

    async runFullResearchCycle() {
        console.log('🎯 MCP統合研究自動化システム開始');
        console.log('=' * 80);
        
        try {
            // 1. 研究環境初期化
            await this.initializeResearchEnvironment();
            
            // 2. 自動データ収集
            await this.autoDataCollection();
            
            // 3. 自動実験実行
            await this.autoExperimentExecution();
            
            // 4. 自動レポート生成
            await this.autoReportGeneration();
            
            // 5. ウェブサイト更新
            await this.autoWebsiteUpdate();
            
            this.researchSession.success = true;
            this.researchSession.endTime = new Date().toISOString();
            
            // 最終セッションレポート保存
            const sessionPath = path.join(__dirname, '..', 'research-automation', `session-${this.researchSession.id}.json`);
            fs.writeFileSync(sessionPath, JSON.stringify(this.researchSession, null, 2));
            
            console.log('\n' + '=' * 80);
            console.log('🎉 研究自動化サイクル完了!');
            console.log(`📊 実行タスク: ${this.researchSession.tasks.length}`);
            console.log(`📄 セッション記録: ${sessionPath}`);
            console.log('=' * 80);
            
            return this.researchSession;
            
        } catch (error) {
            console.error('❌ 研究自動化失敗:', error.message);
            this.researchSession.success = false;
            this.researchSession.error = error.message;
            this.researchSession.endTime = new Date().toISOString();
            
            throw error;
        } finally {
            await this.cleanup();
        }
    }
}

// コマンドライン実行
async function main() {
    const researchMaster = new MCPResearchMaster();
    
    try {
        await researchMaster.runFullResearchCycle();
    } catch (error) {
        console.error('❌ 実行エラー:', error.message);
        process.exit(1);
    }
}

// 実行
if (require.main === module) {
    main();
}

module.exports = MCPResearchMaster;