# Migrating from python-dotenv

fastenv is a drop-in replacement for python-dotenv with additional features.

## Before (python-dotenv)

```python
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
MAX_CONNECTIONS = int(os.getenv("MAX_CONNECTIONS", "10"))
```

Problems:
- No type validation
- Runtime errors if required vars missing
- No IDE autocomplete

## After (fastenv)

```python
from fastenv import Settings

class AppSettings(Settings):
    database_url: str          # required, validated
    debug: bool = False        # automatic bool parsing
    max_connections: int = 10  # automatic int parsing

settings = AppSettings()  # raises at startup if DATABASE_URL missing
```

Benefits:
- Type validation at startup
- Full IDE autocomplete
- Clear schema of all required config

## .env File Compatibility

fastenv reads `.env` files in the same format as python-dotenv:

```bash
# .env
DATABASE_URL=postgresql://localhost/mydb
DEBUG=true
MAX_CONNECTIONS=20
```

No changes to your `.env` file needed.

## Migration Steps

1. `pip install fastenv`
2. Replace `from dotenv import load_dotenv; load_dotenv()` with `from fastenv import Settings`
3. Define your `Settings` class with typed fields
4. Replace `os.getenv("KEY")` with `settings.key`
