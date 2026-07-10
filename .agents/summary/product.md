# product.md — common-py

## Purpose

`common-py` is a private, internal Python library that provides a curated set of generic, reusable modules intended to
be consumed by other Python projects owned by the same developer/organisation. It is not published to PyPI; instead it
is installed directly from GitHub via SSH (Git URL dependency).

## Key Business Objectives

1. **Eliminate copy-paste drift** — shared concerns (structured logging, YAML utilities, badge generation) live in a
   single versioned source of truth.
2. **Minimise dependency footprint** — core library has zero runtime dependencies; optional extras (`logger`, `utils`)
   add only what is strictly necessary.
3. **Quality gate enforcement** — the library models the code-quality standards (lint, type-check, coverage ≥80%) that
   consuming projects should also adopt.
4. **Self-documenting via badges** — the `generate-badges` CLI entry-point produces SVG badges (Python version, test
   pass/fail, coverage %, ruff status, ty status, release date) for use in README files.

## Modules / Features

| Module                            | Extra    | Purpose                                                                     |
|-----------------------------------|----------|-----------------------------------------------------------------------------|
| `common_py.logger`                | `logger` | Pre-configured `logging.Logger` factory; supports plain and JSON formatting |
| `common_py.utils.generate_badges` | `utils`  | CLI & class for generating README SVG badges from CI reports                |
| `common_py.utils.yaml_reader`     | `utils`  | Safe YAML reader with custom `!join` tag constructor                        |

## Targeted Users

- **Internal Python developers** who own or contribute to sibling repositories that consume `common-py` as a dependency.
- **CI/CD pipelines** that invoke the `generate-badges` entry-point to refresh README badges after test runs.

## Versioning & Distribution

- Versioned with SemVer tags (`vX.Y.Z`); current version tracked in `pyproject.toml`.
- Installed via `uv add git+ssh://...@vX.Y.Z` or equivalent pip/poetry syntax.
- Changelog maintained in `CHANGELOG.md`.
