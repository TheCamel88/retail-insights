from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import cv2
import io

router = APIRouter()

def generate_frames():
    cap = cv2.VideoCapture(0)  # 0 = webcam, swap for RTSP URL later
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    cap.release()

@router.get("/feed")
def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
