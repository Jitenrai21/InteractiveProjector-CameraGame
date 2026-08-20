"""
Balloon entity for the interactive projector game.
Each balloon rises from the bottom of the projector screen with a
personality movement pattern and occasional wind gusts.
"""
import math
import random
import time


class Balloon:
    def __init__(self, images, screen_width, screen_height, zone_count, zone_width, occupied_zones):
        self.images = images
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.zone_count = zone_count
        self.zone_width = zone_width
        self.occupied_zones = occupied_zones

        self.image = random.choice(self.images)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.radius = min(self.width, self.height) // 2
        self.popped = False
        self.movement_type = random.choice(['zigzag', 'sway', 'spiral'])
        self.wind_offset = 0
        self.birth_time = time.time()
        self.reset()

    def reset(self):
        """Reposition balloon into a free spawn zone at the bottom of the screen."""
        if len(self.occupied_zones) >= self.zone_count:
            self.occupied_zones.clear()

        zone = random.choice([i for i in range(self.zone_count) if i not in self.occupied_zones])
        max_x_offset = max(0, self.zone_width - self.width)
        self.x = zone * self.zone_width + random.randint(0, max_x_offset)
        self.occupied_zones.add(zone)

        self.y = self.screen_height - 10
        self.speed = random.uniform(28.0, 30.0)
        self.popped = False
        self.movement_type = random.choice(['zigzag', 'spiral', 'sway'])
        self.wind_amplitude = random.uniform(0.8, 2.0)

    def update(self, slow_factor=1.0):
        """Advance balloon position; reset when it leaves the top of the screen."""
        if not self.popped:
            self.y -= self.speed * slow_factor

            t = time.time() - self.birth_time

            if self.movement_type == 'zigzag':
                self.x += math.sin(t * 5) * 8
            elif self.movement_type == 'sway':
                self.x += math.sin(self.y * 0.01) * 6
            elif self.movement_type == 'spiral':
                self.x += math.sin(t * 3) * (self.y * 0.008)

            if random.random() < 0.002:
                self.wind_offset = random.uniform(-10, 10)
            else:
                self.wind_offset *= 0.9

            self.x += self.wind_offset

            if self.y + self.height < 0:
                self.reset()

    def draw(self, screen):
        if not self.popped:
            screen.blit(self.image, (self.x, self.y))

    def is_clicked(self, pos):
        """Return True if the click position falls inside the balloon circle."""
        cx = self.x + self.width // 2
        cy = self.y + self.height // 2
        dx = pos[0] - cx
        dy = pos[1] - cy
        return dx * dx + dy * dy <= self.radius * self.radius