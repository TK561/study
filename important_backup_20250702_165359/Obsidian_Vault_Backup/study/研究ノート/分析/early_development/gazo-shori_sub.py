from ultralytics import YOLO
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# YOLO モデル読み込み
model = YOLO("yolov8n.pt")

# === 画像読み込み ===
def imread_jp(path):
    with open(path, "rb") as f:
        img_buf = np.frombuffer(f.read(), dtype=np.uint8)
    return cv2.imdecode(img_buf, cv2.IMREAD_COLOR)

# === ファイル選択ダイアログ（Tkinterウィンドウはまだ作らない） ===
root_for_dialog = tk.Tk()
root_for_dialog.withdraw()
img_path = filedialog.askopenfilename(
    title="画像を選択",
    filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
)
root_for_dialog.destroy()

if not img_path:
    print("画像が選ばれませんでした。終了します。")
    exit()

img = imread_jp(img_path)
if img is None:
    print("画像の読み込みに失敗しました。")
    exit()

# === YOLOで物体検出 ===
results = model(img)[0]
detected_objects = []
selected_objects = []
for result in results.boxes.data.cpu().numpy():
    x1, y1, x2, y2, conf, cls = result
    center_x, center_y = int((x1 + x2) / 2), int((y1 + y2) / 2)
    detected_objects.append({
        "bbox": [int(x1), int(y1), int(x2 - x1), int(y2 - y1)],
        "center": (center_x, center_y),
        "label": results.names[int(cls)],
        "confidence": float(conf)
    })

# === Tkinter ウィンドウ作成 ===
root = tk.Tk()
root.title("YOLO Object Selector")
root.geometry("900x700")

panel = tk.Label(root)
panel.pack()

running = True

# 完了処理
def on_done(event=None):
    global running
    running = False

# 選択解除処理
def on_clear():
    selected_objects.clear()

# 🔘「全解除」ボタン（完了ボタンの上に配置）
tk.Button(root, text="選択を全解除", command=on_clear).pack(pady=2)

# ✅完了ボタンとEnterキー
tk.Button(root, text="選択完了（Enterでも可）", command=on_done).pack(pady=5)
root.bind("<Return>", on_done)

# マウスクリックで選択/解除
def on_click(event):
    # 表示画像のサイズを取得
    display_width = panel.winfo_width()
    display_height = panel.winfo_height()

    # 元画像のサイズ
    original_width = img.shape[1]
    original_height = img.shape[0]

    # クリック座標を元画像のスケールに変換
    x = int(event.x * (original_width / display_width))
    y = int(event.y * (original_height / display_height))

    # 最近傍の物体を検索
    distances = [np.hypot(x - obj["center"][0], y - obj["center"][1]) for obj in detected_objects]
    if not distances:
        return
    nearest_idx = np.argmin(distances)
    if distances[nearest_idx] < 50:  
        obj = detected_objects[nearest_idx]
        if obj in selected_objects:
            selected_objects.remove(obj)
        else:
            selected_objects.append(obj)

panel.bind("<Button-1>", on_click)

# 表示更新
def update_image():
    # グローバル変数を使用
    global img, detected_objects, selected_objects

    # 元画像をコピー
    display_img = img.copy()

    # 物体の中心点と選択状態を描画
    for obj in detected_objects:
        cx, cy = obj["center"]
        radius = 8
        if obj in selected_objects:
            cv2.circle(display_img, (cx, cy), radius, (0, 0, 255), -1)  # 選択された物体は赤
        else:
            cv2.circle(display_img, (cx, cy), radius, (0, 0, 0), 2)  # 未選択の物体は黒

    # 選択された物体のバウンディングボックスを描画
    for obj in selected_objects:
        x, y, w, h = obj["bbox"]
        label = obj["label"]
        cv2.rectangle(display_img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 赤い枠
        cv2.putText(display_img, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # 表示用にリサイズ
    display_height = panel.winfo_height()
    display_width = panel.winfo_width()
    resized_img = cv2.resize(display_img, (display_width, display_height), interpolation=cv2.INTER_AREA)

    # Tkinterで表示するためにRGB変換
    rgb = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)
    imgtk = ImageTk.PhotoImage(pil_img)
    panel.imgtk = imgtk
    panel.config(image=imgtk)

    # 再帰的に更新
    if running:
        root.after(50, update_image)
    else:
        root.quit()

# 開始
update_image()
root.mainloop()

# 結果出力
print("選択された物体情報：")
for obj in selected_objects:
    print(f"- ラベル: {obj['label']}, 信頼度: {obj['confidence']:.2f}, 中心: {obj['center']}")
