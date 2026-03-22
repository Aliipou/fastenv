# Environment Validation

fastenv validates your configuration at startup, catching misconfigurations before they cause runtime errors.

## Basic Validation

```python
from fastenv import Settings
from pydantic import field_validator, AnyUrl

class AppSettings(Settings):
    database_url: AnyUrl
    redis_url: str = "redis://localhost:6379"
    max_connections: int = 10
    debug: bool = False

    @field_validator("max_connections")
    @classmethod
    def validate_connections(cls, v: int) -> int:
        if not 1 <= v <= 1000:
            raise ValueError("max_connections must be between 1 and 1000")
        return v

# Raises ValidationError at import time if DATABASE_URL is missing
settings = AppSettings()
```

## Required vs Optional

```python
class Settings(Settings):
    # Required (no default): will raise if not set
    secret_key: str
    database_url: AnyUrl

    # Optional with defaults
    log_level: str = "INFO"
    workers: int = 4
```

## Validation Errors

```
fastenv.ValidationError: 2 validation errors for AppSettings
  database_url: field required [type=missing, env=DATABASE_URL]
  max_connections: max_connections must be between 1 and 1000 [type=value_error, env=MAX_CONNECTIONS]
```
