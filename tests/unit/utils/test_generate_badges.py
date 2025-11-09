import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

import pytest
from anybadge import colors
from defusedxml.ElementTree import fromstring

from common_py.utils.generate_badges import BadgeGenerator, main
from definitions import TEST_FILES_DIR

TESTS_REPORT_PATH = TEST_FILES_DIR.joinpath("unit-tests.xml")
COVERAGE_REPORT_PATH = TEST_FILES_DIR.joinpath("coverage.xml")
RUFF_REPORT_PATH = TEST_FILES_DIR.joinpath("ruff.json")
TY_REPORT_PATH = TEST_FILES_DIR.joinpath("ty.json")


def generate_unittest_element_tree(
    num_errors: int, num_failures: int, num_skipped: int, num_tests: int
) -> ET.ElementTree:
    """Helper function to generate an ElementTree for unittest XML."""
    return ET.ElementTree(
        element=fromstring(
            text=f"""<testsuites name="pytest tests">
                        <testsuite name="pytest" errors="{num_errors}" failures="{num_failures}"
                        skipped="{num_skipped}" tests="{num_tests}">
                        </testsuite>
                    </testsuites>"""
        )
    )


def generate_coverage_report_tree(line_rate: float) -> ET.ElementTree:
    """Helper function to generate an ElementTree for coverage report XML."""
    return ET.ElementTree(element=fromstring(text=f"""<coverage line-rate="{line_rate}"></coverage>"""))


UNITTEST_XML_ALL_PASS = generate_unittest_element_tree(num_errors=0, num_failures=0, num_skipped=0, num_tests=1)
UNITTEST_XML_PASS_AND_SKIP = generate_unittest_element_tree(num_errors=0, num_failures=0, num_skipped=1, num_tests=2)
UNITTEST_XML_FAIL = generate_unittest_element_tree(num_errors=0, num_failures=1, num_skipped=1, num_tests=3)

COVERAGE_XML_100_pct = generate_coverage_report_tree(line_rate=1)
COVERAGE_XML_UNROUNDED_pct = generate_coverage_report_tree(line_rate=0.1234)


class TestBadgeGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = TemporaryDirectory()
        cls.badge_generator = BadgeGenerator(
            output_path=Path(cls.temp_dir.name),
            python_version="3.11",
            tests_report_path=TESTS_REPORT_PATH,
            coverage_report_path=COVERAGE_REPORT_PATH,
            ruff_report_path=RUFF_REPORT_PATH,
            ty_report_path=TY_REPORT_PATH,
            generate_release_badge=True,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_dir.cleanup()

    @patch(
        target="sys.argv",
        return_value=[
            "script_name",
            "--output-dir",
            "dummy_output_dir",
            "--python-version",
            "3.11",
            "--tests-report-path",
            "dummy_test_report_path",
            "--coverage-report-path",
            "dummy_coverage_report_path",
            "--ruff-report-path",
            "dummy_ruff_report_path",
            "--ty-report-path",
            "dummy_ty_report_path",
        ],
    )
    @patch(target="common_py.utils.generate_badges.BadgeGenerator.generate_badges")
    def test_badge_generator_main(self, mock_generate_badges: MagicMock, _mock_args: MagicMock) -> None:
        main()
        mock_generate_badges.assert_called_once()

    def test_get_unittest_results_raises_on_missing_tests_report_path(self) -> None:
        badge_generator = self.badge_generator
        badge_generator.tests_report_path = None
        pytest.raises(AttributeError, badge_generator.get_unittest_results)

    @patch(target="common_py.utils.generate_badges.parse", return_value=UNITTEST_XML_ALL_PASS)
    def test_get_unittest_results_all_passed(self, _mock_parse: MagicMock) -> None:
        assert self.badge_generator.get_unittest_results() == ("1 passed", colors.Color.GREEN)

    @patch(target="common_py.utils.generate_badges.parse", return_value=UNITTEST_XML_PASS_AND_SKIP)
    def test_get_unittest_results_pass_and_skip(self, _mock_parse: MagicMock) -> None:
        assert self.badge_generator.get_unittest_results() == ("1 skipped 1 passed", colors.Color.YELLOW)

    @patch(target="common_py.utils.generate_badges.parse", return_value=UNITTEST_XML_FAIL)
    def test_get_unittest_results_fail(self, _mock_parse: MagicMock) -> None:
        assert self.badge_generator.get_unittest_results() == ("1 failed 1 passed", colors.Color.RED)

    def test_get_coverage_results_raises_on_missing_coverage_report_path(self) -> None:
        badge_generator = self.badge_generator
        badge_generator.coverage_report_path = None
        pytest.raises(AttributeError, badge_generator.get_coverage_results)

    @patch(target="common_py.utils.generate_badges.parse", return_value=COVERAGE_XML_100_pct)
    def test_get_coverage_results_100_pct(self, _mock_parse: MagicMock) -> None:
        assert self.badge_generator.get_coverage_results() == 100

    @patch(target="common_py.utils.generate_badges.parse", return_value=COVERAGE_XML_UNROUNDED_pct)
    def test_get_coverage_results_50_pct(self, _mock_parse: MagicMock) -> None:
        assert self.badge_generator.get_coverage_results() == 12.3

    def test_get_ruff_results_raises_on_missing_coverage_report_path(self) -> None:
        badge_generator = self.badge_generator
        badge_generator.ruff_report_path = None
        pytest.raises(AttributeError, badge_generator.get_ruff_results)

    @patch(target="common_py.utils.generate_badges.load", return_value=[])
    def test_get_ruff_results_passing(self, _mock_parse: MagicMock) -> None:
        assert self.badge_generator.get_ruff_results() == ("Passing", colors.Color.GREEN)

    @patch(target="common_py.utils.generate_badges.load", return_value=[{"dummy": "dummy"}])
    def test_get_ruff_results_failing(self, _mock_parse: MagicMock) -> None:
        assert self.badge_generator.get_ruff_results() == ("Failing", colors.Color.RED)
