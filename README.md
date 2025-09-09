# Model Runner Dashboard

An end-to-end full-stack dashboard that allows internal users to:
- Select a model
- Submit input parameters
- Trigger a model run
- Monitor execution progress
- View results and metrics in a clean UI

This project was built as part of the **SODA Full-Stack Take-Home Challenge**.

---

## Features

### Frontend (React + TypeScript + Vite)
- Model selection dropdown
- Run form with inputs (e.g., region, year, parameter set)
- Trigger run & live progress updates
- Results table with summary metrics
- Error handling surfaced in-UI

### Backend (FastAPI)
- `GET /api/models` → List available models
- `POST /api/runs` → Submit run request
- `GET /api/runs/{run_id}/status` → Track status
- `GET /api/runs/{run_id}/results` → Fetch tabular results + summary
- Async simulation of model execution
- SQLite persistence for run metadata & results
- OpenAPI/Swagger docs available at `/docs`

---

## Tech Stack

- **Frontend:** React, TypeScript, Vite, TailwindCSS  
- **Backend:** FastAPI (Python 3.11)  
- **Database:** SQLite (lightweight local persistence)  
- **Containerization:** Docker + Docker Compose  
- **CI/CD:** GitHub Actions  

---

## Project Structure

```bash
model-runner-dashboard-soda/
├── frontend/        # React + TS UI
├── backend/         # FastAPI backend
│   ├── api/         # Endpoints
│   ├── models/      # DB models
│   └── data/        # SQLite db (ignored in git)
├── docker-compose.yml
├── .github/workflows/ci-cd.yml
└── README.md
```

---

## Getting Started

### Prerequisites

- **Node.js 20+**
- **Python 3.11+**
- **Docker** (optional, for containerized run)

---

### Run Locally

#### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 5173
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit: [http://localhost:5173](http://localhost:5173)

---

### Run with Docker

```bash
docker compose up --build
```

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:5173](http://localhost:5173)

---

## Bonus: Design & Extensions

### CI/CD & Deployment
- GitHub Actions pipeline for build, test, and deployment
- Environment promotion strategy (dev → test → prod) with separate configs
- Deployable to Azure App Service + Azure Container Registry

### Databricks & Unity Catalog Integration (Design)
- Backend could read training/inference data directly from Unity Catalog
- Trigger long-running jobs via Databricks Jobs API
- Store outputs in Delta tables; dashboard reads processed results

---

## Database Schema

- **models** → available models
- **runs** → run metadata
- **run_results** → tabular outputs
- Extendable to support users / projects

---

## AuthN/AuthZ

- Plan to integrate MSAL (Azure AD) for login/logout
- Secure API access per user/project scope

---

## API Docs

Once backend is running, interactive API docs available at:  
[http://localhost:5173/docs](http://localhost:5173/docs)

---

## Deliverables

- GitHub repository (this repo)
- Ready for live demo and technical presentation
