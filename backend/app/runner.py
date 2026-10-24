from __future__ import annotations
import os, platform, shutil, subprocess, sys, time, uuid
from datetime import datetime, timezone
from pathlib import Path
from .config import MAX_OUTPUT_CHARS
from .schemas import RunRecord
from .security import redact_text


def now(): return datetime.now(timezone.utc)

def git_metadata(cwd: Path) -> tuple[str | None, str | None, bool | None]:
    def git(args: list[str]) -> str | None:
        try:
            p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=2, shell=False)
            return p.stdout.strip() if p.returncode == 0 else None
        except (OSError, subprocess.SubprocessError): return None
    commit = git(["rev-parse", "HEAD"])
    branch = git(["branch", "--show-current"])
    status = git(["status", "--porcelain"])
    return commit, branch, (bool(status) if status is not None else None)


def execute_run(experiment_id: str, command: list[str], working_directory: str, timeout_seconds: int, notes: str = "") -> RunRecord:
    cwd = Path(working_directory).expanduser().resolve()
    if not cwd.exists() or not cwd.is_dir():
        raise ValueError("Working directory must be an existing directory")
    if not shutil.which(command[0]) and not (Path(command[0]).is_absolute() and Path(command[0]).exists()):
        started = now()
        message = f"Executable not found: {command[0]}"
        return RunRecord(id=str(uuid.uuid4()), experiment_id=experiment_id, command=command, working_directory=str(cwd), started_at=started, finished_at=now(), duration_ms=0, status="failed", exit_code=None, stdout="", stderr=message, platform=platform.platform(), python_version=sys.version.split()[0], notes=notes)
    started = now(); t0 = time.perf_counter(); timed_out = False; exit_code = None; out = ""; err = ""
    try:
        proc = subprocess.run(command, cwd=cwd, capture_output=True, text=True, errors="replace", timeout=timeout_seconds, shell=False, env=os.environ.copy())
        exit_code, out, err = proc.returncode, proc.stdout, proc.stderr
        status = "passed" if exit_code == 0 else "failed"
    except subprocess.TimeoutExpired as exc:
        timed_out = True; status = "timed_out"; exit_code = None
        out = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        err = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        err += f"\nReplayKit: command timed out after {timeout_seconds} seconds."
    except OSError as exc:
        status = "failed"; err = f"Could not start command: {exc}"
    duration_ms = int((time.perf_counter() - t0) * 1000)
    out = out[-MAX_OUTPUT_CHARS:]; err = err[-MAX_OUTPUT_CHARS:]
    out, red1 = redact_text(out); err, red2 = redact_text(err)
    commit, branch, dirty = git_metadata(cwd)
    return RunRecord(id=str(uuid.uuid4()), experiment_id=experiment_id, command=command, working_directory=str(cwd), started_at=started, finished_at=now(), duration_ms=duration_ms, status=status, exit_code=exit_code, stdout=out, stderr=err, timed_out=timed_out, git_commit=commit, git_branch=branch, git_dirty=dirty, platform=platform.platform(), python_version=sys.version.split()[0], notes=notes, redactions_applied=red1+red2)
