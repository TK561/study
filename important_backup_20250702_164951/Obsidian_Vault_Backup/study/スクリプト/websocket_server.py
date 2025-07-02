#!/usr/bin/env python3
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
