#!/usr/bin/env node

/**
 * MCP Playwright統合デプロイ後自動テストシステム
 * デプロイ後の自動テスト実行とパフォーマンス監視
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

class MCPVercelTesting {
    constructor() {
        this.env = this.loadEnv();
        this.mcpPlaywrightUrl = 'http://localhost:9222';
        this.siteUrl = 'https://study-research-final.vercel.app';
        this.testResults = [];
        this.testConfig = {
            timeout: 30000,
            retries: 3,
            screenshots: true
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
        console.log('🎭 テスト用Playwright初期化中...');
        
        const initCommand = {
            action: 'launch_browser',
            options: {
                headless: false,
                slowMo: 500,
                viewport: { width: 1920, height: 1080 }
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

    async testHomePage() {
        console.log('🏠 ホームページテスト開始...');
        
        const startTime = Date.now();
        const testResult = {
            name: 'ホームページ読み込み',
            status: 'running',
            startTime: startTime,
            errors: []
        };

        try {
            // ページにアクセス
            const navigateCommand = {
                action: 'navigate',
                url: this.siteUrl
            };
            
            await this.sendMCPCommand(navigateCommand);
            
            // ページタイトル確認
            const titleCommand = {
                action: 'get_title'
            };
            
            const titleResult = await this.sendMCPCommand(titleCommand);
            
            if (titleResult && titleResult.title) {
                console.log(`✅ ページタイトル: ${titleResult.title}`);
            } else {
                testResult.errors.push('ページタイトル取得失敗');
            }
            
            // 主要要素の存在確認
            const elementsToCheck = [
                'h1', 'nav', 'main', 'footer'
            ];
            
            for (const element of elementsToCheck) {
                const elementCommand = {
                    action: 'wait_for_selector',
                    selector: element,
                    timeout: 5000
                };
                
                try {
                    await this.sendMCPCommand(elementCommand);
                    console.log(`✅ ${element} 要素確認`);
                } catch (error) {
                    testResult.errors.push(`${element} 要素が見つかりません`);
                }
            }
            
            // パフォーマンス測定
            const performanceCommand = {
                action: 'evaluate',
                expression: `
                    const perfData = performance.getEntriesByType('navigation')[0];
                    return {
                        loadTime: perfData.loadEventEnd - perfData.navigationStart,
                        domReady: perfData.domContentLoadedEventEnd - perfData.navigationStart,
                        firstPaint: performance.getEntriesByType('paint')[0]?.startTime || 0
                    };
                `
            };
            
            const performanceResult = await this.sendMCPCommand(performanceCommand);
            
            if (performanceResult) {
                console.log(`⚡ 読み込み時間: ${performanceResult.loadTime}ms`);
                console.log(`📄 DOM準備完了: ${performanceResult.domReady}ms`);
                testResult.performance = performanceResult;
            }
            
            // スクリーンショット撮影
            if (this.testConfig.screenshots) {
                await this.takeTestScreenshot('homepage');
            }
            
            testResult.status = testResult.errors.length > 0 ? 'failed' : 'passed';
            testResult.endTime = Date.now();
            testResult.duration = testResult.endTime - testResult.startTime;
            
            this.testResults.push(testResult);
            
            console.log(`✅ ホームページテスト完了 (${testResult.duration}ms)`);
            return testResult;
            
        } catch (error) {
            testResult.status = 'failed';
            testResult.errors.push(error.message);
            testResult.endTime = Date.now();
            testResult.duration = testResult.endTime - testResult.startTime;
            
            this.testResults.push(testResult);
            console.error('❌ ホームページテスト失敗:', error.message);
            throw error;
        }
    }

    async testNavigation() {
        console.log('🧭 ナビゲーションテスト開始...');
        
        const testResult = {
            name: 'ナビゲーション機能',
            status: 'running',
            startTime: Date.now(),
            errors: [],
            testedLinks: []
        };

        try {
            // ナビゲーションリンクを取得
            const linksCommand = {
                action: 'evaluate',
                expression: `
                    const links = Array.from(document.querySelectorAll('nav a, [href]'));
                    return links.map(link => ({
                        text: link.textContent.trim(),
                        href: link.href,
                        selector: link.tagName + (link.className ? '.' + link.className.split(' ').join('.') : '')
                    })).filter(link => link.href && !link.href.startsWith('javascript:'));
                `
            };
            
            const linksResult = await this.sendMCPCommand(linksCommand);
            
            if (linksResult && linksResult.length > 0) {
                // 各リンクをテスト
                for (const link of linksResult.slice(0, 5)) { // 最大5つのリンクをテスト
                    console.log(`🔗 リンクテスト: ${link.text} (${link.href})`);
                    
                    try {
                        const clickCommand = {
                            action: 'click',
                            selector: `[href="${link.href}"]`
                        };
                        
                        await this.sendMCPCommand(clickCommand);
                        
                        // ページ読み込み待機
                        await this.sleep(2000);
                        
                        // 現在のURLを確認
                        const currentUrlCommand = {
                            action: 'evaluate',
                            expression: 'window.location.href'
                        };
                        
                        const currentUrl = await this.sendMCPCommand(currentUrlCommand);
                        
                        testResult.testedLinks.push({
                            text: link.text,
                            href: link.href,
                            actualUrl: currentUrl,
                            success: true
                        });
                        
                        console.log(`✅ ${link.text} リンク動作確認`);
                        
                        // 元のページに戻る
                        const backCommand = {
                            action: 'go_back'
                        };
                        
                        await this.sendMCPCommand(backCommand);
                        await this.sleep(1000);
                        
                    } catch (error) {
                        testResult.errors.push(`${link.text} リンクエラー: ${error.message}`);
                        testResult.testedLinks.push({
                            text: link.text,
                            href: link.href,
                            error: error.message,
                            success: false
                        });
                    }
                }
            }
            
            testResult.status = testResult.errors.length > 0 ? 'failed' : 'passed';
            testResult.endTime = Date.now();
            testResult.duration = testResult.endTime - testResult.startTime;
            
            this.testResults.push(testResult);
            console.log(`✅ ナビゲーションテスト完了 (${testResult.duration}ms)`);
            return testResult;
            
        } catch (error) {
            testResult.status = 'failed';
            testResult.errors.push(error.message);
            testResult.endTime = Date.now();
            testResult.duration = testResult.endTime - testResult.startTime;
            
            this.testResults.push(testResult);
            console.error('❌ ナビゲーションテスト失敗:', error.message);
            throw error;
        }
    }

    async testResponsiveDesign() {
        console.log('📱 レスポンシブデザインテスト開始...');
        
        const testResult = {
            name: 'レスポンシブデザイン',
            status: 'running',
            startTime: Date.now(),
            errors: [],
            viewports: []
        };

        const viewports = [
            { width: 1920, height: 1080, name: 'デスクトップ' },
            { width: 768, height: 1024, name: 'タブレット' },
            { width: 375, height: 667, name: 'モバイル' }
        ];

        try {
            for (const viewport of viewports) {
                console.log(`📐 ${viewport.name} (${viewport.width}x${viewport.height}) テスト中...`);
                
                // ビューポート設定
                const viewportCommand = {
                    action: 'set_viewport',
                    width: viewport.width,
                    height: viewport.height
                };
                
                await this.sendMCPCommand(viewportCommand);
                
                // ページ再読み込み
                const reloadCommand = {
                    action: 'reload'
                };
                
                await this.sendMCPCommand(reloadCommand);
                await this.sleep(2000);
                
                // レイアウト確認
                const layoutCommand = {
                    action: 'evaluate',
                    expression: `
                        const body = document.body;
                        const nav = document.querySelector('nav');
                        const main = document.querySelector('main');
                        
                        return {
                            bodyWidth: body.scrollWidth,
                            bodyHeight: body.scrollHeight,
                            navVisible: nav ? window.getComputedStyle(nav).display !== 'none' : false,
                            mainVisible: main ? window.getComputedStyle(main).display !== 'none' : false,
                            hasOverflow: body.scrollWidth > window.innerWidth
                        };
                    `
                };
                
                const layoutResult = await this.sendMCPCommand(layoutCommand);
                
                if (layoutResult) {
                    if (layoutResult.hasOverflow && viewport.width < 768) {
                        testResult.errors.push(`${viewport.name}で横スクロールが発生`);
                    }
                    
                    testResult.viewports.push({
                        name: viewport.name,
                        width: viewport.width,
                        height: viewport.height,
                        layout: layoutResult
                    });
                }
                
                // スクリーンショット撮影
                if (this.testConfig.screenshots) {
                    await this.takeTestScreenshot(`responsive-${viewport.name.toLowerCase()}`);
                }
                
                console.log(`✅ ${viewport.name} テスト完了`);
            }
            
            testResult.status = testResult.errors.length > 0 ? 'failed' : 'passed';
            testResult.endTime = Date.now();
            testResult.duration = testResult.endTime - testResult.startTime;
            
            this.testResults.push(testResult);
            console.log(`✅ レスポンシブデザインテスト完了 (${testResult.duration}ms)`);
            return testResult;
            
        } catch (error) {
            testResult.status = 'failed';
            testResult.errors.push(error.message);
            testResult.endTime = Date.now();
            testResult.duration = testResult.endTime - testResult.startTime;
            
            this.testResults.push(testResult);
            console.error('❌ レスポンシブデザインテスト失敗:', error.message);
            throw error;
        }
    }

    async testPerformance() {
        console.log('⚡ パフォーマンステスト開始...');
        
        const testResult = {
            name: 'パフォーマンス',
            status: 'running',
            startTime: Date.now(),
            errors: [],
            metrics: {}
        };

        try {
            // Lighthouse風のパフォーマンス測定
            const performanceCommand = {
                action: 'evaluate',
                expression: `
                    const perfData = performance.getEntriesByType('navigation')[0];
                    const paintEntries = performance.getEntriesByType('paint');
                    
                    return {
                        loadTime: perfData.loadEventEnd - perfData.navigationStart,
                        domReady: perfData.domContentLoadedEventEnd - perfData.navigationStart,
                        firstPaint: paintEntries.find(p => p.name === 'first-paint')?.startTime || 0,
                        firstContentfulPaint: paintEntries.find(p => p.name === 'first-contentful-paint')?.startTime || 0,
                        resourcesLoaded: performance.getEntriesByType('resource').length,
                        pageSize: document.documentElement.innerHTML.length,
                        imageCount: document.querySelectorAll('img').length,
                        scriptCount: document.querySelectorAll('script').length,
                        stylesheetCount: document.querySelectorAll('link[rel="stylesheet"]').length
                    };
                `
            };
            
            const performanceResult = await this.sendMCPCommand(performanceCommand);
            
            if (performanceResult) {
                testResult.metrics = performanceResult;
                
                // パフォーマンス基準チェック
                if (performanceResult.loadTime > 3000) {
                    testResult.errors.push('ページ読み込み時間が3秒を超えています');
                }
                
                if (performanceResult.firstContentfulPaint > 2000) {
                    testResult.errors.push('First Contentful Paintが2秒を超えています');
                }
                
                console.log(`⚡ 読み込み時間: ${performanceResult.loadTime}ms`);
                console.log(`🎨 First Contentful Paint: ${performanceResult.firstContentfulPaint}ms`);
                console.log(`📊 リソース数: ${performanceResult.resourcesLoaded}`);
                console.log(`🖼️ 画像数: ${performanceResult.imageCount}`);
            }
            
            testResult.status = testResult.errors.length > 0 ? 'warning' : 'passed';
            testResult.endTime = Date.now();
            testResult.duration = testResult.endTime - testResult.startTime;
            
            this.testResults.push(testResult);
            console.log(`✅ パフォーマンステスト完了 (${testResult.duration}ms)`);
            return testResult;
            
        } catch (error) {
            testResult.status = 'failed';
            testResult.errors.push(error.message);
            testResult.endTime = Date.now();
            testResult.duration = testResult.endTime - testResult.startTime;
            
            this.testResults.push(testResult);
            console.error('❌ パフォーマンステスト失敗:', error.message);
            throw error;
        }
    }

    async takeTestScreenshot(name) {
        const screenshotDir = path.join(__dirname, '..', 'test-screenshots');
        
        if (!fs.existsSync(screenshotDir)) {
            fs.mkdirSync(screenshotDir, { recursive: true });
        }
        
        const screenshotCommand = {
            action: 'screenshot',
            path: path.join(screenshotDir, `${name}-${Date.now()}.png`)
        };

        try {
            await this.sendMCPCommand(screenshotCommand);
            console.log(`📸 ${name} スクリーンショット保存`);
        } catch (error) {
            console.error(`❌ ${name} スクリーンショット失敗:`, error.message);
        }
    }

    async generateTestReport() {
        console.log('📊 テストレポート生成中...');
        
        const reportData = {
            timestamp: new Date().toISOString(),
            siteUrl: this.siteUrl,
            totalTests: this.testResults.length,
            passedTests: this.testResults.filter(t => t.status === 'passed').length,
            failedTests: this.testResults.filter(t => t.status === 'failed').length,
            warningTests: this.testResults.filter(t => t.status === 'warning').length,
            results: this.testResults
        };
        
        // JSON レポート保存
        const jsonReportPath = path.join(__dirname, '..', 'test-reports', `test-report-${Date.now()}.json`);
        const reportDir = path.dirname(jsonReportPath);
        
        if (!fs.existsSync(reportDir)) {
            fs.mkdirSync(reportDir, { recursive: true });
        }
        
        fs.writeFileSync(jsonReportPath, JSON.stringify(reportData, null, 2));
        
        // HTML レポート生成
        const htmlReport = this.generateHTMLReport(reportData);
        const htmlReportPath = path.join(reportDir, `test-report-${Date.now()}.html`);
        fs.writeFileSync(htmlReportPath, htmlReport);
        
        console.log(`📄 テストレポート保存: ${htmlReportPath}`);
        
        return reportData;
    }

    generateHTMLReport(data) {
        return `
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vercel自動テストレポート</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f0f0f0; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .test-result { margin: 10px 0; padding: 15px; border-radius: 5px; }
        .passed { background: #d4edda; border: 1px solid #c3e6cb; }
        .failed { background: #f8d7da; border: 1px solid #f5c6cb; }
        .warning { background: #fff3cd; border: 1px solid #ffeaa7; }
        .error { color: #721c24; font-weight: bold; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }
        .metric { background: #f8f9fa; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 Vercel自動テストレポート</h1>
        <p>テスト実行日時: ${new Date(data.timestamp).toLocaleString()}</p>
        <p>テスト対象: ${data.siteUrl}</p>
        <p>総テスト数: ${data.totalTests} | 成功: ${data.passedTests} | 失敗: ${data.failedTests} | 警告: ${data.warningTests}</p>
    </div>
    
    ${data.results.map(result => `
        <div class="test-result ${result.status}">
            <h3>${result.name} (${result.status})</h3>
            <p>実行時間: ${result.duration}ms</p>
            
            ${result.errors.length > 0 ? `
                <div class="error">
                    <h4>エラー:</h4>
                    <ul>
                        ${result.errors.map(error => `<li>${error}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            
            ${result.performance ? `
                <div class="metrics">
                    <div class="metric">読み込み時間: ${result.performance.loadTime}ms</div>
                    <div class="metric">DOM準備完了: ${result.performance.domReady}ms</div>
                    <div class="metric">First Paint: ${result.performance.firstPaint}ms</div>
                </div>
            ` : ''}
            
            ${result.metrics ? `
                <div class="metrics">
                    <div class="metric">リソース数: ${result.metrics.resourcesLoaded}</div>
                    <div class="metric">画像数: ${result.metrics.imageCount}</div>
                    <div class="metric">スクリプト数: ${result.metrics.scriptCount}</div>
                    <div class="metric">CSS数: ${result.metrics.stylesheetCount}</div>
                </div>
            ` : ''}
        </div>
    `).join('')}
</body>
</html>
        `;
    }

    async sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async cleanup() {
        console.log('🧹 テスト環境クリーンアップ中...');
        
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

    async runAllTests() {
        console.log('🧪 MCP統合自動テスト開始');
        console.log('=' * 60);
        
        try {
            // 1. Playwright初期化
            await this.initializePlaywright();
            
            // 2. ホームページテスト
            await this.testHomePage();
            
            // 3. ナビゲーションテスト
            await this.testNavigation();
            
            // 4. レスポンシブデザインテスト
            await this.testResponsiveDesign();
            
            // 5. パフォーマンステスト
            await this.testPerformance();
            
            // 6. テストレポート生成
            const report = await this.generateTestReport();
            
            console.log('\n' + '=' * 60);
            console.log('🎉 自動テスト完了!');
            console.log(`📊 成功: ${report.passedTests}/${report.totalTests}テスト`);
            
            if (report.failedTests > 0) {
                console.log(`❌ 失敗: ${report.failedTests}テスト`);
            }
            
            return report;
            
        } catch (error) {
            console.error('❌ テスト実行エラー:', error.message);
            throw error;
        } finally {
            await this.cleanup();
        }
    }
}

// 実行
if (require.main === module) {
    const tester = new MCPVercelTesting();
    tester.runAllTests().catch(error => {
        console.error('❌ 実行エラー:', error);
        process.exit(1);
    });
}

module.exports = MCPVercelTesting;