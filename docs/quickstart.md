# Quickstart

```bash
pip install fastenv
```

```python
from fastenv import Settings

class Config(Settings):
    database_url: str
    debug: bool = False
    port: int = 8000

config = Config()  # reads from environment or .env file
print(config.port)  # 8000
```

Set `DATABASE_URL` in your environment or `.env` file.
