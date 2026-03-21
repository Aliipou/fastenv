"""fastenv CLI — manage .env files from the command line."""
import sys
from pathlib import Path


def cmd_diff(args):
    """Show differences between two .env files."""
    from fastenv.core import EnvFile
    if len(args) < 2:
        print("Usage: fastenv diff <file1> <file2>")
        sys.exit(1)
    a = EnvFile.load(args[0])
    b = EnvFile.load(args[1])
    changes = EnvFile.diff(a, b)
    if not changes:
        print("No differences.")
    else:
        for line in changes:
            print(line)


def cmd_validate(args):
    """Validate an .env file against a schema."""
    from fastenv.core import EnvFile
    from fastenv.schema import EnvSchema
    if len(args) < 2:
        print("Usage: fastenv validate <env-file> <schema-file>")
        sys.exit(1)
    env = EnvFile.load(args[0])
    schema = EnvSchema.load(args[1])
    result = schema.validate(env)
    print(result)
    if not result.valid:
        sys.exit(1)


def cmd_docs(args):
    """Generate a Markdown table from an .env file."""
    from fastenv.core import EnvFile
    if not args:
        print("Usage: fastenv docs <file>")
        sys.exit(1)
    env = EnvFile.load(args[0])
    print("| Variable | Value | Description |")
    print("|----------|-------|-------------|")
    for key, var in env.vars.items():
        sensitive = any(s in key.lower() for s in ("secret", "password", "key", "token", "pwd"))
        val_display = "***" if sensitive else var.value
        desc = var.comment or ""
        print(f"| `{key}` | `{val_display}` | {desc} |")


def cmd_sync(args):
    """Add variables from a template that are missing in the target file."""
    from fastenv.core import EnvFile
    if len(args) < 2:
        print("Usage: fastenv sync <template> <target> [--fill=PLACEHOLDER]")
        sys.exit(1)
    template = EnvFile.load(args[0])
    target = EnvFile.load(args[1])
    fill = "CHANGE_ME"
    for arg in args[2:]:
        if arg.startswith("--fill="):
            fill = arg.split("=", 1)[1]

    added = []
    with open(args[1], "a") as f:
        for key in template.vars:
            if key not in target.vars:
                f.write(f"\n{key}={fill}\n")
                added.append(key)

    if added:
        print(f"Added {len(added)} missing variables: {', '.join(added)}")
    else:
        print("No missing variables. Target is up to date.")


COMMANDS = {
    "diff": cmd_diff,
    "validate": cmd_validate,
    "docs": cmd_docs,
    "sync": cmd_sync,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("fastenv v0.1.0 -- .env file manager")
        print("")
        print("Commands:")
        for name, fn in COMMANDS.items():
            print(f"  {name:<12} {fn.__doc__}")
        sys.exit(0)
    COMMANDS[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    main()
