# System Architecture

## Overview

```
[IP Cameras] ──RTSP──► [Edge Agent]
                              │
                        structured events
                        (HTTPS / batched)
                              │
                              ▼
                       [Cloud Backend]
                        FastAPI + PostgreSQL
                              │
                        ┌─────┴─────┐
                        │           │
                   analytics    AI insights
                   queries      (Claude API)
                        │           │
                        └─────┬─────┘
                              ▼
                       [Web Dashboard]
                           React
```

## Edge Agent

Runs on a small on-premise device (e.g. Raspberry Pi 5, Intel NUC, or any
Linux box) at the store.

- **Capture**: Connects to cameras via RTSP using OpenCV
- **Detection**: YOLOv8n (nano) — runs at ~15 FPS on CPU
- **Tracking**: DeepSORT assigns persistent IDs across frames
- **Zones**: Polygon-based entry/exit/dwell detection
- **Upload**: Batches events and POSTs to the cloud API every N events

## Cloud Backend

Python + FastAPI + PostgreSQL + Redis.

- **Ingestion**: Receives edge events, validates, persists to DB
- **Analytics**: Aggregates raw events into traffic counts, dwell times, heatmaps
- **Recommendations**: Periodic Claude API calls generate store-specific advice
- **Auth**: JWT-based, multi-tenant (one org → many stores)

## Dashboard

React SPA with Recharts visualisations.

- Foot traffic by hour
- Dwell time by zone
- 2D heatmap overlay
- AI-generated recommendations panel
- Multi-store management
