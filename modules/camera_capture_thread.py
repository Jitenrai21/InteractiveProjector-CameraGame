import cv2
import threading
import time
# Camera capture thread
class CameraCaptureThread(threading.Thread):
    def __init__(self, camera_index, frame_queue):
        threading.Thread.__init__(self)
        self.camera_index = camera_index
        self.frame_queue = frame_queue
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            exit(1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # Push the frame to the queue
                self.frame_queue.put(frame)
            time.sleep(0.01)  # Prevent the thread from using too much CPU

    def stop(self):
        self.running = False
        self.cap.release()