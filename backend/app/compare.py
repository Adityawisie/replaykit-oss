from __future__ import annotations
import uuid
from .schemas import ComparisonResult, RunRecord, utc_now


def compare_runs(a: RunRecord, b: RunRecord) -> ComparisonResult:
    differences: list[str] = []
    if a.command != b.command: differences.append("Commands or arguments differ")
    if a.working_directory != b.working_directory: differences.append("Working directories differ")
    if a.exit_code != b.exit_code: differences.append(f"Exit codes differ ({a.exit_code} vs {b.exit_code})")
    if a.status != b.status: differences.append(f"Run statuses differ ({a.status} vs {b.status})")
    if a.stdout != b.stdout: differences.append("Standard output differs")
    if a.stderr != b.stderr: differences.append("Standard error differs")
    if a.platform != b.platform: differences.append("Operating-system/platform metadata differs")
    if a.python_version != b.python_version: differences.append("Python versions differ")
    if a.git_commit != b.git_commit: differences.append("Git commits differ or are unavailable")
    if a.timed_out or b.timed_out or a.status == "not_started" or b.status == "not_started":
        status = "inconclusive"
        summary = "At least one run timed out or did not start; output differences may not fully describe the behavior."
    elif differences:
        status = "different"; summary = f"The runs differ in {len(differences)} recorded field(s). This does not prove which change caused the difference."
    else:
        status = "same"; summary = "The captured fields match. This does not prove the applications are equivalent in all conditions."
    return ComparisonResult(id=str(uuid.uuid4()), experiment_id=a.experiment_id, run_a_id=a.id, run_b_id=b.id, status=status, summary=summary, differences=differences, created_at=utc_now())
