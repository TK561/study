#!/usr/bin/env node

/**
 * MCP統合Vercelデプロイ自動化システム
 * Playwright MCPを使用したVercelダッシュボード監視とデプロイ自動化
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

class MCPVercelDeployment {
    constructor() {
        this.env = this.loadEnv();
        this.mcpPlaywrightUrl = 'http://localhost:9222';
        this.mcpFigmaUrl = 'http://localhost:9223';
        this.projectName = 'study-research-final';
        this.deploymentHistory = [];
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

    async checkMCPServers() {
        console.log('🔍 MCPサーバー接続確認...');
        
        try {
            const playwrightResponse = await fetch(`${this.mcpPlaywrightUrl}/sse`);
            const figmaResponse = await fetch(`${this.mcpFigmaUrl}/sse`);
            
            if (playwrightResponse.ok && figmaResponse.ok) {
                console.log('✅ MCP サーバー接続成功');
                return true;
            } else {
                console.log('❌ MCP サーバー接続失敗');
                return false;
            }
        } catch (error) {
            console.log('⚠️ MCP サーバー未起動 - 自動起動を試行...');
            await this.startMCPServers();
            return true;
        }
    }

    async startMCPServers() {
        console.log('🚀 MCP サーバー起動中...');
        try {
            execSync('npm run start-mcp', { stdio: 'inherit' });
            console.log('✅ MCP サーバー起動完了');
        } catch (error) {
            console.error('❌ MCP サーバー起動失敗:', error.message);
            throw error;
        }
    }

    async deployToVercel() {
        console.log('🚀 Vercel デプロイ開始...');
        
        const deploymentData = {
            name: this.projectName,
            files: await this.prepareFiles(),
            target: 'production'
        };

        try {
            const response = await fetch('https://api.vercel.com/v13/deployments', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.env.VERCEL_TOKEN}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(deploymentData)
            });

            if (response.ok) {
                const result = await response.json();
                console.log('✅ デプロイメント成功!');
                console.log(`🆔 デプロイID: ${result.id}`);
                console.log(`🌐 URL: https://${result.url}`);
                
                this.deploymentHistory.push({
                    id: result.id,
                    url: result.url,
                    timestamp: new Date().toISOString(),
                    status: 'deployed'
                });
                
                return result;
            } else {
                throw new Error(`デプロイ失敗: ${response.status}`);
            }
        } catch (error) {
            console.error('❌ デプロイエラー:', error.message);
            throw error;
        }
    }

    async prepareFiles() {
        const files = [];
        
        // index.htmlを準備
        const indexPath = path.join(__dirname, '..', 'index.html');
        if (fs.existsSync(indexPath)) {
            const content = fs.readFileSync(indexPath, 'utf8');
            files.push({
                file: 'index.html',
                data: Buffer.from(content).toString('base64')
            });
        }

        // vercel.jsonを準備
        const vercelConfigPath = path.join(__dirname, '..', 'vercel.json');
        if (fs.existsSync(vercelConfigPath)) {
            const content = fs.readFileSync(vercelConfigPath, 'utf8');
            files.push({
                file: 'vercel.json',
                data: Buffer.from(content).toString('base64')
            });
        }

        // publicディレクトリの全ファイルを準備
        const publicDir = path.join(__dirname, '..', 'public');
        if (fs.existsSync(publicDir)) {
            await this.addDirectoryFiles(publicDir, files, 'public');
        }

        return files;
    }

    async addDirectoryFiles(dirPath, files, prefix = '') {
        const items = fs.readdirSync(dirPath);
        
        for (const item of items) {
            const itemPath = path.join(dirPath, item);
            const relativePath = prefix ? `${prefix}/${item}` : item;
            
            if (fs.statSync(itemPath).isDirectory()) {
                await this.addDirectoryFiles(itemPath, files, relativePath);
            } else {
                const content = fs.readFileSync(itemPath, 'utf8');
                files.push({
                    file: relativePath,
                    data: Buffer.from(content).toString('base64')
                });
            }
        }
    }

    async runDeployment() {
        console.log('🎯 MCP統合Vercelデプロイシステム');
        console.log('=' * 60);
        
        try {
            // 1. MCPサーバー確認
            await this.checkMCPServers();
            
            // 2. Vercelデプロイ実行
            const deployment = await this.deployToVercel();
            
            // 3. デプロイメント履歴保存
            this.saveDeploymentHistory();
            
            console.log('\n' + '=' * 60);
            console.log('🎉 MCP統合デプロイメント完了!');
            console.log(`🌐 サイト: https://${this.projectName}.vercel.app`);
            console.log('📱 次のステップ: ダッシュボード監視とテスト実行');
            
            return deployment;
            
        } catch (error) {
            console.error('❌ デプロイメント失敗:', error.message);
            throw error;
        }
    }

    saveDeploymentHistory() {
        const historyPath = path.join(__dirname, '..', 'deployment-history.json');
        fs.writeFileSync(historyPath, JSON.stringify(this.deploymentHistory, null, 2));
        console.log('📝 デプロイメント履歴保存完了');
    }
}

// 実行
if (require.main === module) {
    const deployer = new MCPVercelDeployment();
    deployer.runDeployment().catch(error => {
        console.error('❌ 実行エラー:', error);
        process.exit(1);
    });
}

module.exports = MCPVercelDeployment;