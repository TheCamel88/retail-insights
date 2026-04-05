from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.insight import Insight
from app.services.recommendations import generate_insight
from datetime import datetime

router = APIRouter()


@router.post("/{store_id}/generate")
async def create_recommendation(
    store_id: str,
    db: AsyncSession = Depends(get_db),
):
    start = datetime(2026, 4, 4, 0, 0, 0)
    end = datetime(2026, 4, 4, 23, 59, 59)
    result = await generate_insight(store_id, start, end, db)
    return result


@router.get("/{store_id}/latest")
async def get_latest(
    store_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Insight)
        .where(Insight.store_id == store_id)
        .order_by(Insight.created_at.desc())
        .limit(1)
    )
    insight = result.scalar_one_or_none()
    if not insight:
        return {"summary": None}
    return {"id": insight.id, "summary": insight.summary, "created_at": insight.created_at.isoformat()}
