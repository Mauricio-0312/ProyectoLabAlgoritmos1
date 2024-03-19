import tkinter as tk
from typing import Tuple
def staticCircle(
canvas: tk.Canvas,
x: int, y: int,
r: int, c: str
) -> int:
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, outline=c)

def cross(
canvas: tk.Canvas,
x: int, y: int, l: int, c: str
) -> Tuple[int, int]:

    firstLine = canvas.create_line(x-l,y+l,x+l,y-l, fill=c)
    secondLine = canvas.create_line(x-l,y-l,x+l,y+l, fill=c)
    cross = (firstLine, secondLine)
    
    return cross