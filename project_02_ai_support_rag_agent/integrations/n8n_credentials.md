# Support n8n Credentials

Required n8n credentials:

- `Gmail - Portfolio`
- `Postgres - Portfolio`
- `OpenRouter - Portfolio` as HTTP header auth

Import order:

1. `workflows/global_error_handler.json`
2. `workflows/n8n_project_workflow.json`

Attach the global error handler before activating Gmail polling.
