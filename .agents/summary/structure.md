# structure.md — common-py

## High-level Directory Tree

```
common-py/
├── common_py/                  # Installable library package
│   ├── __init__.py             # Package-level exports
│   ├── logger/                 # logger optional-extra sub-package
│   │   ├── __init__.py         # Public API: get_logger, get_json_logger
│   │   ├── logger.py           # Logger factory functions
│   │   └── formatters.py       # Pre-built logging formatters (JSON_FORMATTER)
│   └── utils/                  # utils optional-extra sub-package
│       ├── __init__.py         # Public API: BadgeGenerator, read_yaml
│       ├── generate_badges.py  # BadgeGenerator class + generate-badges CLI entry-point
│       └── yaml_reader.py      # Safe YAML reader with !join custom constructor
│
├── tests/
│   └── unit/                   # All tests are unit tests (no integration/e2e layer yet)
│       ├── __init__.py
│       ├── logger/
│       │   └── test_logger.py
│       └── utils/
│           ├── test_generate_badges.py
│           ├── test_yaml_reader.py
│           └── test_yaml_file.yaml  # Fixture data for YAML reader tests
│
├── docs/
│   └── img/                    # Generated SVG badges (python, unittest, coverage, ruff, ty, release)
│
├── reports/                    # CI report outputs (gitignored at runtime, committed by badge task)
│   ├── unit-tests.xml
│   ├── coverage.xml
│   ├── ruff.json
│   └── ty.json
│
├── .agents/                    # Agent configuration and skills
│   ├── summary/                # Repository steering files (this directory)
│   │   ├── product.md
│   │   ├── tech.md
│   │   └── structure.md
│   └── skills/                 # Reusable agent skill definitions
│       ├── code-summary/
│       └── prepare-for-pr/
│
├── .github/
│   ├── pull_request_template.md
│   └── workflows/
│       ├── test.yml            # CI: run test suite
│       └── tag_and_release.yml # CI: create GitHub release from tag
│
├── AGENTS.md                   # AI agent steering (ASDLC standard)
├── CHANGELOG.md                # SemVer changelog
├── README.md                   # Project overview and usage instructions
├── definitions.py              # Project-root constants (PROJECT_ROOT_DIR, TESTS_ROOT_DIR)
├── pyproject.toml              # Project metadata, deps, tool config
├── uv.lock                     # Dependency lockfile
├── .pre-commit-config.yaml     # Pre-commit hook definitions
├── .coveragerc                 # Coverage measurement exclusions
└── .secrets.baseline.json      # detect-secrets false-positive baseline
```

## File Naming Conventions

| Convention     | Example                                      |
|----------------|----------------------------------------------|
| Source modules | `snake_case.py`                              |
| Test files     | `test_<module_name>.py`                      |
| Test fixtures  | `test_<purpose>.yaml` / `test_<purpose>.xml` |
| CI workflows   | `<purpose>.yml` in `.github/workflows/`      |
| Badge outputs  | `<tool>.svg` in `docs/img/`                  |
| Report outputs | `<tool>.<format>` in `reports/`              |

## Layer Separation

| Layer             | Location                              | Rule                                                       |
|-------------------|---------------------------------------|------------------------------------------------------------|
| Public API        | `common_py/<sub-package>/__init__.py` | Only export symbols needed by consumers                    |
| Implementation    | `common_py/<sub-package>/<module>.py` | Internal details; not imported directly by consumers       |
| Project constants | `definitions.py` (root)               | Only repo-path helpers; excluded from coverage/install     |
| Tests             | `tests/unit/` mirrors `common_py/`    | 1-to-1 sub-package structure; no test code in `common_py/` |
| CI reports        | `reports/`                            | Generated artefacts; not part of the installable package   |
| Badge images      | `docs/img/`                           | Generated SVG artefacts referenced by `README.md`          |

## Key Constraints

- `common_py/logger/` must remain **stdlib-only** (no extra dependencies).
- New sub-packages must be added to `[tool.hatch.build.targets.wheel] packages` in `pyproject.toml`.
- New optional-extra groups must be declared in `[project.optional-dependencies]` and should have a matching test
  sub-directory under `tests/unit/`.
- `definitions.py` at the root is for developer convenience only; it is **not** shipped in the wheel.
