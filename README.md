# Model Runner Dashboard

An end-to-end full-stack dashboard that allows internal users to:
- Select a model
- Submit input parameters
- Trigger a model run
- Monitor execution progress
- View results and metrics in a clean UI

This project was built as part of the **SODA Full-Stack Take-Home Challenge**.

---

## 🚀 Features

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

## 🛠️ Tech Stack

- **Frontend:** React, TypeScript, Vite, TailwindCSS
- **Backend:** FastAPI (Python 3.11)
- **Database:** SQLite (lightweight local persistence)
- **Containerization:** Docker + Docker Compose
- **CI/CD:** GitHub Actions

---

## 📂 Project Structure
