import math
import random
from dataclasses import dataclass

import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (20, 20, 45)
BOID_COLOR = (255, 100, 100)
BOID_SPEED = 2.0
BOID_SIZE = 10.0
BOID_COUNT = 100
PERCEPTION_RADIUS = 50
SEPARATION_RADIUS = 30
SEPARATION_WEIGHT = 1.5
ALIGNMENT_WEIGHT = 1.0
COHESION_WEIGHT = 1.0
MAX_SPEED = 4.0


@dataclass
class Boid:
    x: float
    y: float
    vx: float
    vy: float


def make_random_boid() -> Boid:
    x = random.uniform(0, SCREEN_WIDTH)  # noqa: S311
    y = random.uniform(0, SCREEN_HEIGHT)  # noqa: S311
    angle = random.uniform(0, 2 * math.pi)  # noqa: S311
    vx = math.cos(angle) * BOID_SPEED
    vy = math.sin(angle) * BOID_SPEED
    return Boid(x, y, vx, vy)


def distance(a: Boid, b: Boid) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)


def get_neighbors(boid: Boid, boids: list[Boid]) -> list[Boid]:
    neighbors = []
    for other in boids:
        if other is boid:
            continue
        if distance(boid, other) < PERCEPTION_RADIUS:
            neighbors.append(other)
    return neighbors


def separation(boid: Boid, neighbors: list[Boid]) -> tuple:
    steer_x, steer_y = 0.0, 0.0
    count = 0

    for other in neighbors:
        d = distance(boid, other)
        if d < SEPARATION_RADIUS and d > 0:
            steer_x += (boid.x - other.x) / (d * d)
            steer_y += (boid.y - other.y) / (d * d)
            count += 1
    if count > 0:
        steer_x /= count
        steer_y /= count

    return steer_x, steer_y


def alignment(boid: Boid, neighbors: list[Boid]) -> tuple[float, float]:
    if not neighbors:
        return 0.0, 0.0
    avg_vx = sum(n.vx for n in neighbors) / len(neighbors)
    avg_vy = sum(n.vy for n in neighbors) / len(neighbors)
    return avg_vx - boid.vx, avg_vy - boid.vy


def cohesion(boid: Boid, neighbors: list[Boid]) -> tuple[float, float]:
    if not neighbors:
        return 0.0, 0.0
    center_x = sum(n.x for n in neighbors) / len(neighbors)
    center_y = sum(n.y for n in neighbors) / len(neighbors)
    return center_x - boid.x, center_y - boid.y


def limit_speed(vx: float, vy: float, max_speed: float) -> tuple[float, float]:
    speed = math.hypot(vx, vy)
    if speed <= max_speed:
        return vx, vy
    scale = max_speed / speed
    return vx * scale, vy * scale


def update_boid(boid: Boid, boids: list[Boid]) -> None:
    neighbors = get_neighbors(boid, boids)

    sep_x, sep_y = separation(boid, neighbors)
    align_x, align_y = alignment(boid, neighbors)
    coh_x, coh_y = cohesion(boid, neighbors)

    boid.vx += (
        sep_x * SEPARATION_WEIGHT
        + align_x * ALIGNMENT_WEIGHT
        + coh_x * COHESION_WEIGHT * 0.01
    )
    boid.vy += (
        sep_y * SEPARATION_WEIGHT
        + align_y * ALIGNMENT_WEIGHT
        + coh_y * COHESION_WEIGHT * 0.01
    )

    boid.vx, boid.vy = limit_speed(boid.vx, boid.vy, MAX_SPEED)

    boid.x = (boid.x + boid.vx) % SCREEN_WIDTH
    boid.y = (boid.y + boid.vy) % SCREEN_HEIGHT


def draw_boid(screen, boid: Boid) -> None:
    angle = math.atan2(boid.vy, boid.vx)

    local_points = [
        (BOID_SIZE, 0),
        (-BOID_SIZE * 0.6, -BOID_SIZE * 0.6),
        (-BOID_SIZE * 0.6, BOID_SIZE * 0.6),
    ]

    cos_a, sin_a = math.cos(angle), math.sin(angle)
    points = []
    for px, py in local_points:
        new_px = boid.x + px * cos_a - py * sin_a
        new_py = boid.y + px * sin_a + py * cos_a
        points.append((new_px, new_py))

    pygame.draw.polygon(screen, BOID_COLOR, points)


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("--->", type(screen))
    pygame.display.set_caption("Boids")
    clock = pygame.time.Clock()

    boids = [make_random_boid() for _ in range(BOID_COUNT)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for boid in boids:
            update_boid(boid, boids)

        screen.fill(BACKGROUND_COLOR)

        for boid in boids:
            draw_boid(screen, boid)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
