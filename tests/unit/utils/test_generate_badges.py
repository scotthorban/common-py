import unittest
import xml.etree.ElementTree as ET
from argparse import Namespace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, call, mock_open, patch

import pytest
from anybadge import colors
from defusedxml.ElementTree import fromstring
from freezegun import freeze_time

from common_py.utils.generate_badges import BadgeGenerator, main


def generate_unittest_element_tree(
    num_errors: int, num_failures: int, num_skipped: int, num_tests: int
) -> ET.ElementTree:
    """Helper function to generate an ElementTree for unittest XML."""
    xml = f"""<testsuites name="pytest tests">
                <testsuite name="pytest" errors="{num_errors}" failures="{num_failures}"
                skipped="{num_skipped}" tests="{num_tests}">
                </testsuite>
              </testsuites>"""
    return ET.ElementTree(element=fromstring(text=xml))


def generate_coverage_report_tree(line_rate: float) -> ET.ElementTree:
    """Helper function to generate an ElementTree for coverage report XML."""
    return ET.ElementTree(element=fromstring(text=f"""<coverage line-rate="{line_rate}"></coverage>"""))


MOCK_NAMESPACE = Namespace(
    output_dir="dummy_output_dir",
    python_version=None,
    tests_report_path=None,
    coverage_report_path=None,
    ruff_report_path=None,
    ty_report_path=None,
    release_badge=None,
)

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
            tests_report_path="dummy_test_report_path",
            coverage_report_path="--coverage-report-path",
            ruff_report_path="dummy_ruff_report_path",
            ty_report_path="dummy_ty_report_path",
            generate_release_badge=True,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_dir.cleanup()

    @patch(target="common_py.utils.generate_badges.argparse.ArgumentParser.parse_args", return_value=MOCK_NAMESPACE)
    @patch(target="common_py.utils.generate_badges.BadgeGenerator.generate_badges")
    def test_badge_generator_main(self, mock_generate_badges: MagicMock, _mock_args: MagicMock) -> None:
        main()
        mock_generate_badges.assert_called_once()

    @patch(target="common_py.utils.generate_badges.BadgeGenerator.make_badge")
    @patch(target="common_py.utils.generate_badges.BadgeGenerator.make_coverage_badge")
    @patch(
        target="common_py.utils.generate_badges.BadgeGenerator.get_unittest_results",
        return_value=("1 passed", colors.Color.GREEN),
    )
    @patch(target="common_py.utils.generate_badges.BadgeGenerator.get_coverage_results", return_value=100)
    @patch(
        target="common_py.utils.generate_badges.BadgeGenerator.get_ruff_results",
        return_value=("Passing", colors.Color.GREEN),
    )
    @patch(
        target="common_py.utils.generate_badges.BadgeGenerator.get_ty_results",
        return_value=("Passing", colors.Color.GREEN),
    )
    @freeze_time(time_to_freeze="1900-01-01")
    def test_generate_badges(
        self,
        _mock_get_ty_results: MagicMock,
        _mock_get_ruff_results: MagicMock,
        _mock_get_coverage_results: MagicMock,
        _mock_get_unittest_results: MagicMock,
        mock_make_coverage_badge: MagicMock,
        mock_make_badge: MagicMock,
    ) -> None:
        self.badge_generator.generate_badges()
        mock_make_badge.assert_has_calls(
            calls=[
                call(label="python", value="3.11", filename="python.svg", colour=colors.Color.STEELBLUE),
                call(label="unittest", value="1 passed", filename="unittest.svg", colour=colors.Color.GREEN),
                call(label="ruff", value="Passing", filename="ruff.svg", colour=colors.Color.GREEN),
                call(label="ty", value="Passing", filename="ty.svg", colour=colors.Color.GREEN),
                call(label="release", value="1900-01-01", filename="release.svg", colour=colors.Color.STEELBLUE),
            ]
        )
        mock_make_coverage_badge.assert_called_once_with(label="coverage", value=100, filename="coverage.svg")

    def test_make_badge(self) -> None:
        self.badge_generator.make_badge(
            label="test_badge", value="test", filename="test_badge.svg", colour=colors.Color.GREEN
        )
        assert Path(self.temp_dir.name).joinpath("test_badge.svg").exists()

    def test_make_coverage_badge(self) -> None:
        self.badge_generator.make_coverage_badge(label="test_badge", value=60, filename="test_coverage_badge.svg")
        assert Path(self.temp_dir.name).joinpath("test_coverage_badge.svg").exists()

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

    @patch.object(target=Path, attribute="open", new_callable=mock_open, read_data="[]")
    def test_get_ruff_results_passing(self, mock_file: MagicMock) -> None:
        assert self.badge_generator.get_ruff_results() == ("Passing", colors.Color.GREEN)
        mock_file.assert_called_once_with(mode="r")

    @patch.object(target=Path, attribute="open", new_callable=mock_open, read_data='[{"dummy": "dummy"}]')
    def test_get_ruff_results_failing(self, mock_file: MagicMock) -> None:
        assert self.badge_generator.get_ruff_results() == ("Failing", colors.Color.RED)
        mock_file.assert_called_once_with(mode="r")

    def test_get_ty_results_raises_on_missing_coverage_report_path(self) -> None:
        badge_generator = self.badge_generator
        badge_generator.ty_report_path = None
        pytest.raises(AttributeError, badge_generator.get_ty_results)

    @patch.object(target=Path, attribute="stat")
    def test_get_ty_results_passing(self, mock_path_stat: MagicMock) -> None:
        mock_path_stat.return_value = MagicMock(st_size=0)
        assert self.badge_generator.get_ty_results() == ("Passing", colors.Color.GREEN)

    @patch.object(target=Path, attribute="stat")
    def test_get_ty_results_failing(self, mock_path_stat: MagicMock) -> None:
        mock_path_stat.return_value = MagicMock(st_size=1)
        assert self.badge_generator.get_ty_results() == ("Failing", colors.Color.RED)
