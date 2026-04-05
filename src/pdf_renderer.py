import logging
import os
import sys
from pathlib import Path

from src.constants import APP_NAME, MSYS2_DLL_DIR

if sys.platform == "win32" and Path(MSYS2_DLL_DIR).is_dir():
    os.add_dll_directory(MSYS2_DLL_DIR)

from weasyprint import HTML  # noqa: E402

logger = logging.getLogger(APP_NAME)


def render(html: str, output_path: Path, base_url: str) -> None:
    HTML(string=html, base_url=base_url).write_pdf(str(output_path))
    logger.info("PDF written to %s", output_path)
