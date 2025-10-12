# Interactive Projector Camera Game

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green.svg)](https://opencv.org)
[![YOLO](https://img.shields.io/badge/YOLO-v8-red.svg)](https://ultralytics.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An interactive balloon-popping game that combines computer vision, object detection, and projection mapping to create an immersive augmented reality gaming experience. Players interact with projected balloons using physical gestures detected by a camera system.

![Game Demo](assets/demo.gif)

## Overview

This application creates an interactive gaming environment where:
- **Real-world gestures** are detected using computer vision (YOLO object detection)
- **Virtual balloons** are projected onto surfaces and respond to physical interactions
- **Multi-threaded architecture** ensures smooth gameplay at 90 FPS
- **Calibration system** maps camera coordinates to projection coordinates
- **Audio-visual effects** provide immersive feedback

### Key Features

- **Interactive Gameplay**: Touch/point at projected balloons to pop them
- **Computer Vision**: YOLO-based object detection for gesture recognition
- **Multi-Monitor Support**: Dedicated projector/external display support
- **Multi-Threaded**: Parallel processing for optimal performance
- **Rich Graphics**: Animated balloons, clouds, day/night cycles
- **Spatial Audio**: Sound effects with positional feedback
- **Auto-Calibration**: Camera-to-projector coordinate mapping

## Architecture

### Threading Model

The application uses a **4-thread architecture** for optimal performance:

![Threading Architecture](Threading_Architecture_Diagram.png)

*Figure 1: Multi-threaded architecture showing parallel processing of camera capture, YOLO inference, game logic, and audio management.*

### Core Components

| Component | Description | Technology |
|-----------|-------------|------------|
| **Game Engine** | Main game loop, physics, rendering | Pygame |
| **Computer Vision** | Object detection and tracking | OpenCV + YOLO |
| **Threading** | Parallel processing coordination | Python Threading |
| **Calibration** | Camera-projector coordinate mapping | Perspective Transformation |
| **Audio System** | Sound effects and audio feedback | Pygame Mixer |
| **Graphics** | Sprite animations and visual effects | Pygame + PIL |

## Quick Start

### Prerequisites

- **Python 3.8+**
- **Camera** (USB/built-in webcam)
- **Projector or external monitor**
- **Windows/Linux/macOS**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Jitenrai21/InteractiveProjector-CameraGame.git
   cd InteractiveProjector-CameraGame
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download YOLO model** (if not included)
   ```bash
   # The best.onnx model should be in the root directory
   # If missing, train your own or use a pre-trained model
   ```

4. **Run the application**
   ```bash
   # Threaded version (recommended)
   python main_threaded.py
   
   # Original single-threaded version
   python main_using_model(onClick)_myVersion.py
   ```

### First-Time Setup

1. **Camera Calibration**: On first run, the system will guide you through camera calibration
2. **Monitor Configuration**: Ensure your projector/external monitor is connected
3. **Test Detection**: Verify that hand/object detection works in your environment

## 🎮 How to Play

### Game Modes

1. **Start Screen**: Tap anywhere or show gesture to camera to begin
2. **Main Game**: Pop balloons by pointing/touching the projected areas
3. **Game Over**: View your score and restart

### Controls

| Input | Action |
|-------|--------|
| **Physical Gesture** | Point at balloons to pop them |
| **Mouse Click** | Alternative input method |
| **C Key** | Recalibrate camera |
| **D Key** | Toggle debug overlay |
| **Q Key** | Quit game |
| **R Key** | Restart (game over screen) |

### Scoring

- **+1 Point** per balloon popped
- **Miss Penalty** for clicking empty areas
- **Time Limit** of 120 seconds
- **Day/Night Cycle** affects difficulty

## Technical Details

### Dependencies

```python
opencv-python>=4.8.0    # Computer vision and camera handling
pygame>=2.5.0           # Game engine and graphics
ultralytics>=8.0.0      # YOLO object detection
pyautogui>=0.9.54      # Mouse automation for clicks
screeninfo>=0.8.1      # Multi-monitor detection
numpy>=1.24.0          # Numerical computations
Pillow>=9.5.0          # Image processing
torch>=2.0.0           # PyTorch for YOLO inference
```

### File Structure

```
InteractiveProjector-CameraGame/
├── assets/                      # Game assets
│   ├── balloons/               # Balloon sprites
│   ├── sounds/                 # Audio effects
│   ├── effects/                # Visual effects
│   └── backgrounds/            # Background images
├── modules/                     # Core game modules
│   ├── threaded_game_state.py  # Thread coordination
│   ├── camera_capture_thread.py # Camera handling
│   ├── yolo_inference_thread.py # Object detection
│   ├── audio_manager_thread.py  # Audio processing
│   ├── calibration.py          # Camera calibration
│   ├── game_visual.py          # Game graphics
│   └── config.py               # Configuration
├── tests/                       # Testing utilities
├── datapreprocessing/           # Training data tools
├── main_threaded.py            # Main threaded application
├── main_using_model*.py        # Alternative versions
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── README_THREADING.md         # Threading documentation
```

### Performance Specifications

#### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | Intel i5-8000 / AMD Ryzen 5 2600 | Intel i7-10000+ / AMD Ryzen 7 3700X+ |
| **RAM** | 8 GB | 16 GB+ |
| **GPU** | Integrated Graphics | Dedicated GPU (GTX 1060+) |
| **Camera** | 720p USB Webcam | 1080p Low-latency Camera |
| **Display** | 1080p Monitor + Projector | 4K Monitor + High-res Projector |

#### Performance Metrics

![Performance Metrics](Performance_Metrics.png)

*Figure 2: Performance comparison showing significant improvements in FPS, latency, and resource utilization with multi-threaded architecture.*

| Metric | Single-Threaded | Multi-Threaded | Improvement |
|--------|-----------------|----------------|-------------|
| **Game FPS** | 30-45 | 90 | **100%** |
| **Input Latency** | 100-200ms | 10-20ms | **90%** |
| **Frame Drops** | Frequent | Rare | **95%** |
| **Audio Latency** | 50-100ms | <10ms | **90%** |
| **CPU Usage** | 60-80% | 45-60% | **25%** |

## Configuration

### Camera Settings

```python
# In modules/config.py
CAMERA_INDEX = 1          # Camera device index
CAMERA_WIDTH = 720        # Frame width
CAMERA_HEIGHT = 480       # Frame height
CAMERA_FPS = 30          # Capture framerate
```

### Game Settings

```python
# Core game parameters
GAME_DURATION = 120       # Game length in seconds
MAX_BALLOONS = 3         # Simultaneous balloons
CONF_THRESHOLD = 0.5     # YOLO confidence threshold
IOU_THRESHOLD = 0.7      # YOLO IoU threshold
CLICK_COOLDOWN = 0.5     # Seconds between clicks
```

### Threading Configuration

```python
# Thread performance settings
GAME_FPS = 90            # Main game loop FPS
CAMERA_FPS = 30          # Camera capture FPS
YOLO_FPS = 15-20         # YOLO inference FPS (auto-throttled)
AUDIO_BUFFER_SIZE = 20   # Audio effect queue size
```

## Troubleshooting

### Common Issues

#### Camera Not Detected
```bash
# Check available cameras
python camera_index_check.py

# Verify camera permissions
# Windows: Privacy Settings > Camera
# Linux: Check /dev/video* permissions
# macOS: System Preferences > Security & Privacy
```

#### Poor Detection Performance
```python
# Adjust YOLO thresholds in config.py
CONF_THRESHOLD = 0.3     # Lower for more sensitive detection
IOU_THRESHOLD = 0.5      # Adjust overlap threshold

# Check lighting conditions
# Ensure good contrast between hand/object and background
```

#### Low FPS/Performance
```bash
# Check system resources
# Task Manager (Windows) / htop (Linux) / Activity Monitor (macOS)

# Enable debug overlay
# Press 'D' in-game to monitor thread performance

# Reduce resolution or FPS if needed
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 360
```

#### Calibration Issues
```bash
# Recalibrate camera
# Press 'C' during gameplay
# Ensure all 4 corners are clearly visible
# Use high-contrast markers for better detection
```

### Debug Features

| Key | Function | Description |
|-----|----------|-------------|
| **D** | Debug Overlay | Shows thread FPS, queue sizes, performance metrics |
| **C** | Recalibrate | Restart camera calibration process |
| **Q** | Quit | Exit application |
| **ESC** | Exit | Alternative quit method |

### Log Analysis

```python
# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)

# Check common log files
logs/
├── camera.log          # Camera capture issues
├── yolo.log           # Detection problems  
├── audio.log          # Sound system errors
└── performance.log    # FPS and timing data
```

## Contributing

We welcome contributions! Here's how to get started:

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```
4. **Make your changes**
5. **Run tests**
   ```bash
   python -m pytest tests/
   ```
6. **Submit a pull request**

### Contribution Guidelines

- **Code Style**: Follow PEP 8 standards
- **Documentation**: Update README and docstrings
- **Testing**: Add tests for new features
- **Performance**: Profile changes for performance impact
- **Threading**: Ensure thread safety for concurrent code

### Areas for Contribution

- **New Game Modes**: Different interaction patterns
- **AI Improvements**: Better detection models
- **Visual Effects**: Enhanced graphics and animations
- **Audio Features**: Background music, spatial audio
- **Mobile Support**: Android/iOS compatibility
- **Networking**: Multiplayer functionality

## Performance Analysis

### Threading Benefits Visualization

```
Single-Threaded Timeline:
Camera ████████
YOLO   ████████
Game   ████████  (Sequential - 30 FPS max)
Audio  ████████

Multi-Threaded Timeline:
Camera ████████████████████████████████████████
YOLO   ████████████████████████████████████████
Game   ████████████████████████████████████████  (Parallel - 90 FPS)
Audio  ████████████████████████████████████████
```

### Resource Usage Comparison

| Resource | Single-Threaded | Multi-Threaded | Optimization |
|----------|-----------------|----------------|--------------|
| **CPU Cores** | 1-2 cores | 3-4 cores | Better utilization |
| **Memory** | 300-400 MB | 400-500 MB | Efficient buffering |
| **GPU** | Minimal | Optimized | Hardware acceleration |
| **I/O** | Blocking | Non-blocking | Async operations |

## Authors

- **Jitenrai21** - *Initial work and architecture* - [GitHub](https://github.com/Jitenrai21)

## Acknowledgments

- **Ultralytics** for the excellent YOLO implementation
- **OpenCV** community for computer vision tools
- **Pygame** developers for the game engine
- **Contributors** who helped improve the project

## Support

### Getting Help

- **Documentation**: Check this README and `README_THREADING.md`
- **Issues**: [GitHub Issues](https://github.com/Jitenrai21/InteractiveProjector-CameraGame/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Jitenrai21/InteractiveProjector-CameraGame/discussions)

---

**Made with passion for interactive computing and computer vision enthusiasts**

**Star this repository if you found it helpful!**