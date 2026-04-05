# Quick Start Guide

## Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

## 1. Start Cloud Services

```bash
cd infra/docker
docker-compose up -d
```

## 2. Run Database Migrations

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
```

## 3. Start Backend

```bash
uvicorn app.main:app --reload
# API at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

## 4. Start Dashboard

```bash
cd dashboard
npm install && npm run dev
# Dashboard at http://localhost:3000
```

## 5. Configure Edge Agent

```bash
cd edge-agent
pip install -r requirements.txt
cp config/example.env config/.env
cp config/cameras.example.json config/cameras.json
# Edit .env with your store credentials
# Edit cameras.json with your camera RTSP URLs and zone polygons
python src/main.py
```

## Privacy Notes

- Raw video **never leaves the store**. Only structured events are sent to the cloud.
- All data in the cloud is scoped to an `organization_id` (multi-tenant).

## Next Steps

- See `docs/architecture.md` for the full system design
- See `docs/api-reference.md` for endpoint documentation
