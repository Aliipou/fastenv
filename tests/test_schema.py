"""Tests for schema-based .env validation."""
import os
import tempfile
import pytest
from fastenv.core import EnvFile
from fastenv.schema import EnvSchema, FieldSpec, ValidationResult


def make_file(content: str) -> str:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False)
    f.write(content)
    f.close()
    return f.name


def make_schema_file(content: str) -> str:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".schema", delete=False)
    f.write(content)
    f.close()
    return f.name


def test_field_spec_required_missing():
    spec = FieldSpec(name="KEY", required=True)
    errors = spec.validate(None)
    assert any("required" in e for e in errors)


def test_field_spec_optional_missing():
    spec = FieldSpec(name="KEY", required=False)
    errors = spec.validate(None)
    assert errors == []


def test_field_spec_int_valid():
    spec = FieldSpec(name="KEY", type="int")
    assert spec.validate("42") == []


def test_field_spec_int_invalid():
    spec = FieldSpec(name="KEY", type="int")
    errors = spec.validate("not-a-number")
    assert errors


def test_field_spec_bool_valid():
    spec = FieldSpec(name="KEY", type="bool")
    for val in ("true", "false", "1", "0", "yes", "no"):
        assert spec.validate(val) == [], f"Should accept {val!r}"


def test_field_spec_bool_invalid():
    spec = FieldSpec(name="KEY", type="bool")
    assert spec.validate("maybe")


def test_field_spec_url_valid():
    spec = FieldSpec(name="KEY", type="url")
    assert spec.validate("https://example.com") == []


def test_field_spec_url_invalid():
    spec = FieldSpec(name="KEY", type="url")
    assert spec.validate("not-a-url")


def test_field_spec_pattern():
    spec = FieldSpec(name="KEY", pattern=r"[a-z]+-[0-9]+")
    assert spec.validate("abc-123") == []
    assert spec.validate("ABC-123")  # uppercase not matched


def test_schema_load_and_validate():
    schema_path = make_schema_file("""# description: Database URL
# type: url
# required: true
DATABASE_URL=

# description: Worker count
# type: int
# required: false
# default: 4
WORKERS=
""")
    env_path = make_file("DATABASE_URL=https://db.example.com/mydb\nWORKERS=8\n")

    schema = EnvSchema.load(schema_path)
    env = EnvFile.load(env_path)
    result = schema.validate(env)

    assert result.valid
    os.unlink(schema_path)
    os.unlink(env_path)


def test_schema_validate_missing_required():
    schema_path = make_schema_file("# required: true\nSECRET_KEY=\n")
    env_path = make_file("OTHER=value\n")

    schema = EnvSchema.load(schema_path)
    env = EnvFile.load(env_path)
    result = schema.validate(env)

    assert not result.valid
    assert any("SECRET_KEY" in e for e in result.errors)
    os.unlink(schema_path)
    os.unlink(env_path)


def test_validation_result_str_on_valid():
    result = ValidationResult()
    assert "OK" in str(result)


def test_validation_result_str_on_errors():
    result = ValidationResult(errors=["KEY: required but not set"])
    assert "ERROR" in str(result)
