# `[NO-EXPORT]` … `[/NO-EXPORT]` — Exclude a section from export

Mark a section of a note that must not appear in the exported PDF.

## Usage

Put each tag on its own line. Everything between them (tags included) is
removed before conversion:

```markdown
Visible text.

[NO-EXPORT]
# Private heading

Draft notes, todo lists, anything not meant for the PDF.
[/NO-EXPORT]

More visible text.
```

Multiple blocks per document are fine. The tags are exact and case-sensitive:
`[NO-EXPORT]` / `[/NO-EXPORT]`.

Because the section is stripped before any other processing, its headings never
show up in a `[TOC]`, and its images are never resolved.

> In Obsidian's own preview the tags show as literal text — only this exporter
> consumes them.

## Unmatched tags

A start tag without a matching end tag (or a stray end tag) does **not** remove
anything: the content is kept, the bare tag lines are dropped from the output,
and a warning is logged.

## How it works

A text-level preprocessing step (`strip_no_export_sections` in
`src/obsidian_parser.py`) removes the tagged sections right after frontmatter
stripping, before image resolution, page breaks, and ToC collection.

Relevant files:

- `src/obsidian_parser.py` — `NO_EXPORT_PATTERN`, `strip_no_export_sections`
- `src/constants.py` — `NO_EXPORT_START`, `NO_EXPORT_END`
