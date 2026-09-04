import pygame
from CircleShape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
import random

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def split(self):
        # 1. Šitas asteroid visada sunaikinamas
        self.kill()

        # 2. Jei per mažas – nesidalinaÍ›
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # 3. Log event (Boot.dev CLI tikrina būtent šitą)
        log_event("asteroid_split")

        # 4. Atsitiktinis kampas tarp 20 ir 50 laipsnių
        angle = random.uniform(20, 50)

        # 5. Sukuriam du naujus velocity vektorius
        v1 = self.velocity.rotate(angle)
        v2 = self.velocity.rotate(-angle)

        # 6. Naujas mažesnių asteroidų radius
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # 7. Sukuriam du naujus asteroidus toje pačioje vietoje
        a1 = Asteroid(self.position.x, self.position.y, new_radius)
        a2 = Asteroid(self.position.x, self.position.y, new_radius)

        # 8. Padidinam greitį ×1.2 (Boot.dev reikalavimas)
        a1.velocity = v1 * 1.2
        a2.velocity = v2 * 1.2