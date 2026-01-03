"""Definitions contains project-level constants specific to this repository."""

from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).parent
"""A dynamically calculated variable to store the project root directory."""
TESTS_ROOT_DIR = PROJECT_ROOT_DIR.joinpath("tests")
