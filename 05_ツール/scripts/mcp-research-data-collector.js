#!/usr/bin/env node

/**
 * MCP研究データ収集・分析自動化システム
 * 研究データの自動収集、整理、分析を実行
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

class MCPResearchDataCollector {
    constructor() {
        this.mcpPlaywrightUrl = 'http://localhost:9222';
        this.researchPaths = {
            data: path.join(__dirname, '..', '03_研究資料'),
            analysis: path.join(__dirname, '..', '03_研究資料', 'research', 'analysis'),
            reports: path.join(__dirname, '..', '03_研究資料', 'research', 'analysis', 'analysis_reports'),
            experiments: path.join(__dirname, '..', '03_研究資料', 'research', 'experiments'),
            system: path.join(__dirname, '..', '04_システム実装'),
            website: path.join(__dirname, '..', '02_ウェブサイト')
        };
        
        this.collectionSession = {
            id: Date.now(),
            startTime: new Date().toISOString(),
            collections: [],
            analyses: [],
            insights: [],
            success: false
        };
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

    async collectResearchFiles() {
        console.log('📁 研究ファイル収集開始...');
        
        const fileCollection = {
            name: '研究ファイル収集',
            startTime: new Date().toISOString(),
            files: {
                python: [],
                markdown: [],
                json: [],
                html: [],
                analysis: []
            }
        };

        try {
            // 各ディレクトリからファイルを収集
            const collectFromDirectory = (dirPath, category) => {
                if (!fs.existsSync(dirPath)) return;
                
                const files = fs.readdirSync(dirPath, { withFileTypes: true });
                
                files.forEach(file => {
                    const filePath = path.join(dirPath, file.name);
                    
                    if (file.isDirectory()) {
                        collectFromDirectory(filePath, category);
                    } else {
                        const ext = path.extname(file.name).toLowerCase();
                        const stat = fs.statSync(filePath);
                        
                        const fileInfo = {
                            name: file.name,
                            path: filePath,
                            size: stat.size,
                            modified: stat.mtime,
                            created: stat.birthtime,
                            category: category
                        };
                        
                        switch (ext) {
                            case '.py':
                                fileCollection.files.python.push(fileInfo);
                                break;
                            case '.md':
                                fileCollection.files.markdown.push(fileInfo);
                                break;
                            case '.json':
                                fileCollection.files.json.push(fileInfo);
                                break;
                            case '.html':
                                fileCollection.files.html.push(fileInfo);
                                break;
                        }
                    }
                });
            };

            // 各カテゴリから収集
            collectFromDirectory(this.researchPaths.analysis, 'analysis');
            collectFromDirectory(this.researchPaths.experiments, 'experiments');
            collectFromDirectory(this.researchPaths.system, 'system');
            collectFromDirectory(this.researchPaths.website, 'website');
            
            fileCollection.status = 'completed';
            fileCollection.endTime = new Date().toISOString();
            fileCollection.summary = {
                python: fileCollection.files.python.length,
                markdown: fileCollection.files.markdown.length,
                json: fileCollection.files.json.length,
                html: fileCollection.files.html.length,
                total: Object.values(fileCollection.files).reduce((sum, arr) => sum + arr.length, 0)
            };
            
            this.collectionSession.collections.push(fileCollection);
            
            console.log(`✅ ファイル収集完了: ${fileCollection.summary.total}件`);
            return fileCollection;
            
        } catch (error) {
            fileCollection.status = 'failed';
            fileCollection.error = error.message;
            console.error('❌ ファイル収集失敗:', error.message);
            throw error;
        }
    }

    async analyzeResearchContent() {
        console.log('🔍 研究内容分析開始...');
        
        const contentAnalysis = {
            name: '研究内容分析',
            startTime: new Date().toISOString(),
            analyses: {}
        };

        try {
            // Pythonスクリプト分析
            const pythonAnalysis = await this.analyzePythonScripts();
            contentAnalysis.analyses.python = pythonAnalysis;
            
            // Markdownファイル分析
            const markdownAnalysis = await this.analyzeMarkdownFiles();
            contentAnalysis.analyses.markdown = markdownAnalysis;
            
            // JSONデータ分析
            const jsonAnalysis = await this.analyzeJsonFiles();
            contentAnalysis.analyses.json = jsonAnalysis;
            
            // 実験結果分析
            const experimentAnalysis = await this.analyzeExperimentResults();
            contentAnalysis.analyses.experiments = experimentAnalysis;
            
            contentAnalysis.status = 'completed';
            contentAnalysis.endTime = new Date().toISOString();
            
            this.collectionSession.analyses.push(contentAnalysis);
            
            console.log('✅ 研究内容分析完了');
            return contentAnalysis;
            
        } catch (error) {
            contentAnalysis.status = 'failed';
            contentAnalysis.error = error.message;
            console.error('❌ 研究内容分析失敗:', error.message);
            throw error;
        }
    }

    async analyzePythonScripts() {
        console.log('🐍 Pythonスクリプト分析中...');
        
        const pythonFiles = this.findFilesByExtension('.py');
        const analysis = {
            totalFiles: pythonFiles.length,
            scripts: [],
            functions: [],
            imports: [],
            errors: []
        };

        for (const file of pythonFiles) {
            try {
                const content = fs.readFileSync(file.path, 'utf8');
                
                // 基本的な分析
                const scriptAnalysis = {
                    name: file.name,
                    path: file.path,
                    lines: content.split('\n').length,
                    functions: this.extractPythonFunctions(content),
                    imports: this.extractPythonImports(content),
                    classes: this.extractPythonClasses(content),
                    lastModified: file.modified
                };
                
                analysis.scripts.push(scriptAnalysis);
                analysis.functions.push(...scriptAnalysis.functions);
                analysis.imports.push(...scriptAnalysis.imports);
                
            } catch (error) {
                analysis.errors.push({
                    file: file.name,
                    error: error.message
                });
            }
        }

        return analysis;
    }

    async analyzeMarkdownFiles() {
        console.log('📄 Markdownファイル分析中...');
        
        const markdownFiles = this.findFilesByExtension('.md');
        const analysis = {
            totalFiles: markdownFiles.length,
            documents: [],
            keywords: {},
            totalWords: 0
        };

        for (const file of markdownFiles) {
            try {
                const content = fs.readFileSync(file.path, 'utf8');
                
                const docAnalysis = {
                    name: file.name,
                    path: file.path,
                    wordCount: content.split(/\s+/).length,
                    headings: this.extractMarkdownHeadings(content),
                    links: this.extractMarkdownLinks(content),
                    lastModified: file.modified
                };
                
                analysis.documents.push(docAnalysis);
                analysis.totalWords += docAnalysis.wordCount;
                
                // キーワード頻度分析
                const words = content.toLowerCase().match(/\b\w+\b/g) || [];
                words.forEach(word => {
                    if (word.length > 3) {
                        analysis.keywords[word] = (analysis.keywords[word] || 0) + 1;
                    }
                });
                
            } catch (error) {
                console.error(`⚠️ Markdownファイル分析エラー: ${file.name}`);
            }
        }

        return analysis;
    }

    async analyzeJsonFiles() {
        console.log('📊 JSONファイル分析中...');
        
        const jsonFiles = this.findFilesByExtension('.json');
        const analysis = {
            totalFiles: jsonFiles.length,
            datasets: [],
            schemas: {},
            totalRecords: 0
        };

        for (const file of jsonFiles) {
            try {
                const content = fs.readFileSync(file.path, 'utf8');
                const data = JSON.parse(content);
                
                const dataAnalysis = {
                    name: file.name,
                    path: file.path,
                    size: file.size,
                    structure: this.analyzeJsonStructure(data),
                    recordCount: Array.isArray(data) ? data.length : 1,
                    lastModified: file.modified
                };
                
                analysis.datasets.push(dataAnalysis);
                analysis.totalRecords += dataAnalysis.recordCount;
                
            } catch (error) {
                console.error(`⚠️ JSONファイル分析エラー: ${file.name}`);
            }
        }

        return analysis;
    }

    async analyzeExperimentResults() {
        console.log('🧪 実験結果分析中...');
        
        const analysis = {
            experiments: [],
            results: [],
            performance: {},
            insights: []
        };

        try {
            // 実験結果ファイルを検索
            const experimentFiles = [
                'cohens_power_experiment_report.json',
                'saturation_point_experiment_report.json',
                'supplementary_experiments_results.json'
            ];

            for (const filename of experimentFiles) {
                const filePath = path.join(this.researchPaths.analysis, filename);
                
                if (fs.existsSync(filePath)) {
                    const content = fs.readFileSync(filePath, 'utf8');
                    const data = JSON.parse(content);
                    
                    const expAnalysis = {
                        name: filename,
                        path: filePath,
                        data: data,
                        insights: this.extractExperimentInsights(data)
                    };
                    
                    analysis.experiments.push(expAnalysis);
                }
            }

            // パフォーマンス分析
            analysis.performance = await this.analyzePerformanceData();
            
            // インサイト生成
            analysis.insights = this.generateResearchInsights(analysis.experiments);
            
        } catch (error) {
            console.error('⚠️ 実験結果分析エラー:', error.message);
        }

        return analysis;
    }

    async analyzePerformanceData() {
        console.log('⚡ パフォーマンスデータ分析中...');
        
        const performance = {
            webSitePerformance: null,
            systemPerformance: null,
            experimentPerformance: null
        };

        try {
            // ウェブサイトパフォーマンス測定
            const webPerf = await this.measureWebsitePerformance();
            performance.webSitePerformance = webPerf;
            
            // システムパフォーマンス測定
            const sysPerf = await this.measureSystemPerformance();
            performance.systemPerformance = sysPerf;
            
        } catch (error) {
            console.error('⚠️ パフォーマンス分析エラー:', error.message);
        }

        return performance;
    }

    async measureWebsitePerformance() {
        console.log('🌐 ウェブサイトパフォーマンス測定中...');
        
        try {
            const navigateCommand = {
                action: 'navigate',
                url: 'https://study-research-final.vercel.app'
            };
            
            await this.sendMCPCommand(navigateCommand);
            
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
                        resourceCount: performance.getEntriesByType('resource').length,
                        pageSize: document.documentElement.innerHTML.length
                    };
                `
            };
            
            const result = await this.sendMCPCommand(performanceCommand);
            
            return {
                timestamp: new Date().toISOString(),
                metrics: result,
                status: 'success'
            };
            
        } catch (error) {
            return {
                timestamp: new Date().toISOString(),
                error: error.message,
                status: 'failed'
            };
        }
    }

    async measureSystemPerformance() {
        console.log('💻 システムパフォーマンス測定中...');
        
        try {
            const systemInfo = {
                memory: process.memoryUsage(),
                uptime: process.uptime(),
                platform: process.platform,
                nodeVersion: process.version,
                cpuUsage: process.cpuUsage()
            };
            
            return {
                timestamp: new Date().toISOString(),
                metrics: systemInfo,
                status: 'success'
            };
            
        } catch (error) {
            return {
                timestamp: new Date().toISOString(),
                error: error.message,
                status: 'failed'
            };
        }
    }

    // ユーティリティメソッド
    findFilesByExtension(extension) {
        const files = [];
        
        const searchDirectory = (dirPath) => {
            if (!fs.existsSync(dirPath)) return;
            
            const items = fs.readdirSync(dirPath, { withFileTypes: true });
            
            items.forEach(item => {
                const itemPath = path.join(dirPath, item.name);
                
                if (item.isDirectory()) {
                    searchDirectory(itemPath);
                } else if (item.name.endsWith(extension)) {
                    const stat = fs.statSync(itemPath);
                    files.push({
                        name: item.name,
                        path: itemPath,
                        size: stat.size,
                        modified: stat.mtime,
                        created: stat.birthtime
                    });
                }
            });
        };
        
        Object.values(this.researchPaths).forEach(searchDirectory);
        return files;
    }

    extractPythonFunctions(content) {
        const functionRegex = /def\s+(\w+)\s*\(/g;
        const functions = [];
        let match;
        
        while ((match = functionRegex.exec(content)) !== null) {
            functions.push(match[1]);
        }
        
        return functions;
    }

    extractPythonImports(content) {
        const importRegex = /(?:from\s+(\w+)\s+import|import\s+(\w+))/g;
        const imports = [];
        let match;
        
        while ((match = importRegex.exec(content)) !== null) {
            imports.push(match[1] || match[2]);
        }
        
        return imports;
    }

    extractPythonClasses(content) {
        const classRegex = /class\s+(\w+)/g;
        const classes = [];
        let match;
        
        while ((match = classRegex.exec(content)) !== null) {
            classes.push(match[1]);
        }
        
        return classes;
    }

    extractMarkdownHeadings(content) {
        const headingRegex = /^(#{1,6})\s+(.+)$/gm;
        const headings = [];
        let match;
        
        while ((match = headingRegex.exec(content)) !== null) {
            headings.push({
                level: match[1].length,
                text: match[2]
            });
        }
        
        return headings;
    }

    extractMarkdownLinks(content) {
        const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
        const links = [];
        let match;
        
        while ((match = linkRegex.exec(content)) !== null) {
            links.push({
                text: match[1],
                url: match[2]
            });
        }
        
        return links;
    }

    analyzeJsonStructure(data) {
        if (Array.isArray(data)) {
            return {
                type: 'array',
                length: data.length,
                sampleItem: data.length > 0 ? this.analyzeJsonStructure(data[0]) : null
            };
        } else if (typeof data === 'object' && data !== null) {
            const structure = {
                type: 'object',
                properties: {}
            };
            
            Object.keys(data).forEach(key => {
                structure.properties[key] = typeof data[key];
            });
            
            return structure;
        } else {
            return {
                type: typeof data,
                value: data
            };
        }
    }

    extractExperimentInsights(data) {
        const insights = [];
        
        // 基本的なインサイト抽出
        if (data.results) {
            insights.push('実験結果データが含まれています');
        }
        
        if (data.performance) {
            insights.push('パフォーマンスデータが含まれています');
        }
        
        if (data.statistics) {
            insights.push('統計データが含まれています');
        }
        
        return insights;
    }

    generateResearchInsights(experiments) {
        const insights = [];
        
        // 実験数に基づくインサイト
        if (experiments.length > 0) {
            insights.push(`${experiments.length}件の実験結果を分析しました`);
        }
        
        // 共通パターンの検出
        const commonPatterns = this.detectCommonPatterns(experiments);
        insights.push(...commonPatterns);
        
        // 推奨事項の生成
        const recommendations = this.generateRecommendations(experiments);
        insights.push(...recommendations);
        
        return insights;
    }

    detectCommonPatterns(experiments) {
        const patterns = [];
        
        // 実験名パターン分析
        const experimentNames = experiments.map(exp => exp.name);
        if (experimentNames.some(name => name.includes('power'))) {
            patterns.push('統計的検出力分析が実施されています');
        }
        
        if (experimentNames.some(name => name.includes('saturation'))) {
            patterns.push('飽和点分析が実施されています');
        }
        
        return patterns;
    }

    generateRecommendations(experiments) {
        const recommendations = [];
        
        if (experiments.length > 3) {
            recommendations.push('多数の実験が実施されているため、結果の統合分析を検討してください');
        }
        
        if (experiments.some(exp => exp.insights.length === 0)) {
            recommendations.push('一部の実験でインサイトが不足しています。追加分析を検討してください');
        }
        
        return recommendations;
    }

    async generateAnalysisReport() {
        console.log('📊 分析レポート生成中...');
        
        const report = {
            sessionId: this.collectionSession.id,
            timestamp: new Date().toISOString(),
            collections: this.collectionSession.collections,
            analyses: this.collectionSession.analyses,
            insights: this.collectionSession.insights,
            summary: {
                totalFiles: this.collectionSession.collections.reduce((sum, col) => sum + (col.summary?.total || 0), 0),
                totalAnalyses: this.collectionSession.analyses.length,
                totalInsights: this.collectionSession.insights.length
            }
        };
        
        // JSONレポート保存
        const reportPath = path.join(__dirname, '..', 'research-automation', `data-analysis-${Date.now()}.json`);
        fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
        
        // HTMLレポート生成
        const htmlReport = this.generateHTMLReport(report);
        const htmlPath = path.join(__dirname, '..', 'research-automation', `data-analysis-${Date.now()}.html`);
        fs.writeFileSync(htmlPath, htmlReport);
        
        console.log(`📄 分析レポート保存: ${htmlPath}`);
        return report;
    }

    generateHTMLReport(report) {
        return `
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>研究データ分析レポート</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #e3f2fd; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
        .metric { background: #f5f5f5; padding: 15px; border-radius: 5px; text-align: center; }
        .metric-number { font-size: 24px; font-weight: bold; color: #1976d2; }
        .list-item { margin: 5px 0; padding: 5px; background: #f9f9f9; border-radius: 3px; }
        .insight { background: #e8f5e8; padding: 10px; border-left: 4px solid #4caf50; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 研究データ分析レポート</h1>
        <p>生成日時: ${new Date(report.timestamp).toLocaleString()}</p>
        <p>セッションID: ${report.sessionId}</p>
    </div>
    
    <div class="section">
        <h2>📊 分析サマリー</h2>
        <div class="metrics">
            <div class="metric">
                <div class="metric-number">${report.summary.totalFiles}</div>
                <div>総ファイル数</div>
            </div>
            <div class="metric">
                <div class="metric-number">${report.summary.totalAnalyses}</div>
                <div>実行分析数</div>
            </div>
            <div class="metric">
                <div class="metric-number">${report.summary.totalInsights}</div>
                <div>生成インサイト数</div>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>📁 ファイル収集結果</h2>
        ${report.collections.map(col => `
            <div class="list-item">
                <h3>${col.name}</h3>
                <p>ステータス: ${col.status}</p>
                ${col.summary ? `
                    <p>Python: ${col.summary.python}件, Markdown: ${col.summary.markdown}件, JSON: ${col.summary.json}件, HTML: ${col.summary.html}件</p>
                ` : ''}
            </div>
        `).join('')}
    </div>
    
    <div class="section">
        <h2>🔍 分析結果</h2>
        ${report.analyses.map(analysis => `
            <div class="list-item">
                <h3>${analysis.name}</h3>
                <p>ステータス: ${analysis.status}</p>
                ${analysis.analyses ? `
                    <p>Python分析: ${analysis.analyses.python?.totalFiles || 0}ファイル</p>
                    <p>Markdown分析: ${analysis.analyses.markdown?.totalFiles || 0}ファイル</p>
                    <p>JSON分析: ${analysis.analyses.json?.totalFiles || 0}ファイル</p>
                ` : ''}
            </div>
        `).join('')}
    </div>
    
    <div class="section">
        <h2>💡 インサイト</h2>
        ${report.insights.map(insight => `
            <div class="insight">${insight}</div>
        `).join('')}
    </div>
</body>
</html>
        `;
    }

    async runDataCollection() {
        console.log('🎯 MCP研究データ収集・分析開始');
        console.log('=' * 60);
        
        try {
            // 1. ファイル収集
            await this.collectResearchFiles();
            
            // 2. 内容分析
            await this.analyzeResearchContent();
            
            // 3. レポート生成
            const report = await this.generateAnalysisReport();
            
            this.collectionSession.success = true;
            this.collectionSession.endTime = new Date().toISOString();
            
            console.log('\n' + '=' * 60);
            console.log('🎉 データ収集・分析完了!');
            console.log(`📊 総ファイル数: ${report.summary.totalFiles}`);
            console.log(`📄 レポート保存済み`);
            console.log('=' * 60);
            
            return this.collectionSession;
            
        } catch (error) {
            console.error('❌ データ収集・分析失敗:', error.message);
            this.collectionSession.success = false;
            this.collectionSession.error = error.message;
            this.collectionSession.endTime = new Date().toISOString();
            
            throw error;
        }
    }
}

// 実行
if (require.main === module) {
    const collector = new MCPResearchDataCollector();
    collector.runDataCollection().catch(error => {
        console.error('❌ 実行エラー:', error);
        process.exit(1);
    });
}

module.exports = MCPResearchDataCollector;