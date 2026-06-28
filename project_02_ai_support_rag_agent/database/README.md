# Support Database

Local PostgreSQL setup for the Support RAG Real Integration Mode.

```powershell
cd project_02_ai_support_rag_agent/database
docker compose up -d
```

This starts PostgreSQL on host port `5434` with ticket, KB, response, approval, and error tables.

