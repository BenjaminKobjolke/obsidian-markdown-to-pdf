#!/usr/bin/env python3
import sys
from pathlib import Path

from src.app_logger import AppLogger
from src.cli import parse_args, resolve_output_path
from src.constants import ERR_CONVERSION_FAILED, ERR_INPUT_NOT_FOUND
from src.html_converter import convert
from src.obsidian_parser import find_vault_root, parse
from src.pdf_renderer import render


def main() -> int:
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        AppLogger.error(ERR_INPUT_NOT_FOUND.format(path=input_path))
        return 1

    try:
        md_content = input_path.read_text(encoding="utf-8")
        md_dir = input_path.parent.resolve()

        parsed = parse(md_content, md_dir)
        vault_root = find_vault_root(md_dir)
        output_path = resolve_output_path(input_path, args.output, parsed.output_tag, vault_root, args.default_output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        html = convert(parsed.content)
        render(html, output_path, base_url=str(md_dir))

        AppLogger.info("Converted %s -> %s", input_path.name, output_path)
    except Exception as exc:
        AppLogger.error(ERR_CONVERSION_FAILED.format(error=exc))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
