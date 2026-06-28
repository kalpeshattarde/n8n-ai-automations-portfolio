# RevOps Database

Local PostgreSQL setup for the RevOps Real Integration Mode.

```powershell
cd project_01_ai_revops_automation/database
docker compose up -d
```

This starts PostgreSQL on host port `5433` with project-owned CRM, approval, and error tables.

