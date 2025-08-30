## Common Py

![](docs/img/python.svg)
![](docs/img/unittest.svg)
![](docs/img/coverage.svg)
![](docs/img/ruff.svg)
![](docs/img/release.svg)

### 1. Description
A library of common, generic python modules designed to be used in other projects.

### 2. Installation
#### 2.1 Pre-Requisites
This project template uses [uv](https://docs.astral.sh/uv/) for package and project management. 

```shell
# Create virtual environment using python 3.11
uv venv --python 3.11

# Install dependencies
uv sync --all-extras --dev

# Install pre-commit hooks
uv run task install-hooks

# View other uv tasks
uv run task --list
```
