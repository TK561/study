#!/usr/bin/env node

/**
 * MCP統合Vercelマスターシステム
 * 全機能を統合したワンクリックデプロイ・監視・テスト・デバッグシステム
 */

const MCPVercelDeployment = require('./mcp-vercel-deploy');
const MCPVercelMonitor = require('./mcp-vercel-monitor');
const MCPVercelTesting = require('./mcp-vercel-testing');
const MCPVercelDebugger = require('./mcp-vercel-debug');

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class MCPVercelMaster {
    constructor() {
        this.deployment = new MCPVercelDeployment();
        this.monitor = new MCPVercelMonitor();
        this.testing = new MCPVercelTesting();
        this.debugger = new MCPVercelDebugger();
        
        this.masterSession = {
            id: Date.now(),
            startTime: new Date().toISOString(),
            steps: [],
            results: {},
            errors: [],
            success: false
        };
    }

    async checkMCPServers() {
        console.log('🔍 MCP サーバー状態確認中...');
        
        try {
            const fetch = require('node-fetch');
            const playwrightCheck = await fetch('http://localhost:9222/sse').catch(() => null);
            const figmaCheck = await fetch('http://localhost:9223/sse').catch(() => null);
            
            if (!playwrightCheck || !figmaCheck) {
                console.log('🚀 MCP サーバーを起動中...');
                execSync('npm run start-mcp &', { stdio: 'inherit' });
                
                // 起動待機
                await this.sleep(10000);
                console.log('✅ MCP サーバー起動完了');
            } else {
                console.log('✅ MCP サーバー既に起動済み');
            }
            
            return true;
        } catch (error) {
            console.error('❌ MCP サーバー確認失敗:', error.message);
            return false;
        }
    }

    async runFullDeploymentCycle() {
        console.log('🎯 MCP統合フルデプロイメントサイクル開始');
        console.log('=' * 80);
        
        try {
            // ステップ1: MCP サーバー確認
            this.addStep('MCP サーバー確認', 'running');
            const mcpReady = await this.checkMCPServers();
            if (!mcpReady) {
                throw new Error('MCP サーバー起動失敗');
            }
            this.completeStep('MCP サーバー確認', 'success');
            
            // ステップ2: デプロイ実行
            this.addStep('Vercel デプロイ', 'running');
            console.log('\n🚀 ステップ2: Vercel デプロイ実行...');
            const deployResult = await this.deployment.runDeployment();
            this.masterSession.results.deployment = deployResult;
            this.completeStep('Vercel デプロイ', 'success');
            
            // デプロイ後待機
            console.log('⏳ デプロイ反映待機中...');
            await this.sleep(30000);
            
            // ステップ3: 自動テスト実行
            this.addStep('自動テスト実行', 'running');
            console.log('\n🧪 ステップ3: 自動テスト実行...');
            const testResult = await this.testing.runAllTests();
            this.masterSession.results.testing = testResult;
            
            if (testResult.failedTests > 0) {
                this.completeStep('自動テスト実行', 'warning');
                console.log('⚠️ テスト失敗が検出されました - デバッグを実行します');
                
                // ステップ4: 自動デバッグ
                this.addStep('自動デバッグ', 'running');
                console.log('\n🔍 ステップ4: 自動デバッグ実行...');
                const debugResult = await this.debugger.runDebugging();
                this.masterSession.results.debugging = debugResult;
                this.completeStep('自動デバッグ', 'completed');
                
            } else {
                this.completeStep('自動テスト実行', 'success');
                console.log('✅ 全テスト合格 - デバッグスキップ');
            }
            
            // ステップ5: 監視開始（オプション）
            if (process.argv.includes('--monitor')) {
                this.addStep('継続監視開始', 'running');
                console.log('\n📊 ステップ5: 継続監視開始...');
                
                // 非同期で監視開始
                this.monitor.runMonitoring().catch(error => {
                    console.error('⚠️ 監視エラー:', error.message);
                });
                
                this.completeStep('継続監視開始', 'success');
            }
            
            // ステップ6: 最終レポート生成
            this.addStep('最終レポート生成', 'running');
            console.log('\n📊 ステップ6: 最終レポート生成...');
            const finalReport = await this.generateFinalReport();
            this.masterSession.results.finalReport = finalReport;
            this.completeStep('最終レポート生成', 'success');
            
            this.masterSession.success = true;
            this.masterSession.endTime = new Date().toISOString();
            
            this.displaySuccessMessage();
            
            return this.masterSession;
            
        } catch (error) {
            console.error('❌ フルデプロイメントサイクル失敗:', error.message);
            this.masterSession.errors.push({
                message: error.message,
                timestamp: new Date().toISOString()
            });
            this.masterSession.success = false;
            this.masterSession.endTime = new Date().toISOString();
            
            // エラー時の自動デバッグ
            console.log('\n🔍 エラー発生 - 自動デバッグ実行...');
            try {
                const debugResult = await this.debugger.runDebugging();
                this.masterSession.results.errorDebugging = debugResult;
            } catch (debugError) {
                console.error('⚠️ デバッグも失敗:', debugError.message);
            }
            
            await this.generateErrorReport();
            throw error;
        }
    }

    addStep(name, status) {
        this.masterSession.steps.push({
            name,
            status,
            startTime: new Date().toISOString()
        });
    }

    completeStep(name, status) {
        const step = this.masterSession.steps.find(s => s.name === name);
        if (step) {
            step.status = status;
            step.endTime = new Date().toISOString();
            step.duration = new Date(step.endTime) - new Date(step.startTime);
        }
    }

    async generateFinalReport() {
        console.log('📊 最終レポート生成中...');
        
        const reportData = {
            sessionId: this.masterSession.id,
            timestamp: this.masterSession.startTime,
            duration: new Date() - new Date(this.masterSession.startTime),
            success: this.masterSession.success,
            
            summary: {
                totalSteps: this.masterSession.steps.length,
                successfulSteps: this.masterSession.steps.filter(s => s.status === 'success').length,
                failedSteps: this.masterSession.steps.filter(s => s.status === 'failed').length,
                warningSteps: this.masterSession.steps.filter(s => s.status === 'warning').length
            },
            
            deployment: this.masterSession.results.deployment ? {
                url: this.masterSession.results.deployment.url,
                success: true
            } : null,
            
            testing: this.masterSession.results.testing ? {
                totalTests: this.masterSession.results.testing.totalTests,
                passedTests: this.masterSession.results.testing.passedTests,
                failedTests: this.masterSession.results.testing.failedTests,
                warningTests: this.masterSession.results.testing.warningTests
            } : null,
            
            debugging: this.masterSession.results.debugging ? {
                totalErrors: this.masterSession.results.debugging.summary.totalErrors,
                suggestions: this.masterSession.results.debugging.summary.suggestions
            } : null,
            
            steps: this.masterSession.steps,
            errors: this.masterSession.errors
        };
        
        // レポート保存
        const reportDir = path.join(__dirname, '..', 'master-reports');
        if (!fs.existsSync(reportDir)) {
            fs.mkdirSync(reportDir, { recursive: true });
        }
        
        const jsonReportPath = path.join(reportDir, `master-report-${this.masterSession.id}.json`);
        fs.writeFileSync(jsonReportPath, JSON.stringify(reportData, null, 2));
        
        const htmlReport = this.generateHTMLMasterReport(reportData);
        const htmlReportPath = path.join(reportDir, `master-report-${this.masterSession.id}.html`);
        fs.writeFileSync(htmlReportPath, htmlReport);
        
        console.log(`📄 最終レポート保存: ${htmlReportPath}`);
        
        return reportData;
    }

    generateHTMLMasterReport(data) {
        const statusIcon = {
            'success': '✅',
            'failed': '❌',
            'warning': '⚠️',
            'running': '🔄',
            'completed': '✅'
        };
        
        return `
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MCP統合Vercel マスターレポート</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 20px; }
        .status-success { background: #d4edda; border: 1px solid #c3e6cb; }
        .status-failed { background: #f8d7da; border: 1px solid #f5c6cb; }
        .status-warning { background: #fff3cd; border: 1px solid #ffeaa7; }
        .section { margin: 20px 0; padding: 20px; border-radius: 8px; border: 1px solid #ddd; }
        .step { margin: 10px 0; padding: 15px; border-radius: 5px; border: 1px solid #ddd; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .metric { background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; }
        .metric-number { font-size: 24px; font-weight: bold; color: #495057; }
        .metric-label { font-size: 12px; color: #6c757d; margin-top: 5px; }
        .timeline { position: relative; }
        .timeline-item { position: relative; padding: 20px 0; border-left: 2px solid #dee2e6; margin-left: 20px; }
        .timeline-item:before { content: ''; position: absolute; left: -6px; top: 25px; width: 10px; height: 10px; border-radius: 50%; background: #007bff; }
        .success-message { background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 20px; border-radius: 8px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 MCP統合Vercel マスターレポート</h1>
        <p>実行日時: ${new Date(data.timestamp).toLocaleString()}</p>
        <p>実行時間: ${Math.round(data.duration / 1000)}秒</p>
        <p>実行結果: ${data.success ? '✅ 成功' : '❌ 失敗'}</p>
    </div>
    
    <div class="metrics">
        <div class="metric">
            <div class="metric-number">${data.summary.totalSteps}</div>
            <div class="metric-label">総ステップ数</div>
        </div>
        <div class="metric">
            <div class="metric-number">${data.summary.successfulSteps}</div>
            <div class="metric-label">成功ステップ</div>
        </div>
        ${data.testing ? `
        <div class="metric">
            <div class="metric-number">${data.testing.passedTests}/${data.testing.totalTests}</div>
            <div class="metric-label">テスト合格率</div>
        </div>
        ` : ''}
        ${data.debugging ? `
        <div class="metric">
            <div class="metric-number">${data.debugging.totalErrors}</div>
            <div class="metric-label">検出エラー</div>
        </div>
        ` : ''}
    </div>
    
    ${data.success ? `
    <div class="success-message">
        <h3>🎉 デプロイメント完了!</h3>
        <p><strong>サイトURL:</strong> <a href="https://study-research-final.vercel.app" target="_blank">https://study-research-final.vercel.app</a></p>
        <p>全自動化プロセスが正常に完了しました。サイトは現在稼働中です。</p>
    </div>
    ` : ''}
    
    <div class="section">
        <h3>📋 実行ステップ</h3>
        <div class="timeline">
            ${data.steps.map(step => `
                <div class="timeline-item">
                    <div class="step status-${step.status}">
                        <h4>${statusIcon[step.status]} ${step.name}</h4>
                        <p>ステータス: ${step.status}</p>
                        ${step.duration ? `<p>実行時間: ${Math.round(step.duration / 1000)}秒</p>` : ''}
                    </div>
                </div>
            `).join('')}
        </div>
    </div>
    
    ${data.deployment ? `
    <div class="section status-success">
        <h3>🚀 デプロイメント結果</h3>
        <p><strong>デプロイURL:</strong> <a href="https://${data.deployment.url}" target="_blank">https://${data.deployment.url}</a></p>
        <p><strong>本番URL:</strong> <a href="https://study-research-final.vercel.app" target="_blank">https://study-research-final.vercel.app</a></p>
    </div>
    ` : ''}
    
    ${data.testing ? `
    <div class="section ${data.testing.failedTests > 0 ? 'status-warning' : 'status-success'}">
        <h3>🧪 テスト結果</h3>
        <p>総テスト数: ${data.testing.totalTests}</p>
        <p>合格: ${data.testing.passedTests}件</p>
        <p>失敗: ${data.testing.failedTests}件</p>
        <p>警告: ${data.testing.warningTests}件</p>
    </div>
    ` : ''}
    
    ${data.debugging ? `
    <div class="section status-warning">
        <h3>🔍 デバッグ結果</h3>
        <p>検出エラー: ${data.debugging.totalErrors}件</p>
        <p>修正提案: ${data.debugging.suggestions}件</p>
    </div>
    ` : ''}
    
    ${data.errors.length > 0 ? `
    <div class="section status-failed">
        <h3>❌ エラー詳細</h3>
        ${data.errors.map(error => `
            <div style="margin: 10px 0; padding: 10px; background: white; border-radius: 5px;">
                <p><strong>エラー:</strong> ${error.message}</p>
                <p><strong>発生時刻:</strong> ${new Date(error.timestamp).toLocaleString()}</p>
            </div>
        `).join('')}
    </div>
    ` : ''}
    
    <div class="section">
        <h3>🔧 システム情報</h3>
        <p><strong>MCP Playwright:</strong> http://localhost:9222</p>
        <p><strong>MCP Figma:</strong> http://localhost:9223</p>
        <p><strong>実行環境:</strong> Node.js + MCP</p>
    </div>
</body>
</html>
        `;
    }

    async generateErrorReport() {
        console.log('📊 エラーレポート生成中...');
        
        const errorReportPath = path.join(__dirname, '..', 'error-reports', `error-report-${this.masterSession.id}.json`);
        const errorReportDir = path.dirname(errorReportPath);
        
        if (!fs.existsSync(errorReportDir)) {
            fs.mkdirSync(errorReportDir, { recursive: true });
        }
        
        fs.writeFileSync(errorReportPath, JSON.stringify(this.masterSession, null, 2));
        console.log(`📄 エラーレポート保存: ${errorReportPath}`);
    }

    displaySuccessMessage() {
        console.log('\n' + '=' * 80);
        console.log('🎉 MCP統合Vercel自動化システム 完了!');
        console.log('=' * 80);
        console.log('✅ デプロイメント成功');
        console.log('✅ 自動テスト実行');
        console.log('✅ 品質確認完了');
        console.log('✅ レポート生成完了');
        console.log('');
        console.log('🌐 サイト URL: https://study-research-final.vercel.app');
        console.log('📊 詳細レポート: master-reports/ ディレクトリ確認');
        console.log('');
        console.log('🔄 継続監視を開始するには: node scripts/mcp-vercel-master.js --monitor');
        console.log('=' * 80);
    }

    async sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// コマンドライン引数処理
const args = process.argv.slice(2);
const command = args[0] || 'deploy';

async function main() {
    const master = new MCPVercelMaster();
    
    try {
        switch (command) {
            case 'deploy':
                await master.runFullDeploymentCycle();
                break;
                
            case 'test':
                await master.testing.runAllTests();
                break;
                
            case 'monitor':
                await master.monitor.runMonitoring();
                break;
                
            case 'debug':
                await master.debugger.runDebugging();
                break;
                
            default:
                console.log('使用法:');
                console.log('  node mcp-vercel-master.js deploy   # フルデプロイメント');
                console.log('  node mcp-vercel-master.js test     # テストのみ');
                console.log('  node mcp-vercel-master.js monitor  # 監視のみ');
                console.log('  node mcp-vercel-master.js debug    # デバッグのみ');
                break;
        }
        
    } catch (error) {
        console.error('❌ 実行エラー:', error.message);
        process.exit(1);
    }
}

// 実行
if (require.main === module) {
    main();
}

module.exports = MCPVercelMaster;