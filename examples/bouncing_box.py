"""Run with: python examples/bouncing_box.py"""

from pyengine import Canvas, ConsoleRenderer

canvas = Canvas(20, 8)
canvas.draw_rect(2, 2, 5, 3, "@")
print(ConsoleRenderer().present(canvas))
