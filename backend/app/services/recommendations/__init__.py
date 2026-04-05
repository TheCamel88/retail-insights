from sqlalchemy.ext.asyncio import AsyncSession
from app.services.analytics import dwell_by_zone, foot_traffic_by_hour
from app.models.insight import Insight
from app.core.config import settings
from datetime import datetime
import anthropic


async def generate_insight(store_id: str, start: datetime, end: datetime, db: AsyncSession) -> dict:
    # Pull analytics data
    dwell = await dwell_by_zone(store_id, start, end, db)
    traffic = await foot_traffic_by_hour(store_id, start, end, db)

    # Build a summary for Claude
    dwell_summary = "\n".join([
        f"- {z['zone']}: {z['visits']} visits, avg dwell {z['avg_seconds']}s"
        for z in dwell
    ]) or "No dwell data available."

    traffic_summary = "\n".join([
        f"- {t['hour']}: {t['count']} visitors"
        for t in traffic
    ]) or "No traffic data available."

    prompt = f"""You are a retail analytics expert advising a boutique store owner.

Here is their store data for today:

ZONE DWELL TIMES:
{dwell_summary}

FOOT TRAFFIC BY HOUR:
{traffic_summary}

Based on this data, provide 3 specific, actionable recommendations to help this store owner improve customer engagement and sales. Be concise and practical. Format as a numbered list."""

    # Call Claude
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )
    summary = message.content[0].text

    # Save to database
    insight = Insight(
        store_id=store_id,
        period_start=start,
        period_end=end,
        summary=summary,
    )
    db.add(insight)
    await db.commit()
    await db.refresh(insight)

    return {"id": insight.id, "summary": summary, "created_at": insight.created_at.isoformat()}
