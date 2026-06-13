"""PyEngine: a compact, dependency-free Python game engine."""

from .assets import AssetManager
from .core import Game, Scene
from .demo import DemoState, build_demo_payload, build_demo_state
from .ecs import Component, Entity, System, Transform, Velocity
from .events import Event, EventBus
from .input import InputState
from .math import Vector2, clamp, lerp
from .physics import AABB, PhysicsWorld
from .renderer import Canvas, Color, ConsoleRenderer
from .time import Clock

__all__ = [
    "AABB",
    "AssetManager",
    "Canvas",
    "Clock",
    "Color",
    "Component",
    "ConsoleRenderer",
    "DemoState",
    "Entity",
    "Event",
    "EventBus",
    "Game",
    "InputState",
    "PhysicsWorld",
    "Scene",
    "System",
    "Transform",
    "Vector2",
    "Velocity",
    "build_demo_payload",
    "build_demo_state",
    "clamp",
    "lerp",
]

from .version import __version__
