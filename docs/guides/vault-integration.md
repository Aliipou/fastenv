# HashiCorp Vault Integration

Load secrets from Vault with zero code changes.

## Setup

```bash
pip install fastenv[vault]
```

## Configuration

```python
from fastenv import Settings
from fastenv.backends import VaultBackend

class AppSettings(Settings):
    vault_url: str = "https://vault.internal"
    vault_token: str  # from environment: VAULT_TOKEN

settings = AppSettings(
    _backend=VaultBackend(
        url="https://vault.internal",
        mount="secret",
        path="my-app/production",
    )
)

# Access secrets transparently
print(settings.database_url)  # loaded from Vault
```

## Dynamic Renewal

```python
from fastenv.backends import VaultBackend

backend = VaultBackend(
    url="https://vault.internal",
    mount="secret",
    path="my-app/prod",
    renew_interval_seconds=3600,  # re-fetch every hour
)
```
