"""
Shared event schemas — edge agent → cloud backend.
All communication uses these Pydantic models so both sides
stay in sync without duplicating definitions.
"""
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime
import uuid


class BoundingBox(BaseModel):
    x: float        # normalised 0–1
    y: float
    width: float
    height: float


class PersonDetectedEvent(BaseModel):
    event_type: Literal["person_detected"] = "person_detected"
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    store_id: str
    camera_id: str
    timestamp: datetime
    track_id: str
    bounding_box: BoundingBox
    confidence: float


class ZoneCrossedEvent(BaseModel):
    event_type: Literal["zone_crossed"] = "zone_crossed"
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    store_id: str
    camera_id: str
    timestamp: datetime
    track_id: str
    zone_id: str
    zone_name: str
    direction: Literal["enter", "exit"]


class DwellEvent(BaseModel):
    event_type: Literal["dwell"] = "dwell"
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    store_id: str
    camera_id: str
    timestamp: datetime
    track_id: str
    zone_id: str
    zone_name: str
    dwell_seconds: float


class HeatmapFrameEvent(BaseModel):
    """Sampled position grid — sent every N seconds per camera."""
    event_type: Literal["heatmap_frame"] = "heatmap_frame"
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    store_id: str
    camera_id: str
    timestamp: datetime
    grid_width: int
    grid_height: int
    grid_data: list[list[float]]  # 2D array, values 0.0–1.0


AnyEvent = PersonDetectedEvent | ZoneCrossedEvent | DwellEvent | HeatmapFrameEvent
