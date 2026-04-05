from sqlalchemy import String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
from datetime import datetime
import uuid


class ZoneEvent(Base):
    __tablename__ = "zone_events"
    id:        Mapped[str]      = mapped_column(String, primary_key=True,
                                                default=lambda: str(uuid.uuid4()))
    store_id:  Mapped[str]      = mapped_column(String, index=True)
    camera_id: Mapped[str]      = mapped_column(String)
    zone_id:   Mapped[str]      = mapped_column(String, index=True)
    zone_name: Mapped[str]      = mapped_column(String)
    track_id:  Mapped[str]      = mapped_column(String)
    direction: Mapped[str]      = mapped_column(String)   # enter | exit
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)


class DwellEvent(Base):
    __tablename__ = "dwell_events"
    id:             Mapped[str]      = mapped_column(String, primary_key=True,
                                                     default=lambda: str(uuid.uuid4()))
    store_id:       Mapped[str]      = mapped_column(String, index=True)
    camera_id:      Mapped[str]      = mapped_column(String)
    zone_id:        Mapped[str]      = mapped_column(String, index=True)
    zone_name:      Mapped[str]      = mapped_column(String)
    track_id:       Mapped[str]      = mapped_column(String)
    dwell_seconds:  Mapped[float]    = mapped_column(Float)
    timestamp:      Mapped[datetime] = mapped_column(DateTime, index=True)


class HeatmapFrame(Base):
    __tablename__ = "heatmap_frames"
    id:          Mapped[str]      = mapped_column(String, primary_key=True,
                                                  default=lambda: str(uuid.uuid4()))
    store_id:    Mapped[str]      = mapped_column(String, index=True)
    camera_id:   Mapped[str]      = mapped_column(String)
    timestamp:   Mapped[datetime] = mapped_column(DateTime, index=True)
    grid_width:  Mapped[int]      = mapped_column()
    grid_height: Mapped[int]      = mapped_column()
    grid_data:   Mapped[list]     = mapped_column(JSON)
