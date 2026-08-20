"""
Visual feedback effects for balloon pops and missed clicks.
Effects are time-based frame animations that grow and fade out.
"""
import time


class CrackEffect:
    """Animated crack/boom effect shown when a balloon is popped."""

    def __init__(self, x, y, frames, duration=1):
        self.x = x
        self.y = y
        self.frames = frames
        self.start_time = time.time()
        self.duration = duration
        self.frame_duration = duration / len(frames)

    def update(self):
        """Return True while the effect is still animating."""
        return time.time() - self.start_time < self.duration

    def draw(self, screen):
        elapsed = time.time() - self.start_time
        if elapsed < self.duration:
            frame_index = int(elapsed / self.frame_duration)
            if frame_index < len(self.frames):
                frame = self.frames[frame_index]
                fx = self.x - frame.get_width() // 2
                fy = self.y - frame.get_height() // 2
                screen.blit(frame, (fx, fy))


class MissEffect(CrackEffect):
    """Miss animation effect (same mechanics as CrackEffect)."""
    pass