from abc import abstractmethod

import tkinter as tk

from command import Command


class Drawable():
    @abstractmethod
    def draw(x: int, y: int) -> None:
        pass


class DrawCanvas(tk.Canvas, Drawable):
    draw_canvas = None

    def __init__(self, x0, y0, x1, y1, **key):
        self.id = self.draw_canvas.create_line(x0, y0, x1, y1, **key)


class DrawCommand(Command):
    def __init__(self, drawable, position):
        self.drawable = drawable
        self.position = position

    def execute(self):
        self.drawable.draw(x=self.position.x, y=self.position.y)
