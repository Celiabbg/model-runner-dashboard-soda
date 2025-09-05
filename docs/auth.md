# AuthN/AuthZ (MSAL / Azure AD) Plan

- **Frontend**: MSAL Browser handles login; we gate the app (optional) behind Azure AD. Configure `VITE_AAD_CLIENT_ID` and `VITE_AAD_TENANT_ID`. Obtain an ID token and call backend with `Authorization: Bearer ...` (future work).
- **Backend**: Protect `/api/*` by validating JWTs issued by Microsoft identity platform (via `pyjwt` or `msal` middlewares). For MVP, endpoints are open; add a JWT dependency for production.
- **Scopes & RBAC**: Use Entra ID app roles (`reader`, `runner`, `admin`); map `roles` claim to API authorization.
- **Data scoping**: Filter accessible models/runs by user role and (optional) project/team claims.