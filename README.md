# Retail Insights Platform

A hybrid edge-cloud retail analytics platform that connects to in-store camera systems
and delivers customer behavior insights via a web dashboard.

## Architecture

```
[Store Cameras] → RTSP
      ↓
[Edge Agent]         ← Python + YOLOv8 + DeepSORT (runs on-prem)
  - Person detection
  - Zone tracking
  - Dwell time events
      ↓ MQTT/HTTPS
[Cloud Backend]      ← Python + FastAPI + PostgreSQL + Redis
  - Event aggregation
  - Heatmap computation
  - AI recommendations
      ↓
[Web Dashboard]      ← React + Recharts
  - Per-store analytics
  - Real-time + historical views
  - Store management
```

## Modules

| Module | Description |
|--------|-------------|
| `edge-agent/` | On-premise agent: RTSP capture, CV processing, event upload |
| `backend/` | Cloud API: event ingestion, analytics, auth, multi-tenancy |
| `dashboard/` | React frontend: dashboards, heatmaps, recommendations |
| `shared/` | Shared event schemas and protocols |
| `infra/` | Docker Compose, Kubernetes configs |
| `docs/` | Architecture docs, API reference, deployment guides |

## Quick Start

See `docs/quickstart.md` for setup instructions.
# retail-insights
# retail-insights
