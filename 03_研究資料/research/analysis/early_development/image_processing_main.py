import cv2
import tkinter as tk
from tkinter import filedialog
import numpy as np
import os

# グローバル変数定義
img = None
roi_coords = None
color_mode = "RGB"
r_var, g_var, b_var = None, None, None
slider_window = None
img_path = None

# 日本語を含むパスから画像を読み込む関数（BGR形式で読み込み）
def imread_jp(path):
    with open(path, "rb") as f:
        img_buf = np.frombuffer(f.read(), dtype=np.uint8)
    return cv2.imdecode(img_buf, cv2.IMREAD_COLOR)

# 日本語を含むパスへ画像を保存する関数
def imwrite_jp(path, img):
    ext = "." + path.split(".")[-1]
    ret, buf = cv2.imencode(ext, img)
    if ret:
        with open(path, mode='wb') as f:
            buf.tofile(f)
        return True
    return False

# スライダーの値に基づいて画像の選択範囲をリアルタイムで更新表示
def update():
    global roi_coords, img
    if roi_coords is None:
        return
    x1, y1, x2, y2 = roi_coords
    h, w = img.shape[:2]

    # 画像の範囲内に収める
    x1 = max(0, min(x1, w))
    x2 = max(0, min(x2, w))
    y1 = max(0, min(y1, h))
    y2 = max(0, min(y2, h))

    width, height = x2 - x1, y2 - y1
    if width <= 0 or height <= 0:
        return

    # 塗りつぶす色を作成（RGBまたはHSVに応じて）
    if color_mode == "RGB":
        fill_color = np.full((height, width, 3), (b_var.get(), g_var.get(), r_var.get()), dtype=np.uint8)
    else:
        hsv_fill = np.full((height, width, 3), (r_var.get(), g_var.get(), b_var.get()), dtype=np.uint8)
        fill_color = cv2.cvtColor(hsv_fill, cv2.COLOR_HSV2BGR)

    # 塗りつぶして一時表示
    temp_img = img.copy()
    temp_img[y1:y2, x1:x2] = fill_color
    cv2.imshow("Image", temp_img)
    cv2.waitKey(1)

# スライダーUIウィンドウを作成し、色の調整インターフェースを表示
def open_slider(avg_color):
    global slider_window, r_var, g_var, b_var
    if slider_window is not None and tk.Toplevel.winfo_exists(slider_window):
        return

    slider_window = tk.Toplevel()
    slider_window.title("色調整")
    slider_window.geometry("300x250")

    # 平均色をスライダーの初期値に設定
    r_var = tk.IntVar(value=int(avg_color[0]))
    g_var = tk.IntVar(value=int(avg_color[1]))
    b_var = tk.IntVar(value=int(avg_color[2]))

    # RGB or HSVスライダー
    tk.Label(slider_window, text="R / H").pack()
    tk.Scale(slider_window, from_=0, to=255, orient="horizontal", variable=r_var, command=lambda _: update()).pack(fill="x")
    tk.Label(slider_window, text="G / S").pack()
    tk.Scale(slider_window, from_=0, to=255, orient="horizontal", variable=g_var, command=lambda _: update()).pack(fill="x")
    tk.Label(slider_window, text="B / V").pack()
    tk.Scale(slider_window, from_=0, to=255, orient="horizontal", variable=b_var, command=lambda _: update()).pack(fill="x")

    # 「保存」ボタンの処理
    def save_image():
        global img_path
        original_name = os.path.splitext(os.path.basename(img_path))[0]
        default_filename = f"{original_name}_editer.png"
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg;*.jpeg")],
            initialfile=default_filename
        )
        if path:
            x1, y1, x2, y2 = roi_coords
            h, w = img.shape[:2]

            # 画像範囲に収める
            x1 = max(0, min(x1, w))
            x2 = max(0, min(x2, w))
            y1 = max(0, min(y1, h))
            y2 = max(0, min(y2, h))

            width, height = x2 - x1, y2 - y1
            if width <= 0 or height <= 0:
                return

            # 色変換
            if color_mode == "RGB":
                fill_color = np.full((height, width, 3), (b_var.get(), g_var.get(), r_var.get()), dtype=np.uint8)
            else:
                hsv_fill = np.full((height, width, 3), (r_var.get(), g_var.get(), b_var.get()), dtype=np.uint8)
                fill_color = cv2.cvtColor(hsv_fill, cv2.COLOR_HSV2BGR)

            # 画像保存
            final_img = img.copy()
            final_img[y1:y2, x1:x2] = fill_color
            if imwrite_jp(path, final_img):
                print("保存成功:", path)
            else:
                print("保存失敗:", path)

    tk.Button(slider_window, text="保存", command=save_image).pack(pady=5)

    # 閉じたときの処理（状態リセット）
    def on_slider_close():
        global slider_window, roi_coords
        slider_window.destroy()
        slider_window = None
        roi_coords = None
        cv2.imshow("Image", img)

    slider_window.protocol("WM_DELETE_WINDOW", on_slider_close)

    # 初期値で画像反映
    update()

# マウスによる領域選択イベント（矩形選択）
selection_data = {"start": None, "end": None, "selecting": False}

def mouse_event(event, x, y, flags, param):
    global roi_coords, slider_window
    if event == cv2.EVENT_LBUTTONDOWN:
        selection_data["start"] = (x, y)
        selection_data["selecting"] = True
    elif event == cv2.EVENT_MOUSEMOVE and selection_data["selecting"]:
        # ドラッグ中は矩形描画
        temp = img.copy()
        cv2.rectangle(temp, selection_data["start"], (x, y), (0, 255, 0), 2)
        cv2.imshow("Image", temp)
        cv2.waitKey(1)
    elif event == cv2.EVENT_LBUTTONUP:
        # 範囲確定
        selection_data["end"] = (x, y)
        selection_data["selecting"] = False
        x1 = min(selection_data["start"][0], selection_data["end"][0])
        y1 = min(selection_data["start"][1], selection_data["end"][1])
        x2 = max(selection_data["start"][0], selection_data["end"][0])
        y2 = max(selection_data["start"][1], selection_data["end"][1])
        roi_coords = (x1, y1, x2, y2)

        roi_img = img[y1:y2, x1:x2]
        if roi_img.size == 0:
            return

        # 平均色を計算（色空間によって分岐）
        if color_mode == "RGB":
            avg_color = roi_img.mean(axis=(0, 1))[::-1]  # BGR→RGB
        else:
            roi_hsv = cv2.cvtColor(roi_img, cv2.COLOR_BGR2HSV)
            avg_color = roi_hsv.mean(axis=(0, 1))

        # スライダーウィンドウが開いてたら閉じる → 再表示
        if slider_window is not None and tk.Toplevel.winfo_exists(slider_window):
            slider_window.destroy()
        open_slider(avg_color)

# 起動時にRGB/HSVモードを選択するUI
def select_mode():
    root = tk.Tk()
    root.title("色空間選択")
    root.geometry("300x150")
    mode_var = tk.StringVar(value="RGB")
    tk.Label(root, text="モードを選択してください").pack(pady=10)
    tk.Radiobutton(root, text="RGB モード", variable=mode_var, value="RGB").pack(anchor="w", padx=20)
    tk.Radiobutton(root, text="HSV モード", variable=mode_var, value="HSV").pack(anchor="w", padx=20)
    tk.Button(root, text="決定", command=root.quit).pack(pady=10)
    root.mainloop()
    selected = mode_var.get()
    root.destroy()
    return selected

# メイン処理：画像を選択→モード選択→表示・編集開始
def main():
    global img, color_mode, slider_window, img_path
    tk.Tk().withdraw()  # ファイルダイアログのみ使用
    img_path = filedialog.askopenfilename(title="画像を選択", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if not img_path:
        return
    img = imread_jp(img_path)
    if img is None:
        print("画像読み込みエラー")
        return
    color_mode = select_mode()
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouse_event)

    # ウィンドウが閉じられるまでループ
    while True:
        if cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
            if slider_window is not None and tk.Toplevel.winfo_exists(slider_window):
                slider_window.destroy()
            break
        if slider_window is not None and tk.Toplevel.winfo_exists(slider_window):
            slider_window.update()
        if cv2.waitKey(100) & 0xFF == 27:
            if slider_window is not None and tk.Toplevel.winfo_exists(slider_window):
                slider_window.destroy()
            break
    cv2.destroyAllWindows()

# プログラム開始点
if __name__ == "__main__":
    main()
