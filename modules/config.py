"""
Central configuration for the Interactive Projector Camera Game.
All tunable constants live here so behavior can be adjusted without
touching game, threading, or vision code.
"""
import os

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Target screen size used for calibration and coordinate mapping
SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 768

# Game loop
FPS = 90
GAME_DURATION = 120  # seconds
CLICK_COOLDOWN = 0.5  # seconds between clicks

# YOLO detection thresholds
CONF_THRESHOLD = 0.5
IOU_THRESHOLD = 0.7

# Camera
CAMERA_INDEX = 1
CAMERA_WIDTH = 720
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Assets
MODEL_PATH = os.path.join(MODELS_DIR, "best.onnx")
CALIBRATION_FILE = os.path.join(BASE_DIR, "calibration.json")
BALLOON_FILES = ["balloon1.png", "balloon2.png", "balloon3.png"]
CRACK_PATH = os.path.join(ASSETS_DIR, "boom1.png")
MISS_PATH = os.path.join(ASSETS_DIR, "miss.png")
BACKGROUND_IMAGE_PATH = os.path.join(ASSETS_DIR, "background.jpg")
POP_SOUND_PATH = os.path.join(ASSETS_DIR, "balloon-pop.mp3")
MISS_SOUND_PATH = os.path.join(ASSETS_DIR, "miss.mp3")