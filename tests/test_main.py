import math

from boids.main import (
    MAX_SPEED,
    Boid,
    cohesion,
    distance,
    limit_speed,
)


def test_distance_to_self_is_zero():
    boid = Boid(x=0.0, y=0.0, vx=0.0, vy=0.0)
    assert distance(boid, boid) == 0.0, "distance from boid to itself should return 0.0"


def test_distance_is_symmetric():
    a = Boid(x=0.0, y=0.0, vx=0.0, vy=0.0)
    b = Boid(x=3.0, y=4.0, vx=0.0, vy=0.0)
    assert distance(a, b) == distance(b, a)
    assert distance(a, b) == 5.0


def test_limit_speed_caps_velocity():
    vx, vy = limit_speed(vx=100.0, vy=0.0, max_speed=MAX_SPEED)
    speed = math.hypot(vx, vy)
    assert speed <= MAX_SPEED + 1e-8


def test_limit_speed_leaves_slow_velocity_untouched():
    vx, vy = limit_speed(vx=1.0, vy=0.0, max_speed=MAX_SPEED)
    assert (vx, vy) == (1.0, 0.0)


def test_cohesion_with_no_neighbors_is_zero():
    boid = Boid(x=50.0, y=50.0, vx=0.0, vy=0.0)
    assert cohesion(boid, []) == (0.0, 0.0)


def test_cohesion_pulls_toward_neighbor_center():
    boid = Boid(x=0.0, y=0.0, vx=0.0, vy=0.0)
    neighbors = [
        Boid(x=10.0, y=0.0, vx=0.0, vy=0.0),
        Boid(x=0.0, y=10.0, vx=0.0, vy=0.0),
    ]
    steer_x, steer_y = cohesion(boid, neighbors)
    assert steer_x == 5.0
    assert steer_y == 5.0

