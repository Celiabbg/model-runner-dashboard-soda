# Model Runner Dashboard — **API Reference**

A minimal REST API to submit model runs, track progress, and fetch results.
Designed for the SODA Full‑Stack Take‑Home Challenge (MVP + production‑minded details).

---

## Overview

- **Base URL**: `http://localhost:8000`
- **Media Type**: `application/json; charset=utf-8`
- **Auth**: _None_ for MVP (production: Bearer JWT via Azure AD/MSAL)
- **OpenAPI/Docs** (FastAPI default):
  - Swagger UI: `/docs`
  - ReDoc: `/redoc`
  - JSON: `/openapi.json`
- **CORS**: Allow localhost frontend during MVP

---

## Data Models (Pydantic)

### `Model`
```json
{ "id": "linear_reg", "name": "Linear Regression", "params": { "alpha": [0.1, 1.0, 10.0] } }
```

### `RunCreate` (request to create a run)
| Field     | Type               | Required | Notes                         |
|-----------|--------------------|----------|-------------------------------|
| model_id  | string             | ✅        | Must exist in `/api/models`   |
| inputs    | object (dict)      | ✅        | Free-form params for the run  |

### `RunStatus`
| Field    | Type    | Notes                                              |
|----------|---------|----------------------------------------------------|
| run_id   | string  | UUID or unique string                              |
| status   | string  | One of: `queued` · `running` · `succeeded` · `failed` |
| progress | integer | 0..100                                             |
| message  | string? | Optional human-readable status                      |

### `RunResults`
| Field    | Type                | Notes                                     |
|----------|---------------------|-------------------------------------------|
| run_id   | string              |                                           |
| summary  | object (dict)       | e.g., `{ "rows": 20, "avg_value": 1234.56 }` |
| rows     | array<object>       | Tabular rows produced by the run          |

### `Error`
_All non-2xx responses SHOULD follow this shape in production_
```json
{ "error": "Human-readable message", "code": "STRING_CODE", "details": { } }
```

---

## Status & Execution Conventions

- **Lifecycle**: `queued → running → succeeded|failed`
- **Progress**: integer `0..100` (monotonic)
- **Polling**: client polls `/status` until `succeeded` (or `failed`)
- **Results availability**: only after `succeeded`
- **Timestamps** (optional in MVP): `started_at`, `updated_at` (ISO 8601, UTC)

---

## Endpoints

### 1) List Models
**GET** `/api/models` → `200 OK`

**Response**
```json
{
  "models": [
    { "id": "linear_reg", "name": "Linear Regression", "params": { "alpha": [0.1, 1.0, 10.0] } },
    { "id": "xgb_forecast", "name": "XGBoost Forecast", "params": { "max_depth": [3, 5, 7] } },
    { "id": "simulator", "name": "Monte Carlo Simulator", "params": { "trials": [100, 1000, 10000] } }
  ]
}
```

**Errors**
- `500` server error → Error schema

**cURL**
```bash
curl -s http://localhost:8000/api/models | jq
```

---

### 2) Submit Run
**POST** `/api/runs` → `201 Created`

**Request (RunCreate)**
```json
{
  "model_id": "linear_reg",
  "inputs": { "region": "NA", "year": 2024, "parameter_set": "baseline" }
}
```

**Response**
```json
{ "run_id": "uuid-1234", "status": "queued" }
```

**Notes**
- Validates `model_id` against `/api/models`
- Starts async worker; client should poll `/status`

**Errors**
- `400` invalid request body → Error schema
- `404` model not found → Error schema
- `500` server error → Error schema

**cURL**
```bash
curl -s -X POST http://localhost:8000/api/runs \
  -H 'Content-Type: application/json' \
  -d '{"model_id":"linear_reg","inputs":{"region":"NA","year":2024,"parameter_set":"baseline"}}'
```

---

### 3) Run Status
**GET** `/api/runs/{run_id}/status` → `200 OK`

**Response (RunStatus)**
```json
{
  "run_id": "uuid-1234",
  "status": "running",
  "progress": 30,
  "message": "Processing step 3/10",
  "started_at": "2025-09-05T12:34:56Z",
  "updated_at": "2025-09-05T12:35:10Z"
}
```

**Polling Guidance**
- MVP: poll every 1–2s
- Production: exponential backoff + jitter (e.g., 1s → 2s → 4s → 8s)

**Errors**
- `404` run not found → Error schema
- `500` server error → Error schema

**cURL**
```bash
curl -s http://localhost:8000/api/runs/uuid-1234/status | jq
```

---

### 4) Run Results
**GET** `/api/runs/{run_id}/results` → `200 OK` when ready

**Response (RunResults)**
```json
{
  "run_id": "uuid-1234",
  "summary": { "rows": 20, "avg_value": 1234.56 },
  "rows": [
    { "region": "NA", "year": 2024, "kpi": "revenue", "value": 4567.89 }
  ]
}
```

**Notes**
- Before completion, server may respond with:
  - `404 Not Found` (MVP simple path) **or**
  - `409 Conflict` (explicit “not ready” contract)
- Clients should rely on `/status` to know readiness

**Errors**
- `404` run or results not found/not ready → Error schema
- `500` server error → Error schema

**cURL**
```bash
curl -s http://localhost:8000/api/runs/uuid-1234/results | jq
```

---

## End‑to‑End Example (Shell)

```bash
# 1) List models
curl -s http://localhost:8000/api/models | jq

# 2) Submit a run
RUN_ID=$(curl -s -X POST http://localhost:8000/api/runs \
  -H 'Content-Type: application/json' \
  -d '{"model_id":"linear_reg","inputs":{"region":"NA","year":2024,"parameter_set":"baseline"}}' \
  | jq -r '.run_id')
echo "run_id=$RUN_ID"

# 3) Poll status until succeeded
until STATUS=$(curl -s http://localhost:8000/api/runs/$RUN_ID/status | jq -r '.status'); \
      [ "$STATUS" = "succeeded" ] || [ "$STATUS" = "failed" ]; do
  curl -s http://localhost:8000/api/runs/$RUN_ID/status | jq
  sleep 2
done

# 4) Fetch results (if succeeded)
curl -s http://localhost:8000/api/runs/$RUN_ID/results | jq
```

---

## HTTP Status Codes (Summary)

| Endpoint                      | 2xx              | 4xx                         | 5xx     |
|------------------------------|------------------|-----------------------------|---------|
| GET `/api/models`            | 200              | —                           | 500     |
| POST `/api/runs`             | 201              | 400 (bad body), 404 (model) | 500     |
| GET `/api/runs/{id}/status`  | 200              | 404 (unknown id)            | 500     |
| GET `/api/runs/{id}/results` | 200 (ready)      | 404/409 (not ready/unknown) | 500     |

---

## Versioning & Limits (Optional for MVP)

- **Versioning**: prefix future versions with `/v1`, `/v2` …
- **Rate limits**: e.g., `429 Too Many Requests` with `Retry-After`
- **Caching**: disable or set low TTL for `/status`; allow caching for `/models`

---

## Security (Roadmap)

- **Auth**: Azure AD (MSAL) → Bearer tokens/JWT validation in API
- **RBAC**: model-level ACLs; attribute-based filters (region/project)
- **Secrets**: store in Key Vault; rotate regularly
- **Audit**: add `submitted_by` and timestamps to runs

---

## Changelog

- **v0.1 (MVP)**: endpoints for models, runs, status, results; async simulation; SQLite; no auth.