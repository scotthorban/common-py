"""A module to generate project badges designed for use in a README.md file."""

import argparse
import subprocess
from pathlib import Path

RED = "#be403c"
YELLOW = "#c8991d"
GREEN = "#00a10b"
BLUE = "#0f5fa5"


class BadgeGenerator:
    """A class to generate badges designed for use in a README.md file.

    Attributes:
        output_dir (Path): Path to the output directory.
    """

    def __init__(self, output_dir: str | Path, python_version: str | None) -> None:
        """Initializes a BadgeGenerator instance."""
        self.output_dir = output_dir if isinstance(output_dir, Path) else Path(output_dir)
        self.python_version = python_version

    def generate_badges(self) -> None:
        """Generate project badges based on arguments provided to the class."""
        if self.python_version:
            self.make_badge(label="python", value=self.python_version, filename="python.svg", color=BLUE)

    def make_badge(self, label: str, value: str, filename: str, color: str) -> None:
        """Creates a badge using the given label, value and color, saving the result to filename.

        Existing badges will be removed before the new badge is generated.
        Parameters:
            label (str): The label of the badge.
            value (str): The value of the badge.
            filename (str): The filename where the badge will be saved.
            color (str): The color of the badge.
        """
        img_path = self.output_dir.joinpath(filename)
        img_path.unlink(missing_ok=True)

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
                str(img_path),
                "--color",
                color,
            ],
            check=False,
        )


def main() -> None:
    """Main function for badge generation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output-dir", type=str, default="docs/img", help="Output directory for project badges")
    parser.add_argument(
        "-pv",
        "--python-version",
        type=str,
        help="Supported python versions",
    )
    args = parser.parse_args()

    badge_generator = BadgeGenerator(output_dir=args.output_dir, python_version=args.python_version)
    badge_generator.generate_badges()


if __name__ == "__main__":
    main()
