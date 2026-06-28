# DataOps n8n Credentials

Required n8n credentials:

- `Postgres - Portfolio`
- `Gmail - Portfolio`
- `OpenRouter - Portfolio` as HTTP header auth
- Optional `Power BI - Service Principal` if using REST refresh

Import order:

1. `workflows/global_error_handler.json`
2. `workflows/n8n_project_workflow.json`
