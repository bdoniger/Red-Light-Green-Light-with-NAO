from ultralytics import YOLO
import cv2
from collections import defaultdict
import numpy as np
from cap_from_youtube import cap_from_youtube
from scipy import signal
# Load the YOLOv8 model
model = YOLO("yolov8m.pt")

# Open youtube video
link = "https://www.youtube.com/watch?v=bwJ-TNu0hGM&ab_channel=GKorb "
cap = cap_from_youtube(link, "720p")
track_history = defaultdict(lambda: [])
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    if success:
        # Run YOLOv8 inference on the frame
        results = model.track(frame,persist=True) 
        # Visualize the results on the frame
        # Get the boxes and track IDs
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()

        annotated_frame = results[0].plot()
        # Display the annotated frame
        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box
            track = track_history[track_id]
            track.append((float(x), float(y)))  # x, y center point
            if len(track) > 90:  # retain 90 tracks for 90 frames
                track.pop(0)

            # Draw the tracking lines
            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(
                annotated_frame,
                [points],
                isClosed=False,
                color=(230, 230, 230),
                thickness=10,
            )

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()