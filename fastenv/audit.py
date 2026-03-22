"""Audit trail for .env file changes — track who changed what and when."""
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass
class AuditEntry:
    timestamp: str
    file: str
    key: str
    action: str  # "added" | "removed" | "changed"
    old_hash: str | None
    new_hash: str | None


def _hash_value(value: str) -> str:
    """One-way hash of a value for audit trail (never store plaintext)."""
    return hashlib.sha256(value.encode()).hexdigest()[:16]


class EnvAuditor:
    """Tracks changes to .env files and writes an audit trail.

    Usage::

        auditor = EnvAuditor(audit_file=".env.audit.jsonl")
        auditor.record_changes(before=old_env, after=new_env, file=".env")
    """

    def __init__(self, audit_file: str = ".env.audit.jsonl") -> None:
        self._path = Path(audit_file)

    def record_changes(
        self,
        before: dict[str, str],
        after: dict[str, str],
        file: str = ".env",
    ) -> list[AuditEntry]:
        entries = []
        all_keys = set(before) | set(after)
        for key in sorted(all_keys):
            old = before.get(key)
            new = after.get(key)
            if old is None and new is not None:
                action = "added"
            elif old is not None and new is None:
                action = "removed"
            elif old != new:
                action = "changed"
            else:
                continue
            entry = AuditEntry(
                timestamp=datetime.now(UTC).isoformat(),
                file=file, key=key, action=action,
                old_hash=_hash_value(old) if old else None,
                new_hash=_hash_value(new) if new else None,
            )
            entries.append(entry)

        if entries:
            with self._path.open("a") as f:
                for e in entries:
                    f.write(json.dumps(e.__dict__) + "\n")
        return entries
