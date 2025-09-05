# Azure Deployment (Where/How)

## Option A: Azure Web Apps for Containers (simple)
- Build/push images to GHCR.
- Create two Web Apps (frontend & backend) per environment.
- Configure settings:
  - Backend: `APP_ENV`, `DATABASE_URL`.
  - Frontend: `VITE_API_BASE` pointing to backend URL.
- Use Actions `azure/login` + `azure/webapps-deploy`.

## Option B: AKS (scalable)
- Use `infrastructure/k8s/*.yaml`.
- Create `Namespace` per env; set `Secret` (DB URL, AAD info).
- Use Actions `azure/aks-set-context` + `kubectl apply -f`.

## DNS/TLS
- Use Azure Front Door or App Gateway for TLS and WAF in front of frontend & backend ingresses.