"""
YOLO inference thread for real-time object detection.
Processes frames from camera thread and sends results to game state manager.
"""
import threading
import cv2
import numpy as np
import time
import logging
import sys
import os
from ultralytics import YOLO
from .threaded_game_state import ThreadSafeGameState

# Suppress YOLO logging
os.environ["YOLO_VERBOSE"] = "False"
logging.getLogger('ultralytics').setLevel(logging.CRITICAL)


class YOLOInferenceThread(threading.Thread):
    """
    Dedicated thread for YOLO model inference.
    Continuously processes frames and detects objects without blocking main game loop.
    """
    
    def __init__(self, model_path: str, game_state: ThreadSafeGameState, 
                 conf_threshold: float = 0.5, iou_threshold: float = 0.7,
                 transform_matrix=None, offset_x=0, offset_y=0):
        super().__init__(name="YOLOInference")
        self.daemon = True  # Dies when main thread dies
        
        self.game_state = game_state
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.transform_matrix = transform_matrix
        self.offset_x = offset_x
        self.offset_y = offset_y
        
        # Performance tracking
        self.frame_count = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        
        # Load YOLO model with suppressed output
        try:
            original_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')
            self.model = YOLO(model_path, task="detect", verbose=False)
            sys.stdout = original_stdout
            print(f"YOLO model loaded successfully: {model_path}")
        except Exception as e:
            print(f"Error loading YOLO model: {e}")
            raise
        
        # Compute inverse transform for coordinate mapping
        self.inv_transform_matrix = None
        if self.transform_matrix is not None:
            try:
                self.inv_transform_matrix = np.linalg.inv(self.transform_matrix)
            except np.linalg.LinAlgError:
                print("Warning: Could not compute inverse transform matrix")
        
        self.running = True
    
    def run(self):
        """Main inference loop"""
        print("YOLO inference thread started")
        
        while self.running and self.game_state.running:
            try:
                # Get latest frame from camera thread
                frame, frame_timestamp = self.game_state.get_current_frame(timeout=0.1)
                
                if frame is None:
                    time.sleep(0.01)  # Short sleep if no frame available
                    continue
                
                # Skip inference if game not started (performance optimization)
                if self.game_state.start_screen_active:
                    # Still check for start gestures
                    detections = self._run_inference(frame)
                    if detections:
                        # Trigger game start
                        self.game_state.start_screen_active = False
                        self.game_state.game_started = True
                        self.game_state.start_time = time.time()
                    time.sleep(0.05)  # Reduced frequency on start screen
                    continue
                
                # Skip if game is over
                if self.game_state.game_over:
                    time.sleep(0.1)
                    continue
                
                # Run YOLO inference
                detections = self._run_inference(frame)
                
                # Process detections and add to game state
                for detection in detections:
                    screen_x, screen_y = self._transform_coordinates(
                        detection['x'], detection['y']
                    )
                    
                    if self._is_valid_screen_position(screen_x, screen_y):
                        self.game_state.add_detection(
                            screen_x, screen_y, detection['confidence']
                        )
                
                # Update FPS counter
                self._update_fps()
                
            except Exception as e:
                print(f"Error in YOLO inference thread: {e}")
                time.sleep(0.1)  # Prevent tight error loop
        
        print("YOLO inference thread stopped")
    
    def _run_inference(self, frame):
        """Run YOLO inference on frame and return detections"""
        try:
            # Apply perspective transform if available
            if self.transform_matrix is not None:
                frame = cv2.warpPerspective(
                    frame, self.transform_matrix, 
                    (frame.shape[1], frame.shape[0])
                )
            
            # Run YOLO prediction
            results = self.model.predict(
                frame, 
                imgsz=640,
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                device="cpu",
                verbose=False
            )
            
            detections = []
            for result in results:
                if result.boxes:
                    for box in result.boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cx = (x1 + x2) / 2
                        cy = (y1 + y2) / 2
                        confidence = float(box.conf[0])
                        
                        detections.append({
                            'x': cx,
                            'y': cy,
                            'confidence': confidence,
                            'bbox': (x1, y1, x2, y2)
                        })
            
            return detections
            
        except Exception as e:
            print(f"Error running YOLO inference: {e}")
            return []
    
    def _transform_coordinates(self, x, y):
        """Transform detection coordinates to screen coordinates"""
        if self.inv_transform_matrix is not None:
            try:
                point = np.float32([[[x, y]]])
                warped_point = cv2.perspectiveTransform(point, self.inv_transform_matrix)[0][0]
                return int(warped_point[0]), int(warped_point[1])
            except Exception:
                pass
        
        # Fallback: use coordinates with offsets
        return int(x + self.offset_x), int(y + self.offset_y)
    
    def _is_valid_screen_position(self, x, y, margin=50):
        """Check if coordinates are within valid screen bounds"""
        # Get screen dimensions (you might want to pass this as parameter)
        screen_width = 1920  # Default, should be configurable
        screen_height = 1080
        
        return (-margin <= x <= screen_width + margin and 
                -margin <= y <= screen_height + margin)
    
    def _update_fps(self):
        """Update FPS calculation"""
        self.frame_count += 1
        current_time = time.time()
        
        if current_time - self.fps_start_time >= 1.0:  # Update every second
            self.current_fps = self.frame_count / (current_time - self.fps_start_time)
            self.game_state.update_fps(inference_fps=self.current_fps)
            
            # Reset counters
            self.frame_count = 0
            self.fps_start_time = current_time
    
    def stop(self):
        """Stop the inference thread"""
        self.running = False
    
    def get_debug_info(self):
        """Get debug information for monitoring"""
        return {
            'fps': self.current_fps,
            'running': self.running,
            'model_loaded': hasattr(self, 'model'),
            'transform_available': self.transform_matrix is not None
        }