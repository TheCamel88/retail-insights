"""
Sends structured events to the cloud backend over HTTPS.
Batches events and retries on failure.
"""
import httpx, logging, asyncio
from datetime import datetime, timezone

log = logging.getLogger(__name__)
BATCH_SIZE  = 50
RETRY_DELAY = 5   # seconds


class EventUploader:
    def __init__(self, backend_url: str, store_id: str,
                 camera_id: str, api_key: str):
        self.url       = f"{backend_url}/ingest/events"
        self.store_id  = store_id
        self.camera_id = camera_id
        self.headers   = {"X-API-Key": api_key, "Content-Type": "application/json"}
        self._buffer: list[dict] = []

    async def send_events(self, raw_events: list[dict]):
        for ev in raw_events:
            self._buffer.append(self._to_payload(ev))
        if len(self._buffer) >= BATCH_SIZE:
            await self._flush()

    def _to_payload(self, ev: dict) -> dict:
        now = datetime.now(timezone.utc).isoformat()
        base = {"store_id": self.store_id, "camera_id": self.camera_id, "timestamp": now}
        if ev["type"] == "zone_crossed":
            return {**base, "event_type": "zone_crossed",
                    "track_id": ev["track_id"], "zone_id": ev["zone"].zone_id,
                    "zone_name": ev["zone"].zone_name, "direction": ev["direction"]}
        if ev["type"] == "dwell":
            return {**base, "event_type": "dwell",
                    "track_id": ev["track_id"], "zone_id": ev["zone"].zone_id,
                    "zone_name": ev["zone"].zone_name, "dwell_seconds": ev["dwell_seconds"]}
        if ev["type"] == "heatmap_frame":
            return {**base, "event_type": "heatmap_frame",
                    "grid_width": 20, "grid_height": 20, "grid_data": ev["grid"]}
        return {**base, **ev}

    async def _flush(self):
        batch, self._buffer = self._buffer[:], []
        for attempt in range(3):
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    r = await client.post(self.url, json=batch, headers=self.headers)
                    r.raise_for_status()
                return
            except Exception as e:
                log.warning(f"Upload failed (attempt {attempt+1}): {e}")
                await asyncio.sleep(RETRY_DELAY)
        log.error(f"Dropped {len(batch)} events after 3 retries")
