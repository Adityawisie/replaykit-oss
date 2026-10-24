from __future__ import annotations
import json
from .schemas import ReportExportRequest, RunRecord, Experiment, ComparisonResult, AIAnalysis, VerificationResult
from .security import redact_text


def build_report(experiment: Experiment, runs: list[RunRecord], comparison: ComparisonResult | None = None, analysis: AIAnalysis | None = None, verification: VerificationResult | None = None) -> dict:
    payload = {"product": "ReplayKit OSS", "experiment": experiment.model_dump(mode="json"), "runs": [r.model_dump(mode="json") for r in runs], "comparison": comparison.model_dump(mode="json") if comparison else None, "ai_analysis": analysis.model_dump(mode="json") if analysis else None, "verification": verification.model_dump(mode="json") if verification else None, "notes": ["AI analysis is advisory.", "Captured evidence does not prove causation."]}
    return payload

def markdown_report(payload: dict) -> str:
    exp = payload["experiment"]
    lines = [f"# ReplayKit Evidence: {exp['name']}", "", exp.get("description", ""), "", "## Runs"]
    for run in payload["runs"]:
        lines += [f"### Run `{run['id']}` — {run['status']}", f"- Command: `{run['command']}`", f"- Exit code: `{run.get('exit_code')}`", f"- Duration: {run['duration_ms']} ms", f"- Commit: `{run.get('git_commit') or 'unavailable'}`", "", "#### stderr", "```text", run.get("stderr", "")[:12000], "```", "", "#### stdout", "```text", run.get("stdout", "")[:12000], "```", ""]
    if payload.get("comparison"):
        c = payload["comparison"]; lines += ["## Comparison", f"- Result: **{c['status'].upper()}**", c["summary"], *[f"- {d}" for d in c["differences"]], ""]
    if payload.get("ai_analysis"):
        a = payload["ai_analysis"]; lines += ["## AI Analysis (advisory)", a["error_summary"], "", "### Likely causes", *[f"- {x}" for x in a["likely_causes"]], "", "### Evidence", *[f"- {x}" for x in a["evidence"]], ""]
    if payload.get("verification"):
        v = payload["verification"]; lines += ["## Fix Verification", f"- Status: **{v['status'].upper()}**", v["summary"], *[f"- {x}" for x in v["checks"]], ""]
    lines += ["## Limitations", *[f"- {x}" for x in payload["notes"]]]
    text = "\n".join(lines)
    return redact_text(text)[0]
