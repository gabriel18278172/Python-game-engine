"""Main game loop and scene orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .ecs import Entity, MovementSystem, System
from .events import EventBus
from .input import InputState
from .time import Clock


@dataclass
class Scene:
    """Collection of entities and systems updated together."""

    name: str
    entities: list[Entity] = field(default_factory=list)
    systems: list[System] = field(default_factory=lambda: [MovementSystem()])

    def add_entity(self, entity: Entity) -> Entity:
        self.entities.append(entity)
        return entity

    def add_system(self, system: System) -> System:
        self.systems.append(system)
        self.systems.sort(key=lambda item: item.priority)
        return system

    def update(self, dt: float) -> None:
        for system in sorted(self.systems, key=lambda item: item.priority):
            system.update(self.entities, dt)


class Game:
    """Production-minded fixed-step game runner with lifecycle hooks."""

    def __init__(self, *, target_fps: int = 60, fixed_dt: float = 1 / 60) -> None:
        self.clock = Clock(target_fps)
        self.fixed_dt = fixed_dt
        self.events = EventBus()
        self.input = InputState()
        self.scenes: dict[str, Scene] = {}
        self.active_scene: Scene | None = None
        self.running = False

    def add_scene(self, scene: Scene, *, activate: bool = False) -> Scene:
        self.scenes[scene.name] = scene
        if activate or self.active_scene is None:
            self.active_scene = scene
        return scene

    def set_scene(self, name: str) -> None:
        self.active_scene = self.scenes[name]
        self.events.emit("scene_changed", name=name)

    def stop(self) -> None:
        self.running = False

    def step(self, dt: float) -> None:
        if self.active_scene is not None:
            self.active_scene.update(dt)
        self.input.end_frame()

    def run_for_frames(self, frames: int) -> None:
        if frames < 0:
            raise ValueError("frames cannot be negative")
        self.running = True
        for _ in range(frames):
            if not self.running:
                break
            self.step(self.fixed_dt)

    def entities(self) -> Iterable[Entity]:
        return () if self.active_scene is None else tuple(self.active_scene.entities)
