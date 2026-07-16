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

    def test_default_output(self) -> None:
        args = parse_args(["--input", "test.md", "--default-output", "D:/exports"])
        assert args.default_output == "D:/exports"
        assert args.output is None


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


class TestResolveOutputPathTag:
    def test_cli_output_wins_over_tag(self) -> None:
        result = resolve_output_path(Path("/docs/note.md"), "cli.pdf", tag_value="./pdfs", vault_root=Path("/vault"))
        assert result == Path("/docs/cli.pdf")

    def test_tag_directory_relative_to_vault_root(self, tmp_path: Path) -> None:
        vault = tmp_path / "vault"
        result = resolve_output_path(vault / "sub" / "note.md", None, tag_value="./pdfs", vault_root=vault)
        assert result == vault / "pdfs" / "note.pdf"

    def test_tag_directory_without_vault_root_uses_note_dir(self, tmp_path: Path) -> None:
        result = resolve_output_path(tmp_path / "note.md", None, tag_value="./pdfs", vault_root=None)
        assert result == tmp_path / "pdfs" / "note.pdf"

    def test_tag_pdf_value_is_full_file_path(self, tmp_path: Path) -> None:
        result = resolve_output_path(tmp_path / "note.md", None, tag_value="./pdfs/custom.pdf", vault_root=tmp_path)
        assert result == tmp_path / "pdfs" / "custom.pdf"

    def test_tag_absolute_directory(self, tmp_path: Path) -> None:
        target = tmp_path / "exports"
        result = resolve_output_path(Path("/docs/note.md"), None, tag_value=str(target), vault_root=None)
        assert result == target / "note.pdf"

    def test_tag_absolute_pdf_path(self, tmp_path: Path) -> None:
        target = tmp_path / "exports" / "final.pdf"
        result = resolve_output_path(Path("/docs/note.md"), None, tag_value=str(target), vault_root=None)
        assert result == target

    def test_tag_trailing_slash_normalized(self, tmp_path: Path) -> None:
        result = resolve_output_path(tmp_path / "note.md", None, tag_value="./pdfs/", vault_root=tmp_path)
        assert result == tmp_path / "pdfs" / "note.pdf"

    def test_uppercase_pdf_suffix_is_file_path(self, tmp_path: Path) -> None:
        result = resolve_output_path(tmp_path / "note.md", None, tag_value="./OUT.PDF", vault_root=tmp_path)
        assert result == tmp_path / "OUT.PDF"

    def test_no_tag_no_cli_uses_default(self) -> None:
        result = resolve_output_path(Path("/docs/note.md"), None, tag_value=None, vault_root=None)
        assert result == Path("/docs/note.pdf")


class TestResolveOutputPathDefaultOutput:
    def test_tag_beats_default_output(self, tmp_path: Path) -> None:
        result = resolve_output_path(
            tmp_path / "note.md", None, tag_value="./pdfs", vault_root=tmp_path, default_output="D:/exports"
        )
        assert result == tmp_path / "pdfs" / "note.pdf"

    def test_default_output_dir_appends_note_name(self, tmp_path: Path) -> None:
        target = tmp_path / "exports"
        result = resolve_output_path(tmp_path / "note.md", None, default_output=str(target))
        assert result == target / "note.pdf"

    def test_default_output_pdf_value_is_full_file_path(self, tmp_path: Path) -> None:
        target = tmp_path / "exports" / "final.pdf"
        result = resolve_output_path(tmp_path / "note.md", None, default_output=str(target))
        assert result == target

    def test_cli_output_beats_default_output(self) -> None:
        result = resolve_output_path(Path("/docs/note.md"), "cli.pdf", default_output="D:/exports")
        assert result == Path("/docs/cli.pdf")

    def test_no_default_output_falls_back_to_note_dir(self) -> None:
        result = resolve_output_path(Path("/docs/note.md"), None, default_output=None)
        assert result == Path("/docs/note.pdf")
