# Change Log
All changes to this project will be documented in this file. 

This format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [semantic versioning](https://semver.org/).

## 2.2.1
- Updated `README.md` to add more info about project repo contents and to detail the use of `uv`.

## 2.2.0
- Enables all ruff rulesets (including pydocstyle), disabling specific rules only.

## 2.1.0
- Adds a GitHub actions job to create a git tag and a GitHub Release when merging to `main`.
- Removes redundant "Setup python version" step from test GitHub actions job

## 2.0.0
- Replace poetry with uv and tox with uv taskipy.
- Replace isort and black with ruff + pre-commit hooks.
- Rename `projectname` folder to `src`.
- Added `CHANGELOG.md`.

## 1.0.0
- Initial release of template repository using poetry and tox for environment management, pylint for code linting, black for code formatting.
