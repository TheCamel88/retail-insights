"""
Ingestion service — persists raw edge events to the database.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.events import ZoneEvent, DwellEvent, HeatmapFrame
from datetime import datetime


async def ingest_events(events: list[dict], db: AsyncSession):
    for ev in events:
        ts = datetime.fromisoformat(ev["timestamp"])
        event_type = ev.get("event_type")

        if event_type == "zone_crossed":
            db.add(ZoneEvent(
                store_id=ev["store_id"], camera_id=ev["camera_id"],
                zone_id=ev["zone_id"], zone_name=ev["zone_name"],
                track_id=ev["track_id"], direction=ev["direction"], timestamp=ts,
            ))
        elif event_type == "dwell":
            db.add(DwellEvent(
                store_id=ev["store_id"], camera_id=ev["camera_id"],
                zone_id=ev["zone_id"], zone_name=ev["zone_name"],
                track_id=ev["track_id"], dwell_seconds=ev["dwell_seconds"], timestamp=ts,
            ))
        elif event_type == "heatmap_frame":
            db.add(HeatmapFrame(
                store_id=ev["store_id"], camera_id=ev["camera_id"], timestamp=ts,
                grid_width=ev["grid_width"], grid_height=ev["grid_height"],
                grid_data=ev["grid_data"],
            ))
    await db.commit()
