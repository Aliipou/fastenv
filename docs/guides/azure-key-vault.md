# Azure Key Vault Integration

Load secrets from Azure Key Vault.

## Setup

```bash
pip install fastenv[azure]
```

## Authentication

fastenv uses the Azure SDK's `DefaultAzureCredential`:
1. Environment variables (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_SECRET`)
2. Azure managed identity (for Azure VMs, App Service, AKS)
3. Azure CLI credentials

## Usage

```python
from fastenv import Settings
from fastenv.backends import AzureKeyVaultBackend

class AppSettings(Settings):
    database_url: str
    api_key: str

settings = AppSettings(
    _backend=AzureKeyVaultBackend(
        vault_url="https://my-vault.vault.azure.net",
    )
)
```

Secret names are derived from field names: `database_url` → looks for secret `database-url`.

## Custom Secret Names

```python
from fastenv import Settings, Field

class AppSettings(Settings):
    database_url: str = Field(alias="my-app-db-connection-string")
```

## Caching

Secrets are cached for 5 minutes by default:

```python
backend = AzureKeyVaultBackend(
    vault_url="...",
    cache_ttl_seconds=300,
)
```
