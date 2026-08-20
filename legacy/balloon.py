import random

# Balloon class
class Balloon:
    def __init__(self):
        self.image = random.choice(BALLOON_IMAGES)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.radius = min(self.width, self.height) // 2
        self.popped = False
        self.reset()

    def reset(self):
        self.x = random.randint(0, actual_width - self.width)
        self.y = actual_height + random.randint(0, 300)
        self.speed = random.uniform(8.0, 9.0)
        self.popped = False

    def update(self):
        if not self.popped:
            self.y -= self.speed
            self.x += math.sin(time.time() * 2 + self.y * 0.01) * 0.5
            if self.y + self.height < 0:
                self.reset()

    def draw(self, win):
        if not self.popped:
            win.blit(self.image, (self.x, self.y))

    def is_clicked(self, pos):
        cx = self.x + self.width // 2
        cy = self.y + self.height // 2
        dx = pos[0] - cx
        dy = pos[1] - cy
        return dx * dx + dy * dy <= self.radius * self.radius
