"""
https://yamakatsusan.web.fc2.com/pythonpattern23.html
を参考にさせていただき、実装。
"""
import tkinter as tk

from command import MacroCommand
from drawer import DrawCanvas, DrawCommand


class MainFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("Command Pattern Sample")
        # 履歴
        self.history = MacroCommand()
        # クリアボタン
        self.clear_button = tk.Button(
            self, text="clear", command=self.clear_click)
        self.clear_button.pack(side=tk.TOP)
        # キャンバス（別のクラス）
        self.canvas = tk.Canvas(
            self, bg="white", width=500, height=500)
        self.canvas.pack()
        # お絵かきのためのマウス操作のイベントドリブン
        self.canvas.bind('<ButtonPress-1>', self.mouse_left_click)
        self.canvas.bind('<B1-Motion>', self.mouse_drag)
        # 調合した色のサンプル
        self.label = tk.Label(self, text='Selected', fg='#ffffff', width=15)
        self.label.pack()
        # 色の調合のためのスケール
        self.R_scale = tk.Scale(
            self, label='Red', orient=tk.HORIZONTAL, from_=0, to=255,
            length=300, resolution=1, command=self.palette)
        self.R_scale.set(255)
        self.R_scale.pack()
        self.G_scale = tk.Scale(
            self, label='Green', orient=tk.HORIZONTAL, from_=0, to=255,
            length=300, resolution=1, command=self.palette)
        self.G_scale.pack()
        self.B_scale = tk.Scale(
            self, label='Blue', orient=tk.HORIZONTAL, from_=0, to=255,
            length=300, resolution=1, command=self.palette)
        self.B_scale.pack()
        # 線の太さを選ぶ
        self.line_width = tk.Scale(
            self, label='Line Width', from_=1, to=15, orient=tk.HORIZONTAL)
        self.line_width.set(5)
        self.line_width.pack()
    # コンストラクタ終

    # 左ボタンクリック
    def mouse_left_click(self, event):
        self.sx = event.x
        self.sy = event.y

    # マウスドラッグ
    def mouse_drag(self, event):
        DrawCanvas.draw_canvas = self.canvas
        DrawCanvas(self.sx, self.sy, event.x, event.y,
                   fill=self.select_color, width=self.line_width.get())
        self.sx = event.x
        self.sy = event.y
        command = DrawCommand(drawable=self.canvas, position=event)
        self.history.append(command=command)

    # 色の調合
    def palette(self, event):
        self.select_color = '#%02x%02x%02x' % (
            self.R_scale.get(), self.G_scale.get(), self.B_scale.get())
        self.label.configure(bg=self.select_color)

    def clear_click(self):
        self.history.clear()
        self.canvas.delete("all")


if __name__ == '__main__':
    app = MainFrame()
    app.pack()
    app.mainloop()
