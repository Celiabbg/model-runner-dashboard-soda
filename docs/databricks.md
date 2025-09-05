# Databricks & Unity Catalog Integration (Design)

## Reading data from UC
- Option A: **Databricks SQL Connector** from backend to query UC tables (read-only) for reference data or results.
- Option B: **Delta Sharing** for cross-platform reads.
- Option C: **Job output** written to **Delta tables** in UC; backend queries them by `run_id`.

## Trigger long runs
1. Backend calls **Databricks Jobs API 2.1** to start a job with params.
2. Save `run_id` ↔ `databricks_run_id` mapping.
3. Poll **runs/get** (or subscribe to webhooks) for status.
4. When finished, read artifacts (e.g., Delta table path or DBFS files) and cache a compact subset in our DB.

See `integrations/databricks/trigger_job.py` and `integrations/databricks/uc_reader_example.py` for stubs.