import cv2
from ultralytics import YOLO
import httpx
from datetime import datetime, timezone

model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)
print("Detecting... press Ctrl+C to stop")
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_count += 1
    if frame_count % 15 != 0:
        continue
    results = model(frame, classes=[0], conf=0.4, verbose=False)[0]
    people = len(results.boxes)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    if people > 0:
        print(f"Detected {people} person(s) - sending...")
        event = [{
            "event_type": "zone_crossed",
            "store_id": "store_001",
            "camera_id": "cam_webcam",
            "zone_id": "zone_main",
            "zone_name": "Main Area",
            "track_id": "person_" + str(frame_count),
            "direction": "enter",
            "timestamp": now
        }]
        r = httpx.post(
            "http://localhost:8000/ingest/events",
            json=event,
            headers={"X-API-Key": "test-key"},
            timeout=5
        )
        print("  Response:", r.json())
    else:
        print("No people detected")

cap.release()
