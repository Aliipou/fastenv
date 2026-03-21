"""Schema-based .env validation with rich error reporting."""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from fastenv.core import EnvFile


@dataclass
class FieldSpec:
    """Specification for a single environment variable."""
    name: str
    required: bool = True
    type: str = "string"          # string | int | float | bool | url | email
    default: Optional[str] = None
    pattern: Optional[str] = None  # Regex pattern
    description: str = ""

    def validate(self, value: Optional[str]) -> list[str]:
        """Validate a value against this spec. Returns list of error messages."""
        errors = []
        if value is None:
            if self.required and self.default is None:
                errors.append(f"{self.name}: required but not set")
            return errors

        if self.type == "int":
            try:
                int(value)
            except ValueError:
                errors.append(f"{self.name}: expected integer, got {value!r}")

        elif self.type == "float":
            try:
                float(value)
            except ValueError:
                errors.append(f"{self.name}: expected float, got {value!r}")

        elif self.type == "bool":
            if value.lower() not in ("true", "false", "1", "0", "yes", "no"):
                errors.append(f"{self.name}: expected bool (true/false/1/0), got {value!r}")

        elif self.type == "url":
            if not value.startswith(("http://", "https://")):
                errors.append(f"{self.name}: expected URL starting with http/https, got {value!r}")

        elif self.type == "email":
            if "@" not in value or "." not in value.split("@")[-1]:
                errors.append(f"{self.name}: expected valid email, got {value!r}")

        if self.pattern and not re.fullmatch(self.pattern, value):
            errors.append(f"{self.name}: does not match pattern {self.pattern!r}")

        return errors


@dataclass
class ValidationResult:
    """Result of validating an EnvFile against a schema."""
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return len(self.errors) == 0

    def __str__(self) -> str:
        lines = []
        for e in self.errors:
            lines.append(f"ERROR   {e}")
        for w in self.warnings:
            lines.append(f"WARNING {w}")
        if not lines:
            lines.append("OK  All variables valid.")
        return "\n".join(lines)


@dataclass
class EnvSchema:
    """Schema for validating .env files."""
    fields: dict[str, FieldSpec] = field(default_factory=dict)

    @classmethod
    def load(cls, path: str | Path) -> "EnvSchema":
        """Parse a .env.schema file into a schema object.

        Schema format (each field defined by comments above the key):

            # description: PostgreSQL connection string
            # type: url
            # required: true
            DATABASE_URL=

            # description: Number of worker processes
            # type: int
            # default: 4
            WORKERS=
        """
        schema = cls()
        current_meta: dict = {}

        for line in Path(path).read_text().splitlines():
            stripped = line.strip()

            if stripped.startswith("#"):
                comment = stripped[1:].strip()
                if ":" in comment:
                    key, _, value = comment.partition(":")
                    current_meta[key.strip().lower()] = value.strip()
                continue

            if "=" in line:
                name, _, default = line.partition("=")
                name = name.strip()
                schema.fields[name] = FieldSpec(
                    name=name,
                    required=current_meta.get("required", "true").lower() == "true",
                    type=current_meta.get("type", "string"),
                    default=default.strip() or current_meta.get("default"),
                    pattern=current_meta.get("pattern"),
                    description=current_meta.get("description", ""),
                )
                current_meta = {}

        return schema

    def validate(self, env: EnvFile) -> ValidationResult:
        """Validate an EnvFile against this schema."""
        result = ValidationResult()

        for name, spec in self.fields.items():
            var = env.vars.get(name)
            value = var.value if var else None
            errors = spec.validate(value)
            result.errors.extend(errors)

        # Warn about variables in env but not in schema
        for name in env.vars:
            if name not in self.fields:
                result.warnings.append(f"{name}: not in schema (undocumented variable)")

        return result
