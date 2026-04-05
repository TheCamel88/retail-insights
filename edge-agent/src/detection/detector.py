"""YOLOv8 person detector."""
from ultralytics import YOLO
import numpy as np


class Detection:
    def __init__(self, bbox, confidence, track_id=None):
        self.bbox       = bbox         # [x1, y1, x2, y2] normalised
        self.confidence = confidence
        self.track_id   = track_id


class PersonDetector:
    PERSON_CLASS = 0   # COCO class index for "person"

    def __init__(self, model_path: str = "yolov8n.pt", confidence: float = 0.4):
        self.model      = YOLO(model_path)
        self.confidence = confidence

    def detect(self, frame: np.ndarray) -> list[Detection]:
        h, w = frame.shape[:2]
        results = self.model(frame, classes=[self.PERSON_CLASS],
                             conf=self.confidence, verbose=False)[0]
        detections = []
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            detections.append(Detection(
                bbox=[x1/w, y1/h, x2/w, y2/h],
                confidence=float(box.conf[0]),
            ))
        return detections
