from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EnvVar:
    key: str
    value: str
    comment: Optional[str] = None
    line_number: int = 0


@dataclass
class EnvFile:
    path: Path
    vars: dict = field(default_factory=dict)

    @classmethod
    def load(cls, path) -> "EnvFile":
        p = Path(path)
        env = cls(path=p)
        current_comment = []
        for i, line in enumerate(p.read_text().splitlines(), 1):
            stripped = line.strip()
            if not stripped:
                current_comment = []
                continue
            if stripped.startswith("#"):
                current_comment.append(stripped[1:].strip())
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            env.vars[key] = EnvVar(
                key=key, value=value,
                comment=" ".join(current_comment) if current_comment else None,
                line_number=i,
            )
            current_comment = []
        return env

    @staticmethod
    def diff(a: "EnvFile", b: "EnvFile") -> list:
        result = []
        keys_a, keys_b = set(a.vars), set(b.vars)
        for key in sorted(keys_a - keys_b):
            result.append(f"+ {key} (only in {a.path.name})")
        for key in sorted(keys_b - keys_a):
            result.append(f"- {key} (only in {b.path.name})")
        for key in sorted(keys_a & keys_b):
            va, vb = a.vars[key].value, b.vars[key].value
            if va != vb:
                result.append(f"~ {key}  {a.path.name}={va}  {b.path.name}={vb}")
        return result

    def to_dict(self) -> dict:
        return {k: v.value for k, v in self.vars.items()}
