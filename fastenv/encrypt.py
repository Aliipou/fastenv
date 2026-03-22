"""AES-256-GCM encryption for sensitive .env values.

Allows storing encrypted secrets in .env files so they can be safely
committed to version control, decrypted at runtime with a master key.
"""
from __future__ import annotations
import base64
import os
import secrets


def _require_cryptography() -> None:
    try:
        import cryptography  # noqa: F401
    except ImportError as exc:
        raise ImportError(
            "fastenv[encrypt] required: pip install fastenv[encrypt]"
        ) from exc


def encrypt_value(plaintext: str, key: bytes) -> str:
    """Encrypt a string value with AES-256-GCM. Returns base64-encoded ciphertext."""
    _require_cryptography()
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    nonce = secrets.token_bytes(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return "enc:" + base64.b64encode(nonce + ciphertext).decode()


def decrypt_value(encrypted: str, key: bytes) -> str:
    """Decrypt an AES-256-GCM encrypted env var value."""
    _require_cryptography()
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    if not encrypted.startswith("enc:"):
        return encrypted  # Not encrypted, return as-is
    raw = base64.b64decode(encrypted[4:])
    nonce, ciphertext = raw[:12], raw[12:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None).decode()


def generate_key() -> str:
    """Generate a new random 256-bit key, base64-encoded."""
    return base64.b64encode(secrets.token_bytes(32)).decode()
