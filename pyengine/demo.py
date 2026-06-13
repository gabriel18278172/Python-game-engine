"""Reusable demo scene helpers for local examples and Vercel deployments."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .version import __version__
from .core import Game, Scene
from .ecs import Entity, Transform, Velocity
from .math import Vector2
from .physics import AABB, PhysicsWorld
from .renderer import Canvas, ConsoleRenderer


@dataclass(frozen=True, slots=True)
class DemoState:
    """Serializable snapshot of a tiny deterministic engine simulation."""

    engine: str
    version: str
    frames: int
    player_position: dict[str, float]
    collisions: list[tuple[str, str]]
    frame: str


def build_demo_state(frames: int = 12) -> DemoState:
    """Run a deterministic micro-scene and return data suitable for an API response."""
    player = Entity("Player")
    player.add(Transform(position=Vector2(1, 2)))
    player.add(Velocity(Vector2(6, 0)))

    game = Game(fixed_dt=1 / 12)
    game.add_scene(Scene("vercel-demo"), activate=True).add_entity(player)
    game.run_for_frames(frames)

    transform = player.require(Transform)
    canvas = Canvas(24, 8, ".")
    x = round(transform.position.x)
    y = round(transform.position.y)
    canvas.draw_rect(x, y, 4, 2, "@")

    world = PhysicsWorld()
    world.add_collider("player", AABB(Vector2(x, y), Vector2(4, 2)))
    world.add_collider("goal", AABB(Vector2(6, 2), Vector2(4, 2)))

    return DemoState(
        engine="PyEngine",
        version=__version__,
        frames=frames,
        player_position={"x": transform.position.x, "y": transform.position.y},
        collisions=list(world.collisions()),
        frame=ConsoleRenderer().present(canvas),
    )


def build_demo_payload(frames: int = 12) -> dict[str, object]:
    """Return a JSON-ready dictionary for web frontends and serverless functions."""
    return asdict(build_demo_state(frames))
