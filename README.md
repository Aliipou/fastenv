# fastenv

> Blazing-fast `.env` file manager for Python projects

[![Python](https://img.shields.io/badge/python-3.10+-3776AB?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

`fastenv` is a CLI tool and Python library for managing `.env` files with validation, diffing, and auto-documentation.

## The Problem

Managing environment variables across `dev`, `staging`, and `prod` is painful:
- Did you add `NEW_VAR` to all three `.env` files?
- Which variables are in `.env.example` but missing from `.env.prod`?

## Install

```bash
pip install fastenv
```

## Usage

```bash
# Diff two .env files
fastenv diff .env .env.prod

# Generate docs from .env
fastenv docs .env --output env-docs.md

# Validate against schema
fastenv validate .env --schema .env.schema
```

## Python API

```python
from fastenv import EnvFile

env = EnvFile.load(".env")
prod = EnvFile.load(".env.prod")

for change in EnvFile.diff(env, prod):
    print(change)
```

## License

MIT
