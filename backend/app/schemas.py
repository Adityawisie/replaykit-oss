from __future__ import annotations
from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, Field, field_validator

RunStatus = Literal["passed", "failed", "timed_out", "not_started"]
ComparisonStatus = Literal["same", "different", "inconclusive"]
VerificationStatus = Literal["verified", "not_fixed", "regression_detected", "inconclusive"]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ExperimentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    description: str = Field(default="", max_length=4000)
    reproduction_steps: str = Field(default="", max_length=8000)
    working_directory: str = Field(default="", max_length=2000)


class Experiment(ExperimentCreate):
    id: str
    created_at: datetime
    updated_at: datetime


class RunCreate(BaseModel):
    experiment_id: str
    command: list[str] = Field(min_length=1, max_length=80, description="Executable and arguments; never a shell command string")
    working_directory: str = Field(min_length=1, max_length=2000)
    timeout_seconds: int = Field(default=30, ge=1, le=300)
    approved: bool = False
    notes: str = Field(default="", max_length=4000)
    @field_validator("command")
    @classmethod
    def command_args_are_nonempty(cls, value: list[str]) -> list[str]:
        if not value or not value[0].strip():
            raise ValueError("command[0] must name an executable")
        if any("\x00" in arg for arg in value):
            raise ValueError("Command arguments cannot contain NUL characters")
        return value


class RunRecord(BaseModel):
    id: str
    experiment_id: str
    command: list[str]
    working_directory: str
    started_at: datetime
    finished_at: datetime
    duration_ms: int
    status: RunStatus
    exit_code: int | None = None
    stdout: str = ""
    stderr: str = ""
    timed_out: bool = False
    git_commit: str | None = None
    git_branch: str | None = None
    git_dirty: bool | None = None
    platform: str
    python_version: str
    notes: str = ""
    redactions_applied: int = 0


class ComparisonResult(BaseModel):
    id: str
    experiment_id: str
    run_a_id: str
    run_b_id: str
    status: ComparisonStatus
    summary: str
    differences: list[str]
    created_at: datetime


class AnalysisRequest(BaseModel):
    run_id: str
    source_context: str = Field(default="", max_length=24000)
    include_source_context: bool = False


class AIAnalysis(BaseModel):
    id: str
    run_id: str
    provider: str
    model: str
    error_summary: str
    likely_causes: list[str]
    evidence: list[str]
    suggested_investigations: list[str]
    source_locations: list[str]
    confidence: Literal["low", "medium", "high"]
    limitations: list[str]
    created_at: datetime


class FixPromptRequest(BaseModel):
    run_id: str
    analysis_id: str | None = None
    target: Literal["generic", "codex", "claude_code", "cursor"] = "generic"
    additional_constraints: str = Field(default="", max_length=4000)


class FixPrompt(BaseModel):
    id: str
    run_id: str
    target: str
    prompt: str
    created_at: datetime


class CompareRequest(BaseModel):
    run_a_id: str
    run_b_id: str


class VerificationRequest(BaseModel):
    original_run_id: str
    after_run_id: str
    regression_run_ids: list[str] = Field(default_factory=list, max_length=30)


class VerificationResult(BaseModel):
    id: str
    original_run_id: str
    after_run_id: str
    status: VerificationStatus
    summary: str
    checks: list[str]
    created_at: datetime


class ReportExportRequest(BaseModel):
    experiment_id: str
    run_ids: list[str] = Field(default_factory=list, max_length=100)
    comparison_id: str | None = None
    analysis_id: str | None = None
    verification_id: str | None = None
