from datetime import datetime
from pathlib import Path

import pytest
from src.constants import APP_NAME, NO_EXPORT_END, NO_EXPORT_START, PAGE_BREAK_HTML
from src.obsidian_parser import (
    convert_datetime_tags,
    convert_page_breaks,
    convert_wiki_images,
    extract_output_tag,
    find_vault_root,
    make_image_paths_absolute,
    parse,
    resolve_image_path,
    strip_frontmatter,
    strip_no_export_sections,
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

    def test_preserves_data_uris(self) -> None:
        md_dir = Path("/docs")
        content = "![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA4s=)"
        result = make_image_paths_absolute(content, md_dir)
        assert result == content


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


class TestStripNoExportSections:
    def test_removes_section_between_tags(self) -> None:
        content = f"Before\n{NO_EXPORT_START}\nSecret text\n{NO_EXPORT_END}\nAfter"
        result = strip_no_export_sections(content)
        assert "Secret text" not in result
        assert "Before" in result
        assert "After" in result

    def test_removes_multiple_blocks_keeps_between(self) -> None:
        content = (
            f"{NO_EXPORT_START}\nHidden 1\n{NO_EXPORT_END}\n"
            f"Visible middle\n"
            f"{NO_EXPORT_START}\nHidden 2\n{NO_EXPORT_END}\nEnd"
        )
        result = strip_no_export_sections(content)
        assert "Hidden 1" not in result
        assert "Hidden 2" not in result
        assert "Visible middle" in result
        assert "End" in result

    def test_unmatched_start_keeps_content_and_warns(self, caplog: pytest.LogCaptureFixture) -> None:
        content = f"Before\n{NO_EXPORT_START}\nStill here\nAfter"
        with caplog.at_level("WARNING", logger=APP_NAME):
            result = strip_no_export_sections(content)
        assert "Still here" in result
        assert NO_EXPORT_START not in result
        assert "Unmatched" in caplog.text

    def test_no_tags_content_unchanged(self) -> None:
        content = "Just regular content\nwith lines"
        assert strip_no_export_sections(content) == content

    def test_inline_tag_not_matched(self) -> None:
        content = f"Text mentioning {NO_EXPORT_START} inline stays"
        result = strip_no_export_sections(content)
        assert "inline stays" in result


class TestConvertDatetimeTags:
    NOW = datetime(2025, 7, 16, 8, 31, 5)

    def test_date_default_format(self) -> None:
        assert convert_datetime_tags("[date]", now=self.NOW) == "16.07.2025"

    def test_time_default_format(self) -> None:
        assert convert_datetime_tags("[time]", now=self.NOW) == "08:31"

    def test_date_custom_format(self) -> None:
        assert convert_datetime_tags('[date format="YYMMDD"]', now=self.NOW) == "250716"

    def test_time_custom_format_with_seconds(self) -> None:
        assert convert_datetime_tags('[time format="HH:mm:ss"]', now=self.NOW) == "08:31:05"

    def test_literal_chars_pass_through(self) -> None:
        assert convert_datetime_tags('[date format="YYYY-MM-DD"]', now=self.NOW) == "2025-07-16"

    def test_inline_usage_replaces_both(self) -> None:
        result = convert_datetime_tags("Created: [date] at [time]", now=self.NOW)
        assert result == "Created: 16.07.2025 at 08:31"

    def test_no_tags_content_unchanged(self) -> None:
        content = "Just regular content\nwith [brackets] but no tags"
        assert convert_datetime_tags(content, now=self.NOW) == content

    def test_wrong_case_untouched(self) -> None:
        content = "[DATE] and [Time]"
        assert convert_datetime_tags(content, now=self.NOW) == content


class TestExtractOutputTag:
    def test_extracts_value_and_strips_tag(self) -> None:
        result = extract_output_tag('Text\n[output="./pdfs"]\nMore')
        assert result.output_tag == "./pdfs"
        assert "[output" not in result.content
        assert "Text" in result.content
        assert "More" in result.content

    def test_no_tag_returns_none_content_unchanged(self) -> None:
        content = "Just regular content\nwith [brackets]"
        result = extract_output_tag(content)
        assert result.output_tag is None
        assert result.content == content

    def test_multiple_tags_first_wins_and_warns(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level("WARNING", logger=APP_NAME):
            result = extract_output_tag('[output="./a"]\ntext\n[output="./b"]')
        assert result.output_tag == "./a"
        assert "[output" not in result.content
        assert "Multiple" in caplog.text

    def test_empty_value_warns_and_returns_none(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level("WARNING", logger=APP_NAME):
            result = extract_output_tag('[output=""]')
        assert result.output_tag is None
        assert "[output" not in result.content
        assert "empty" in caplog.text

    def test_whitespace_value_treated_as_empty(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level("WARNING", logger=APP_NAME):
            result = extract_output_tag('[output="   "]')
        assert result.output_tag is None

    def test_wrong_case_stays_literal(self) -> None:
        content = '[OUTPUT="./pdfs"]'
        result = extract_output_tag(content)
        assert result.output_tag is None
        assert result.content == content


class TestParseOutputTag:
    def test_parse_returns_result_with_output_tag(self, tmp_path: Path) -> None:
        result = parse('Hello\n[output="./pdfs"]', tmp_path)
        assert result.output_tag == "./pdfs"
        assert "[output" not in result.content
        assert "Hello" in result.content

    def test_parse_without_tag_returns_none(self, tmp_path: Path) -> None:
        result = parse("Hello world", tmp_path)
        assert result.output_tag is None
        assert "Hello world" in result.content

    def test_tag_inside_no_export_ignored(self, tmp_path: Path) -> None:
        content = f'Before\n{NO_EXPORT_START}\n[output="./hidden"]\n{NO_EXPORT_END}\nAfter'
        result = parse(content, tmp_path)
        assert result.output_tag is None

    def test_tag_in_frontmatter_ignored(self, tmp_path: Path) -> None:
        content = "---\nnote: '[output=\"./fm\"]'\n---\nBody"
        result = parse(content, tmp_path)
        assert result.output_tag is None
        assert "Body" in result.content
