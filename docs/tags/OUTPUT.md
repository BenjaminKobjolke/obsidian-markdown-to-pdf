# `[output="..."]` — Override the PDF output path

Let a note declare where its exported PDF is written, instead of the default
(next to the markdown file).

## Usage

Put the tag anywhere in the note; it is removed from the rendered PDF:

```markdown
[output="./pdfs"]
```

The value is either a **directory** or a **file path**:

| Value | Result |
| --- | --- |
| `[output="./pdfs"]` | `<vault>/pdfs/<note-name>.pdf` |
| `[output="./pdfs/report.pdf"]` | `<vault>/pdfs/report.pdf` |
| `[output="C:/exports"]` | `C:/exports/<note-name>.pdf` |
| `[output="C:/exports/final.pdf"]` | `C:/exports/final.pdf` |

A value ending in `.pdf` (case-insensitive) is treated as the full file path;
anything else as a directory, with the PDF keeping the note's name.

Relative paths resolve against the **vault root** (the folder containing
`.obsidian/`). Outside a vault they resolve against the note's own directory.
Missing directories are created automatically.

The tag is lowercase and case-sensitive: `[OUTPUT="x"]` stays literal text.

## Precedence

| Given | Output path |
| --- | --- |
| CLI `--output` | CLI value wins, tag ignored |
| Tag | Tag value as described above |
| CLI `--default-output` | Fallback with the same dir/`.pdf` semantics — used only when no tag |
| None of the above | Next to the markdown file, `.pdf` extension |

The Obsidian plugin passes its **Export folder** setting as `--default-output`,
so a note's `[output]` tag overrides the plugin's export folder.

## Notes

- Multiple `[output]` tags: the first wins, all are stripped, a warning is
  logged.
- An empty value (`[output=""]`) is ignored with a warning.
- Tags inside `[NO-EXPORT]` sections or YAML frontmatter are ignored.

## How it works

`extract_output_tag` (`src/obsidian_parser.py`) pulls the value out during
parsing (after `[NO-EXPORT]` stripping) and returns it in `ParseResult`;
`resolve_output_path` (`src/cli.py`) applies precedence and resolves the
final path.

Relevant files:

- `src/obsidian_parser.py` — `OUTPUT_TAG_PATTERN`, `extract_output_tag`,
  `ParseResult`
- `src/cli.py` — `resolve_output_path`, `_resolve_tag_output`
- `src/constants.py` — `OUTPUT_TAG`
