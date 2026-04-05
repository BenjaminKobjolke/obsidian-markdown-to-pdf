from pathlib import Path

from src.constants import PAGE_BREAK_HTML
from src.obsidian_parser import (
    convert_page_breaks,
    convert_wiki_images,
    find_vault_root,
    make_image_paths_absolute,
    resolve_image_path,
    strip_frontmatter,
)


class TestStripFrontmatter:
    def test_removes_yaml_frontmatter(self) -> None:
        content = "---\nAuthor: Test\nDate: 2026-01-01\n---\nHello world"
        result = strip_frontmatter(content)
        assert result.strip() == "Hello world"

    def test_no_frontmatter_returns_content(self) -> None:
        content = "Just regular content"
        result = strip_frontmatter(content)
        assert result.strip() == "Just regular content"

    def test_frontmatter_does_not_become_page_break(self) -> None:
        content = "---\nkey: value\n---\nContent after frontmatter"
        result = strip_frontmatter(content)
        assert "---" not in result


class TestResolveImagePath:
    def test_finds_in_resources_dir(self, tmp_path: Path) -> None:
        resources = tmp_path / "_resources"
        resources.mkdir()
        (resources / "image.png").touch()
        result = resolve_image_path("image.png", tmp_path, None)
        assert result.startswith("file:///")
        assert "_resources/image.png" in result

    def test_finds_in_same_dir(self, tmp_path: Path) -> None:
        (tmp_path / "image.png").touch()
        result = resolve_image_path("image.png", tmp_path, None)
        assert result.startswith("file:///")
        assert "image.png" in result

    def test_resources_takes_priority(self, tmp_path: Path) -> None:
        resources = tmp_path / "_resources"
        resources.mkdir()
        (resources / "image.png").touch()
        (tmp_path / "image.png").touch()
        result = resolve_image_path("image.png", tmp_path, None)
        assert "_resources" in result

    def test_returns_original_when_not_found(self, tmp_path: Path) -> None:
        result = resolve_image_path("missing.png", tmp_path, None)
        assert result == "missing.png"

    def test_finds_in_vault_root_resources(self, tmp_path: Path) -> None:
        vault = tmp_path / "vault"
        vault.mkdir()
        (vault / ".obsidian").mkdir()
        vault_res = vault / "_resources"
        vault_res.mkdir()
        (vault_res / "image.png").touch()
        note_dir = vault / "subfolder"
        note_dir.mkdir()
        result = resolve_image_path("image.png", note_dir, vault)
        assert result.startswith("file:///")
        assert "_resources/image.png" in result


class TestConvertWikiImages:
    def test_converts_wiki_image_with_width(self, tmp_path: Path) -> None:
        (tmp_path / "_resources").mkdir()
        (tmp_path / "_resources" / "photo.png").touch()
        content = "![[photo.png|697]]"
        result = convert_wiki_images(content, tmp_path, None)
        assert "![697](" in result
        assert "photo.png" in result

    def test_converts_wiki_image_without_width(self, tmp_path: Path) -> None:
        (tmp_path / "photo.png").touch()
        content = "![[photo.png]]"
        result = convert_wiki_images(content, tmp_path, None)
        assert "![](" in result
        assert "photo.png" in result

    def test_leaves_standard_images_untouched(self, tmp_path: Path) -> None:
        content = "![alt](image.png)"
        result = convert_wiki_images(content, tmp_path, None)
        assert result == content


class TestFindVaultRoot:
    def test_finds_vault_with_obsidian_dir(self, tmp_path: Path) -> None:
        vault = tmp_path / "vault"
        vault.mkdir()
        (vault / ".obsidian").mkdir()
        sub = vault / "sub" / "deep"
        sub.mkdir(parents=True)
        result = find_vault_root(sub)
        assert result == vault.resolve()

    def test_returns_none_when_no_vault(self, tmp_path: Path) -> None:
        result = find_vault_root(tmp_path)
        assert result is None


class TestMakeImagePathsAbsolute:
    def test_makes_relative_paths_absolute(self) -> None:
        md_dir = Path("/docs/notes")
        content = "![alt](_resources/image.png)"
        result = make_image_paths_absolute(content, md_dir)
        assert "file:///" in result
        assert "_resources/image.png" in result

    def test_preserves_http_urls(self) -> None:
        md_dir = Path("/docs")
        content = "![alt](https://example.com/image.png)"
        result = make_image_paths_absolute(content, md_dir)
        assert "https://example.com/image.png" in result

    def test_preserves_absolute_paths(self) -> None:
        md_dir = Path("/docs")
        content = "![alt](/absolute/image.png)"
        result = make_image_paths_absolute(content, md_dir)
        assert "/absolute/image.png" in result

    def test_preserves_file_uris(self) -> None:
        md_dir = Path("/docs")
        content = "![697](file:///E:/vault/_resources/image.png)"
        result = make_image_paths_absolute(content, md_dir)
        assert "file:///E:/vault/_resources/image.png" in result


class TestConvertPageBreaks:
    def test_converts_triple_dash_to_page_break(self) -> None:
        content = "Some text\n---\nMore text"
        result = convert_page_breaks(content)
        assert PAGE_BREAK_HTML in result
        assert "---" not in result

    def test_converts_with_surrounding_whitespace(self) -> None:
        content = "Text\n  ---  \nMore"
        result = convert_page_breaks(content)
        assert PAGE_BREAK_HTML in result

    def test_preserves_dashes_in_text(self) -> None:
        content = "This has a dash-word and some---em-dash"
        result = convert_page_breaks(content)
        assert PAGE_BREAK_HTML not in result

    def test_multiple_page_breaks(self) -> None:
        content = "Page 1\n---\nPage 2\n---\nPage 3"
        result = convert_page_breaks(content)
        assert result.count(PAGE_BREAK_HTML) == 2
