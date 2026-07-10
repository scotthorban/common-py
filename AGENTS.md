# AGENTS.md — common-py

> Steering file for AI coding agents. Follows the [ASDLC open standard](https://asdlc.dev).

---

## Mission

`common-py` is a shared internal Python library that provides generic, reusable modules (logging, utilities) consumed by
other Python projects via SSH-based Git installation. The goal is a small, well-tested, strictly linted set of building
blocks that remain dependency-light and easy to vendor.

---

## Toolchain Registry

| Concern              | Tool / Version constraint                            |
|----------------------|------------------------------------------------------|
| Language             | Python `>=3.11,<4`                                   |
| Package manager      | `uv` (recommended) / poetry / pip                    |
| Build backend        | `hatchling`                                          |
| Task runner          | `taskipy` (`uv run task <name>`)                     |
| Linter               | `ruff >=0.15.0` (ALL rules, select ignores)          |
| Formatter            | `ruff format`                                        |
| Type checker         | `ty >=0.0.56`                                        |
| Test framework       | `pytest >=8.4.1`                                     |
| Coverage             | `pytest-cov >=6.2.1` (≥80% gate)                     |
| Secret scanning      | `detect-secrets >=1.5.0`                             |
| Pre-commit hooks     | `prek` + `conventional-pre-commit` + `ruff`          |
| Badge generation     | `anybadge >=1.16.0` (entry-point: `generate-badges`) |
| XML parsing          | `defusedxml >=0.7.1`                                 |
| Time mocking (tests) | `freezegun >=1.5.5`                                  |
| CI                   | GitHub Actions (`.github/workflows/`)                |
| Docstring convention | Google style                                         |

---

## Judgment Boundaries

### Always do

- Run `uv run task tests` (unit → coverage → lint → format-check → type-check → badge) before committing.
- Follow Google-style docstrings on all public symbols.
- Keep the `common_py.logger` optional-extra dependency-free (no extra deps in
  `[project.optional-dependencies] logger`).
- Preserve the ≥80% coverage gate; do not exclude new modules from coverage without justification.
- Commit messages must follow Conventional Commits (enforced by `conventional-pre-commit` hook).

### Never do

- Add runtime dependencies to the `[project]` core `dependencies` list without explicit approval — the library must stay
  dependency-light.
- Import `yaml` inside `common_py.logger` (yaml is only used in `utils`).
- Use `assert` outside of test files (ruff S101 is disabled in tests only).
- Bypass secret-scanning baseline without auditing false positives first.
- Use `subprocess` or unsafe XML parsers (`xml.etree.ElementTree`); prefer `defusedxml`.

### Reference files

- Detailed directory layout → `.agents/summary/structure.md`
- Technology inventory → `.agents/summary/tech.md`
- Product context → `.agents/summary/product.md`
