from __future__ import annotations
import json, uuid
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from .config import OLLAMA_BASE_URL, OLLAMA_MODEL
from . import store
from .schemas import (ExperimentCreate, Experiment, RunCreate, RunRecord, CompareRequest, ComparisonResult,
    AnalysisRequest, AIAnalysis, FixPromptRequest, FixPrompt, VerificationRequest, VerificationResult,
    ReportExportRequest, utc_now)
from .runner import execute_run
from .compare import compare_runs
from .ai import analyze_run
from .prompts import build_fix_prompt
from .reports import build_report, markdown_report
from .security import redact_text

app = FastAPI(title="ReplayKit OSS API", version="0.1.0", description="Local-first experiment capture, AI failure analysis, fix prompts, and verification.")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=False, allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["*"])

@app.on_event("startup")
def startup(): store.init_db()

def item(table: str, item_id: str, what: str):
    data = store.get(table, item_id)
    if data is None: raise HTTPException(404, f"{what} not found")
    return data

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "replaykit-oss-api", "ai_provider": "ollama", "ai_model": OLLAMA_MODEL}

@app.get("/api/ai/status")
async def ai_status():
    import httpx
    try:
        async with httpx.AsyncClient(timeout=2.5) as client:
            r = await client.get(f"{OLLAMA_BASE_URL}/api/tags"); r.raise_for_status(); data = r.json()
        models = [m.get("name", "") for m in data.get("models", [])]
        return {"available": True, "base_url": OLLAMA_BASE_URL, "configured_model": OLLAMA_MODEL, "model_present": any(x == OLLAMA_MODEL or x.startswith(OLLAMA_MODEL + ":") for x in models), "models": models}
    except Exception as exc:
        return {"available": False, "base_url": OLLAMA_BASE_URL, "configured_model": OLLAMA_MODEL, "model_present": False, "message": "Ollama is not reachable. Start Ollama and pull the configured model.", "detail": str(exc)}

@app.post("/api/experiments", response_model=Experiment)
def create_experiment(body: ExperimentCreate):
    now = utc_now(); data = Experiment(id=str(uuid.uuid4()), **body.model_dump(), created_at=now, updated_at=now)
    store.put("experiments", data.id, data.model_dump(mode="json"), created_at=now.isoformat(), updated_at=now.isoformat())
    return data

@app.get("/api/experiments", response_model=list[Experiment])
def list_experiments(limit: int = Query(100, ge=1, le=500)):
    return store.list_items("experiments", limit)

@app.get("/api/experiments/{experiment_id}", response_model=Experiment)
def get_experiment(experiment_id: str): return item("experiments", experiment_id, "Experiment")

@app.get("/api/experiments/{experiment_id}/runs", response_model=list[RunRecord])
def list_runs(experiment_id: str, limit: int = Query(100, ge=1, le=500)):
    item("experiments", experiment_id, "Experiment")
    return store.list_items("runs", limit, experiment_id)

@app.post("/api/runs", response_model=RunRecord)
def create_run(body: RunCreate):
    if not body.approved:
        raise HTTPException(400, "Explicit approval is required before command execution")
    exp = item("experiments", body.experiment_id, "Experiment")
    try:
        record = execute_run(body.experiment_id, body.command, body.working_directory, body.timeout_seconds, body.notes or exp.get("reproduction_steps", ""))
    except ValueError as exc: raise HTTPException(400, str(exc)) from exc
    store.put("runs", record.id, record.model_dump(mode="json"), experiment_id=record.experiment_id, created_at=record.started_at.isoformat())
    return record

@app.get("/api/runs/{run_id}", response_model=RunRecord)
def get_run(run_id: str): return item("runs", run_id, "Run")

@app.post("/api/compare", response_model=ComparisonResult)
def compare(body: CompareRequest):
    a = RunRecord.model_validate(item("runs", body.run_a_id, "Run")); b = RunRecord.model_validate(item("runs", body.run_b_id, "Run"))
    if a.experiment_id != b.experiment_id: raise HTTPException(400, "Runs must belong to the same experiment")
    result = compare_runs(a, b)
    store.put("comparisons", result.id, result.model_dump(mode="json"), experiment_id=result.experiment_id, created_at=result.created_at.isoformat())
    return result

@app.get("/api/comparisons/{comparison_id}", response_model=ComparisonResult)
def get_comparison(comparison_id: str): return item("comparisons", comparison_id, "Comparison")

@app.post("/api/ai/analyze", response_model=AIAnalysis)
async def ai_analyze(body: AnalysisRequest):
    run = RunRecord.model_validate(item("runs", body.run_id, "Run"))
    if body.source_context and not body.include_source_context:
        raise HTTPException(400, "Set include_source_context=true to include source code in AI analysis")
    try: result = await analyze_run(run, body.source_context, body.include_source_context)
    except Exception as exc:
        raise HTTPException(502, f"AI analysis failed. Check Ollama availability and model configuration. Details: {exc}") from exc
    store.put("analyses", result.id, result.model_dump(mode="json"), run_id=result.run_id, created_at=result.created_at.isoformat())
    return result

@app.get("/api/ai/analyses/{analysis_id}", response_model=AIAnalysis)
def get_analysis(analysis_id: str): return item("analyses", analysis_id, "Analysis")

@app.post("/api/ai/fix-prompt", response_model=FixPrompt)
def fix_prompt(body: FixPromptRequest):
    run = RunRecord.model_validate(item("runs", body.run_id, "Run"))
    analysis = AIAnalysis.model_validate(item("analyses", body.analysis_id, "Analysis")) if body.analysis_id else None
    if analysis and analysis.run_id != run.id: raise HTTPException(400, "Analysis does not belong to the selected run")
    result = build_fix_prompt(run, analysis, body.target, body.additional_constraints)
    store.put("prompts", result.id, result.model_dump(mode="json"), run_id=result.run_id, created_at=result.created_at.isoformat())
    return result

@app.get("/api/ai/fix-prompts/{prompt_id}", response_model=FixPrompt)
def get_fix_prompt(prompt_id: str): return item("prompts", prompt_id, "Fix prompt")

@app.post("/api/verify", response_model=VerificationResult)
def verify(body: VerificationRequest):
    before = RunRecord.model_validate(item("runs", body.original_run_id, "Original run")); after = RunRecord.model_validate(item("runs", body.after_run_id, "After run"))
    if before.experiment_id != after.experiment_id: raise HTTPException(400, "Runs must belong to the same experiment")
    checks = []
    if before.status == "failed" and after.status == "passed":
        status = "verified"; checks.append("Original failing run failed and after-change run passed")
        summary = "The recorded after-change run passed while the original run failed. This verifies only the configured reproduction, not all possible behavior."
    elif after.status in {"failed", "timed_out"}:
        status = "not_fixed"; checks.append(f"After-change run status is {after.status}")
        summary = "The after-change run did not pass; the fix is not verified."
    else:
        status = "inconclusive"; checks.append("The before/after statuses do not establish a successful fix")
        summary = "The available run results are insufficient to verify the fix."
    for rid in body.regression_run_ids:
        rr = RunRecord.model_validate(item("runs", rid, "Regression run"))
        if rr.experiment_id != before.experiment_id: raise HTTPException(400, "All runs must belong to the same experiment")
        if rr.status in {"failed", "timed_out"}:
            status = "regression_detected"; checks.append(f"Regression run {rid} has status {rr.status}")
        else: checks.append(f"Regression run {rid} passed")
    result = VerificationResult(id=str(uuid.uuid4()), original_run_id=before.id, after_run_id=after.id, status=status, summary=summary, checks=checks, created_at=utc_now())
    store.put("verifications", result.id, result.model_dump(mode="json"), created_at=result.created_at.isoformat())
    return result

@app.get("/api/verifications/{verification_id}", response_model=VerificationResult)
def get_verification(verification_id: str): return item("verifications", verification_id, "Verification")

@app.post("/api/reports/export")
def export_report(body: ReportExportRequest, format: str = Query("json", pattern="^(json|markdown)$")):
    exp = Experiment.model_validate(item("experiments", body.experiment_id, "Experiment"))
    runs = [RunRecord.model_validate(item("runs", rid, "Run")) for rid in body.run_ids]
    if any(r.experiment_id != exp.id for r in runs): raise HTTPException(400, "All runs must belong to the selected experiment")
    comparison = ComparisonResult.model_validate(item("comparisons", body.comparison_id, "Comparison")) if body.comparison_id else None
    analysis = AIAnalysis.model_validate(item("analyses", body.analysis_id, "Analysis")) if body.analysis_id else None
    verification = VerificationResult.model_validate(item("verifications", body.verification_id, "Verification")) if body.verification_id else None
    payload = build_report(exp, runs, comparison, analysis, verification)
    if format == "markdown":
        return Response(markdown_report(payload), media_type="text/markdown; charset=utf-8", headers={"Content-Disposition": "attachment; filename=replaykit-evidence.md"})
    safe_json = redact_text(json.dumps(payload, indent=2, ensure_ascii=False))[0]
    return Response(safe_json, media_type="application/json", headers={"Content-Disposition": "attachment; filename=replaykit-evidence.json"})

@app.get("/api/experiments/{experiment_id}/summary")
def experiment_summary(experiment_id: str):
    exp = item("experiments", experiment_id, "Experiment")
    runs = store.list_items("runs", 500, experiment_id)
    return {"experiment": exp, "run_count": len(runs), "failed_count": sum(1 for r in runs if r["status"] in {"failed", "timed_out"}), "latest_run": runs[0] if runs else None}
