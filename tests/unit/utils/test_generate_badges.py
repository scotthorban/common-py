import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from common_py.utils.generate_badges import main
from definitions import TEST_FILES_DIR


class TestBadgeGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = TemporaryDirectory()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_dir.cleanup()

    def test_badge_generator(self) -> None:
        with patch(
            "sys.argv",
            [
                "script_name",
                "--output-dir",
                str(self.temp_dir.name),
                "--python-version",
                "3.11",
                "--tests-report-path",
                str(TEST_FILES_DIR.joinpath("unit-tests.xml")),
                "--coverage-report-path",
                str(TEST_FILES_DIR.joinpath("coverage.xml")),
                "--ruff-report-path",
                str(TEST_FILES_DIR.joinpath("ruff.json")),
            ],
        ):
            main()
        assert Path(self.temp_dir.name).joinpath("python.svg").exists()
        assert Path(self.temp_dir.name).joinpath("release.svg").exists()
        assert Path(self.temp_dir.name).joinpath("unittest.svg").exists()
        assert Path(self.temp_dir.name).joinpath("coverage.svg").exists()
        assert Path(self.temp_dir.name).joinpath("ruff.svg").exists()
