"""
Edge Agent — entry point.
Spawns one async pipeline per configured camera.
"""
import asyncio, logging, json
from capture.stream import RTSPCapture
from detection.detector import PersonDetector
from tracking.tracker import PersonTracker
from zones.zone_manager import ZoneManager
from uploader.event_uploader import EventUploader
from config.settings import Settings

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


async def camera_pipeline(cam: dict, settings: Settings):
    capture      = RTSPCapture(cam["rtsp_url"])
    detector     = PersonDetector(settings.yolo_model_path)
    tracker      = PersonTracker()
    zone_mgr     = ZoneManager(cam["zones"])
    uploader     = EventUploader(settings.backend_url, settings.store_id,
                                 cam["id"], settings.api_key)

    log.info(f"Pipeline started: {cam['id']}")
    async for frame in capture.stream_frames():
        detections = detector.detect(frame)
        tracks     = tracker.update(detections)
        events     = zone_mgr.process(tracks, frame)
        await uploader.send_events(events)


async def main():
    settings = Settings()
    cameras  = json.load(open("config/cameras.json"))
    await asyncio.gather(*[camera_pipeline(c, settings) for c in cameras])


if __name__ == "__main__":
    asyncio.run(main())
