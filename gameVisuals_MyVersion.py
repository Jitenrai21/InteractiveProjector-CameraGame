import pygame
import numpy as np
import sys
import math
import os
import random
import time
import logging
from screeninfo import get_monitors
from modules.background import draw_text_with_bg
from modules.boom_animation import generate_boom_frames
from modules.cloud import Cloud
from modules.pop_score import ScorePopup

# Constants
SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 768
FPS = 90
CRACK_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "boom1.png")
BACKGROUND_IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "background.jpg")
BALLOON_FILES = ["balloon1.png", "balloon2.png", "balloon3.png"]
POP_SOUND_PATH = "balloon-pop.mp3"

# Initialize Pygame
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
pygame.init()
monitors = get_monitors()
main_screen = monitors[0]
screen = pygame.display.set_mode((main_screen.width, main_screen.height)) # 2040, 1152
pygame.display.set_caption("Balloon Popping Game")
clock = pygame.time.Clock()

# Load assets
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
BALLOON_IMAGES = []

# Load balloon images
for file in BALLOON_FILES:
    path = os.path.join(base_dir, "assets", file)
    if not os.path.exists(path):
        print(f"Warning: Balloon image {path} not found. Skipping.")
        continue
    try:
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (420, 480))
        BALLOON_IMAGES.append(img)
    except pygame.error as e:
        print(f"Warning: Failed to load {path}: {e}. Skipping.")

if not BALLOON_IMAGES:
    print("Error: No valid balloon images loaded. Exiting.")
    pygame.quit()
    sys.exit(1)

# Load crack image
try:
    base_crack = pygame.image.load(CRACK_PATH).convert_alpha()
    base_crack = pygame.transform.scale(base_crack, (200, 120))  # adjust if needed
    boom_frames = generate_boom_frames(base_crack, num_frames=6)

except pygame.error as e:
    print(f"Error loading boom1.png: {e}")
    sys.exit(1)

miss_image = pygame.image.load("assets/miss.png").convert_alpha()
miss_image = pygame.transform.scale(miss_image, (150, 100))
miss_frames = generate_boom_frames(miss_image, num_frames=6)

miss_sound = pygame.mixer.Sound("assets/miss.mp3")

# Load pop sound
def load_sound(filename):
    path = os.path.join(base_dir, "assets", filename)
    if os.path.exists(path):
        try:
            return pygame.mixer.Sound(path)
        except pygame.error as e:
            print(f"Failed to load sound {filename}: {e}")
    return None

pop_sound = load_sound(POP_SOUND_PATH)

# Load background image
try:
    background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
    background_image = pygame.transform.scale(background_image, (main_screen.width, main_screen.height))
except pygame.error as e:
    print(f"Error loading background image {BACKGROUND_IMAGE_PATH}: {e}")
    pygame.quit()
    sys.exit(1)

# Load animated background elements
cloud_image1 = pygame.image.load(os.path.join(base_dir, "assets", "cloud1.png")).convert_alpha()
cloud_image2 = pygame.image.load(os.path.join(base_dir, "assets", "cloud2.png")).convert_alpha()
cloud_images = [cloud_image1, cloud_image2]

clouds = [Cloud(cloud_images, main_screen.width, main_screen.height) for _ in range(10)]

sparkle_img = pygame.image.load(os.path.join(base_dir, "assets", "sparkle.png")).convert_alpha()
sparkle_img = pygame.transform.scale(sparkle_img, (main_screen.width, main_screen.height))  # Adjust as needed

def get_day_night_overlay(elapsed_time, total_time):
    overlay = pygame.Surface((main_screen.width, main_screen.height), pygame.SRCALPHA)
    progress = elapsed_time / total_time
    alpha = int(min(180, 255 * progress))  # Max darkness
    overlay.fill((0, 0, 64, alpha))  # Night bluish tint
    return overlay

# Colors and fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
FONT = pygame.font.SysFont("Impact", 32)
BIG_FONT = pygame.font.SysFont("Impact", 48)

# Balloon movement variables
ZONE_COUNT = 5
zone_width = main_screen.width // ZONE_COUNT
occupied_zones = set()

# Balloon class
class Balloon:
    def __init__(self):
        self.image = random.choice(BALLOON_IMAGES)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.radius = min(self.width, self.height) // 2
        self.popped = False
        self.movement_type = random.choice(['zigzag', 'sway', 'spiral'])
        self.wind_offset = 0  # used for wind gusts
        self.birth_time = time.time()
        self.reset()

    def reset(self):
        global occupied_zones
        if len(occupied_zones) >= ZONE_COUNT:
            occupied_zones.clear()
        
        zone = random.choice([i for i in range(ZONE_COUNT) if i not in occupied_zones])
        max_x_offset = max(0, zone_width - self.width)
        self.x = zone * zone_width + random.randint(0, max_x_offset)
        occupied_zones.add(zone)

        # self.y = actual_height + random.randint(0, 50)
        self.y = main_screen.height - 10  # Almost just off-screen
        self.speed = random.uniform(3.0, 5.0)  # higher speed
        self.popped = False
        self.style = random.choice(['zigzag', 'spiral', 'sway'])  # re-randomize style
        self.wind_amplitude = random.uniform(0.8, 2.0)

    def update(self, slow_factor=1.0):
        if not self.popped:
            # Vertical movement
            self.y -= self.speed * slow_factor
            
            # Horizontal personality movement
            t = time.time() - self.birth_time

            if self.movement_type == 'zigzag':
                self.x += math.sin(t * 5) * 8  # fast side-to-side
            elif self.movement_type == 'sway':
                self.x += math.sin(self.y * 0.01) * 6  # smooth slow sway
            elif self.movement_type == 'spiral':
                self.x += math.sin(t * 3) * (self.y * 0.008)  # spiral outward

            # Occasional wind gust
            if random.random() < 0.002:  # ~0.2% chance per frame
                self.wind_offset = random.uniform(-10, 10)
            else:
                self.wind_offset *= 0.9  # fade out wind

            self.x += self.wind_offset

            # Reset if out of screen
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

# Main loop variables
balloons = [Balloon() for _ in range(1)]
cracks = []
misses = []
last_click_time = 0
running = True
show_debug_overlay = False
font = pygame.font.SysFont(None, 36)
score = 0
GAME_DURATION = 20
start_time = pygame.time.get_ticks()
game_over = False
score_popups = []

#start screen
def draw_start_screen(surface, alpha=255):
    surface.blit(background_image, (0, 0))
    
    for cloud in clouds:
        cloud.update()
        cloud.draw(surface)

    # Optional: draw floating balloons
    for balloon in start_balloons:
        balloon.update()
        balloon.draw(surface)

    overlay = pygame.Surface((main_screen.width, main_screen.height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # semi-transparent dark
    surface.blit(overlay, (0, 0))

    font = pygame.font.SysFont("Impact", 72)
    text = font.render("Tap to Start", True, (255, 255, 255))
    text_rect = text.get_rect(center=(main_screen.width//2, main_screen.height//2))
    surface.blit(text, text_rect)

start_screen_active = True
fade_out_timer = None
fade_duration = 1.0  # seconds for the fade out effect
fade_alpha = 100  # Fully opaque to begin with
game_started = False

start_balloons = [Balloon() for _ in range(4)]

# Game Over screen
fade_overlay = pygame.Surface((main_screen.width, main_screen.height))
fade_overlay.fill((0, 0, 0))
fade_alpha = 0
game_over_y = -100  # Start off-screen
game_over_target_y = SCREEN_HEIGHT // 2 - 80
# Fade overlay
dim_overlay = pygame.Surface((main_screen.width, main_screen.height))
dim_overlay.fill((0, 0, 0))
dim_overlay.set_alpha(fade_alpha)  # Range from 0 to ~180
screen.blit(background_image, (0, 0))  # Draw game background
screen.blit(dim_overlay, (0, 0))       # Apply fade

def ease_out_bounce(t):
    n1 = 7.5625
    d1 = 2.75
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375
    
game_over_start_time = None

def draw_glow_text(surface, text, font, x, y, color):
    base = font.render(text, True, color)
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        glow = font.render(text, True, (100, 100, 100))
        glow.set_alpha(120)
        surface.blit(glow, (x + dx, y + dy))
    surface.blit(base, (x, y))

# Main loop
while running:
   
    # Check for tap to begin game
    if start_screen_active:
        draw_start_screen(screen)
        pygame.display.flip()

        # Process events JUST to check for tap
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                start_screen_active = False
                game_started = True
                start_time = pygame.time.get_ticks()
        continue

    if not game_over:

        # Add new balloons if needed
        if len(balloons) == 0:
            balloons.append(Balloon())
    
    # Update and draw balloons
    for balloon in balloons:
        balloon.update()    
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    time_left = max(0, GAME_DURATION - int(elapsed_time))
    if elapsed_time >= GAME_DURATION and not game_over:
        game_over = True
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif game_over:
                if event.key == pygame.K_r:
                    score = 0
                    start_time = pygame.time.get_ticks()
                    game_over = False
                    start_screen_active = True
                    fade_alpha = 0
                    game_over_y = -100
                    game_over_start_time = None
                    for b in balloons:
                        b.reset()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            current_time = time.time()
            if current_time - last_click_time >= 0.5:
                mx, my = event.pos
                point = np.float32([[[mx, my]]])
                clicked = False
                for balloon in balloons[:]:
                    if balloon.is_clicked((mx, my)):
                        balloon.popped = True
                        if pop_sound:
                            pop_sound.play()
                        cracks.append(CrackEffect(mx, my))
                        balloons.remove(balloon)
                        score += 1
                        score_popups.append(ScorePopup(mx, my))
                        clicked = True
                        break
                last_click_time = current_time
            if not clicked:
                misses.append(MissEffect(mx, my))
                miss_sound.play()
    # Render screen
    screen.blit(background_image, (0, 0))

    # Clouds
    for cloud in clouds:
        cloud.update()
        cloud.draw(screen)

    if not game_over:
        overlay = get_day_night_overlay(elapsed_time, GAME_DURATION)
        screen.blit(overlay, (0, 0))
        
        # Draw sparkles
        if elapsed_time > GAME_DURATION * 0.5:
            # Calculate how much time has passed since fade-in started
            fade_duration = GAME_DURATION * 0.5  # Remaining time after 60%
            fade_elapsed = elapsed_time - (GAME_DURATION * 0.5)

            # Compute alpha (0 to 255) based on progress
            fade_alpha = int(min(255, (fade_elapsed / fade_duration) * 255))

            # Apply the alpha to a copy of the sparkle image
            sparkle_fade = sparkle_img.copy()
            sparkle_fade.set_alpha(fade_alpha)

            # Blit with fading
            screen.blit(sparkle_fade, (0, 0))

        for balloon in balloons:
            balloon.draw(screen)
        cracks = [c for c in cracks if c.draw(screen)]
        score_popups = [s for s in score_popups if s.draw(screen)]
        misses = [m for m in misses if m.draw(screen)]
        timer_text = FONT.render(f"Time Left: {time_left}s", True, (0,0,0))
        score_text = FONT.render(f"Score: {score}", True, (0,0,0))
        draw_text_with_bg(screen, timer_text, 20, 20)
        draw_text_with_bg(screen, score_text, 20, 100)

    # Game over handling
    else:
        if game_over_start_time is None:
            game_over_start_time = pygame.time.get_ticks()

        # Draw background consistent with start screen
        screen.blit(background_image, (0, 0))
        
        # Draw clouds
        for cloud in clouds:
            cloud.update()
            cloud.draw(screen)

        # Draw floating balloons (same as start screen)
        for balloon in start_balloons:
            balloon.update()  # Use normal update, not slow-motion
            balloon.draw(screen)

        # Apply semi-transparent overlay (same as start screen)
        overlay = pygame.Surface((main_screen.width, main_screen.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Match start screen's overlay
        screen.blit(overlay, (0, 0))

        # Animate "Game Over" drop
        elapsed_drop = (pygame.time.get_ticks() - game_over_start_time) / 1000
        drop_duration = 2  # seconds
        t = min(1, elapsed_drop / drop_duration)
        eased_y = int(ease_out_bounce(t) * (game_over_target_y + 80))

        # Define fonts for hierarchy
        title_font = pygame.font.SysFont("Impact", 80)  # Larger for "Game Over!"
        score_font = pygame.font.SysFont("Impact", 60)  # Slightly smaller for score
        message_font = pygame.font.SysFont("Impact", 48)  # Smaller for messages

        # Calculate total text block height
        text_lines = [
            ("Oops!!! The time is up.", message_font, YELLOW),
            ("Game Over!", title_font, RED),
            (f"Your Final Score: {score}", score_font, WHITE),
            ("Press R to restart", message_font, GREEN),
            ("TRY AGAIN!!!", message_font, WHITE)
        ]
        line_spacing = 50  # Consistent spacing between lines
        total_height = sum(font.size(text)[1] for text, font, _ in text_lines) + line_spacing * (len(text_lines) - 1)
        start_y = main_screen.height // 2 - total_height // 2 + eased_y - game_over_target_y  # Center the block around eased_y

        # Optional: Draw semi-transparent background box
        max_width = max(font.size(text)[0] for text, font, _ in text_lines)
        box_padding = 20
        box_rect = pygame.Rect(
            main_screen.width // 2 - max_width // 2 - box_padding,
            main_screen.height // 2 - total_height // 2 - box_padding,
            max_width + 2 * box_padding,
            total_height + 2 * box_padding
        )
        pygame.draw.rect(screen, (0, 0, 0, 20), box_rect, border_radius=10)

        # Draw text lines
        current_y = start_y
        for text, font, color in text_lines:
            draw_glow_text(screen, text, font,
                        main_screen.width // 2 - font.size(text)[0] // 2,
                        current_y - 80, color)
            current_y += font.size(text)[1] + line_spacing

    pygame.display.flip()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
        pygame.quit()
        exit()
    

# Cleanup
pygame.quit()
sys.exit()