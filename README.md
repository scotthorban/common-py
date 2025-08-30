## common-py

![](docs/img/python.svg)
![](docs/img/unittest.svg)
![](docs/img/coverage.svg)
![](docs/img/ruff.svg)
![](docs/img/release.svg)

### 1. Description
A library of common, generic python modules designed to be used in other projects.

### 2. Installtion 
> ⚠️ **Important**
> 
> To use `common-py` modules in other repositories, you must have configured your git with an SSH key with access to clone the `common-py` repository.

In all cases below, `X.Y.Z` represents the desired version of `common-py` to use. This can also be replaced with a specific branch name or commit hash but this is not recommended.

#### 2.1 uv (recommended)
```shell
# All modules
uv add git+ssh://git@github.com/scotthorban/common-py.git@vX.Y.Z

# Logger only
uv add git+ssh://git@github.com/scotthorban/common-py.git@vX.Y.Z#subdirectory=common_py/logger
```

#### 2.2 poetry
```shell
# All modules
poetry add git+ssh://git@github.com/scotthorban/common-py.git@vX.Y.Z

# Logger only
poetry add git+ssh://git@github.com/scotthorban/common-py.git@vX.Y.Z#subdirectory=common_py/logger
```

#### 2.3 requirements.txt
```shell
# All modules
git+ssh://git@github.com/scotthorban/common-py.git@vX.Y.Z

# Logger only
git+ssh://git@github.com/scotthorban/common-py.git@vX.Y.Z#subdirectory=common_py/logger
```

### 3. Usage
In the python repository where `common-py` has been installed, import common code like so:

```python
from common_py.logger import get_json_logger
import logging

my_json_logger = get_json_logger(name="my_json_logger", level=logging.WARN)
```

### 4. Local development
This project template uses [uv](https://docs.astral.sh/uv/) for package and project management. 
To install uv, follow the instructions [here](https://docs.astral.sh/uv/getting-started/installation/). 

```shell
# Create virtual environment using python 3.11
uv venv --python 3.11
source .venv/bin/activate

# Install dependencies
uv sync --all-extras --dev

# Install pre-commit hooks
uv run task install-hooks

# (Optional) View other uv tasks
uv run task --list
```
