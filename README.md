# ReplayKit OSS — integrated local application

ReplayKit OSS captures approved command runs, analyzes failures with a local Ollama model, generates fix prompts, compares run evidence, verifies before/after outcomes, and exports reports.

## Project structure

- `frontend/` — React + TypeScript + Vite + Tailwind UI, based on the supplied Stitch design direction.
- `backend/` — FastAPI backend, SQLite persistence, safe command runner, comparison, Ollama analysis, fix prompts, verification, reports, and tests.

## Requirements

- Python 3.11+
- Node.js 20+ and npm
- Ollama only for AI analysis (the core app works without it)

## Start the backend (Windows PowerShell)

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API docs: http://127.0.0.1:8000/docs

## Start the frontend (a second PowerShell window)

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Open http://127.0.0.1:5173

`frontend/.env` can set `VITE_API_BASE_URL` if the backend URL changes. Restart Vite after changing it.

## Enable local AI

Install and start Ollama, then pull the model configured by the backend:

```powershell
ollama pull gemma4:e4b

ReplayKit is configured to use **Gemma 4 E4B** (`gemma4:e4b`) to meet the Best Use of Gemma 4 hackathon requirement. You can confirm the model is installed with `ollama list`.
```

The default model and Ollama URL are in `backend/.env.example`. You can change `OLLAMA_MODEL` and `OLLAMA_BASE_URL` in `backend/.env`.

## Safety notes

- A run requires explicit confirmation in the UI and explicit `approved: true` in the API request.
- The backend executes argument arrays without shell interpretation. The UI's simple command field splits on whitespace; commands needing arguments with spaces should be entered via API until a structured argv editor is added.
- Run commands with the same permissions as your local user. Only run commands you trust.
- The API is intended for local development and has no authentication. Keep it bound to `127.0.0.1`.
- Review source context and logs for secrets before asking AI to analyze them. Ollama runs locally, but logs and reports may still contain sensitive data.
- Fix verification describes the selected reproduction evidence; it cannot prove a change is correct in all cases.

## Tests

From `backend/` with the virtual environment active:

```powershell
pytest
```

## Known MVP limitations

- The frontend connects to the existing FastAPI endpoints; no cloud provider is used.
- The UI presents the supplied Stitch design direction in a responsive custom layout, not a pixel-for-pixel rendering of the HTML exports.
- The comparison view shows captured output side-by-side; line-level diff rendering is a future enhancement.
- Git metadata depends on the runner's working directory being a Git repository.
