%% Mermaid: System Context
flowchart LR
  User[User (AAD)] -->|MSAL| FE[React App]
  FE -->|REST| BE[FastAPI API]
  BE --> DB[(SQLite / Postgres)]
  BE -.->|Optional| DAB[Databricks Jobs/UC]

  subgraph Azure
    FE
    BE
    DB
  end
