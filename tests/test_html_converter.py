from src.html_converter import convert, markdown_to_html, wrap_html


class TestMarkdownToHtml:
    def test_converts_heading(self) -> None:
        result = markdown_to_html("## Hello")
        assert "<h2>" in result
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
        assert "<h2>" in result
        assert "Some paragraph" in result
