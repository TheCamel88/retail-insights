from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.analytics import foot_traffic_by_hour, dwell_by_zone, aggregate_heatmap
from datetime import datetime

router = APIRouter()


@router.get("/{store_id}/traffic")
async def get_traffic(
    store_id: str,
    start: datetime = Query(...),
    end: datetime = Query(...),
    db: AsyncSession = Depends(get_db),
):
    data = await foot_traffic_by_hour(store_id, start, end, db)
    return {"store_id": store_id, "traffic": data}


@router.get("/{store_id}/dwell")
async def get_dwell(
    store_id: str,
    start: datetime = Query(...),
    end: datetime = Query(...),
    db: AsyncSession = Depends(get_db),
):
    data = await dwell_by_zone(store_id, start, end, db)
    return {"store_id": store_id, "dwell": data}


@router.get("/{store_id}/heatmap")
async def get_heatmap(
    store_id: str,
    start: datetime = Query(...),
    end: datetime = Query(...),
    db: AsyncSession = Depends(get_db),
):
    data = await aggregate_heatmap(store_id, start, end, db)
    return {"store_id": store_id, **data}
