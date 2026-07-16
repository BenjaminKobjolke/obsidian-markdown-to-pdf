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
    parser.add_argument(
        "--default-output",
        required=False,
        default=None,
        help="Fallback output directory or .pdf path, overridable by the note's [output] tag",
    )
    return parser.parse_args(argv)


def resolve_output_path(
    input_path: Path,
    output_arg: str | None,
    tag_value: str | None = None,
    vault_root: Path | None = None,
    default_output: str | None = None,
) -> Path:
    if output_arg is not None:
        output = Path(output_arg)
        if output.parent == Path("."):
            return input_path.parent / output
        return output

    if tag_value is not None:
        return _resolve_tag_output(tag_value, input_path, vault_root)

    if default_output is not None:
        return _resolve_tag_output(default_output, input_path, vault_root)

    return input_path.with_suffix(".pdf")


def _resolve_tag_output(tag_value: str, input_path: Path, vault_root: Path | None) -> Path:
    target = Path(tag_value)
    if not target.is_absolute():
        anchor = vault_root if vault_root is not None else input_path.parent
        target = anchor / target
    if target.suffix.lower() == ".pdf":
        return target
    return target / f"{input_path.stem}.pdf"
