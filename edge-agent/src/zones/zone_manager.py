"""
Zone manager — detects enter/exit/dwell events and builds heatmap frames.
Zones are defined as normalised polygons in cameras.json.
"""
import time
from dataclasses import dataclass, field
from typing import Any
import numpy as np

HEATMAP_SAMPLE_INTERVAL = 10   # seconds between heatmap uploads
HEATMAP_GRID = (20, 20)


@dataclass
class ZoneState:
    zone_id: str
    zone_name: str
    polygon: list[list[float]]
    active_tracks: dict[str, float] = field(default_factory=dict)  # track_id → enter_time


def point_in_polygon(px: float, py: float, polygon: list[list[float]]) -> bool:
    n = len(polygon)
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


class ZoneManager:
    def __init__(self, zones: list[dict]):
        self.zones = [ZoneState(z["id"], z["name"], z["polygon"]) for z in zones]
        self._heatmap_grid = np.zeros(HEATMAP_GRID)
        self._last_heatmap_flush = time.time()

    def process(self, tracks, frame) -> list[dict]:
        events = []
        now = time.time()
        track_ids_seen = {t.track_id for t in tracks}

        for track in tracks:
            cx = (track.bbox[0] + track.bbox[2]) / 2
            cy = (track.bbox[1] + track.bbox[3]) / 2
            # Accumulate heatmap
            gx = min(int(cx * HEATMAP_GRID[1]), HEATMAP_GRID[1] - 1)
            gy = min(int(cy * HEATMAP_GRID[0]), HEATMAP_GRID[0] - 1)
            self._heatmap_grid[gy][gx] += 1

            for zone in self.zones:
                inside = point_in_polygon(cx, cy, zone.polygon)
                if inside and track.track_id not in zone.active_tracks:
                    zone.active_tracks[track.track_id] = now
                    events.append({"type": "zone_crossed", "zone": zone,
                                   "track_id": track.track_id, "direction": "enter"})
                elif not inside and track.track_id in zone.active_tracks:
                    enter_time = zone.active_tracks.pop(track.track_id)
                    dwell = now - enter_time
                    events.append({"type": "zone_crossed", "zone": zone,
                                   "track_id": track.track_id, "direction": "exit"})
                    events.append({"type": "dwell", "zone": zone,
                                   "track_id": track.track_id, "dwell_seconds": dwell})

        # Flush lost tracks
        for zone in self.zones:
            lost = [tid for tid in zone.active_tracks if tid not in track_ids_seen]
            for tid in lost:
                enter_time = zone.active_tracks.pop(tid)
                events.append({"type": "dwell", "zone": zone,
                                "track_id": tid, "dwell_seconds": now - enter_time})

        # Periodic heatmap snapshot
        if now - self._last_heatmap_flush >= HEATMAP_SAMPLE_INTERVAL:
            peak = self._heatmap_grid.max() or 1
            events.append({"type": "heatmap_frame",
                            "grid": (self._heatmap_grid / peak).tolist()})
            self._heatmap_grid = np.zeros(HEATMAP_GRID)
            self._last_heatmap_flush = now

        return events
