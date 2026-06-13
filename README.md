# Python Game Engine

A compact, dependency-free 2D Python game engine foundation designed for clean architecture, deterministic tests, and easy extension into a full game runtime.

## Highlights

- **Entity Component System** with entities, components, systems, transforms, and velocity-based movement.
- **Deterministic game loop** with fixed-step frame execution for reproducible gameplay and tests.
- **Event bus** for decoupled scene and gameplay communication.
- **Input abstraction** that can be fed by any platform adapter.
- **Asset manager** with caching and path traversal protection.
- **2D math and physics** including vectors and AABB collision detection.
- **Renderer abstraction** with a dependency-free terminal canvas backend.
- **Test suite** covering movement, rendering, and collision behavior.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python examples/bouncing_box.py
```

## Minimal game

```python
from pyengine import Entity, Game, Scene, Transform, Vector2, Velocity

player = Entity("Player")
player.add(Transform(position=Vector2(0, 0)))
player.add(Velocity(Vector2(10, 0)))

game = Game(fixed_dt=1 / 60)
scene = game.add_scene(Scene("Level 1"), activate=True)
scene.add_entity(player)

game.run_for_frames(60)
print(player.require(Transform).position)  # Vector2(x=10.0, y=0.0)
```

## Project layout

```text
pyengine/
  assets.py     Safe asset loading and caching
  core.py       Game loop and scene orchestration
  ecs.py        Entity Component System primitives
  events.py     Event bus
  input.py      Platform-neutral input state
  math.py       Vector and interpolation helpers
  physics.py    AABB collisions
  renderer.py   Canvas and console renderer
  time.py       Frame clock
tests/          Regression tests
examples/       Runnable demos
```

## Development

```bash
python -m pytest
python -m compileall pyengine examples tests
```

The engine intentionally avoids mandatory third-party runtime dependencies so it can be embedded in tools, teaching projects, terminal games, or custom graphical frontends. Add platform adapters such as Pygame, Arcade, or pyglet on top of the core abstractions when you need windowing, audio, or GPU-backed rendering.
