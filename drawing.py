#!/user/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.colorchooser as tc
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesno
from PIL import ImageGrab, Image, ImageTk
import time
import threading
import os
import random


class Drawer(threading.Thread):
    color = 'black'  # 描画色
    before = (None, None)  # 線を引く時使用。前の座標と直前の座標との差異を線とする
    work = list()  # Undoする為の描画OBJを保存
    image = list()  # GCにイメージを消されない為に保存
    file_name = 'example.png'  # 記録するファイルの名前

    def __init__(self):
        super().__init__(name='GUI', daemon=True)
        # 一時ファイル作成
        if not os.path.exists('tmp'):
            os.makedirs('tmp')

    def run(self):
        def mouse_move(event):
            # マウスを動かす度に発生するEvent
            x, y = event.x, event.y
            if self.before[0] is None:
                # 始点なので
                self.before = (x, y)
                self.work.append(list())
                return
            else:
                # 途中の点なので
                obj = canvas.create_line(
                    self.before[0], self.before[1], x, y,
                    fill=self.color, width=pen_var.get())
                self.work[-1].append(obj)
                self.before = (x, y)

        def mouse_release(event):
            # マウスを離した時の動作、線の終点
            self.before = (None, None)
            return

        def mouse_undo():
            # 操作のやり直し
            try:
                for obj in self.work[-1]:
                    canvas.delete(obj)
                self.work.pop()
            except:
                pass

        def set_color_palette():
            # 線の色を選択
            color_tuple, self.color = tc.askcolor()
            w_color = 'black' if sum(color_tuple) > 255 * 1.2 else 'white'
            palette_btn.config(bg=self.color, fg=w_color)

        def recode_image():
            # 画像を保存、スクリーンショットを使用するので注意
            # 一時ファイルに保存
            x = root.winfo_rootx() + canvas.winfo_x()
            y = root.winfo_rooty() + canvas.winfo_y()
            x1 = x + canvas.winfo_width()
            y1 = y + canvas.winfo_height()
            img = ImageGrab.grab().crop((x, y, x1, y1))
            _tmp = 'tmp/' + str(random.randint(10000000, 99999999)) + '.png'
            img.save(_tmp)

            # 保存する場所名前を選択
            save_path = asksaveasfilename(
                filetypes=[("", "png")],
                initialdir=os.path.abspath(os.path.dirname(__file__)),
                initialfile=self.file_name.split('/')[-1])
            if '.png//' not in save_path + '//':
                save_path += '.png'

            # 保存する
            try:
                os.rename(_tmp, save_path)
            except FileExistsError as e:
                if askyesno('File editor', 'Overwrite "%s" ?' % save_path.split('/')[-1]):
                    os.remove(save_path)
                    os.rename(_tmp, save_path)
                else:
                    pass

        def road_image():
            # 画像を読み込む
            # 画像へのパス
            file_name = askopenfilename(filetypes=[("", "ps"), ("", "png")],
                                        initialdir=os.path.abspath(os.path.dirname(__file__)))
            if file_name == "": return

            # 画像の読み込み
            self.file_name = file_name
            image = Image.open(file_name)
            image_tk = ImageTk.PhotoImage(image=image)
            self.image.append(image_tk)
            # Canvasへ描写
            canvas.create_image(canvas.winfo_width() // 2, canvas.winfo_height() // 2, image=image_tk)
            root.title("drawing (%s)" % file_name.split('/')[-1])

        """ 初期化 """
        root = tk.Tk()
        root.title("drawing (empty)")
        root.geometry("800x600")

        # Canvas
        canvas = tk.Canvas(root, bg="white", width=750, height=500)
        canvas.bind("<B1-Motion>", mouse_move)
        canvas.bind("<ButtonRelease-1>", mouse_release)
        canvas.pack(padx=1, pady=1, fill=tk.BOTH)

        # Palette
        palette_btn = tk.Button(root, text='色', command=set_color_palette)
        palette_btn.configure(font=("", 20))
        palette_btn.pack(padx=10, pady=10, side=tk.LEFT)

        # Undo
        undo_btn = tk.Button(root, text='戻', command=mouse_undo)
        undo_btn.configure(font=("", 20))
        undo_btn.pack(padx=10, pady=10, side=tk.LEFT)

        # Recode
        recode_btn = tk.Button(root, text='録', command=recode_image)
        recode_btn.configure(font=("", 20))
        recode_btn.pack(padx=10, pady=10, side=tk.LEFT)

        # Load
        road_btn = tk.Button(root, text='読', command=road_image)
        road_btn.configure(font=("", 20))
        road_btn.pack(padx=10, pady=10, side=tk.LEFT)

        # PenGage
        pen_var = tk.IntVar()
        pen_var.set(1)
        gage_pen = tk.Scale(root, orient=tk.HORIZONTAL, from_=1, to=32, variable=pen_var)
        gage_pen.pack(padx=5, pady=5, fill=tk.BOTH)
        root.mainloop()


def test():
    t = Drawer()
    t.start()

    print("""    ##################################################
    #      tkinter hello world program               #
    #      drawing board                             #
    #      creator: namuyan                          #
    ##################################################""")
    while True:
        try:
            cmd = input(">> ")
            if cmd == 'exit' or cmd == '':
                break
            else:
                exec(cmd)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    test()
