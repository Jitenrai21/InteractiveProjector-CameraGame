import random
import pygame


class Cloud:
    def __init__(self, images, screen_width, screen_height):
        self.image = random.choice(images)

        # Random scale
        scale = random.uniform(0.3, 1.2)
        width = int(self.image.get_width() * scale)
        height = int(self.image.get_height() * scale)
        self.image = pygame.transform.scale(self.image, (width, height))

        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height // 2)  # upper half only
        self.speed = random.uniform(1.5, 3)
        self.width = self.image.get_width()
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        self.x += self.speed
        if self.x > self.screen_width:
            self.x = -self.width
            self.y = random.randint(0, self.screen_height // 2)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))