# Change Log

All changes to this project will be documented in this file.

This format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [semantic versioning](https://semver.org/).

## 0.5.2

- [#19](https://github.com/scotthorban/common-py/issues/19) - Add `AGENTS.md` at the repository root following the ASDLC
  open standard, documenting mission, toolchain registry, and judgment boundaries for AI coding agents.
- [#19](https://github.com/scotthorban/common-py/issues/19) - Add `.agents/summary/` directory with `product.md`,
  `tech.md`, and `structure.md` steering files to minimise token drift across agent sessions.
- [#19](https://github.com/scotthorban/common-py/issues/19) - Add `.agents/skills/` directory containing `code-summary`
  and `prepare-for-pr` reusable agent skill definitions.
- [#19](https://github.com/scotthorban/common-py/issues/19) - Add `.gitattributes` enforcing LF line-endings across all
  text file types for consistent cross-platform behaviour.
- [#19](https://github.com/scotthorban/common-py/issues/19) - Upgrade `ruff` pre-commit hook from `v0.12.8` to
  `v0.15.0`.
- [#19](https://github.com/scotthorban/common-py/issues/19) - Fix minor wording in `.github/pull_request_template.md`.

## 0.5.1

- [#17](https://github.com/scotthorban/common-py/issues/17) - Upgrade ruff and ty versions & fix any new issues.
- [#17](https://github.com/scotthorban/common-py/issues/17) - Fix ty badge generation for newer ty versions, which write
  an empty list to a file instead of an empty file.

## 0.5.0

- [#14](https://github.com/scotthorban/common-py/issues/14) - Added a `yaml_reader` util for loading YAML files
  containing custom constructors.

## 0.4.0

- [#5](https://github.com/scotthorban/common-py/issues/5) - Added `ty` for type checking purposes.
- [#5](https://github.com/scotthorban/common-py/issues/5) - Added badge generation for `ty`.
- [#5](https://github.com/scotthorban/common-py/issues/5) - Refactor `badge_generator` tests.

## 0.3.0

- [#4](https://github.com/scotthorban/common-py/issues/4) - Added project badge generation module and CLI tool via
  `uv run generate-badges` for projects using `common-py`.

## 0.2.1

- [#9](https://github.com/scotthorban/common-py/issues/9) - Added information to `README.md` about how to install
  `common-py` directly from GitHub.
- [#9](https://github.com/scotthorban/common-py/issues/9) - Change from setuptools to hatchling build backend.

## 0.2.0

- [#2](https://github.com/scotthorban/common-py/issues/2) - Added common logger module with support for JSON formatting.

## 0.1.0

- [#1](https://github.com/scotthorban/common-py/issues/1) - Remove remnants from python project template repository.
