import unittest

from src.run_project import main


class TestRunProject(unittest.TestCase):
    """Example Unit Test Class docstring."""

    def test_run_project(self) -> None:
        """Example Unit Test docstring."""
        assert main() == 1
