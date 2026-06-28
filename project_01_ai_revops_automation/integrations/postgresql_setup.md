# RevOps PostgreSQL Setup

The RevOps workflow stores scored leads, lead events, approval tasks, and workflow errors.

Local connection:

```text
postgresql://akcelerate_app:akcelerate_revops_password@localhost:5433/akcelerate_revops
```

Run:

```powershell
cd project_01_ai_revops_automation/database
docker compose up -d
```

Use parameterized Postgres nodes in production and keep raw lead payloads minimal.

