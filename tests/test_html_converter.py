from pathlib import Path

from src.html_converter import convert, markdown_to_html, wrap_html
from src.obsidian_parser import parse


class TestMarkdownToHtml:
    def test_converts_heading(self) -> None:
        result = markdown_to_html("## Hello")
        assert "<h2" in result
        assert "Hello" in result

    def test_converts_table(self) -> None:
        table = "|A|B|\n|---|---|\n|1|2|"
        result = markdown_to_html(table)
        assert "<table>" in result
        assert "<td>1</td>" in result

    def test_converts_paragraph(self) -> None:
        result = markdown_to_html("Some text here")
        assert "<p>Some text here</p>" in result


class TestWrapHtml:
    def test_wraps_with_html_structure(self) -> None:
        result = wrap_html("<p>Test</p>")
        assert "<!DOCTYPE html>" in result
        assert "<style>" in result
        assert "<body>" in result
        assert "<p>Test</p>" in result


class TestConvert:
    def test_full_conversion(self) -> None:
        md = "## Title\n\nSome paragraph."
        result = convert(md)
        assert "<!DOCTYPE html>" in result
        assert "<h2" in result
        assert "Some paragraph" in result

    def test_toc_generates_clickable_links(self) -> None:
        result = convert("[TOC]\n\n# Alpha\n\n## Beta One")
        assert 'class="toc"' in result
        assert '<a href="#alpha">Alpha</a>' in result
        assert '<a href="#beta-one">Beta One</a>' in result
        assert '<h1 id="alpha">' in result
        assert '<h2 id="beta-one">' in result


class TestTocScope:
    def test_excludes_headings_before_marker(self) -> None:
        result = convert("# Cheat Sheet\n\n[TOC]\n\n# Setup\n\n## Wifi")
        # Heading above the marker still renders but is not in the ToC.
        assert "<h1>Cheat Sheet</h1>" in result
        assert '<a href="#cheat-sheet">' not in result
        # Headings below the marker are listed.
        assert '<a href="#setup">Setup</a>' in result
        assert '<a href="#wifi">Wifi</a>' in result

    def test_per_heading_omit(self) -> None:
        result = convert("[TOC]\n\n# Setup\n\n## Secret { .toc-omit }\n\n## Theme")
        # Omitted heading renders but is excluded from the ToC.
        assert "Secret</h2>" in result
        assert '<a href="#secret">' not in result
        assert '<a href="#theme">Theme</a>' in result

    def test_no_marker_lists_all_headings(self) -> None:
        # Without a marker, no positional hiding: headings still get ids.
        result = convert("# Alpha\n\n## Beta")
        assert '<h1 id="alpha">' in result
        assert '<h2 id="beta">' in result


class TestNoExportIntegration:
    def test_stripped_section_absent_from_pdf_and_toc(self, tmp_path: Path) -> None:
        md = "[TOC]\n\n# Visible\n\nKeep this.\n\n[NO-EXPORT]\n# Hidden\n\nDrop this.\n[/NO-EXPORT]\n\n## Also Visible"
        result = convert(parse(md, tmp_path).content)
        assert "Hidden" not in result
        assert "Drop this" not in result
        assert '<a href="#visible">Visible</a>' in result
        assert '<a href="#also-visible">Also Visible</a>' in result
