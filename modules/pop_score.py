import time
import pygame

class ScorePopup:
    def __init__(self, x, y, text="+1", color=(0, 255, 0), duration=0.8):
        self.x = x + 60
        self.y = y
        self.text = text
        self.color = color
        self.start_time = time.time()
        self.duration = duration
        self.font = pygame.font.SysFont("Impact", 60)

    def draw(self, surface):
        elapsed = time.time() - self.start_time
        if elapsed >= self.duration:
            return False

        # Float upward and fade out
        offset_y = int(50 * (elapsed / self.duration))  # How far up it floats
        alpha = max(0, 255 - int((elapsed / self.duration) * 255))

        # main text and shadow
        text_surface = self.font.render(self.text, True, self.color)
        shadow_surface = self.font.render(self.text, True, (0, 0, 0))  # Black shadow

        # fading alpha
        text_surface.set_alpha(alpha)
        shadow_surface.set_alpha(alpha)

         # Slight shadow offset for fake bold or drop shadow
        draw_x = self.x
        draw_y = self.y - offset_y
        surface.blit(shadow_surface, (draw_x + 2, draw_y + 2))  # Shadow below/right
        surface.blit(text_surface, (draw_x, draw_y))            # Main text

        return True
