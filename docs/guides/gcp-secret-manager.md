# GCP Secret Manager Integration

Load secrets from Google Cloud Secret Manager.

## Setup

```bash
pip install fastenv[gcp]
```

## Authentication

Uses Application Default Credentials (ADC):
- Local dev: `gcloud auth application-default login`
- Cloud Run / GKE: Workload Identity Federation

## Usage

```python
from fastenv import Settings
from fastenv.backends import GCPSecretManagerBackend

class AppSettings(Settings):
    database_url: str
    stripe_key: str

settings = AppSettings(
    _backend=GCPSecretManagerBackend(
        project_id="my-gcp-project",
        # Accesses secrets: database-url, stripe-key
    )
)
```

## Secret Versioning

```python
backend = GCPSecretManagerBackend(
    project_id="my-gcp-project",
    version="latest",  # or specific version like "3"
)
```

## Testing

```python
from unittest.mock import patch

def test_settings():
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///test.db"}):
        settings = AppSettings()  # uses env vars, bypasses GCP
        assert settings.database_url == "sqlite:///test.db"
```
