import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import frontmatter

from src.app_logger import AppLogger
from src.constants import (
    DATE_TAG,
    DEFAULT_DATE_FORMAT,
    DEFAULT_TIME_FORMAT,
    NO_EXPORT_END,
    NO_EXPORT_START,
    OUTPUT_TAG,
    PAGE_BREAK_HTML,
    RESOURCES_DIR,
    TIME_TAG,
)

WIKI_IMAGE_PATTERN = re.compile(r"!\[\[([^\]|]+?)(?:\|(\d+))?\]\]")
PAGE_BREAK_PATTERN = re.compile(r"^\s*---\s*$", re.MULTILINE)
STANDARD_IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
NO_EXPORT_PATTERN = re.compile(
    rf"^[ \t]*{re.escape(NO_EXPORT_START)}[ \t]*\r?\n"
    rf".*?"
    rf"^[ \t]*{re.escape(NO_EXPORT_END)}[ \t]*(?:\r?\n|$)",
    re.DOTALL | re.MULTILINE,
)
_NO_EXPORT_TAG_LINE = re.compile(
    rf"^[ \t]*(?:{re.escape(NO_EXPORT_START)}|{re.escape(NO_EXPORT_END)})[ \t]*(?:\r?\n|$)",
    re.MULTILINE,
)
DATETIME_TAG_PATTERN = re.compile(rf"\[({re.escape(DATE_TAG)}|{re.escape(TIME_TAG)})(?:\s+format=\"([^\"]*)\")?\]")
OUTPUT_TAG_PATTERN = re.compile(rf"\[{re.escape(OUTPUT_TAG)}=\"([^\"]*)\"\]")
# Moment.js tokens (Obsidian convention) → strftime; longest-first so YYYY wins over YY
_MOMENT_TOKEN_PATTERN = re.compile(r"dddd|ddd|MMMM|MMM|YYYY|YY|MM|DD|HH|hh|mm|ss|A")
_MOMENT_TO_STRFTIME = {
    "dddd": "%A",
    "ddd": "%a",
    "MMMM": "%B",
    "MMM": "%b",
    "YYYY": "%Y",
    "YY": "%y",
    "MM": "%m",
    "DD": "%d",
    "HH": "%H",
    "hh": "%I",
    "mm": "%M",
    "ss": "%S",
    "A": "%p",
}


def strip_frontmatter(content: str) -> str:
    post = frontmatter.loads(content)
    return str(post.content)


def _path_to_uri(path: Path) -> str:
    return path.resolve().as_uri()


def find_vault_root(md_dir: Path) -> Path | None:
    current = md_dir.resolve()
    while current != current.parent:
        if (current / ".obsidian").is_dir():
            return current
        current = current.parent
    return None


def resolve_image_path(image_name: str, md_dir: Path, vault_root: Path | None) -> str:
    resources_path = md_dir / RESOURCES_DIR / image_name
    if resources_path.exists():
        return _path_to_uri(resources_path)

    same_dir_path = md_dir / image_name
    if same_dir_path.exists():
        return _path_to_uri(same_dir_path)

    if vault_root and vault_root != md_dir:
        vault_resources = vault_root / RESOURCES_DIR / image_name
        if vault_resources.exists():
            return _path_to_uri(vault_resources)

        vault_same = vault_root / image_name
        if vault_same.exists():
            return _path_to_uri(vault_same)

    return image_name


def convert_wiki_images(content: str, md_dir: Path, vault_root: Path | None) -> str:
    def _replace(match: re.Match[str]) -> str:
        image_name = match.group(1).strip()
        width = match.group(2)
        resolved = resolve_image_path(image_name, md_dir, vault_root)
        if not resolved.startswith("file:///"):
            width_attr = f' width="{width}"' if width else ""
            return f'<img alt="{image_name}" src="{image_name}"{width_attr} />'
        alt = width if width else ""
        return f"![{alt}]({resolved})"

    return WIKI_IMAGE_PATTERN.sub(_replace, content)


def make_image_paths_absolute(content: str, md_dir: Path) -> str:
    def _replace(match: re.Match[str]) -> str:
        alt = match.group(1)
        path = match.group(2)
        if path.startswith(("http://", "https://", "/", "file:///", "data:")):
            return match.group(0)
        absolute = md_dir / path
        return f"![{alt}]({_path_to_uri(absolute)})"

    return STANDARD_IMAGE_PATTERN.sub(_replace, content)


def convert_page_breaks(content: str) -> str:
    return PAGE_BREAK_PATTERN.sub(PAGE_BREAK_HTML, content)


def strip_no_export_sections(content: str) -> str:
    result = NO_EXPORT_PATTERN.sub("", content)
    if NO_EXPORT_START in result or NO_EXPORT_END in result:
        AppLogger.warning("Unmatched %s/%s tag — section kept in export", NO_EXPORT_START, NO_EXPORT_END)
        result = _NO_EXPORT_TAG_LINE.sub("", result)
    return result


def _moment_to_strftime(fmt: str) -> str:
    return _MOMENT_TOKEN_PATTERN.sub(lambda m: _MOMENT_TO_STRFTIME[m.group(0)], fmt)


@dataclass(frozen=True)
class ParseResult:
    content: str
    output_tag: str | None


def extract_output_tag(content: str) -> ParseResult:
    matches = OUTPUT_TAG_PATTERN.findall(content)
    stripped = OUTPUT_TAG_PATTERN.sub("", content)
    if not matches:
        return ParseResult(content=stripped, output_tag=None)
    if len(matches) > 1:
        AppLogger.warning("Multiple [%s] tags — using the first", OUTPUT_TAG)
    value = matches[0].strip()
    if not value:
        AppLogger.warning("[%s] tag has empty value — ignored", OUTPUT_TAG)
        return ParseResult(content=stripped, output_tag=None)
    return ParseResult(content=stripped, output_tag=value)


def convert_datetime_tags(content: str, now: datetime | None = None) -> str:
    moment = now if now is not None else datetime.now()

    def _replace(match: re.Match[str]) -> str:
        tag, fmt = match.group(1), match.group(2)
        if fmt is None:
            fmt = DEFAULT_DATE_FORMAT if tag == DATE_TAG else DEFAULT_TIME_FORMAT
        return moment.strftime(_moment_to_strftime(fmt))

    return DATETIME_TAG_PATTERN.sub(_replace, content)


def parse(content: str, md_dir: Path) -> ParseResult:
    vault_root = find_vault_root(md_dir)
    result = strip_frontmatter(content)
    result = strip_no_export_sections(result)
    extraction = extract_output_tag(result)
    result = convert_datetime_tags(extraction.content)
    result = convert_wiki_images(result, md_dir, vault_root)
    result = make_image_paths_absolute(result, md_dir)
    result = convert_page_breaks(result)
    return ParseResult(content=result, output_tag=extraction.output_tag)
