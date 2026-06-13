"""Small math primitives used across the engine."""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot


def clamp(value: float, minimum: float, maximum: float) -> float:
    """Clamp *value* to the inclusive range [minimum, maximum]."""
    if minimum > maximum:
        raise ValueError("minimum cannot be greater than maximum")
    return max(minimum, min(maximum, value))


def lerp(start: float, end: float, alpha: float) -> float:
    """Linearly interpolate between *start* and *end*."""
    return start + (end - start) * alpha


@dataclass(frozen=True, slots=True)
class Vector2:
    """Immutable 2D vector with common arithmetic operations."""

    x: float = 0.0
    y: float = 0.0

    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2) -> Vector2:
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vector2:
        return Vector2(self.x * scalar, self.y * scalar)

    __rmul__ = __mul__

    def __truediv__(self, scalar: float) -> Vector2:
        if scalar == 0:
            raise ZeroDivisionError("cannot divide a vector by zero")
        return Vector2(self.x / scalar, self.y / scalar)

    @property
    def magnitude(self) -> float:
        return hypot(self.x, self.y)

    def normalized(self) -> Vector2:
        length = self.magnitude
        return self if length == 0 else self / length

    def dot(self, other: Vector2) -> float:
        return self.x * other.x + self.y * other.y
