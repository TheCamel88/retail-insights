from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    store_id:       str
    api_key:        str
    backend_url:    str = "https://api.yourplatform.com"
    yolo_model_path: str = "models/yolov8n.pt"

    class Config:
        env_file = "config/.env"
