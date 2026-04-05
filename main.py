#!/usr/bin/env python3
import sys
from pathlib import Path

from src.cli import parse_args, resolve_output_path
from src.constants import ERR_CONVERSION_FAILED, ERR_INPUT_NOT_FOUND
from src.html_converter import convert
from src.logger import get_logger
from src.obsidian_parser import parse
from src.pdf_renderer import render


def main() -> int:
    logger = get_logger()
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        logger.error(ERR_INPUT_NOT_FOUND.format(path=input_path))
        return 1

    output_path = resolve_output_path(input_path, args.output)

    try:
        md_content = input_path.read_text(encoding="utf-8")
        md_dir = input_path.parent.resolve()

        parsed = parse(md_content, md_dir)
        html = convert(parsed)
        render(html, output_path, base_url=str(md_dir))

        logger.info("Converted %s -> %s", input_path.name, output_path)
    except Exception as exc:
        logger.error(ERR_CONVERSION_FAILED.format(error=exc))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
