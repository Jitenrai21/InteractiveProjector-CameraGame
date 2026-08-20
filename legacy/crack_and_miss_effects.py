import time
import pygame
from modules.boom_animation import generate_boom_frames
from modules.config import *

base_crack = pygame.image.load('../assets/crack.png').convert_alpha()
base_crack = pygame.transform.scale(base_crack, (200, 120))
boom_frames = generate_boom_frames(base_crack, num_frames=6)
miss_image = pygame.image.load("../assets/miss.png").convert_alpha()
miss_image = pygame.transform.scale(miss_image, (150, 100))
miss_frames = generate_boom_frames(miss_image, num_frames=6)

class CrackEffect:
    def __init__(self, x, y, duration=1):
        self.x = x
        self.y = y
        self.start_time = time.time()
        self.duration = duration
        self.frame_duration = duration / len(boom_frames)

    def draw(self, win):
        elapsed = time.time() - self.start_time
        if elapsed < self.duration:
            frame_index = int(elapsed / self.frame_duration)
            if frame_index < len(boom_frames):
                frame = boom_frames[frame_index]
                # Adjust position to keep effect centered
                fx = self.x - frame.get_width() // 2
                fy = self.y - frame.get_height() // 2
                win.blit(frame, (fx, fy))
            return True
        return False

class MissEffect:
    def __init__(self, x, y, duration=1):
        self.x = x
        self.y = y
        self.start_time = time.time()
        self.duration = duration
        self.frame_duration = duration / len(miss_frames)

    def draw(self, win):
        elapsed = time.time() - self.start_time
        if elapsed < self.duration:
            frame_index = int(elapsed / self.frame_duration)
            if frame_index < len(miss_frames):
                frame = miss_frames[frame_index]
                # Adjust position to keep effect centered
                fx = self.x - frame.get_width() // 2
                fy = self.y - frame.get_height() // 2
                win.blit(frame, (fx, fy))
            return True
        return False