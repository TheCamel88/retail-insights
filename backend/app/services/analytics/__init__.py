from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.events import ZoneEvent, DwellEvent, HeatmapFrame
from datetime import datetime


async def foot_traffic_by_hour(store_id: str, start: datetime, end: datetime, db: AsyncSession):
    result = await db.execute(
        select(
            func.date_trunc('hour', ZoneEvent.timestamp).label('hour'),
            func.count(func.distinct(ZoneEvent.track_id)).label('count')
        )
        .where(ZoneEvent.store_id == store_id)
        .where(ZoneEvent.direction == 'enter')
        .where(ZoneEvent.timestamp >= start)
        .where(ZoneEvent.timestamp <= end)
        .group_by('hour')
        .order_by('hour')
    )
    return [{"hour": row.hour.isoformat(), "count": row.count} for row in result]


async def dwell_by_zone(store_id: str, start: datetime, end: datetime, db: AsyncSession):
    result = await db.execute(
        select(
            DwellEvent.zone_name,
            func.avg(DwellEvent.dwell_seconds).label('avg_seconds'),
            func.count(DwellEvent.id).label('visits')
        )
        .where(DwellEvent.store_id == store_id)
        .where(DwellEvent.timestamp >= start)
        .where(DwellEvent.timestamp <= end)
        .group_by(DwellEvent.zone_name)
        .order_by(func.avg(DwellEvent.dwell_seconds).desc())
    )
    return [{"zone": row.zone_name, "avg_seconds": round(row.avg_seconds, 1), "visits": row.visits} for row in result]


async def aggregate_heatmap(store_id: str, start: datetime, end: datetime, db: AsyncSession):
    result = await db.execute(
        select(HeatmapFrame.grid_data)
        .where(HeatmapFrame.store_id == store_id)
        .where(HeatmapFrame.timestamp >= start)
        .where(HeatmapFrame.timestamp <= end)
    )
    frames = [row.grid_data for row in result]
    if not frames:
        return {"grid": [], "frames": 0}
    rows = len(frames[0])
    cols = len(frames[0][0])
    combined = [[0.0] * cols for _ in range(rows)]
    for frame in frames:
        for r in range(rows):
            for c in range(cols):
                combined[r][c] += frame[r][c]
    peak = max(max(row) for row in combined) or 1
    normalized = [[round(v / peak, 3) for v in row] for row in combined]
    return {"grid": normalized, "frames": len(frames)}
