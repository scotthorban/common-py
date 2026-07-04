"""A module to generate project badges designed for use in a README.md file."""

import argparse
import logging
from datetime import UTC, datetime
from json import load
from pathlib import Path

from anybadge import Badge, colors
from defusedxml.ElementTree import parse

from common_py.logger import get_logger

COVERAGE_THRESHOLDS: dict[int | float, str] = {
    50: colors.Color.RED.value,
    60: colors.Color.ORANGE.value,
    75: colors.Color.YELLOW.value,
    90: colors.Color.YELLOWGREEN.value,
    100: colors.Color.GREEN.value,
}


class BadgeGenerator:
    """A class to generate badges designed for use in a README.md file.

    Attributes:
        output_path (Path): Path to the output directory.
        logger (logging.Logger): Logger instance for log messages.
        python_version (str): Python version.
        tests_report_path (Path): Path to the unit tests XML report.
        coverage_report_path (Path): Path to the unit test coverage XML report.
        ruff_report_path (Path): Path to the ruff JSON report.
        ty_report_path (Path): Path to the ty JSON report.
        generate_release_badge (bool): Whether to generate a release badge or not.
    """

    def __init__(
        self,
        output_path: Path,
        *,
        logger: logging.Logger | None = None,
        python_version: str | None,
        tests_report_path: str | None,
        coverage_report_path: str | None,
        ruff_report_path: str | None,
        ty_report_path: str | None,
        generate_release_badge: bool,
    ) -> None:
        """Initializes a BadgeGenerator instance."""
        self.output_path = output_path

        self.logger = logger or get_logger()
        self.logger.setLevel(level=logging.INFO)

        self.python_version = python_version
        self.tests_report_path = Path(tests_report_path) if tests_report_path else None
        self.coverage_report_path = Path(coverage_report_path) if coverage_report_path else None
        self.ruff_report_path = Path(ruff_report_path) if ruff_report_path else None
        self.ty_report_path = Path(ty_report_path) if ty_report_path else None
        self.generate_release_badge = generate_release_badge

    def generate_badges(self) -> None:
        """Generate project badges based on arguments provided to the class."""
        if self.python_version:
            self.logger.info("Generating Python version badge.")
            self.make_badge(
                label="python", value=self.python_version, filename="python.svg", colour=colors.Color.STEELBLUE
            )

        if self.tests_report_path:
            self.logger.info("Generating unit tests badge.")
            results = self.get_unittest_results()
            self.make_badge(label="unittest", value=results[0], filename="unittest.svg", colour=results[1])

        if self.coverage_report_path:
            self.logger.info("Generating test coverage badge.")
            results = self.get_coverage_results()
            self.make_coverage_badge(label="coverage", value=results, filename="coverage.svg")

        if self.ruff_report_path:
            self.logger.info("Generating ruff badge.")
            results = self.get_ruff_results()
            self.make_badge(label="ruff", value=results[0], filename="ruff.svg", colour=results[1])

        if self.ty_report_path:
            self.logger.info("Generating ty badge.")
            results = self.get_ty_results()
            self.make_badge(label="ty", value=results[0], filename="ty.svg", colour=results[1])

        if self.generate_release_badge:
            self.logger.info("Generating release badge.")
            today = datetime.now(tz=UTC).date()
            formatted_date = today.strftime("%Y-%m-%d")
            self.make_badge(
                label="release", value=formatted_date, filename="release.svg", colour=colors.Color.STEELBLUE
            )

    def make_badge(self, label: str, value: str, filename: str, colour: colors.Color) -> None:
        """Creates a badge using the given label, value and colour, saving the result to filename.

        Existing badges will be removed before the new badge is generated.
        Parameters:
            label (str): The label of the badge.
            value (str): The value of the badge.
            filename (str): The filename where the badge will be saved.
            colour (anybadge.colors.Color): Optional colour of the badge.
                Anybadge will infer the colour if omitted and the value is a float between 0 and 100.
        """
        badge = Badge(label=label, value=str(value), default_color=colour.value)
        badge.write_badge(str(self.output_path.joinpath(filename)), overwrite=True)

    def make_coverage_badge(self, label: str, value: float, filename: str) -> None:
        """Creates a badge using the given label and value, saving the result to filename.

        Parameters:
            label (str): The label of the badge.
            value (float): The float coverage score.
            filename (str): The filename where the badge will be saved.
        """
        badge = Badge(label=label, value=value, value_suffix="%", thresholds=COVERAGE_THRESHOLDS)
        badge.write_badge(str(self.output_path.joinpath(filename)), overwrite=True)

    def get_unittest_results(self) -> tuple[str, colors.Color]:
        """Read and return test results from a unit-tests.xml file.

        Returns:
             A tuple of the test results and the colour of the badge.
        """
        if not self.tests_report_path:
            err_msg = "Tests report path not provided."
            raise AttributeError(err_msg)

        root = parse(source=self.tests_report_path).getroot()

        failures = 0
        skipped = 0
        tests = 0
        for type_tag in root.findall("testsuite"):
            failures = int(type_tag.get("failures"))
            skipped = int(type_tag.get("skipped"))
            tests = int(type_tag.get("tests"))

        if failures > 0:
            return f"{failures} failed {tests - failures - skipped} passed", colors.Color.RED

        if skipped > 0:
            return f"{skipped} skipped {tests - skipped} passed", colors.Color.YELLOW

        return f"{tests} passed", colors.Color.GREEN

    def get_coverage_results(self) -> float:
        """Read and return coverage from a unit-tests.xml file."""
        if not self.coverage_report_path:
            err_msg = "Coverage report path not provided."
            raise AttributeError(err_msg)

        root = parse(source=self.coverage_report_path).getroot()
        coverage_score = root.attrib["line-rate"]

        return 100 if coverage_score == "1" else round(100.0 * float(coverage_score), 1)

    def get_ruff_results(self) -> tuple[str, colors.Color]:
        """Read and return Ruff result from a ruff results JSON file.

        Returns:
            A tuple of either "passing" or "failing" alongside the corresponding badge colour.
        """
        if not self.ruff_report_path:
            err_msg = "Ruff report path not provided."
            raise AttributeError(err_msg)

        with self.ruff_report_path.open(mode="r") as linting_file:
            content = load(fp=linting_file)

        return ("Passing", colors.Color.GREEN) if content == [] else ("Failing", colors.Color.RED)

    def get_ty_results(self) -> tuple[str, colors.Color]:
        """Read and return ty result from a ty results JSON file.

        Returns:
            A tuple of either "passing" or "failing" alongside the corresponding badge colour.
        """
        if not self.ty_report_path:
            err_msg = "Ty report path not provided."
            raise AttributeError(err_msg)

        if self.ty_report_path.stat().st_size == 0:
            return "Passing", colors.Color.GREEN

        return "Failing", colors.Color.RED


def main() -> None:
    """Main function for badge generation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output-dir", type=str, required=True, help="Output directory for project badges")
    parser.add_argument("-pv", "--python-version", type=str, default=None, help="Supported python versions")
    parser.add_argument(
        "-trp",
        "--tests-report-path",
        type=str,
        default=None,
        help="Path to the unit tests XML report",
    )
    parser.add_argument(
        "-crp",
        "--coverage-report-path",
        type=str,
        default=None,
        help="Path to the unit test coverage XML report",
    )
    parser.add_argument(
        "-rrp",
        "--ruff-report-path",
        type=str,
        default=None,
        help="Path to the ruff JSON report",
    )
    parser.add_argument(
        "-tyrp",
        "--ty-report-path",
        type=str,
        default=None,
        help="Path to the ty JSON report",
    )
    parser.add_argument(
        "-rb",
        "--release-badge",
        type=bool,
        default=False,
        help="Set to true to generate a release badge in YYYY-MM-DD format",
    )
    args = parser.parse_args()

    badge_generator = BadgeGenerator(
        output_path=Path(args.output_dir),
        logger=get_logger(),
        python_version=args.python_version,
        tests_report_path=args.tests_report_path,
        coverage_report_path=args.coverage_report_path,
        ruff_report_path=args.ruff_report_path,
        ty_report_path=args.ty_report_path,
        generate_release_badge=args.release_badge,
    )
    badge_generator.generate_badges()


if __name__ == "__main__":
    main()
