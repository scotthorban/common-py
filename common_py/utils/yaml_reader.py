"""A YAML reader which supports a set of custom constructors within the YAML file itself."""

from pathlib import Path

import yaml


def __join_constructor(loader: yaml.SafeLoader, node: yaml.SequenceNode) -> str:
    """YAML constructor to join tags and strings together."""
    values = list(loader.construct_sequence(node=node))
    return "".join(values)


def read_yaml(path: Path) -> dict:
    """Reads a YAML file supporting a number of custom constructors.

    Parameters:
        path (Path): Path to the YAML file.
    """
    loader = yaml.SafeLoader
    loader.add_constructor(tag="!join", constructor=__join_constructor)

    with path.open() as file:
        return yaml.load(stream=file, Loader=loader)  # noqa: S506
