"""Renderer abstractions and a dependency-free console backend."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Color:
    r: int
    g: int
    b: int


class Canvas:
    """Character canvas for tests, tools, and terminal games."""

    def __init__(self, width: int, height: int, fill: str = " ") -> None:
        if width <= 0 or height <= 0:
            raise ValueError("canvas dimensions must be positive")
        self.width = width
        self.height = height
        self.fill = fill[0]
        self._pixels = [[self.fill for _ in range(width)] for _ in range(height)]

    def clear(self, fill: str | None = None) -> None:
        char = (fill or self.fill)[0]
        for y in range(self.height):
            self._pixels[y] = [char for _ in range(self.width)]

    def draw_point(self, x: int, y: int, char: str = "#") -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self._pixels[y][x] = char[0]

    def draw_rect(self, x: int, y: int, width: int, height: int, char: str = "#") -> None:
        for row in range(y, y + height):
            for col in range(x, x + width):
                self.draw_point(col, row, char)

    def render(self) -> str:
        return "\n".join("".join(row) for row in self._pixels)


class ConsoleRenderer:
    """Renderer that returns frames as strings for terminal output."""

    def present(self, canvas: Canvas) -> str:
        return canvas.render()
