# Field-Level Encryption

Encrypt sensitive configuration values before storing them in .env files or version control.

## Setup

```bash
pip install fastenv[encryption]
```

## Encrypting Values

```bash
# Encrypt a value
fastenv encrypt --key-file .fastenv.key "my-secret-value"
enc:AES256:3a8d9f2b1c...

# Store the encrypted value in .env
DATABASE_URL=enc:AES256:3a8d9f2b1c...
```

## Usage in Application

```python
from fastenv import Settings
from fastenv.encryption import AES256Backend

class AppSettings(Settings):
    database_url: str  # automatically decrypted

settings = AppSettings(
    _encryption=AES256Backend(key_file=".fastenv.key")
)
print(settings.database_url)  # decrypted value
```

## Key Management

```bash
# Generate a new key
fastenv keygen --output .fastenv.key

# Rotate keys
fastenv rotate-key --old-key .fastenv.key.old --new-key .fastenv.key
```

Add `.fastenv.key` to `.gitignore`. The encrypted `.env` file is safe to commit.
