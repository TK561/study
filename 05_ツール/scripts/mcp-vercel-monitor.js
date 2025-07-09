#!/usr/bin/env node

/**
 * MCP Playwright統合Vercelダッシュボード監視システム
 * リアルタイムでVercelダッシュボードを監視し、デプロイ状況を追跡
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

class MCPVercelMonitor {
    constructor() {
        this.env = this.loadEnv();
        this.mcpPlaywrightUrl = 'http://localhost:9222';
        this.vercelDashboardUrl = 'https://vercel.com/dashboard';
        this.projectName = 'study-research-final';
        this.monitoringActive = false;
        this.deploymentStatus = {};
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
        console.log('🎭 Playwright初期化中...');
        
        const initCommand = {
            action: 'launch_browser',
            options: {
                headless: false,
                slowMo: 1000
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

    async navigateToVercelDashboard() {
        console.log('🌐 Vercelダッシュボードにアクセス中...');
        
        const navigateCommand = {
            action: 'navigate',
            url: this.vercelDashboardUrl
        };

        try {
            const result = await this.sendMCPCommand(navigateCommand);
            console.log('✅ Vercelダッシュボードアクセス完了');
            return result;
        } catch (error) {
            console.error('❌ ダッシュボードアクセス失敗:', error.message);
            throw error;
        }
    }

    async loginToVercel() {
        console.log('🔐 Vercelログイン処理中...');
        
        const loginCommand = {
            action: 'click',
            selector: '[data-testid="login-button"]'
        };

        try {
            await this.sendMCPCommand(loginCommand);
            
            // GitHub認証の場合
            const githubLoginCommand = {
                action: 'click',
                selector: '[data-testid="github-login"]'
            };
            
            await this.sendMCPCommand(githubLoginCommand);
            console.log('✅ Vercelログイン完了');
            
        } catch (error) {
            console.log('⚠️ 既にログイン済みまたはログインスキップ');
        }
    }

    async selectProject() {
        console.log('📂 プロジェクト選択中...');
        
        const projectCommand = {
            action: 'click',
            selector: `[data-testid="project-${this.projectName}"], [href*="${this.projectName}"]`
        };

        try {
            const result = await this.sendMCPCommand(projectCommand);
            console.log(`✅ プロジェクト "${this.projectName}" 選択完了`);
            return result;
        } catch (error) {
            console.error('❌ プロジェクト選択失敗:', error.message);
            throw error;
        }
    }

    async monitorDeployments() {
        console.log('📊 デプロイメント監視開始...');
        
        this.monitoringActive = true;
        
        while (this.monitoringActive) {
            try {
                // デプロイメントリストを取得
                const deploymentsCommand = {
                    action: 'get_text',
                    selector: '[data-testid="deployment-list"]'
                };
                
                const result = await this.sendMCPCommand(deploymentsCommand);
                
                if (result && result.text) {
                    this.parseDeploymentStatus(result.text);
                    this.displayDeploymentStatus();
                }
                
                // 30秒間隔で監視
                await this.sleep(30000);
                
            } catch (error) {
                console.error('⚠️ 監視エラー:', error.message);
                await this.sleep(10000);
            }
        }
    }

    parseDeploymentStatus(deploymentText) {
        const lines = deploymentText.split('\n');
        const deployments = [];
        
        for (const line of lines) {
            if (line.includes('Building') || line.includes('Ready') || line.includes('Error')) {
                const parts = line.split(' ');
                const status = parts.find(p => ['Building', 'Ready', 'Error'].includes(p));
                const timestamp = parts.find(p => p.includes('ago') || p.includes('min') || p.includes('hour'));
                
                deployments.push({
                    status: status || 'Unknown',
                    timestamp: timestamp || 'Unknown',
                    line: line.trim()
                });
            }
        }
        
        this.deploymentStatus = {
            lastUpdate: new Date().toISOString(),
            deployments: deployments,
            total: deployments.length
        };
    }

    displayDeploymentStatus() {
        console.clear();
        console.log('🎯 Vercelデプロイメント監視ダッシュボード');
        console.log('=' * 60);
        console.log(`📅 最終更新: ${new Date(this.deploymentStatus.lastUpdate).toLocaleString()}`);
        console.log(`📊 総デプロイメント数: ${this.deploymentStatus.total}`);
        console.log('-' * 60);
        
        this.deploymentStatus.deployments.forEach((deployment, index) => {
            const statusEmoji = this.getStatusEmoji(deployment.status);
            console.log(`${statusEmoji} ${deployment.status} - ${deployment.timestamp}`);
            console.log(`   ${deployment.line}`);
        });
        
        console.log('-' * 60);
        console.log('📱 監視継続中... (Ctrl+C で終了)');
    }

    getStatusEmoji(status) {
        switch (status) {
            case 'Ready': return '✅';
            case 'Building': return '🔄';
            case 'Error': return '❌';
            default: return '⚪';
        }
    }

    async takeScreenshot() {
        console.log('📸 スクリーンショット撮影中...');
        
        const screenshotCommand = {
            action: 'screenshot',
            path: path.join(__dirname, '..', 'screenshots', `vercel-dashboard-${Date.now()}.png`)
        };

        try {
            const result = await this.sendMCPCommand(screenshotCommand);
            console.log('✅ スクリーンショット保存完了');
            return result;
        } catch (error) {
            console.error('❌ スクリーンショット失敗:', error.message);
            throw error;
        }
    }

    async checkDeploymentHealth() {
        console.log('🏥 デプロイメント健康状態確認中...');
        
        const healthCommand = {
            action: 'evaluate',
            expression: `
                const deployments = document.querySelectorAll('[data-testid="deployment-item"]');
                const health = {
                    total: deployments.length,
                    ready: 0,
                    building: 0,
                    error: 0
                };
                
                deployments.forEach(deployment => {
                    const statusElement = deployment.querySelector('[data-testid="deployment-status"]');
                    if (statusElement) {
                        const status = statusElement.textContent.toLowerCase();
                        if (status.includes('ready')) health.ready++;
                        else if (status.includes('building')) health.building++;
                        else if (status.includes('error')) health.error++;
                    }
                });
                
                return health;
            `
        };

        try {
            const result = await this.sendMCPCommand(healthCommand);
            this.displayHealthStatus(result);
            return result;
        } catch (error) {
            console.error('❌ 健康状態確認失敗:', error.message);
            throw error;
        }
    }

    displayHealthStatus(health) {
        console.log('🏥 デプロイメント健康状態');
        console.log('-' * 40);
        console.log(`✅ 成功: ${health.ready}件`);
        console.log(`🔄 ビルド中: ${health.building}件`);
        console.log(`❌ エラー: ${health.error}件`);
        console.log(`📊 総計: ${health.total}件`);
        
        if (health.error > 0) {
            console.log('⚠️ エラーが検出されました！');
            return false;
        }
        
        return true;
    }

    async sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async cleanup() {
        console.log('🧹 クリーンアップ中...');
        
        this.monitoringActive = false;
        
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

    async runMonitoring() {
        console.log('🎯 MCP Vercelダッシュボード監視開始');
        console.log('=' * 60);
        
        try {
            // 1. Playwright初期化
            await this.initializePlaywright();
            
            // 2. Vercelダッシュボードにアクセス
            await this.navigateToVercelDashboard();
            
            // 3. ログイン処理
            await this.loginToVercel();
            
            // 4. プロジェクト選択
            await this.selectProject();
            
            // 5. 初期健康状態確認
            await this.checkDeploymentHealth();
            
            // 6. スクリーンショット撮影
            await this.takeScreenshot();
            
            // 7. 監視開始
            await this.monitorDeployments();
            
        } catch (error) {
            console.error('❌ 監視エラー:', error.message);
            throw error;
        } finally {
            await this.cleanup();
        }
    }
}

// シグナルハンドラー設定
process.on('SIGINT', async () => {
    console.log('\n🛑 監視停止中...');
    process.exit(0);
});

// 実行
if (require.main === module) {
    const monitor = new MCPVercelMonitor();
    monitor.runMonitoring().catch(error => {
        console.error('❌ 実行エラー:', error);
        process.exit(1);
    });
}

module.exports = MCPVercelMonitor;