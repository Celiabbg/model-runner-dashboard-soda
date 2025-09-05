# CI/CD & Promotion

- **GitHub Actions**: `.github/workflows/ci-cd.yml`
- Stages: **build+test** → **deploy_dev** → **deploy_test** (approval) → **deploy_prod** (approval).
- **Config separation**: use `APP_ENV` and per-environment secrets (DB, ACR, Azure credentials). Frontend uses per-env `VITE_API_BASE`.
- **Artifacts**: Docker images pushed to GHCR (`ghcr.io/<org>/model-runner-frontend` / `model-runner-backend`), tagged by commit SHA and env.