from __future__ import annotations
import uuid
from .schemas import FixPrompt, RunRecord, AIAnalysis, utc_now

TARGET_NOTES = {
    "generic": "You are an AI coding assistant working in the user's repository.",
    "codex": "Work as a careful coding agent. Inspect the repository and relevant tests before making changes.",
    "claude_code": "Work as a careful coding agent. Inspect the repository and relevant tests before making changes.",
    "cursor": "Work as a careful coding assistant. Inspect the repository and relevant tests before making changes.",
}

def build_fix_prompt(run: RunRecord, analysis: AIAnalysis | None, target: str, constraints: str = "") -> FixPrompt:
    analysis_text = "No AI analysis supplied; independently inspect the evidence and do not assume a root cause."
    if analysis:
        analysis_text = (f"Error summary: {analysis.error_summary}\nLikely causes (hypotheses):\n- " + "\n- ".join(analysis.likely_causes or ["Not identified"]) + "\nEvidence:\n- " + "\n- ".join(analysis.evidence or ["None supplied"]) + "\nSuggested investigations:\n- " + "\n- ".join(analysis.suggested_investigations or ["Inspect the failing path"]))
    prompt = f"""{TARGET_NOTES[target]}

Task: investigate and minimally fix the failure captured by ReplayKit OSS.

Execution evidence:
- Command: {run.command!r}
- Working directory: {run.working_directory}
- Status: {run.status}
- Exit code: {run.exit_code}
- Git commit: {run.git_commit or 'unavailable'}
- stdout (redacted/truncated):\n```text\n{run.stdout[-8000:]}\n```
- stderr (redacted/truncated):\n```text\n{run.stderr[-8000:]}\n```

AI analysis (treat as hypotheses, not facts):
{analysis_text}

Instructions:
1. Inspect the actual files and trace the failure before editing.
2. Verify any referenced file and line; do not invent locations.
3. Identify the smallest justified change. Avoid unrelated refactoring.
4. Add or update a regression test that captures the reported failure.
5. Run the relevant test(s) and report actual command output and exit status.
6. Summarize changed files, reasoning, risks, and any remaining uncertainty.
7. Do not claim the bug is fixed unless the relevant verification actually passes.
8. Do not expose secrets or modify unrelated files.

Additional user constraints:
{constraints.strip() or 'None supplied.'}

Do not apply changes until the user reviews and approves your proposed plan."""
    return FixPrompt(id=str(uuid.uuid4()), run_id=run.id, target=target, prompt=prompt, created_at=utc_now())
