# API

Base URL: `http://localhost:8000`

## List Models
`GET /api/models` → `{ models: [{ id, name, params }] }`

## Submit Run
`POST /api/runs`
```json
{ "model_id": "linear_reg", "inputs": { "region":"NA", "year":2024, "parameter_set":"baseline" } }
```
→ `{ "run_id": "uuid" }`

## Run Status
`GET /api/runs/{run_id}/status`
```json
{ "run_id": "...", "status": "running|queued|succeeded|failed", "progress": 0..100, "message": "..." }
```

## Run Results
`GET /api/runs/{run_id}/results`
```json
{ "run_id": "...", "summary": { "rows": 20, "avg_value": 1234.56 }, "rows": [ { ... } ] }
```