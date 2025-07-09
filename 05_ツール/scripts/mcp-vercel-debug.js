#!/usr/bin/env node

/**
 * MCP統合Vercelエラー自動デバッグシステム
 * エラー発生時の自動診断、ログ収集、修正提案
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

class MCPVercelDebugger {
    constructor() {
        this.env = this.loadEnv();
        this.mcpPlaywrightUrl = 'http://localhost:9222';
        this.mcpFigmaUrl = 'http://localhost:9223';
        this.siteUrl = 'https://study-research-final.vercel.app';
        this.debugSessions = [];
        this.errorPatterns = {
            '404': 'ページが見つかりません',
            '500': 'サーバーエラー',
            'timeout': 'タイムアウト',
            'cors': 'CORS エラー',
            'ssl': 'SSL/TLS エラー',
            'build': 'ビルドエラー',
            'deployment': 'デプロイエラー'
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

    async sendMCPCommand(command) {
        try {
            const response = await fetch(`${this.mcpPlaywrightUrl}/mcp`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    id: Date.now(),
                    method: 'tools/call',
                    params: {
                        name: 'playwright_action',
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
            console.error('❌ MCP通信失敗:', error.message);
            throw error;
        }
    }

    async initializePlaywright() {
        console.log('🔍 デバッグ用Playwright初期化中...');
        
        const initCommand = {
            action: 'launch_browser',
            options: {
                headless: false,
                slowMo: 1000,
                devtools: true,
                args: ['--disable-web-security', '--disable-features=VizDisplayCompositor']
            }
        };

        try {
            const result = await this.sendMCPCommand(initCommand);
            console.log('✅ Playwright初期化完了');
            return result;
        } catch (error) {
            console.error('❌ Playwright初期化失敗:', error.message);
            throw error;
        }
    }

    async detectErrors() {
        console.log('🔍 エラー検出開始...');
        
        const debugSession = {
            id: Date.now(),
            startTime: new Date().toISOString(),
            errors: [],
            logs: [],
            networkIssues: [],
            performanceIssues: [],
            suggestions: []
        };

        try {
            // サイトアクセス試行
            const navigateCommand = {
                action: 'navigate',
                url: this.siteUrl
            };
            
            await this.sendMCPCommand(navigateCommand);
            
            // コンソールエラー収集
            const consoleCommand = {
                action: 'evaluate',
                expression: `
                    const errors = [];
                    const originalError = console.error;
                    console.error = function(...args) {
                        errors.push({
                            type: 'error',
                            message: args.join(' '),
                            timestamp: new Date().toISOString()
                        });
                        originalError.apply(console, args);
                    };
                    
                    // 既存のエラーイベントリスナー
                    window.addEventListener('error', (event) => {
                        errors.push({
                            type: 'javascript',
                            message: event.error?.message || event.message,
                            filename: event.filename,
                            lineno: event.lineno,
                            colno: event.colno,
                            stack: event.error?.stack,
                            timestamp: new Date().toISOString()
                        });
                    });
                    
                    // Promise rejection エラー
                    window.addEventListener('unhandledrejection', (event) => {
                        errors.push({
                            type: 'promise',
                            message: event.reason?.message || event.reason,
                            timestamp: new Date().toISOString()
                        });
                    });
                    
                    return errors;
                `
            };
            
            const consoleResult = await this.sendMCPCommand(consoleCommand);
            if (consoleResult && consoleResult.length > 0) {
                debugSession.errors.push(...consoleResult);
            }
            
            // ネットワークエラー検出
            await this.detectNetworkIssues(debugSession);
            
            // パフォーマンス問題検出
            await this.detectPerformanceIssues(debugSession);
            
            // HTTPステータスコード確認
            await this.checkHttpStatus(debugSession);
            
            // リソース読み込み確認
            await this.checkResourceLoading(debugSession);
            
            // デプロイ状況確認
            await this.checkDeploymentStatus(debugSession);
            
            debugSession.endTime = new Date().toISOString();
            this.debugSessions.push(debugSession);
            
            console.log(`✅ エラー検出完了: ${debugSession.errors.length}件のエラー`);
            return debugSession;
            
        } catch (error) {
            debugSession.errors.push({
                type: 'system',
                message: error.message,
                timestamp: new Date().toISOString()
            });
            
            console.error('❌ エラー検出失敗:', error.message);
            throw error;
        }
    }

    async detectNetworkIssues(debugSession) {
        console.log('🌐 ネットワーク問題検出中...');
        
        const networkCommand = {
            action: 'evaluate',
            expression: `
                const resources = performance.getEntriesByType('resource');
                const networkIssues = [];
                
                resources.forEach(resource => {
                    // 読み込み時間が長い
                    if (resource.duration > 5000) {
                        networkIssues.push({
                            type: 'slow_loading',
                            resource: resource.name,
                            duration: resource.duration,
                            message: '読み込み時間が5秒を超えています'
                        });
                    }
                    
                    // 失敗したリソース
                    if (resource.transferSize === 0 && resource.decodedBodySize === 0) {
                        networkIssues.push({
                            type: 'failed_load',
                            resource: resource.name,
                            message: 'リソース読み込み失敗'
                        });
                    }
                });
                
                return networkIssues;
            `
        };
        
        try {
            const networkResult = await this.sendMCPCommand(networkCommand);
            if (networkResult && networkResult.length > 0) {
                debugSession.networkIssues.push(...networkResult);
                console.log(`🌐 ネットワーク問題: ${networkResult.length}件検出`);
            }
        } catch (error) {
            console.error('❌ ネットワーク問題検出失敗:', error.message);
        }
    }

    async detectPerformanceIssues(debugSession) {
        console.log('⚡ パフォーマンス問題検出中...');
        
        const performanceCommand = {
            action: 'evaluate',
            expression: `
                const perfData = performance.getEntriesByType('navigation')[0];
                const performanceIssues = [];
                
                // 読み込み時間が長い
                if (perfData.loadEventEnd - perfData.navigationStart > 3000) {
                    performanceIssues.push({
                        type: 'slow_page_load',
                        duration: perfData.loadEventEnd - perfData.navigationStart,
                        message: 'ページ読み込み時間が3秒を超えています'
                    });
                }
                
                // DOM処理時間が長い
                if (perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart > 1000) {
                    performanceIssues.push({
                        type: 'slow_dom_processing',
                        duration: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
                        message: 'DOM処理時間が1秒を超えています'
                    });
                }
                
                // 大量のリソース
                const resourceCount = performance.getEntriesByType('resource').length;
                if (resourceCount > 50) {
                    performanceIssues.push({
                        type: 'too_many_resources',
                        count: resourceCount,
                        message: 'リソース数が多すぎます'
                    });
                }
                
                return performanceIssues;
            `
        };
        
        try {
            const performanceResult = await this.sendMCPCommand(performanceCommand);
            if (performanceResult && performanceResult.length > 0) {
                debugSession.performanceIssues.push(...performanceResult);
                console.log(`⚡ パフォーマンス問題: ${performanceResult.length}件検出`);
            }
        } catch (error) {
            console.error('❌ パフォーマンス問題検出失敗:', error.message);
        }
    }

    async checkHttpStatus(debugSession) {
        console.log('🌐 HTTPステータス確認中...');
        
        try {
            const response = await fetch(this.siteUrl);
            
            if (!response.ok) {
                debugSession.errors.push({
                    type: 'http_status',
                    status: response.status,
                    statusText: response.statusText,
                    message: `HTTPステータス ${response.status}: ${response.statusText}`,
                    timestamp: new Date().toISOString()
                });
                
                console.log(`❌ HTTPステータス: ${response.status}`);
            } else {
                console.log(`✅ HTTPステータス: ${response.status}`);
            }
            
        } catch (error) {
            debugSession.errors.push({
                type: 'network',
                message: `ネットワークエラー: ${error.message}`,
                timestamp: new Date().toISOString()
            });
            
            console.error('❌ HTTPステータス確認失敗:', error.message);
        }
    }

    async checkResourceLoading(debugSession) {
        console.log('📦 リソース読み込み確認中...');
        
        const resourceCommand = {
            action: 'evaluate',
            expression: `
                const failedResources = [];
                const images = document.querySelectorAll('img');
                const links = document.querySelectorAll('link');
                const scripts = document.querySelectorAll('script');
                
                // 画像読み込み確認
                images.forEach(img => {
                    if (img.complete === false || img.naturalWidth === 0) {
                        failedResources.push({
                            type: 'image',
                            src: img.src,
                            alt: img.alt,
                            error: '画像読み込み失敗'
                        });
                    }
                });
                
                // CSS読み込み確認
                links.forEach(link => {
                    if (link.rel === 'stylesheet' && link.sheet === null) {
                        failedResources.push({
                            type: 'css',
                            href: link.href,
                            error: 'CSS読み込み失敗'
                        });
                    }
                });
                
                return failedResources;
            `
        };
        
        try {
            const resourceResult = await this.sendMCPCommand(resourceCommand);
            if (resourceResult && resourceResult.length > 0) {
                debugSession.errors.push(...resourceResult.map(r => ({
                    type: 'resource_loading',
                    message: r.error,
                    resource: r.src || r.href,
                    resourceType: r.type,
                    timestamp: new Date().toISOString()
                })));
                
                console.log(`📦 リソース読み込み問題: ${resourceResult.length}件検出`);
            }
        } catch (error) {
            console.error('❌ リソース読み込み確認失敗:', error.message);
        }
    }

    async checkDeploymentStatus(debugSession) {
        console.log('🚀 デプロイ状況確認中...');
        
        try {
            const deploymentResponse = await fetch(`https://api.vercel.com/v6/deployments?projectId=${this.env.VERCEL_PROJECT_ID}&limit=1`, {
                headers: {
                    'Authorization': `Bearer ${this.env.VERCEL_TOKEN}`
                }
            });
            
            if (deploymentResponse.ok) {
                const deploymentData = await deploymentResponse.json();
                const latestDeployment = deploymentData.deployments[0];
                
                if (latestDeployment) {
                    if (latestDeployment.state === 'ERROR') {
                        debugSession.errors.push({
                            type: 'deployment',
                            message: 'デプロイメントエラー',
                            deploymentId: latestDeployment.uid,
                            timestamp: new Date().toISOString()
                        });
                        
                        console.log(`❌ デプロイメントエラー: ${latestDeployment.uid}`);
                    } else {
                        console.log(`✅ デプロイメント状況: ${latestDeployment.state}`);
                    }
                }
            }
        } catch (error) {
            console.error('❌ デプロイ状況確認失敗:', error.message);
        }
    }

    async generateSuggestions(debugSession) {
        console.log('💡 修正提案生成中...');
        
        const suggestions = [];
        
        // エラーパターン分析
        debugSession.errors.forEach(error => {
            switch (error.type) {
                case 'http_status':
                    if (error.status === 404) {
                        suggestions.push({
                            type: 'route_fix',
                            message: 'ルーティング設定を確認し、vercel.jsonのroutesを修正してください',
                            priority: 'high',
                            code: `
{
  "routes": [
    {
      "src": "/",
      "dest": "/index.html"
    }
  ]
}
                            `
                        });
                    }
                    break;
                    
                case 'javascript':
                    suggestions.push({
                        type: 'js_fix',
                        message: `JavaScriptエラー修正: ${error.message}`,
                        priority: 'high',
                        file: error.filename,
                        line: error.lineno
                    });
                    break;
                    
                case 'resource_loading':
                    suggestions.push({
                        type: 'resource_fix',
                        message: `リソース読み込み修正: ${error.resource}`,
                        priority: 'medium',
                        suggestion: 'リソースパスを確認し、正しいファイル名とパスを設定してください'
                    });
                    break;
                    
                case 'deployment':
                    suggestions.push({
                        type: 'deployment_fix',
                        message: 'デプロイメント設定を確認してください',
                        priority: 'high',
                        suggestion: 'package.jsonのscriptsとvercel.jsonの設定を確認してください'
                    });
                    break;
            }
        });
        
        // パフォーマンス改善提案
        debugSession.performanceIssues.forEach(issue => {
            switch (issue.type) {
                case 'slow_page_load':
                    suggestions.push({
                        type: 'performance_fix',
                        message: '画像の最適化とコードの圧縮を実施してください',
                        priority: 'medium',
                        suggestion: 'WebP形式の画像使用とminification'
                    });
                    break;
                    
                case 'too_many_resources':
                    suggestions.push({
                        type: 'optimization',
                        message: 'リソースの統合とバンドル化を検討してください',
                        priority: 'low',
                        suggestion: 'CSS/JSファイルの統合とCDN利用'
                    });
                    break;
            }
        });
        
        debugSession.suggestions = suggestions;
        console.log(`💡 修正提案: ${suggestions.length}件生成`);
        
        return suggestions;
    }

    async takeDebugScreenshot(sessionId) {
        console.log('📸 デバッグスクリーンショット撮影中...');
        
        const screenshotDir = path.join(__dirname, '..', 'debug-screenshots');
        
        if (!fs.existsSync(screenshotDir)) {
            fs.mkdirSync(screenshotDir, { recursive: true });
        }
        
        const screenshotCommand = {
            action: 'screenshot',
            path: path.join(screenshotDir, `debug-${sessionId}-${Date.now()}.png`)
        };

        try {
            await this.sendMCPCommand(screenshotCommand);
            console.log('📸 デバッグスクリーンショット保存完了');
        } catch (error) {
            console.error('❌ スクリーンショット失敗:', error.message);
        }
    }

    async generateDebugReport(debugSession) {
        console.log('📊 デバッグレポート生成中...');
        
        const reportData = {
            sessionId: debugSession.id,
            timestamp: debugSession.startTime,
            duration: new Date(debugSession.endTime) - new Date(debugSession.startTime),
            siteUrl: this.siteUrl,
            summary: {
                totalErrors: debugSession.errors.length,
                networkIssues: debugSession.networkIssues.length,
                performanceIssues: debugSession.performanceIssues.length,
                suggestions: debugSession.suggestions.length
            },
            details: debugSession
        };
        
        // JSONレポート保存
        const reportDir = path.join(__dirname, '..', 'debug-reports');
        if (!fs.existsSync(reportDir)) {
            fs.mkdirSync(reportDir, { recursive: true });
        }
        
        const jsonReportPath = path.join(reportDir, `debug-report-${debugSession.id}.json`);
        fs.writeFileSync(jsonReportPath, JSON.stringify(reportData, null, 2));
        
        // HTMLレポート生成
        const htmlReport = this.generateHTMLDebugReport(reportData);
        const htmlReportPath = path.join(reportDir, `debug-report-${debugSession.id}.html`);
        fs.writeFileSync(htmlReportPath, htmlReport);
        
        console.log(`📄 デバッグレポート保存: ${htmlReportPath}`);
        
        return reportData;
    }

    generateHTMLDebugReport(data) {
        return `
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vercel自動デバッグレポート</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .section { margin: 20px 0; padding: 15px; border-radius: 5px; border: 1px solid #ddd; }
        .error { background: #f8d7da; border-color: #f5c6cb; }
        .warning { background: #fff3cd; border-color: #ffeaa7; }
        .info { background: #d1ecf1; border-color: #bee5eb; }
        .suggestion { background: #d4edda; border-color: #c3e6cb; }
        .code { background: #f8f9fa; padding: 10px; border-radius: 3px; font-family: monospace; }
        .priority-high { border-left: 4px solid #dc3545; }
        .priority-medium { border-left: 4px solid #ffc107; }
        .priority-low { border-left: 4px solid #28a745; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Vercel自動デバッグレポート</h1>
        <p>デバッグ実行日時: ${new Date(data.timestamp).toLocaleString()}</p>
        <p>対象サイト: ${data.siteUrl}</p>
        <p>実行時間: ${data.duration}ms</p>
        <div>
            <strong>サマリー:</strong>
            エラー ${data.summary.totalErrors}件 |
            ネットワーク問題 ${data.summary.networkIssues}件 |
            パフォーマンス問題 ${data.summary.performanceIssues}件 |
            修正提案 ${data.summary.suggestions}件
        </div>
    </div>
    
    ${data.details.errors.length > 0 ? `
        <div class="section error">
            <h3>❌ エラー詳細</h3>
            ${data.details.errors.map(error => `
                <div style="margin: 10px 0; padding: 10px; background: white; border-radius: 3px;">
                    <strong>${error.type}</strong>: ${error.message}
                    ${error.filename ? `<br>ファイル: ${error.filename}:${error.lineno}` : ''}
                    ${error.stack ? `<pre class="code">${error.stack}</pre>` : ''}
                </div>
            `).join('')}
        </div>
    ` : ''}
    
    ${data.details.networkIssues.length > 0 ? `
        <div class="section warning">
            <h3>🌐 ネットワーク問題</h3>
            ${data.details.networkIssues.map(issue => `
                <div style="margin: 10px 0; padding: 10px; background: white; border-radius: 3px;">
                    <strong>${issue.type}</strong>: ${issue.message}
                    ${issue.resource ? `<br>リソース: ${issue.resource}` : ''}
                    ${issue.duration ? `<br>時間: ${issue.duration}ms` : ''}
                </div>
            `).join('')}
        </div>
    ` : ''}
    
    ${data.details.performanceIssues.length > 0 ? `
        <div class="section info">
            <h3>⚡ パフォーマンス問題</h3>
            ${data.details.performanceIssues.map(issue => `
                <div style="margin: 10px 0; padding: 10px; background: white; border-radius: 3px;">
                    <strong>${issue.type}</strong>: ${issue.message}
                    ${issue.duration ? `<br>時間: ${issue.duration}ms` : ''}
                    ${issue.count ? `<br>数: ${issue.count}` : ''}
                </div>
            `).join('')}
        </div>
    ` : ''}
    
    ${data.details.suggestions.length > 0 ? `
        <div class="section suggestion">
            <h3>💡 修正提案</h3>
            ${data.details.suggestions.map(suggestion => `
                <div class="priority-${suggestion.priority}" style="margin: 10px 0; padding: 10px; background: white; border-radius: 3px;">
                    <strong>${suggestion.type}</strong> (${suggestion.priority}): ${suggestion.message}
                    ${suggestion.suggestion ? `<br>提案: ${suggestion.suggestion}` : ''}
                    ${suggestion.code ? `<pre class="code">${suggestion.code}</pre>` : ''}
                </div>
            `).join('')}
        </div>
    ` : ''}
</body>
</html>
        `;
    }

    async cleanup() {
        console.log('🧹 デバッグ環境クリーンアップ中...');
        
        const cleanupCommand = {
            action: 'close_browser'
        };

        try {
            await this.sendMCPCommand(cleanupCommand);
            console.log('✅ クリーンアップ完了');
        } catch (error) {
            console.error('⚠️ クリーンアップエラー:', error.message);
        }
    }

    async runDebugging() {
        console.log('🔍 MCP統合自動デバッグ開始');
        console.log('=' * 60);
        
        try {
            // 1. Playwright初期化
            await this.initializePlaywright();
            
            // 2. エラー検出
            const debugSession = await this.detectErrors();
            
            // 3. 修正提案生成
            await this.generateSuggestions(debugSession);
            
            // 4. デバッグスクリーンショット
            await this.takeDebugScreenshot(debugSession.id);
            
            // 5. デバッグレポート生成
            const report = await this.generateDebugReport(debugSession);
            
            console.log('\n' + '=' * 60);
            console.log('🎉 自動デバッグ完了!');
            console.log(`🔍 エラー: ${report.summary.totalErrors}件`);
            console.log(`💡 修正提案: ${report.summary.suggestions}件`);
            
            return report;
            
        } catch (error) {
            console.error('❌ デバッグ実行エラー:', error.message);
            throw error;
        } finally {
            await this.cleanup();
        }
    }
}

// 実行
if (require.main === module) {
    const debugger = new MCPVercelDebugger();
    debugger.runDebugging().catch(error => {
        console.error('❌ 実行エラー:', error);
        process.exit(1);
    });
}

module.exports = MCPVercelDebugger;