from pathlib import Path

from src.cli import parse_args, resolve_output_path


class TestParseArgs:
    def test_input_required(self) -> None:
        args = parse_args(["--input", "test.md"])
        assert args.input == "test.md"
        assert args.output is None

    def test_input_and_output(self) -> None:
        args = parse_args(["--input", "test.md", "--output", "out.pdf"])
        assert args.input == "test.md"
        assert args.output == "out.pdf"


class TestResolveOutputPath:
    def test_no_output_uses_input_with_pdf_extension(self) -> None:
        result = resolve_output_path(Path("/docs/note.md"), None)
        assert result == Path("/docs/note.pdf")

    def test_output_filename_only_uses_input_directory(self) -> None:
        result = resolve_output_path(Path("/docs/note.md"), "custom.pdf")
        assert result == Path("/docs/custom.pdf")

    def test_output_with_full_path(self) -> None:
        result = resolve_output_path(Path("/docs/note.md"), "/output/result.pdf")
        assert result == Path("/output/result.pdf")

    def test_output_with_relative_path(self) -> None:
        result = resolve_output_path(Path("/docs/note.md"), "sub/result.pdf")
        assert result == Path("sub/result.pdf")
