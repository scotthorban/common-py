"""A script to generate project badges designed for use in a README.md file."""

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from defusedxml import ElementTree

from definitions import PROJECT_ROOT_DIR

IMG_PATH = PROJECT_ROOT_DIR.joinpath("docs/img")


def make_badge(label: str, value: str, filename: str, color: str) -> None:
    """Creates a badge using the given label, value and color, saving the result to filename.

    Parameters:
        label (str): The label of the badge.
        value (str): The value of the badge.
        filename (str): The filename where the badge will be saved.
        color (str): The color of the badge.
    """
    subprocess.run(
        args=[
            "uv",
            "run",
            "anybadge",
            "-l",
            label,
            "-v",
            str(value),
            "-f",
            filename,
            "--color",
            color,
        ],
        check=False,
    )


def get_python_version() -> str:
    """Return Python version."""
    return "3.11"


def get_ruff_result() -> str:
    """Read and return Ruff result from PROJECT_ROOT_DIR/reports/linting.txt."""
    report_path = PROJECT_ROOT_DIR.joinpath("reports/ruff.json")
    with Path.open(report_path) as linting_file:
        content = json.load(fp=linting_file)

    return "Passing" if content == [] else "Failing"


def get_unittest_results() -> str:
    """Read and return test results from PROJECT_ROOT_DIR/reports/unit-tests.xml."""
    test_report_path = PROJECT_ROOT_DIR.joinpath("reports/unit-tests.xml")
    root = ElementTree.parse(test_report_path).getroot()

    failures = 0
    skipped = 0
    tests = 0
    for type_tag in root.findall("testsuite"):
        failures = int(type_tag.get("failures"))
        skipped = int(type_tag.get("skipped"))
        tests = int(type_tag.get("tests"))

    text = ""
    if failures > 0:
        text = f"{failures} skipped {tests - failures} passed"

    if skipped > 0:
        text = f"{skipped} skipped {tests - skipped} passed"

    if failures == 0 and skipped == 0:
        text = f"{tests} passed"

    return text


def get_coverage_score() -> str:
    """Read and return Coverage from PROJECT_ROOT_DIR/reports/coverage.xml."""
    coverage_report_path = PROJECT_ROOT_DIR.joinpath("reports/coverage.xml")
    root = ElementTree.parse(coverage_report_path).getroot()
    coverage_score = root.attrib["line-rate"]
    if coverage_score == "1":
        return "100%"

    return f"{round(100.0 * float(coverage_score), 1)}%"


def make_badges() -> None:
    """Creates all project badges."""
    red = "#be403c"
    warn = "#c8991d"
    green = "#00a10b"

    python_version = get_python_version()
    Path(f"{IMG_PATH}/python.svg").unlink(missing_ok=True)

    make_badge(
        label="python",
        value=python_version,
        filename=f"{IMG_PATH}/python.svg",
        color="#0f5fa5",
    )

    unittest_results = get_unittest_results()
    if unittest_results:
        Path(f"{IMG_PATH}/unittest.svg").unlink(missing_ok=True)

        if "failed" in unittest_results:
            make_badge(
                label="unittest",
                value=unittest_results,
                filename=f"{IMG_PATH}/unittest.svg",
                color=red,
            )
        elif "skipped" in unittest_results:
            make_badge(
                label="unittest",
                value=unittest_results,
                filename=f"{IMG_PATH}/unittest.svg",
                color=warn,
            )
        else:
            make_badge(
                label="unittest",
                value=unittest_results,
                filename=f"{IMG_PATH}/unittest.svg",
                color=green,
            )

    coverage_score = get_coverage_score()
    if coverage_score:
        Path(f"{IMG_PATH}/coverage.svg").unlink(missing_ok=True)

        subprocess.run(
            args=[
                "uv",
                "run",
                "anybadge",
                "-l",
                "coverage",
                "-v",
                coverage_score,
                "-f",
                f"{IMG_PATH}/coverage.svg",
            ],
            check=True,
        )

    ruff_result = get_ruff_result()
    if ruff_result:
        Path(f"{IMG_PATH}/ruff.svg").unlink(missing_ok=True)

        color = "green" if ruff_result == "Passing" else "red"
        make_badge(
            label="ruff",
            value=ruff_result,
            filename=f"{IMG_PATH}/ruff.svg",
            color=color,
        )

    Path(f"{IMG_PATH}/release.svg").unlink(missing_ok=True)

    current_month = datetime.now(tz=UTC).strftime("%b")
    current_year = datetime.now(tz=UTC).year

    make_badge(
        label="released",
        value=f"{current_month} {current_year}",
        filename=f"{IMG_PATH}/release.svg",
        color="#0f5fa5",
    )


if __name__ == "__main__":
    make_badges()
