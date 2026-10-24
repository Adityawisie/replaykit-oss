from __future__ import annotations
import re

# Deliberately conservative redaction of common credential patterns. This is not a guarantee
# that all secrets or personal information will be detected.
PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|password|passwd|secret)\s*[:=]\s*(['\"]?)[^\s,'\";]+"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/-]{12,}"),
    re.compile(r"(?i)AKIA[0-9A-Z]{16}"),
]

def redact_text(value: str) -> tuple[str, int]:
    count = 0
    result = value
    for pattern in PATTERNS:
        result, n = pattern.subn(lambda m: (m.group(1) + "=[REDACTED]") if pattern is PATTERNS[0] else "[REDACTED_SECRET]", result)
        count += n
    return result, count
