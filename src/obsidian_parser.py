import re
from pathlib import Path

import frontmatter

from src.constants import PAGE_BREAK_HTML, RESOURCES_DIR

WIKI_IMAGE_PATTERN = re.compile(r"!\[\[([^\]|]+?)(?:\|(\d+))?\]\]")
PAGE_BREAK_PATTERN = re.compile(r"^\s*---\s*$", re.MULTILINE)
STANDARD_IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


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
        if path.startswith(("http://", "https://", "/", "file:///")):
            return match.group(0)
        absolute = md_dir / path
        return f"![{alt}]({_path_to_uri(absolute)})"

    return STANDARD_IMAGE_PATTERN.sub(_replace, content)


def convert_page_breaks(content: str) -> str:
    return PAGE_BREAK_PATTERN.sub(PAGE_BREAK_HTML, content)


def parse(content: str, md_dir: Path) -> str:
    vault_root = find_vault_root(md_dir)
    result = strip_frontmatter(content)
    result = convert_wiki_images(result, md_dir, vault_root)
    result = make_image_paths_absolute(result, md_dir)
    result = convert_page_breaks(result)
    return result
