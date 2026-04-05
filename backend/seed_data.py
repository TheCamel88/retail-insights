import asyncio
import httpx
from datetime import datetime, timedelta
import random

BASE = "http://localhost:8000"
STORE = "store_001"
ZONES = [
    ("zone_entrance", "Entrance"),
    ("zone_display_a", "Display A"),
    ("zone_display_b", "Display B"),
    ("zone_checkout", "Checkout"),
]

async def seed():
    async with httpx.AsyncClient(timeout=30) as client:
        total = 0
        for day in range(7):
            date = datetime.now() - timedelta(days=day)
            visits = random.randint(20, 80)
            for visit in range(visits):
                hour = random.randint(9, 20)
                minute = random.randint(0, 59)
                ts = date.replace(hour=hour, minute=minute, second=0).strftime("%Y-%m-%dT%H:%M:%S")
                zone_id, zone_name = random.choice(ZONES)
                track_id = f"person_{day}_{visit}"
                events = [
                    {"event_type": "zone_crossed", "store_id": STORE,
                     "camera_id": "cam_main", "zone_id": zone_id,
                     "zone_name": zone_name, "track_id": track_id,
                     "direction": "enter", "timestamp": ts},
                    {"event_type": "dwell", "store_id": STORE,
                     "camera_id": "cam_main", "zone_id": zone_id,
                     "zone_name": zone_name, "track_id": track_id,
                     "dwell_seconds": random.uniform(10, 300),
                     "timestamp": ts}
                ]
                r = await client.post(f"{BASE}/ingest/events",
                    json=events, headers={"X-API-Key": "test-key"})
                total += 1
        print(f"Seeded {total} visits across 7 days!")

asyncio.run(seed())
