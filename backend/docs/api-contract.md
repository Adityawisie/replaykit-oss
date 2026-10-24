# API contract summary

- `GET /api/health`: service health and configured AI provider.
- `GET /api/ai/status`: checks whether Ollama responds and whether the configured model is present.
- `POST /api/experiments`, `GET /api/experiments`, `GET /api/experiments/{id}`: experiment management.
- `POST /api/runs`, `GET /api/runs/{id}`, `GET /api/experiments/{id}/runs`: approved execution and run retrieval.
- `POST /api/compare`, `GET /api/comparisons/{id}`: deterministic comparison.
- `POST /api/ai/analyze`, `GET /api/ai/analyses/{id}`: optional Ollama analysis.
- `POST /api/ai/fix-prompt`, `GET /api/ai/fix-prompts/{id}`: generated, copyable repair prompts.
- `POST /api/verify`, `GET /api/verifications/{id}`: before/after verification and optional regression runs.
- `POST /api/reports/export?format=json|markdown`: evidence export.

All endpoints use local SQLite. There is no user authentication; keep the API bound to localhost.
