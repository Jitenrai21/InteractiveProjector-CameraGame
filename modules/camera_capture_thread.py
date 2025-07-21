import cv2
import threading
import queue
import time

class CameraCaptureThread(threading.Thread):
    def __init__(self, camera_index):
        super().__init__()
        self.camera_index = camera_index
        self.frame_queue = queue.Queue(maxsize=1)  # Moved queue creation here
        self.running = True
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise RuntimeError("Error: Could not open camera")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                try:
                    # Non-blocking put: replace old frame if queue is full
                    if self.frame_queue.full():
                        self.frame_queue.get_nowait()
                    self.frame_queue.put(frame, block=False)
                except queue.Full:
                    pass  # Queue is full, skip frame
            else:
                print("Warning: Failed to capture frame")
                time.sleep(0.1)  # Wait longer on failure to avoid spamming
            time.sleep(1/30)  # Target 30 FPS to match main loop
        self.cap.release()

    def stop(self):
        self.running = False