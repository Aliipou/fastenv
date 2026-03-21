"""Example usage of fastenv — diff, validate, sync, and docs."""
from fastenv.core import EnvFile
from fastenv.schema import EnvSchema
from pathlib import Path
import tempfile
import os


def demo_diff():
    """Show how to diff two .env files programmatically."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f1:
        f1.write("DATABASE_URL=postgres://localhost/dev\nWORKERS=4\nDEBUG=true\n")
        path1 = f1.name

    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f2:
        f2.write("DATABASE_URL=postgres://prod-host/app\nWORKERS=16\nNEW_FEATURE=enabled\n")
        path2 = f2.name

    dev = EnvFile.load(path1)
    prod = EnvFile.load(path2)

    print("=== Environment Diff: dev vs prod ===")
    for line in EnvFile.diff(dev, prod):
        print(line)

    os.unlink(path1)
    os.unlink(path2)


def demo_validate():
    """Show schema-based validation."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".schema", delete=False) as sf:
        sf.write(
            "# type: url\n# required: true\nDATABASE_URL=\n"
            "# type: int\n# required: false\n# default: 4\nWORKERS=\n"
        )
        schema_path = sf.name

    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as ef:
        ef.write("DATABASE_URL=https://db.example.com/app\nWORKERS=8\n")
        env_path = ef.name

    schema = EnvSchema.load(schema_path)
    env = EnvFile.load(env_path)
    result = schema.validate(env)

    print("\n=== Schema Validation ===")
    print(result)

    os.unlink(schema_path)
    os.unlink(env_path)


if __name__ == "__main__":
    demo_diff()
    demo_validate()
