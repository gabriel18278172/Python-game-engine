"""Deterministic 2D collision helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .math import Vector2


@dataclass(frozen=True, slots=True)
class AABB:
    """Axis-aligned bounding box."""

    position: Vector2
    size: Vector2

    @property
    def left(self) -> float:
        return self.position.x

    @property
    def right(self) -> float:
        return self.position.x + self.size.x

    @property
    def top(self) -> float:
        return self.position.y

    @property
    def bottom(self) -> float:
        return self.position.y + self.size.y

    def intersects(self, other: AABB) -> bool:
        return not (
            self.right <= other.left
            or self.left >= other.right
            or self.bottom <= other.top
            or self.top >= other.bottom
        )


class PhysicsWorld:
    """Stores colliders and reports overlapping pairs."""

    def __init__(self) -> None:
        self.colliders: list[tuple[str, AABB]] = []

    def add_collider(self, name: str, collider: AABB) -> None:
        self.colliders.append((name, collider))

    def clear(self) -> None:
        self.colliders.clear()

    def collisions(self) -> Iterable[tuple[str, str]]:
        for index, (left_name, left_box) in enumerate(self.colliders):
            for right_name, right_box in self.colliders[index + 1 :]:
                if left_box.intersects(right_box):
                    yield left_name, right_name
