# Model Runner Dashboard (SODA Take‑Home)

This repo implements the **MVP** plus **all bonus design deliverables** for the SODA Full‑Stack Take‑Home Challenge.

## What’s included
- **Frontend (React + TypeScript + Vite)**: model selection → run form → trigger & progress → results + errors.
- **Backend (FastAPI + SQLite/SQLAlchemy)**: `/api/models`, `/api/runs` (submit), `/api/runs/{id}/status`, `/api/runs/{id}/results`. Simulated async run with persisted results.
- **API docs**: automatic (FastAPI `/docs`) + `docs/api.md`.
- **Bonus design** (docs + stubs):
  - CI/CD with GitHub Actions + **environment promotion** (dev → test → prod), **config separation**.
  - **Azure** deployment strategy (Web Apps for Containers or AKS) and secret layouts.
  - **Databricks & Unity Catalog** integration design; Jobs trigger & run tracking stubs.
  - **Database schema & data layer** ERD.
  - **AuthN/AuthZ** with **MSAL (Azure AD)** plan. Frontend includes an optional MSAL login gate (can be off by default).

## Quick start (local)
```bash
# 1) Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# 2) Frontend (in another shell)
cd frontend
npm ci
npm run dev
# visit http://localhost:5173
```

### Docker Compose
```bash
docker compose up --build
# backend: http://localhost:8000
# frontend: http://localhost:5173
```

> If a container name conflict occurs, run: `docker compose down --remove-orphans` and retry.

## Configuration
- Frontend reads `VITE_API_BASE` (defaults to `http://localhost:8000`).
- Backend reads `APP_ENV` (`dev|test|prod`), `DATABASE_URL` (defaults to `sqlite:///./data/app.db`).

## Folders
- `frontend/` React app (+ optional MSAL login gate)
- `backend/` FastAPI app with SQLite persistence
- `docs/` All bonus design docs (CI/CD, Azure, Databricks, ERD, Auth, API, architecture diagram)
- `infrastructure/` K8s manifests + Azure sample (Container Apps)
- `.github/workflows/ci-cd.yml` multi-env pipeline

## License
MIT