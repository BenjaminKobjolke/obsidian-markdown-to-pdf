import argparse
from pathlib import Path

from src.constants import APP_DESCRIPTION


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=APP_DESCRIPTION)
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the Obsidian markdown file",
    )
    parser.add_argument(
        "--output",
        required=False,
        default=None,
        help="Output PDF path (optional)",
    )
    return parser.parse_args(argv)


def resolve_output_path(input_path: Path, output_arg: str | None) -> Path:
    if output_arg is None:
        return input_path.with_suffix(".pdf")

    output = Path(output_arg)

    if output.parent == Path("."):
        return input_path.parent / output

    return output
