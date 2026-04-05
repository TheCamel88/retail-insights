"""RTSP stream reader — yields decoded frames asynchronously."""
import cv2, asyncio
from typing import AsyncIterator
import numpy as np


class RTSPCapture:
    def __init__(self, rtsp_url: str, sample_fps: int = 5):
        self.rtsp_url   = rtsp_url
        self.sample_fps = sample_fps   # process N frames/sec (not all frames)

    async def stream_frames(self) -> AsyncIterator[np.ndarray]:
        cap = cv2.VideoCapture(self.rtsp_url)
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open stream: {self.rtsp_url}")

        native_fps = cap.get(cv2.CAP_PROP_FPS) or 25
        skip = max(1, int(native_fps / self.sample_fps))
        frame_idx = 0

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    await asyncio.sleep(1)   # reconnect pause
                    cap = cv2.VideoCapture(self.rtsp_url)
                    continue
                if frame_idx % skip == 0:
                    yield frame
                frame_idx += 1
                await asyncio.sleep(0)       # yield control
        finally:
            cap.release()
