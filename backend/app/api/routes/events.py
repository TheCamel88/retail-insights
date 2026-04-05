"""Event ingestion endpoint — called by edge agents."""
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.ingestion import ingest_events

router = APIRouter()


@router.post("/events")
async def receive_events(
    payload: list[dict],
    x_api_key: str = Header(...),
    db: AsyncSession = Depends(get_db),
):
    # TODO: validate API key → resolve store
    await ingest_events(payload, db)
    return {"accepted": len(payload)}
