from datetime import timedelta
from app.schemas import RunRecord, utc_now
from app.compare import compare_runs
from app.security import redact_text
from app.prompts import build_fix_prompt


def make_run(**changes):
    now = utc_now()
    base = dict(id="run-a", experiment_id="exp-a", command=["python", "-c", "print('ok')"], working_directory=".", started_at=now, finished_at=now+timedelta(milliseconds=10), duration_ms=10, status="passed", exit_code=0, stdout="ok\n", stderr="", timed_out=False, git_commit="abc", git_branch="main", git_dirty=False, platform="test-platform", python_version="3.12", notes="", redactions_applied=0)
    base.update(changes)
    return RunRecord(**base)


def test_compare_same_captured_evidence():
    a = make_run(); b = make_run(id="run-b")
    result = compare_runs(a, b)
    assert result.status == "same"
    assert result.differences == []


def test_compare_detects_differences():
    a = make_run(); b = make_run(id="run-b", status="failed", exit_code=1, stderr="boom")
    result = compare_runs(a, b)
    assert result.status == "different"
    assert any("Exit codes differ" in d for d in result.differences)


def test_timeout_is_inconclusive():
    a = make_run(); b = make_run(id="run-b", status="timed_out", timed_out=True)
    assert compare_runs(a, b).status == "inconclusive"


def test_redacts_common_secret_patterns():
    result, count = redact_text("API_KEY=secret123456789 and Bearer abcdefghijklmnop")
    assert "secret123456789" not in result
    assert "abcdefghijklmnop" not in result
    assert count >= 2


def test_fix_prompt_includes_evidence_and_safe_instructions():
    run = make_run(status="failed", exit_code=1, stderr="TypeError at app.py:42")
    prompt = build_fix_prompt(run, None, "generic")
    assert "app.py:42" in prompt.prompt
    assert "Avoid unrelated refactoring" in prompt.prompt
    assert "Do not claim the bug is fixed" in prompt.prompt
