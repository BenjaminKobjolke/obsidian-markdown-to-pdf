import sys
from pathlib import Path

import pytest
from main import main


def _make_vault(tmp_path: Path, note_content: str) -> Path:
    vault = tmp_path / "vault"
    (vault / ".obsidian").mkdir(parents=True)
    note_dir = vault / "notes"
    note_dir.mkdir()
    note = note_dir / "note.md"
    note.write_text(note_content, encoding="utf-8")
    return note


@pytest.mark.integration
class TestOutputTagEndToEnd:
    def test_output_tag_writes_pdf_to_vault_relative_dir(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        note = _make_vault(tmp_path, '# Title\n\n[output="./pdfs"]\n\nBody text')
        monkeypatch.setattr(sys, "argv", ["main.py", "--input", str(note)])
        assert main() == 0
        expected = tmp_path / "vault" / "pdfs" / "note.pdf"
        assert expected.is_file()
        assert expected.stat().st_size > 0

    def test_cli_output_overrides_tag(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        note = _make_vault(tmp_path, '# Title\n\n[output="./pdfs"]\n\nBody')
        cli_target = tmp_path / "cli_out" / "result.pdf"
        cli_target.parent.mkdir()
        monkeypatch.setattr(sys, "argv", ["main.py", "--input", str(note), "--output", str(cli_target)])
        assert main() == 0
        assert cli_target.is_file()
        assert not (tmp_path / "vault" / "pdfs").exists()

    def test_output_pdf_value_used_as_exact_file_path(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        note = _make_vault(tmp_path, '# Title\n\n[output="./exports/custom.pdf"]\n\nBody')
        monkeypatch.setattr(sys, "argv", ["main.py", "--input", str(note)])
        assert main() == 0
        assert (tmp_path / "vault" / "exports" / "custom.pdf").is_file()

    def test_tag_wins_over_default_output(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        note = _make_vault(tmp_path, '# Title\n\n[output="./pdfs"]\n\nBody')
        fallback = tmp_path / "fallback"
        monkeypatch.setattr(sys, "argv", ["main.py", "--input", str(note), "--default-output", str(fallback)])
        assert main() == 0
        assert (tmp_path / "vault" / "pdfs" / "note.pdf").is_file()
        assert not fallback.exists()

    def test_default_output_used_without_tag(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        note = _make_vault(tmp_path, "# Title\n\nBody")
        fallback = tmp_path / "fallback"
        monkeypatch.setattr(sys, "argv", ["main.py", "--input", str(note), "--default-output", str(fallback)])
        assert main() == 0
        assert (fallback / "note.pdf").is_file()
