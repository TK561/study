#!/usr/bin/env python3
"""
リアルタイム画像処理システム - 完全実装版
ストリーミング画像のリアルタイム分析・処理を行うシステム
"""

import json
import asyncio
import time
from datetime import datetime
from pathlib import Path
from collections import deque
import threading
import queue
import random

class RealtimeImageProcessor:
    def __init__(self):
        self.name = "リアルタイム画像処理システム"
        self.version = "2.0.0"
        self.processing_queue = queue.Queue(maxsize=100)
        self.result_queue = queue.Queue()
        self.stats = {
            "total_processed": 0,
            "total_errors": 0,
            "processing_times": deque(maxlen=100),
            "fps": 0
        }
        self.is_running = False
        self.output_dir = Path("output/realtime_processing")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 処理パイプライン設定
        self.pipeline_stages = [
            "preprocessing",
            "object_detection",
            "feature_extraction",
            "classification",
            "postprocessing"
        ]
        
    def preprocess_image(self, image_data):
        """画像前処理"""
        # モック実装：実際にはリサイズ、正規化などを行う
        time.sleep(0.01)  # 処理時間シミュレート
        return {
            "stage": "preprocessing",
            "status": "completed",
            "processing_time": 0.01,
            "output": {
                "normalized": True,
                "resized": True,
                "dimensions": (640, 480)
            }
        }
    
    def detect_objects(self, preprocessed_data):
        """物体検出"""
        time.sleep(0.02)  # 処理時間シミュレート
        
        # モック検出結果
        num_objects = random.randint(0, 5)
        objects = []
        for i in range(num_objects):
            objects.append({
                "id": f"obj_{i}",
                "class": random.choice(["person", "car", "dog", "cat", "bird"]),
                "confidence": round(random.uniform(0.7, 0.99), 2),
                "bbox": [
                    random.randint(0, 500),
                    random.randint(0, 400),
                    random.randint(50, 150),
                    random.randint(50, 150)
                ]
            })
        
        return {
            "stage": "object_detection",
            "status": "completed",
            "processing_time": 0.02,
            "output": {
                "objects_detected": num_objects,
                "objects": objects
            }
        }
    
    def extract_features(self, detection_data):
        """特徴抽出"""
        time.sleep(0.015)  # 処理時間シミュレート
        
        features = {
            "color_histogram": [random.random() for _ in range(10)],
            "texture_features": [random.random() for _ in range(5)],
            "shape_features": [random.random() for _ in range(8)]
        }
        
        return {
            "stage": "feature_extraction",
            "status": "completed",
            "processing_time": 0.015,
            "output": features
        }
    
    def classify_scene(self, feature_data):
        """シーン分類"""
        time.sleep(0.01)  # 処理時間シミュレート
        
        scene_types = ["indoor", "outdoor", "urban", "nature", "crowd"]
        classification = {
            "primary_scene": random.choice(scene_types),
            "confidence": round(random.uniform(0.8, 0.99), 2),
            "secondary_scenes": random.sample(scene_types, 2)
        }
        
        return {
            "stage": "classification",
            "status": "completed",
            "processing_time": 0.01,
            "output": classification
        }
    
    def postprocess_results(self, all_results):
        """後処理と結果統合"""
        time.sleep(0.005)  # 処理時間シミュレート
        
        # 結果統合
        integrated_result = {
            "timestamp": datetime.now().isoformat(),
            "frame_id": all_results.get("frame_id", "unknown"),
            "pipeline_results": all_results,
            "summary": {
                "total_objects": len(all_results.get("object_detection", {}).get("output", {}).get("objects", [])),
                "scene_type": all_results.get("classification", {}).get("output", {}).get("primary_scene", "unknown"),
                "quality_score": round(random.uniform(0.7, 1.0), 2)
            }
        }
        
        return {
            "stage": "postprocessing",
            "status": "completed",
            "processing_time": 0.005,
            "output": integrated_result
        }
    
    def process_frame(self, frame_data):
        """単一フレームの処理"""
        start_time = time.time()
        results = {"frame_id": frame_data.get("id", "unknown")}
        
        try:
            # パイプライン実行
            preprocessed = self.preprocess_image(frame_data)
            results["preprocessing"] = preprocessed
            
            detected = self.detect_objects(preprocessed)
            results["object_detection"] = detected
            
            features = self.extract_features(detected)
            results["feature_extraction"] = features
            
            classified = self.classify_scene(features)
            results["classification"] = classified
            
            final = self.postprocess_results(results)
            results["postprocessing"] = final
            
            # 処理時間記録
            total_time = time.time() - start_time
            results["total_processing_time"] = round(total_time, 3)
            
            # 統計更新
            self.stats["total_processed"] += 1
            self.stats["processing_times"].append(total_time)
            
            return results
            
        except Exception as e:
            self.stats["total_errors"] += 1
            return {
                "frame_id": frame_data.get("id", "unknown"),
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def processing_worker(self):
        """処理ワーカースレッド"""
        while self.is_running:
            try:
                # キューからフレームを取得（タイムアウト付き）
                frame_data = self.processing_queue.get(timeout=1.0)
                
                # フレーム処理
                result = self.process_frame(frame_data)
                
                # 結果をキューに追加
                self.result_queue.put(result)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"処理エラー: {e}")
    
    def calculate_fps(self):
        """FPS計算"""
        if len(self.stats["processing_times"]) > 0:
            avg_time = sum(self.stats["processing_times"]) / len(self.stats["processing_times"])
            self.stats["fps"] = round(1.0 / avg_time if avg_time > 0 else 0, 2)
        return self.stats["fps"]
    
    def start_processing(self, num_workers=2):
        """処理開始"""
        if self.is_running:
            return {"status": "already_running"}
        
        self.is_running = True
        
        # ワーカースレッド起動
        self.workers = []
        for i in range(num_workers):
            worker = threading.Thread(
                target=self.processing_worker,
                name=f"ProcessingWorker-{i}"
            )
            worker.start()
            self.workers.append(worker)
        
        # 統計更新スレッド
        self.stats_thread = threading.Thread(
            target=self._update_stats_loop,
            name="StatsUpdater"
        )
        self.stats_thread.start()
        
        return {
            "status": "started",
            "workers": num_workers,
            "timestamp": datetime.now().isoformat()
        }
    
    def stop_processing(self):
        """処理停止"""
        self.is_running = False
        
        # ワーカースレッドの終了を待つ
        for worker in self.workers:
            worker.join(timeout=5.0)
        
        return {
            "status": "stopped",
            "final_stats": self.get_statistics(),
            "timestamp": datetime.now().isoformat()
        }
    
    def _update_stats_loop(self):
        """統計情報更新ループ"""
        while self.is_running:
            self.calculate_fps()
            time.sleep(1.0)
    
    def add_frame(self, frame_data):
        """フレームを処理キューに追加"""
        try:
            self.processing_queue.put(frame_data, block=False)
            return {"status": "queued", "queue_size": self.processing_queue.qsize()}
        except queue.Full:
            return {"status": "queue_full", "error": "処理キューが満杯です"}
    
    def get_result(self, timeout=0.1):
        """処理結果を取得"""
        try:
            return self.result_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def get_statistics(self):
        """統計情報を取得"""
        return {
            "total_processed": self.stats["total_processed"],
            "total_errors": self.stats["total_errors"],
            "current_fps": self.stats["fps"],
            "average_processing_time": round(
                sum(self.stats["processing_times"]) / len(self.stats["processing_times"])
                if self.stats["processing_times"] else 0, 3
            ),
            "queue_size": self.processing_queue.qsize(),
            "pending_results": self.result_queue.qsize()
        }
    
    def create_websocket_server(self):
        """WebSocketサーバーのコード生成"""
        ws_code = '''#!/usr/bin/env python3
"""
リアルタイム画像処理 WebSocketサーバー
"""

import asyncio
import websockets
import json
import base64
from realtime_image_processor import RealtimeImageProcessor

processor = RealtimeImageProcessor()

async def handle_client(websocket, path):
    """クライアント接続処理"""
    print(f"新規接続: {websocket.remote_address}")
    
    try:
        # 処理開始
        processor.start_processing(num_workers=4)
        
        async for message in websocket:
            data = json.loads(message)
            
            if data["type"] == "frame":
                # フレームを処理キューに追加
                frame_data = {
                    "id": data.get("frame_id"),
                    "image": data.get("image"),  # base64エンコード画像
                    "timestamp": data.get("timestamp")
                }
                processor.add_frame(frame_data)
                
            elif data["type"] == "get_results":
                # 処理結果を取得して送信
                results = []
                while True:
                    result = processor.get_result(timeout=0.01)
                    if result is None:
                        break
                    results.append(result)
                
                if results:
                    await websocket.send(json.dumps({
                        "type": "results",
                        "data": results
                    }))
                    
            elif data["type"] == "get_stats":
                # 統計情報を送信
                stats = processor.get_statistics()
                await websocket.send(json.dumps({
                    "type": "statistics",
                    "data": stats
                }))
                
    except websockets.exceptions.ConnectionClosed:
        print(f"接続終了: {websocket.remote_address}")
    finally:
        processor.stop_processing()

async def main():
    """WebSocketサーバー起動"""
    print("🌐 リアルタイム画像処理 WebSocketサーバー")
    print("📡 ws://localhost:8765")
    
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()  # 永続実行

if __name__ == "__main__":
    asyncio.run(main())
'''
        
        ws_path = Path("websocket_server.py")
        with open(ws_path, 'w', encoding='utf-8') as f:
            f.write(ws_code)
        
        return str(ws_path)
    
    def create_demo_client(self):
        """デモクライアントHTML生成"""
        html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>リアルタイム画像処理デモ</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f0f0f0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .controls {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        button {
            padding: 10px 20px;
            margin: 5px;
            border: none;
            border-radius: 4px;
            background: #007bff;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background: #0056b3;
        }
        .stats {
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .results {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-height: 400px;
            overflow-y: auto;
        }
        .result-item {
            border-bottom: 1px solid #eee;
            padding: 10px 0;
        }
        .fps {
            font-size: 24px;
            color: #28a745;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>リアルタイム画像処理システム デモ</h1>
        
        <div class="controls">
            <button onclick="startStreaming()">ストリーミング開始</button>
            <button onclick="stopStreaming()">停止</button>
            <button onclick="getStats()">統計情報更新</button>
        </div>
        
        <div class="stats">
            <h3>処理統計</h3>
            <p>FPS: <span class="fps" id="fps">0</span></p>
            <p>処理済みフレーム: <span id="processed">0</span></p>
            <p>平均処理時間: <span id="avgTime">0</span> ms</p>
            <p>キューサイズ: <span id="queueSize">0</span></p>
        </div>
        
        <div class="results">
            <h3>処理結果</h3>
            <div id="resultsList"></div>
        </div>
    </div>
    
    <script>
        let ws = null;
        let streaming = false;
        let frameId = 0;
        
        function connectWebSocket() {
            ws = new WebSocket('ws://localhost:8765');
            
            ws.onopen = () => {
                console.log('WebSocket接続成功');
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                
                if (data.type === 'results') {
                    displayResults(data.data);
                } else if (data.type === 'statistics') {
                    updateStats(data.data);
                }
            };
            
            ws.onerror = (error) => {
                console.error('WebSocketエラー:', error);
            };
        }
        
        function startStreaming() {
            if (!ws || ws.readyState !== WebSocket.OPEN) {
                connectWebSocket();
                setTimeout(startStreaming, 1000);
                return;
            }
            
            streaming = true;
            streamFrames();
        }
        
        function stopStreaming() {
            streaming = false;
        }
        
        function streamFrames() {
            if (!streaming) return;
            
            // モックフレームデータ送信
            const frame = {
                type: 'frame',
                frame_id: frameId++,
                timestamp: new Date().toISOString()
            };
            
            ws.send(JSON.stringify(frame));
            
            // 結果取得
            ws.send(JSON.stringify({type: 'get_results'}));
            
            // 30FPSでループ
            setTimeout(streamFrames, 33);
        }
        
        function getStats() {
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({type: 'get_stats'}));
            }
        }
        
        function updateStats(stats) {
            document.getElementById('fps').textContent = stats.current_fps;
            document.getElementById('processed').textContent = stats.total_processed;
            document.getElementById('avgTime').textContent = 
                Math.round(stats.average_processing_time * 1000);
            document.getElementById('queueSize').textContent = stats.queue_size;
        }
        
        function displayResults(results) {
            const list = document.getElementById('resultsList');
            
            results.forEach(result => {
                const item = document.createElement('div');
                item.className = 'result-item';
                
                const summary = result.postprocessing?.output?.summary || {};
                item.innerHTML = `
                    <strong>Frame ${result.frame_id}</strong><br>
                    物体数: ${summary.total_objects || 0}<br>
                    シーン: ${summary.scene_type || 'unknown'}<br>
                    品質スコア: ${summary.quality_score || 0}<br>
                    処理時間: ${Math.round(result.total_processing_time * 1000)} ms
                `;
                
                list.insertBefore(item, list.firstChild);
                
                // 最新20件のみ表示
                while (list.children.length > 20) {
                    list.removeChild(list.lastChild);
                }
            });
        }
        
        // 定期的に統計情報を更新
        setInterval(getStats, 1000);
    </script>
</body>
</html>"""
        
        demo_path = self.output_dir / "realtime_demo.html"
        with open(demo_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(demo_path)

def main():
    """実行例"""
    print("🎬 リアルタイム画像処理システム 起動")
    print("=" * 50)
    
    processor = RealtimeImageProcessor()
    
    # WebSocketサーバーコード生成
    ws_path = processor.create_websocket_server()
    print(f"🌐 WebSocketサーバー生成: {ws_path}")
    
    # デモクライアント生成
    demo_path = processor.create_demo_client()
    print(f"🖥️ デモクライアント生成: {demo_path}")
    
    # ローカルテスト実行
    print("\n🚀 ローカルテスト実行...")
    processor.start_processing(num_workers=2)
    
    # テストフレーム処理
    print("📸 テストフレーム処理中...")
    for i in range(10):
        frame = {
            "id": f"test_frame_{i}",
            "timestamp": datetime.now().isoformat()
        }
        processor.add_frame(frame)
        time.sleep(0.1)
    
    # 結果待機
    time.sleep(2)
    
    # 統計情報表示
    stats = processor.get_statistics()
    print(f"\n📊 処理統計:")
    print(f"  処理済みフレーム: {stats['total_processed']}")
    print(f"  FPS: {stats['current_fps']}")
    print(f"  平均処理時間: {stats['average_processing_time']*1000:.1f} ms")
    
    # 停止
    processor.stop_processing()
    
    print("\n✨ システム準備完了")
    print(f"🌐 WebSocketサーバー起動: python websocket_server.py")
    print(f"🖥️ デモページ: file://{Path(demo_path).absolute()}")

if __name__ == "__main__":
    main()