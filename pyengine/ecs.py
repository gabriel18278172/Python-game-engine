"""Entity Component System primitives."""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import count
from typing import Iterable, TypeVar

from .math import Vector2


class Component:
    """Marker base class for entity components."""


@dataclass(slots=True)
class Transform(Component):
    position: Vector2 = field(default_factory=Vector2)
    rotation: float = 0.0
    scale: Vector2 = field(default_factory=lambda: Vector2(1, 1))


@dataclass(slots=True)
class Velocity(Component):
    value: Vector2 = field(default_factory=Vector2)


T = TypeVar("T", bound=Component)
_next_entity_id = count(1)


class Entity:
    """A lightweight container of components."""

    def __init__(self, name: str = "Entity") -> None:
        self.id = next(_next_entity_id)
        self.name = name
        self._components: dict[type[Component], Component] = {}
        self.active = True

    def add(self, component: T) -> T:
        self._components[type(component)] = component
        return component

    def get(self, component_type: type[T]) -> T | None:
        component = self._components.get(component_type)
        return component if isinstance(component, component_type) else None

    def require(self, component_type: type[T]) -> T:
        component = self.get(component_type)
        if component is None:
            raise KeyError(f"{self.name} is missing {component_type.__name__}")
        return component

    def has(self, *component_types: type[Component]) -> bool:
        return all(component_type in self._components for component_type in component_types)


class System:
    """Base class for systems that update entities each frame."""

    priority = 0

    def update(self, entities: Iterable[Entity], dt: float) -> None:  # pragma: no cover - interface
        raise NotImplementedError


class MovementSystem(System):
    """Applies velocity to transform positions."""

    priority = 100

    def update(self, entities: Iterable[Entity], dt: float) -> None:
        for entity in entities:
            if not entity.active or not entity.has(Transform, Velocity):
                continue
            transform = entity.require(Transform)
            velocity = entity.require(Velocity)
            transform.position = transform.position + velocity.value * dt
