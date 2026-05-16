# fastenv

> CLI tool for managing `.env` files across environments

[![Python](https://img.shields.io/badge/python-3.10+-3776AB?logo=python)](https://python.org)
[![CI](https://github.com/Aliipou/fastenv/actions/workflows/ci.yml/badge.svg)](https://github.com/Aliipou/fastenv/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## The Problem

Managing environment variables across `dev`, `staging`, and `prod` is error-prone:

- Did you add `NEW_API_KEY` to all three `.env` files?
- Which variables are in `.env.example` but missing from `.env.prod`?
- Which `.env.prod` variables contain plaintext secrets that should be references?

`fastenv` solves this with four focused commands.

## Install

```bash
pip install fastenv
```

## Commands

### `diff` — compare two .env files

Shows variables present in one file but not the other, and variables with different values.

```bash
fastenv diff .env .env.prod
```

Example output:
```
+ NEW_FEATURE_FLAG (only in .env)
- LEGACY_ENDPOINT (only in .env.prod)
~ DATABASE_URL  .env=postgresql://localhost/myapp  .env.prod=postgresql://prod-host/myapp
```

---

### `sync` — forward-fill missing variables from a template

Adds any variable that exists in the template but is missing from the target. Existing values are never overwritten.

```bash
# Add missing vars from .env.example into .env.prod, prefilled with CHANGE_ME
fastenv sync .env.example .env.prod

# Use a custom placeholder
fastenv sync .env.example .env.prod --fill=REPLACE_ME
```

Example output:
```
Added 3 missing variables: NEW_FEATURE_FLAG, STRIPE_WEBHOOK_SECRET, REDIS_TLS_URL
```

---

### `validate` — check an .env file against a schema

Validates that required keys exist and (optionally) match expected patterns. Schema is a JSON file.

```bash
fastenv validate .env .env.schema
```

Example `.env.schema`:
```json
{
  "DATABASE_URL": {"required": true, "pattern": "^postgresql://"},
  "LOG_LEVEL": {"required": true, "enum": ["debug", "info", "warning", "error"]},
  "STRIPE_KEY": {"required": false}
}
```

Exit code 1 on failure — safe to use in CI pre-deploy checks.

---

### `docs` — generate a Markdown table from a .env file

Outputs a Markdown table of all variables. Secret-looking keys (`PASSWORD`, `KEY`, `TOKEN`, `SECRET`) are redacted automatically.

```bash
fastenv docs .env
```

Example output:
```
| Variable        | Value       | Description              |
|-----------------|-------------|--------------------------|
| `APP_ENV`       | `prod`      | Deployment environment   |
| `DATABASE_URL`  | `postgresql://...` |                   |
| `API_KEY`       | `***`       | Third-party API key      |
```

---

## Python API

All commands are also usable as a library:

```python
from fastenv import EnvFile
from fastenv.schema import EnvSchema

# Load and diff
env = EnvFile.load(".env")
prod = EnvFile.load(".env.prod")
for change in EnvFile.diff(env, prod):
    print(change)

# Validate
schema = EnvSchema.load(".env.schema")
result = schema.validate(env)
if not result.valid:
    for err in result.errors:
        print(err)
```

## What Is and Isn't Here

| Feature | Status |
|---------|--------|
| `diff` — key/value comparison | Done |
| `sync` — forward-fill from template | Done |
| `validate` — schema validation | Done |
| `docs` — Markdown table generation | Done |
| Encryption at rest | Stub in `fastenv/encrypt.py` — not production-ready |
| Audit logging | Stub in `fastenv/audit.py` — not production-ready |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
