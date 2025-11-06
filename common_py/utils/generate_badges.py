"""A module to generate project badges designed for use in a README.md file."""

import argparse
from pathlib import Path

from anybadge import Badge, colors
from defusedxml import ElementTree

COVERAGE_THRESHOLDS = {
    50: colors.Color.RED.value,
    60: colors.Color.ORANGE.value,
    75: colors.Color.YELLOW.value,
    90: colors.Color.GREEN.value,
    100: colors.Color.LIGHTGREEN.value,
}


class BadgeGenerator:
    """A class to generate badges designed for use in a README.md file.

    Attributes:
        output_path (Path): Path to the output directory.
        python_version (str): Python version.
        tests_report_path (Path): Path to the unit tests XML report.
        coverage_report_path (Path): Path to the unit test coverage XML report.
    """

    def __init__(
        self,
        output_dir: str | Path,
        python_version: str | None,
        tests_report_path: str | Path,
        coverage_report_path: str | Path,
    ) -> None:
        """Initializes a BadgeGenerator instance."""
        self.output_path = Path(output_dir)
        self.python_version = python_version
        self.tests_report_path = Path(tests_report_path)
        self.coverage_report_path = Path(coverage_report_path)

    def generate_badges(self) -> None:
        """Generate project badges based on arguments provided to the class."""
        if self.python_version:
            self.make_badge(label="python", value=self.python_version, filename="python.svg", colour=colors.Color.BLUE)

        if self.tests_report_path:
            results = self.get_unittest_results()
            self.make_badge(label="unittest", value=results[0], filename="unittest.svg", colour=results[1])

        if self.coverage_report_path:
            results = self.get_coverage_results()
            self.make_coverage_badge(label="coverage", value=results, filename="coverage.svg")

    def make_badge(self, label: str, value: str, filename: str, colour: colors.Color) -> None:
        """Creates a badge using the given label, value and colour, saving the result to filename.

        Existing badges will be removed before the new badge is generated.
        Parameters:
            label (str): The label of the badge.
            value (str): The value of the badge.
            filename (str): The filename where the badge will be saved.
            colour (str | None): Optional colour of the badge.
                Anybadge will infer the colour if omitted and the value is an integer between 0 and 100.
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

        Returns a tuple of the test results and the colour of the badge.
        """
        root = ElementTree.parse(source=self.tests_report_path).getroot()

        failures = 0
        skipped = 0
        tests = 0
        for type_tag in root.findall("testsuite"):
            failures = int(type_tag.get("failures"))
            skipped = int(type_tag.get("skipped"))
            tests = int(type_tag.get("tests"))

        result_mapping = {
            failures > 0: (f"{failures} skipped {tests - failures} passed", colors.Color.RED),
            skipped > 0: (f"{skipped} skipped {tests - skipped} passed", colors.Color.YELLOW),
            failures == 0 and skipped == 0: (f"{tests} passed", colors.Color.GREEN),
        }

        return result_mapping.get(True)

    def get_coverage_results(self) -> float:
        """Read and return coverage from a unit-tests.xml file."""
        root = ElementTree.parse(source=self.coverage_report_path).getroot()
        coverage_score = root.attrib["line-rate"]
        if coverage_score == "1":
            return 100

        return round(100.0 * float(coverage_score), 1)


def main() -> None:
    """Main function for badge generation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output-dir", type=str, default="docs/img", help="Output directory for project badges")
    parser.add_argument("-pv", "--python-version", type=str, help="Supported python versions")
    parser.add_argument(
        "-trp",
        "--tests-report-path",
        type=str,
        default="reports/unit-tests.xml",
        help="Path to the unit tests XML report",
    )
    parser.add_argument(
        "-crp",
        "--coverage-report-path",
        type=str,
        default="reports/coverage.xml",
        help="Path to the unit test coverage XML report",
    )
    args = parser.parse_args()

    badge_generator = BadgeGenerator(
        output_dir=args.output_dir,
        python_version=args.python_version,
        tests_report_path=args.tests_report_path,
        coverage_report_path=args.coverage_report_path,
    )
    badge_generator.generate_badges()


if __name__ == "__main__":
    main()
