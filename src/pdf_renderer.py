import os
import sys
from pathlib import Path

from src.app_logger import AppLogger
from src.constants import MSYS2_DLL_DIR

if sys.platform == "win32" and Path(MSYS2_DLL_DIR).is_dir():
    os.add_dll_directory(MSYS2_DLL_DIR)

from weasyprint import HTML  # noqa: E402


def render(html: str, output_path: Path, base_url: str) -> None:
    HTML(string=html, base_url=base_url).write_pdf(str(output_path))
    AppLogger.info("PDF written to %s", output_path)
