import numpy as np
import cv2
from mss import mss
from ultralytics import YOLO
import time

# Load YOLO model
model = YOLO('best.pt')


with mss() as sct:
    monitor = sct.monitors[1]  # your primary monitor
    screen_width = monitor["width"]
    screen_height = monitor["height"]

    # Define capture region: only the left half
    left_half = {
        "top": monitor["top"],
        "left": monitor["left"],
        "width": screen_width // 2,
        "height": screen_height
    }

    
    while True:
        # Capture only the left half
        screenshot = sct.grab(left_half)

        # Convert screenshot to BGR
        frame = np.array(screenshot, dtype=np.uint8)[:, :, :3]

        # Perform YOLO inference
        results = model(frame, verbose=False)

        # Draw bounding boxes
        annotated_frame = results[0].plot()

        # Show the frame
        cv2.imshow("YOLOv8 Left Screen Detection", annotated_frame)

        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
