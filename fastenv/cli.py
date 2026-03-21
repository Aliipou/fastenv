import sys
from pathlib import Path


def cmd_diff(args):
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


def cmd_docs(args):
    from fastenv.core import EnvFile
    if not args:
        print("Usage: fastenv docs <file>")
        sys.exit(1)
    env = EnvFile.load(args[0])
    print("| Variable | Description |")
    print("|----------|-------------|")
    for key, var in env.vars.items():
        desc = var.comment or ""
        print(f"| `{key}` | {desc} |")


COMMANDS = {"diff": cmd_diff, "docs": cmd_docs}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("fastenv v0.1.0 -- .env file manager")
        print("Commands:", ", ".join(COMMANDS))
        sys.exit(0)
    COMMANDS[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    main()
