# AWS Secrets Manager Integration

Load secrets from AWS Secrets Manager with zero application changes.

## Setup

```bash
pip install fastenv[aws]
```

## Usage

```python
from fastenv import Settings
from fastenv.backends import AWSSecretsManagerBackend

class AppSettings(Settings):
    database_url: str
    api_key: str

settings = AppSettings(
    _backend=AWSSecretsManagerBackend(
        secret_name="my-app/production",
        region="eu-west-1",
    )
)
```

AWS credentials are sourced from the standard chain: env vars, ~/.aws/credentials, EC2/ECS/Lambda IAM role.

## Multiple Secrets

```python
backend = AWSSecretsManagerBackend(
    secrets=[
        "my-app/database",
        "my-app/third-party-keys",
    ],
    region="eu-west-1",
)
```

## Local Development

Use AWS SSM Parameter Store or a local mock:

```bash
# moto mock for testing
pip install moto[secretsmanager]

import boto3
from moto import mock_secretsmanager

@mock_secretsmanager
def test_settings():
    client = boto3.client("secretsmanager", region_name="eu-west-1")
    client.create_secret(Name="test/app", SecretString=json.dumps({"API_KEY": "test"}))
    settings = AppSettings(_backend=AWSSecretsManagerBackend(...))
    assert settings.api_key == "test"
```
