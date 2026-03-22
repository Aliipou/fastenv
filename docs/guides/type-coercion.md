# Type Coercion

fastenv automatically converts environment variable strings to Python types.

## Supported Types

### Boolean
```python
class Settings(Settings):
    debug: bool = False

# All of these parse to True:
# DEBUG=true DEBUG=True DEBUG=1 DEBUG=yes DEBUG=on
# All of these parse to False:
# DEBUG=false DEBUG=False DEBUG=0 DEBUG=no DEBUG=off
```

### Integer and Float
```python
class Settings(Settings):
    port: int = 8000
    timeout: float = 30.0

# PORT=8080 → 8080 (int)
# TIMEOUT=45.5 → 45.5 (float)
```

### Lists
```python
class Settings(Settings):
    allowed_hosts: list[str] = ["localhost"]
    cors_origins: list[str] = []

# ALLOWED_HOSTS=localhost,example.com → ["localhost", "example.com"]
```

### Optional
```python
class Settings(Settings):
    sentry_dsn: str | None = None

# SENTRY_DSN not set → None
# SENTRY_DSN="" → None (empty string treated as None for Optional)
# SENTRY_DSN=https://... → "https://..."
```

### URLs
```python
from pydantic import AnyUrl

class Settings(Settings):
    database_url: AnyUrl  # validates URL format
```
