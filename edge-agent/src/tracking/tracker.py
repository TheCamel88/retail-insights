"""DeepSORT wrapper — assigns persistent IDs across frames."""
from deep_sort_realtime.deepsort_tracker import DeepSort
from detection.detector import Detection


class Track:
    def __init__(self, track_id: str, bbox, confidence: float):
        self.track_id   = track_id
        self.bbox       = bbox
        self.confidence = confidence


class PersonTracker:
    def __init__(self, max_age: int = 30):
        self.tracker = DeepSort(max_age=max_age)

    def update(self, detections: list[Detection]) -> list[Track]:
        raw = [[d.bbox, d.confidence, "person"] for d in detections]
        tracked = self.tracker.update_tracks(raw, frame=None)
        tracks = []
        for t in tracked:
            if t.is_confirmed():
                tracks.append(Track(str(t.track_id), t.to_ltrb(), t.det_conf or 1.0))
        return tracks
