import pygame
import os

# Constants
SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 768
FPS = 90
CONF_THRESHOLD = 0.5
IOU_THRESHOLD = 0.7
CLICK_COOLDOWN = 0.5
MODEL_PATH = "best.onnx"
CRACK_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "boom1.png")
BACKGROUND_IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "background.jpg")
CALIBRATION_FILE = "calibration.json"
CAMERA_INDEX = 1  # Configurable camera index
BALLOON_FILES = ["balloon1.png", "balloon2.png", "balloon3.png"]
POP_SOUND_PATH = "balloon-pop.mp3"

# Main loop variables
cracks = []
misses = []
last_click_time = 0
running = True
show_debug_overlay = False
score = 0
GAME_DURATION = 120
start_time = pygame.time.get_ticks()
game_over = False
score_popups = []