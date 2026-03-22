# Testing Guide

```python
from unittest.mock import patch
import os

def test_settings_from_env():
    with patch.dict(os.environ, {'DATABASE_URL': 'sqlite:///test.db'}):
        settings = AppSettings()
        assert settings.database_url == 'sqlite:///test.db'
```
