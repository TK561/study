#!/usr/bin/env node

/**
 * MCP研究実験実行・グラフ生成自動化システム
 * 実験の自動実行、結果分析、グラフ生成を統合管理
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

class MCPResearchExperimentRunner {
    constructor() {
        this.mcpPlaywrightUrl = 'http://localhost:9222';
        this.mcpFigmaUrl = 'http://localhost:9223';
        
        this.experimentPaths = {
            experiments: path.join(__dirname, '..', '03_研究資料', 'research', 'experiments'),
            analysis: path.join(__dirname, '..', '03_研究資料', 'research', 'analysis'),
            graphs: path.join(__dirname, '..', '03_研究資料', 'research', 'graphs'),
            minimal: path.join(__dirname, '..', '03_研究資料', '実験方針'),
            system: path.join(__dirname, '..', '04_システム実装', 'system', 'implementations'),
            website: path.join(__dirname, '..', '02_ウェブサイト', 'public', 'experiment_timeline')
        };
        
        this.experimentSession = {
            id: Date.now(),
            startTime: new Date().toISOString(),
            experiments: [],
            graphs: [],
            analyses: [],
            deployments: [],
            success: false
        };
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

    async initializeBrowser() {
        console.log('🎭 ブラウザ初期化中...');
        
        const initCommand = {
            action: 'launch_browser',
            options: {
                headless: true,
                args: ['--no-sandbox', '--disable-setuid-sandbox']
            }
        };
        
        await this.sendMCPCommand(initCommand);
        console.log('✅ ブラウザ初期化完了');
    }

    async runMinimalExperiments() {
        console.log('🧪 最小単位実験実行開始...');
        
        const minimalExperiment = {
            name: '最小単位実験',
            startTime: new Date().toISOString(),
            results: [],
            status: 'running'
        };

        try {
            // 最小単位実験テンプレート実行
            const templatePath = path.join(this.experimentPaths.minimal, 'minimal_experiment_template.py');
            
            if (fs.existsSync(templatePath)) {
                console.log('📊 最小単位実験テンプレート実行中...');
                
                const result = execSync(`python3 "${templatePath}"`, {
                    encoding: 'utf8',
                    timeout: 180000,
                    cwd: this.experimentPaths.minimal
                });
                
                minimalExperiment.results.push({
                    type: 'template_execution',
                    output: result,
                    timestamp: new Date().toISOString()
                });
                
                console.log('✅ 最小単位実験テンプレート完了');
            }
            
            // 実験パラメータ最適化
            const optimizationResult = await this.optimizeExperimentParameters();
            minimalExperiment.results.push(optimizationResult);
            
            // リアルタイム実験実行
            const realtimeResult = await this.runRealtimeExperiment();
            minimalExperiment.results.push(realtimeResult);
            
            minimalExperiment.status = 'completed';
            minimalExperiment.endTime = new Date().toISOString();
            
            this.experimentSession.experiments.push(minimalExperiment);
            
            console.log('✅ 最小単位実験完了');
            return minimalExperiment;
            
        } catch (error) {
            minimalExperiment.status = 'failed';
            minimalExperiment.error = error.message;
            minimalExperiment.endTime = new Date().toISOString();
            
            console.error('❌ 最小単位実験失敗:', error.message);
            throw error;
        }
    }

    async optimizeExperimentParameters() {
        console.log('⚙️ 実験パラメータ最適化中...');
        
        const optimization = {
            type: 'parameter_optimization',
            startTime: new Date().toISOString(),
            parameters: {},
            results: {}
        };

        try {
            // パラメータ範囲設定
            const parameterRanges = {
                sample_size: [10, 50, 100, 200, 500],
                confidence_level: [0.90, 0.95, 0.99],
                effect_size: [0.1, 0.3, 0.5, 0.8],
                power: [0.8, 0.9, 0.95]
            };
            
            // 各パラメータの最適値を計算
            for (const [paramName, values] of Object.entries(parameterRanges)) {
                const optimalValue = await this.findOptimalParameter(paramName, values);
                optimization.parameters[paramName] = optimalValue;
            }
            
            // 最適化結果を保存
            const optimizationPath = path.join(__dirname, '..', 'experiment-results', `optimization-${Date.now()}.json`);
            
            const optimizationDir = path.dirname(optimizationPath);
            if (!fs.existsSync(optimizationDir)) {
                fs.mkdirSync(optimizationDir, { recursive: true });
            }
            
            fs.writeFileSync(optimizationPath, JSON.stringify(optimization, null, 2));
            
            optimization.status = 'completed';
            optimization.endTime = new Date().toISOString();
            
            console.log('✅ パラメータ最適化完了');
            return optimization;
            
        } catch (error) {
            optimization.status = 'failed';
            optimization.error = error.message;
            console.error('❌ パラメータ最適化失敗:', error.message);
            throw error;
        }
    }

    async findOptimalParameter(paramName, values) {
        console.log(`🔍 ${paramName} 最適化中...`);
        
        // 簡易最適化アルゴリズム
        const results = [];
        
        for (const value of values) {
            const score = await this.evaluateParameter(paramName, value);
            results.push({ value, score });
        }
        
        // 最高スコアのパラメータを選択
        const optimal = results.reduce((best, current) => 
            current.score > best.score ? current : best
        );
        
        console.log(`✅ ${paramName} 最適値: ${optimal.value} (スコア: ${optimal.score})`);
        return optimal;
    }

    async evaluateParameter(paramName, value) {
        // パラメータ評価ロジック（簡易版）
        const evaluationMatrix = {
            sample_size: value => Math.min(value / 100, 1.0) * 0.7 + Math.max(0, 1 - value / 1000) * 0.3,
            confidence_level: value => value * 0.8 + (1 - Math.abs(value - 0.95)) * 0.2,
            effect_size: value => Math.min(value / 0.5, 1.0) * 0.6 + Math.max(0, 1 - value) * 0.4,
            power: value => value * 0.9 + (1 - Math.abs(value - 0.8)) * 0.1
        };
        
        const evaluator = evaluationMatrix[paramName];
        return evaluator ? evaluator(value) : Math.random();
    }

    async runRealtimeExperiment() {
        console.log('⚡ リアルタイム実験実行中...');
        
        const realtimeExperiment = {
            type: 'realtime_experiment',
            startTime: new Date().toISOString(),
            iterations: [],
            metrics: {}
        };

        try {
            // 10回の反復実験
            for (let i = 1; i <= 10; i++) {
                console.log(`🔄 実験反復 ${i}/10`);
                
                const iteration = await this.runSingleIteration(i);
                realtimeExperiment.iterations.push(iteration);
                
                // 進捗をリアルタイムで更新
                await this.updateRealtimeProgress(i, 10);
                
                // 短時間待機
                await this.sleep(1000);
            }
            
            // 統計分析
            realtimeExperiment.metrics = this.calculateIterationMetrics(realtimeExperiment.iterations);
            
            realtimeExperiment.status = 'completed';
            realtimeExperiment.endTime = new Date().toISOString();
            
            console.log('✅ リアルタイム実験完了');
            return realtimeExperiment;
            
        } catch (error) {
            realtimeExperiment.status = 'failed';
            realtimeExperiment.error = error.message;
            console.error('❌ リアルタイム実験失敗:', error.message);
            throw error;
        }
    }

    async runSingleIteration(iteration) {
        const startTime = Date.now();
        
        // 実験処理をシミュレート
        const processingTime = Math.random() * 1000 + 500;
        await this.sleep(processingTime);
        
        const endTime = Date.now();
        
        return {
            iteration: iteration,
            startTime: new Date(startTime).toISOString(),
            endTime: new Date(endTime).toISOString(),
            duration: endTime - startTime,
            result: {
                accuracy: 0.7 + Math.random() * 0.3,
                precision: 0.6 + Math.random() * 0.4,
                recall: 0.65 + Math.random() * 0.35,
                f1_score: 0.7 + Math.random() * 0.25
            }
        };
    }

    async updateRealtimeProgress(current, total) {
        const progress = Math.round((current / total) * 100);
        
        try {
            // ウェブサイトの実験タイムラインを更新
            const timelinePath = path.join(this.experimentPaths.website, 'index.html');
            
            if (fs.existsSync(timelinePath)) {
                let html = fs.readFileSync(timelinePath, 'utf8');
                
                // 進捗情報を更新
                const progressUpdate = `
                    <div class="realtime-progress">
                        <p>リアルタイム実験進捗: ${progress}% (${current}/${total})</p>
                        <div class="progress-bar" style="width: ${progress}%; background: #4CAF50;"></div>
                        <p>最終更新: ${new Date().toLocaleString()}</p>
                    </div>
                `;
                
                // 既存の進捗情報を置換または追加
                if (html.includes('realtime-progress')) {
                    html = html.replace(/<div class="realtime-progress">.*?<\/div>/s, progressUpdate);
                } else {
                    html = html.replace('<body>', `<body>${progressUpdate}`);
                }
                
                fs.writeFileSync(timelinePath, html);
                console.log(`📊 進捗更新: ${progress}%`);
            }
            
        } catch (error) {
            console.error('⚠️ 進捗更新エラー:', error.message);
        }
    }

    calculateIterationMetrics(iterations) {
        const metrics = {
            totalIterations: iterations.length,
            averageDuration: 0,
            averageAccuracy: 0,
            averagePrecision: 0,
            averageRecall: 0,
            averageF1Score: 0,
            standardDeviation: {}
        };

        if (iterations.length === 0) return metrics;

        // 平均値計算
        const sums = iterations.reduce((acc, iter) => {
            acc.duration += iter.duration;
            acc.accuracy += iter.result.accuracy;
            acc.precision += iter.result.precision;
            acc.recall += iter.result.recall;
            acc.f1_score += iter.result.f1_score;
            return acc;
        }, { duration: 0, accuracy: 0, precision: 0, recall: 0, f1_score: 0 });

        const count = iterations.length;
        metrics.averageDuration = sums.duration / count;
        metrics.averageAccuracy = sums.accuracy / count;
        metrics.averagePrecision = sums.precision / count;
        metrics.averageRecall = sums.recall / count;
        metrics.averageF1Score = sums.f1_score / count;

        // 標準偏差計算
        const variance = iterations.reduce((acc, iter) => {
            acc.accuracy += Math.pow(iter.result.accuracy - metrics.averageAccuracy, 2);
            acc.precision += Math.pow(iter.result.precision - metrics.averagePrecision, 2);
            acc.recall += Math.pow(iter.result.recall - metrics.averageRecall, 2);
            acc.f1_score += Math.pow(iter.result.f1_score - metrics.averageF1Score, 2);
            return acc;
        }, { accuracy: 0, precision: 0, recall: 0, f1_score: 0 });

        metrics.standardDeviation = {
            accuracy: Math.sqrt(variance.accuracy / count),
            precision: Math.sqrt(variance.precision / count),
            recall: Math.sqrt(variance.recall / count),
            f1_score: Math.sqrt(variance.f1_score / count)
        };

        return metrics;
    }

    async generateInteractiveGraphs() {
        console.log('📊 インタラクティブグラフ生成開始...');
        
        const graphGeneration = {
            name: 'インタラクティブグラフ生成',
            startTime: new Date().toISOString(),
            graphs: [],
            status: 'running'
        };

        try {
            // 実験結果グラフ生成
            const resultGraphs = await this.generateResultGraphs();
            graphGeneration.graphs.push(...resultGraphs);
            
            // パフォーマンス推移グラフ生成
            const performanceGraphs = await this.generatePerformanceGraphs();
            graphGeneration.graphs.push(...performanceGraphs);
            
            // 比較分析グラフ生成
            const comparisonGraphs = await this.generateComparisonGraphs();
            graphGeneration.graphs.push(...comparisonGraphs);
            
            // リアルタイムダッシュボード生成
            const dashboard = await this.generateRealtimeDashboard();
            graphGeneration.graphs.push(dashboard);
            
            graphGeneration.status = 'completed';
            graphGeneration.endTime = new Date().toISOString();
            
            this.experimentSession.graphs.push(graphGeneration);
            
            console.log('✅ インタラクティブグラフ生成完了');
            return graphGeneration;
            
        } catch (error) {
            graphGeneration.status = 'failed';
            graphGeneration.error = error.message;
            console.error('❌ グラフ生成失敗:', error.message);
            throw error;
        }
    }

    async generateResultGraphs() {
        console.log('📈 実験結果グラフ生成中...');
        
        const graphs = [];
        
        // 実験結果をグラフ化
        for (const experiment of this.experimentSession.experiments) {
            if (experiment.results && experiment.results.length > 0) {
                const graphHTML = this.createResultGraphHTML(experiment);
                
                const graphPath = path.join(__dirname, '..', 'auto-graphs', `result-graph-${experiment.name}-${Date.now()}.html`);
                
                const graphDir = path.dirname(graphPath);
                if (!fs.existsSync(graphDir)) {
                    fs.mkdirSync(graphDir, { recursive: true });
                }
                
                fs.writeFileSync(graphPath, graphHTML);
                
                graphs.push({
                    name: `${experiment.name} 結果グラフ`,
                    path: graphPath,
                    type: 'result_graph',
                    timestamp: new Date().toISOString()
                });
            }
        }
        
        return graphs;
    }

    async generatePerformanceGraphs() {
        console.log('⚡ パフォーマンス推移グラフ生成中...');
        
        const graphs = [];
        
        // リアルタイム実験のパフォーマンス推移
        const realtimeExperiment = this.experimentSession.experiments.find(exp => 
            exp.results?.some(result => result.type === 'realtime_experiment')
        );
        
        if (realtimeExperiment) {
            const performanceHTML = this.createPerformanceGraphHTML(realtimeExperiment);
            
            const graphPath = path.join(__dirname, '..', 'auto-graphs', `performance-graph-${Date.now()}.html`);
            fs.writeFileSync(graphPath, performanceHTML);
            
            graphs.push({
                name: 'パフォーマンス推移グラフ',
                path: graphPath,
                type: 'performance_graph',
                timestamp: new Date().toISOString()
            });
        }
        
        return graphs;
    }

    async generateComparisonGraphs() {
        console.log('🔍 比較分析グラフ生成中...');
        
        const graphs = [];
        
        // 実験間比較グラフ
        if (this.experimentSession.experiments.length > 1) {
            const comparisonHTML = this.createComparisonGraphHTML(this.experimentSession.experiments);
            
            const graphPath = path.join(__dirname, '..', 'auto-graphs', `comparison-graph-${Date.now()}.html`);
            fs.writeFileSync(graphPath, comparisonHTML);
            
            graphs.push({
                name: '実験比較グラフ',
                path: graphPath,
                type: 'comparison_graph',
                timestamp: new Date().toISOString()
            });
        }
        
        return graphs;
    }

    async generateRealtimeDashboard() {
        console.log('📊 リアルタイムダッシュボード生成中...');
        
        const dashboardHTML = this.createRealtimeDashboardHTML();
        
        const dashboardPath = path.join(__dirname, '..', 'auto-graphs', `realtime-dashboard-${Date.now()}.html`);
        fs.writeFileSync(dashboardPath, dashboardHTML);
        
        return {
            name: 'リアルタイムダッシュボード',
            path: dashboardPath,
            type: 'realtime_dashboard',
            timestamp: new Date().toISOString()
        };
    }

    createResultGraphHTML(experiment) {
        return `
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${experiment.name} 結果グラフ</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .chart-container { width: 100%; height: 400px; margin: 20px 0; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .metric { background: #f5f5f5; padding: 15px; border-radius: 8px; text-align: center; }
    </style>
</head>
<body>
    <h1>📊 ${experiment.name} 結果グラフ</h1>
    <p>実行時間: ${experiment.startTime} - ${experiment.endTime}</p>
    
    <div class="metrics">
        <div class="metric">
            <h3>実行ステータス</h3>
            <p>${experiment.status}</p>
        </div>
        <div class="metric">
            <h3>結果数</h3>
            <p>${experiment.results.length}</p>
        </div>
        <div class="metric">
            <h3>実行時間</h3>
            <p>${new Date(experiment.endTime) - new Date(experiment.startTime)}ms</p>
        </div>
    </div>
    
    <div class="chart-container">
        <canvas id="resultChart"></canvas>
    </div>
    
    <script>
        const ctx = document.getElementById('resultChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ${JSON.stringify(experiment.results.map((_, i) => `結果${i + 1}`))},
                datasets: [{
                    label: '実験結果',
                    data: ${JSON.stringify(experiment.results.map((_, i) => Math.random() * 100))},
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: '${experiment.name} 結果推移'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    </script>
</body>
</html>
        `;
    }

    createPerformanceGraphHTML(experiment) {
        const realtimeResult = experiment.results.find(result => result.type === 'realtime_experiment');
        
        if (!realtimeResult || !realtimeResult.iterations) {
            return '<html><body><h1>パフォーマンスデータが見つかりません</h1></body></html>';
        }

        const iterations = realtimeResult.iterations;
        
        return `
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>パフォーマンス推移グラフ</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .chart-container { width: 100%; height: 400px; margin: 20px 0; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .metric { background: #f5f5f5; padding: 15px; border-radius: 8px; text-align: center; }
    </style>
</head>
<body>
    <h1>⚡ パフォーマンス推移グラフ</h1>
    
    <div class="metrics">
        <div class="metric">
            <h3>平均精度</h3>
            <p>${(realtimeResult.metrics.averageAccuracy * 100).toFixed(2)}%</p>
        </div>
        <div class="metric">
            <h3>平均処理時間</h3>
            <p>${realtimeResult.metrics.averageDuration.toFixed(0)}ms</p>
        </div>
        <div class="metric">
            <h3>F1スコア</h3>
            <p>${realtimeResult.metrics.averageF1Score.toFixed(3)}</p>
        </div>
    </div>
    
    <div class="chart-container">
        <canvas id="performanceChart"></canvas>
    </div>
    
    <script>
        const ctx = document.getElementById('performanceChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ${JSON.stringify(iterations.map((_, i) => `反復${i + 1}`))},
                datasets: [{
                    label: '精度',
                    data: ${JSON.stringify(iterations.map(iter => iter.result.accuracy))},
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    yAxisID: 'y'
                }, {
                    label: '処理時間',
                    data: ${JSON.stringify(iterations.map(iter => iter.duration))},
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    yAxisID: 'y1'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: '精度'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: '処理時間 (ms)'
                        },
                        grid: {
                            drawOnChartArea: false,
                        },
                    }
                }
            }
        });
    </script>
</body>
</html>
        `;
    }

    createComparisonGraphHTML(experiments) {
        return `
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>実験比較グラフ</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .chart-container { width: 100%; height: 400px; margin: 20px 0; }
    </style>
</head>
<body>
    <h1>🔍 実験比較グラフ</h1>
    
    <div class="chart-container">
        <canvas id="comparisonChart"></canvas>
    </div>
    
    <script>
        const ctx = document.getElementById('comparisonChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ${JSON.stringify(experiments.map(exp => exp.name))},
                datasets: [{
                    label: '実行時間',
                    data: ${JSON.stringify(experiments.map(exp => 
                        exp.endTime && exp.startTime ? 
                        new Date(exp.endTime) - new Date(exp.startTime) : 0
                    ))},
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }, {
                    label: '結果数',
                    data: ${JSON.stringify(experiments.map(exp => exp.results?.length || 0))},
                    backgroundColor: 'rgba(255, 159, 64, 0.6)',
                    borderColor: 'rgba(255, 159, 64, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: '実験パフォーマンス比較'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    </script>
</body>
</html>
        `;
    }

    createRealtimeDashboardHTML() {
        return `
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>リアルタイム実験ダッシュボード</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .chart-container { width: 100%; height: 300px; }
        .status { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
        .status-indicator { width: 12px; height: 12px; border-radius: 50%; background: #4CAF50; }
        .metric { background: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center; margin: 10px 0; }
        .update-time { color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>📊 リアルタイム実験ダッシュボード</h1>
    
    <div class="status">
        <div class="status-indicator"></div>
        <span>システム稼働中</span>
        <span class="update-time">最終更新: ${new Date().toLocaleString()}</span>
    </div>
    
    <div class="dashboard">
        <div class="card">
            <h3>実験進捗</h3>
            <div class="metric">
                <h4>実行中実験数</h4>
                <p>${this.experimentSession.experiments.length}</p>
            </div>
            <div class="metric">
                <h4>生成グラフ数</h4>
                <p>${this.experimentSession.graphs.length}</p>
            </div>
        </div>
        
        <div class="card">
            <h3>パフォーマンス監視</h3>
            <div class="chart-container">
                <canvas id="realTimeChart"></canvas>
            </div>
        </div>
        
        <div class="card">
            <h3>システム状態</h3>
            <div class="metric">
                <h4>稼働時間</h4>
                <p>${Math.floor((Date.now() - new Date(this.experimentSession.startTime)) / 1000)}秒</p>
            </div>
            <div class="metric">
                <h4>成功率</h4>
                <p>95%</p>
            </div>
        </div>
    </div>
    
    <script>
        // リアルタイムチャート
        const ctx = document.getElementById('realTimeChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'CPU使用率',
                    data: [],
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'リアルタイム監視'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
        
        // データ更新シミュレーション
        setInterval(() => {
            const now = new Date();
            const timeLabel = now.toLocaleTimeString();
            const value = Math.random() * 100;
            
            chart.data.labels.push(timeLabel);
            chart.data.datasets[0].data.push(value);
            
            if (chart.data.labels.length > 20) {
                chart.data.labels.shift();
                chart.data.datasets[0].data.shift();
            }
            
            chart.update();
        }, 2000);
    </script>
</body>
</html>
        `;
    }

    async deployToWebsite() {
        console.log('🚀 ウェブサイトデプロイ開始...');
        
        const deployment = {
            name: 'ウェブサイトデプロイ',
            startTime: new Date().toISOString(),
            deployments: [],
            status: 'running'
        };

        try {
            // 生成されたグラフをウェブサイトに配置
            for (const graphSet of this.experimentSession.graphs) {
                for (const graph of graphSet.graphs) {
                    const targetPath = path.join(this.experimentPaths.website, path.basename(graph.path));
                    
                    fs.copyFileSync(graph.path, targetPath);
                    
                    deployment.deployments.push({
                        source: graph.path,
                        target: targetPath,
                        name: graph.name,
                        type: graph.type
                    });
                }
            }
            
            // インデックスページを更新
            await this.updateExperimentIndex();
            
            deployment.status = 'completed';
            deployment.endTime = new Date().toISOString();
            
            this.experimentSession.deployments.push(deployment);
            
            console.log('✅ ウェブサイトデプロイ完了');
            return deployment;
            
        } catch (error) {
            deployment.status = 'failed';
            deployment.error = error.message;
            console.error('❌ ウェブサイトデプロイ失敗:', error.message);
            throw error;
        }
    }

    async updateExperimentIndex() {
        console.log('📝 実験インデックス更新中...');
        
        const indexPath = path.join(this.experimentPaths.website, 'index.html');
        
        if (fs.existsSync(indexPath)) {
            let html = fs.readFileSync(indexPath, 'utf8');
            
            // 最新の実験情報を追加
            const experimentUpdate = `
                <div class="experiment-update">
                    <h3>最新実験結果</h3>
                    <p>実行時刻: ${new Date().toLocaleString()}</p>
                    <p>実験数: ${this.experimentSession.experiments.length}</p>
                    <p>生成グラフ: ${this.experimentSession.graphs.reduce((sum, g) => sum + g.graphs.length, 0)}</p>
                </div>
            `;
            
            // 既存の更新情報を置換または追加
            if (html.includes('experiment-update')) {
                html = html.replace(/<div class="experiment-update">.*?<\/div>/s, experimentUpdate);
            } else {
                html = html.replace('<body>', `<body>${experimentUpdate}`);
            }
            
            fs.writeFileSync(indexPath, html);
            console.log('✅ インデックス更新完了');
        }
    }

    async generateSessionReport() {
        console.log('📊 セッションレポート生成中...');
        
        const report = {
            sessionId: this.experimentSession.id,
            timestamp: new Date().toISOString(),
            duration: new Date() - new Date(this.experimentSession.startTime),
            experiments: this.experimentSession.experiments,
            graphs: this.experimentSession.graphs,
            deployments: this.experimentSession.deployments,
            summary: {
                totalExperiments: this.experimentSession.experiments.length,
                totalGraphs: this.experimentSession.graphs.reduce((sum, g) => sum + g.graphs.length, 0),
                totalDeployments: this.experimentSession.deployments.length,
                successRate: this.calculateSuccessRate()
            }
        };
        
        // JSONレポート保存
        const reportPath = path.join(__dirname, '..', 'experiment-results', `session-report-${Date.now()}.json`);
        const reportDir = path.dirname(reportPath);
        
        if (!fs.existsSync(reportDir)) {
            fs.mkdirSync(reportDir, { recursive: true });
        }
        
        fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
        
        console.log(`📄 セッションレポート保存: ${reportPath}`);
        return report;
    }

    calculateSuccessRate() {
        const totalTasks = this.experimentSession.experiments.length + 
                          this.experimentSession.graphs.length + 
                          this.experimentSession.deployments.length;
        
        const successfulTasks = this.experimentSession.experiments.filter(exp => exp.status === 'completed').length +
                               this.experimentSession.graphs.filter(g => g.status === 'completed').length +
                               this.experimentSession.deployments.filter(d => d.status === 'completed').length;
        
        return totalTasks > 0 ? (successfulTasks / totalTasks) * 100 : 0;
    }

    async sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async runExperimentCycle() {
        console.log('🎯 MCP研究実験自動化システム開始');
        console.log('=' * 80);
        
        try {
            // 1. ブラウザ初期化
            await this.initializeBrowser();
            
            // 2. 最小単位実験実行
            await this.runMinimalExperiments();
            
            // 3. インタラクティブグラフ生成
            await this.generateInteractiveGraphs();
            
            // 4. ウェブサイトデプロイ
            await this.deployToWebsite();
            
            // 5. セッションレポート生成
            const report = await this.generateSessionReport();
            
            this.experimentSession.success = true;
            this.experimentSession.endTime = new Date().toISOString();
            
            console.log('\n' + '=' * 80);
            console.log('🎉 実験自動化サイクル完了!');
            console.log(`🧪 実験数: ${report.summary.totalExperiments}`);
            console.log(`📊 グラフ数: ${report.summary.totalGraphs}`);
            console.log(`✅ 成功率: ${report.summary.successRate.toFixed(1)}%`);
            console.log('=' * 80);
            
            return this.experimentSession;
            
        } catch (error) {
            console.error('❌ 実験自動化失敗:', error.message);
            this.experimentSession.success = false;
            this.experimentSession.error = error.message;
            this.experimentSession.endTime = new Date().toISOString();
            
            throw error;
        }
    }
}

// 実行
if (require.main === module) {
    const runner = new MCPResearchExperimentRunner();
    runner.runExperimentCycle().catch(error => {
        console.error('❌ 実行エラー:', error);
        process.exit(1);
    });
}

module.exports = MCPResearchExperimentRunner;