# tech.md — common-py

## Language & Runtime

| Item                  | Detail                     |
|-----------------------|----------------------------|
| Language              | Python `>=3.11,<4`         |
| Target version (ruff) | `py311`                    |
| Virtual environment   | `.venv/` (managed by `uv`) |

## Package Management

| Tool      | Role                                                     |
|-----------|----------------------------------------------------------|
| `uv`      | Primary package manager and project runner (recommended) |
| `uv.lock` | Lockfile (committed to repo)                             |

## Build System

| Item          | Detail                                                   |
|---------------|----------------------------------------------------------|
| Build backend | `hatchling`                                              |
| Build target  | `common_py/` wheel                                       |
| Entry point   | `generate-badges → common_py.utils.generate_badges:main` |

## Runtime Dependencies (optional extras only)

| Extra   | Package             | Min Version | Used by                                                           |
|---------|---------------------|-------------|-------------------------------------------------------------------|
| `utils` | `anybadge`          | `>=1.16.0`  | `generate_badges.py` (SVG badge creation)                         |
| `utils` | `defusedxml`        | `>=0.7.1`   | `generate_badges.py` (safe XML parsing of JUnit/coverage reports) |
| `utils` | `pyyaml` (implicit) | —           | `yaml_reader.py` (YAML loading with safe loader)                  |

> The `logger` extra intentionally has **no** dependencies — it uses only the Python stdlib `logging` module.

## Development Dependencies

| Package             | Min Version | Purpose                                 |
|---------------------|-------------|-----------------------------------------|
| `pytest`            | `>=8.4.1`   | Test runner                             |
| `pytest-cov`        | `>=6.2.1`   | Coverage measurement                    |
| `freezegun`         | `>=1.5.5`   | Date/time mocking in tests              |
| `ruff`              | `>=0.15.0`  | Linter + formatter                      |
| `ty`                | `>=0.0.56`  | Static type checker                     |
| `taskipy`           | `>=1.14.1`  | Task runner (wraps common dev commands) |
| `detect-secrets`    | `>=1.5.0`   | Secret scanning                         |
| `prek`              | `>=0.4.8`   | Pre-commit hook installer               |
| `typing-extensions` | `>=4.14.1`  | Backported typing utilities             |

## Linting & Formatting

| Concern       | Config location                        | Notes                                                            |
|---------------|----------------------------------------|------------------------------------------------------------------|
| Ruff lint     | `[tool.ruff.lint]` in `pyproject.toml` | `select = ["ALL"]` with targeted ignores                         |
| Ruff format   | `[tool.ruff.format]`                   | Google docstring convention, double quotes, 120 char line length |
| Ruff isort    | `[tool.ruff.lint.isort]`               | Case-sensitive, combine-as-imports                               |
| Type checking | `ty check`                             | Output written to `reports/ty.json`                              |

## Testing & Coverage

| Item            | Detail                                                                                                            |
|-----------------|-------------------------------------------------------------------------------------------------------------------|
| Test runner     | `pytest`                                                                                                          |
| Test layout     | `tests/unit/` mirroring `common_py/` structure                                                                    |
| Coverage config | `.coveragerc` (omits `__init__.py`, `tests/`, `definitions.py`)                                                   |
| Coverage gate   | `--cov-fail-under=80`                                                                                             |
| Report formats  | XML (`reports/coverage.xml`), JUnit XML (`reports/unit-tests.xml`), JSON (`reports/ruff.json`, `reports/ty.json`) |

## Pre-commit & Git Hooks

| Hook                      | Source                                      | Purpose                                                      |
|---------------------------|---------------------------------------------|--------------------------------------------------------------|
| `conventional-pre-commit` | `compilerla/conventional-pre-commit@v3.2.0` | Enforce Conventional Commits on `commit-msg` stage           |
| `check-yaml`              | `pre-commit/pre-commit-hooks@v2.3.0`        | Validate YAML files (excludes test dirs)                     |
| `detect-secrets`          | `Yelp/detect-secrets@v1.5.0`                | Block committed secrets (baseline: `.secrets.baseline.json`) |
| `ruff` + `ruff-format`    | `astral-sh/ruff-pre-commit@v0.15.0`         | Lint and format on commit                                    |

## CI/CD (GitHub Actions)

| Workflow      | File                                    | Trigger   |
|---------------|-----------------------------------------|-----------|
| Test suite    | `.github/workflows/test.yml`            | PR / push |
| Tag & Release | `.github/workflows/tag_and_release.yml` | Tag push  |

## Task Runner (taskipy)

Run via `uv run task <name>`:

| Task                  | Command summary                                                    |
|-----------------------|--------------------------------------------------------------------|
| `unit`                | `pytest -v tests/unit` → JUnit XML                                 |
| `coverage`            | `pytest --cov` ≥80% gate → coverage XML                            |
| `check-lint`          | `ruff check` → JSON report                                         |
| `lint`                | `ruff check --fix`                                                 |
| `check-format`        | `ruff format --diff`                                               |
| `format`              | `ruff format`                                                      |
| `check-types`         | `ty check` → JSON report                                           |
| `badge`               | `python common_py/utils/generate_badges.py …` → SVG to `docs/img/` |
| `tests`               | Runs all of the above in sequence                                  |
| `install-hooks`       | `prek install` (pre-commit + commit-msg hooks)                     |
| `detect-secrets-scan` | Update `.secrets.baseline.json`                                    |
| `audit-secrets`       | Interactive secret audit                                           |
