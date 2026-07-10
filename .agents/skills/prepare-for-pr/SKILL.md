---
name: prepare-for-pr
description: Bumps the project version in pyproject.toml and drafts CHANGELOG.md updates based on the git diff between the current branch and main.
---

# Skill: Prepare For PR

## Intent
Automate the process of preparing a Pull Request by analyzing code changes between the current working branch and `main`, determining the appropriate Semantic Versioning bump, executing the version bump, and appending changes to the CHANGELOG.md file.

## Protocol

1. **Verify State**:
   - Ensure you are on a feature branch (not `main`).
   - Ensure the working directory is clean or changes are staged/committed as appropriate.

2. **Diff Analysis**:
   - Perform a git diff between the current branch (or staging area/commits) and `main`:
     ```shell
     git diff origin/main...HEAD
     ```
     *(Or check local `main` branch if `origin/main` is not fetched/available).*
   - Ignore changes to `CHANGELOG.md`, `pyproject.toml`, or lock files.
   - Pay close attention to:
     - Functional source code changes inside `src/`.
     - Significant documentation updates (`README.md`, other `.md` files).
     - Tooling and project environment file changes (e.g., `.gitattributes`, `.gitignore`, `.pre-commit-config.yaml`, GitHub workflows).

3. **Determine SemVer Level**:
   - **major**: If there are breaking API changes or massive architecture shifts.
   - **minor**: If there are new features, new scripts, new configs, or substantial additions/updates that do not break backward compatibility.
   - **patch**: If there are bug fixes, internal code refactoring, styling/formatting improvements, or minor document typos/corrections.

4. **Bump Version**:
   - Execute the version bump using `uv` (or `uv run` if wrapper tasks exist):
     ```shell
     # e.g., for patch bump
     uv version --bump patch
     # e.g., for minor bump
     uv version --bump minor
     # e.g., for major bump
     uv version --bump major
     ```
   - *Note: Ensure you do not change the version field manually.*

5. **Update CHANGELOG.md**:
   - Open `CHANGELOG.md`.
   - Insert a new version section at the top (under the header descriptions) using the newly bumped version.
   - List the functional changes summarized from your diff analysis. Do not include changelog edits themselves in the change list.
   - Keep entries concise and align them with the existing style (e.g., `- [#<issue_number>] - Description` or simply `- Description`).

6. **Validation**:
   - Run tests to ensure everything is functional and formatted:
     ```shell
     uv run task tests
     ```
   - Inform the user of the new version and show them the drafted changelog entries.
