# Contributing to fastenv

## Setup

```bash
git clone https://github.com/Aliipou/fastenv.git
cd fastenv
python -m venv .venv && source .venv/bin/activate
make install
```

## Workflow

1. Fork the repo
2. Create a branch: `git checkout -b feat/your-feature`
3. Write code + tests
4. Run `make lint && make test`
5. Open a PR

## Commit Messages

Follow Conventional Commits: `feat:`, `fix:`, `docs:`, `test:`, `chore:`
