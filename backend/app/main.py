from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import events, analytics, stores, auth, recommendations, stream
from app.core.config import settings
from app.db.session import init_db

import app.models.organization
import app.models.store
import app.models.camera
import app.models.zone
import app.models.events
import app.models.insight
import app.models.user

app = FastAPI(title="Retail Insights API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(auth.router,            prefix="/auth",           tags=["Auth"])
app.include_router(stores.router,          prefix="/stores",         tags=["Stores"])
app.include_router(events.router,          prefix="/ingest",         tags=["Ingestion"])
app.include_router(analytics.router,       prefix="/analytics",      tags=["Analytics"])
app.include_router(stream.router,          prefix="/stream",          tags=["Stream"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])

@app.get("/health")
async def health():
    return {"status": "ok"}
