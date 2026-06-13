from pyengine import AABB, Canvas, Entity, Game, PhysicsWorld, Scene, Transform, Vector2, Velocity


def test_vector_math_and_movement_system():
    player = Entity("Player")
    player.add(Transform(position=Vector2(1, 2)))
    player.add(Velocity(Vector2(3, 4)))

    game = Game(fixed_dt=0.5)
    game.add_scene(Scene("level")).add_entity(player)
    game.run_for_frames(2)

    assert player.require(Transform).position == Vector2(4, 6)


def test_canvas_draws_clipped_rectangles():
    canvas = Canvas(4, 3, ".")
    canvas.draw_rect(2, 1, 4, 3, "X")

    assert canvas.render() == "....\n..XX\n..XX"


def test_physics_reports_collisions_once():
    world = PhysicsWorld()
    world.add_collider("a", AABB(Vector2(0, 0), Vector2(2, 2)))
    world.add_collider("b", AABB(Vector2(1, 1), Vector2(2, 2)))
    world.add_collider("c", AABB(Vector2(5, 5), Vector2(1, 1)))

    assert list(world.collisions()) == [("a", "b")]
