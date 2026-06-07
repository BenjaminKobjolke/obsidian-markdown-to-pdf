# `[TOC]` — Table of Contents

Insert a clickable table of contents into the exported PDF.

## Usage

Put the marker on its own line where you want the ToC to appear:

```markdown
[TOC]
```

On export it becomes a nested list of the document's headings. Each entry is a
clickable link that jumps to that section in the PDF. WeasyPrint also adds the
headings to the PDF bookmark/outline sidebar automatically.

The marker is exact and case-sensitive: `[TOC]` (not `[TO]`, `[toc]`, etc.).

> In Obsidian's own preview `[TOC]` shows as literal text — only this exporter
> renders it as a table of contents.

## Scope: exclude headings before the marker

Headings that appear **above** the `[TOC]` marker are left out of the table of
contents. They still render normally — they just get no ToC entry. This lets
you keep a short cheat-sheet at the top of a note without it cluttering the ToC.

```markdown
# Quick reference        <- not in the ToC (above the marker)

## Important number       <- not in the ToC

[TOC]

# Full setup              <- listed
## Step one               <- listed
```

If a document has **no** `[TOC]` marker, nothing is hidden — headings render as
usual (and still get anchor ids).

## Exclude a single heading

Add the `toc-omit` class to any heading to drop just that one from the ToC,
wherever it sits:

```markdown
## Internal notes { .toc-omit }
```

The heading still renders in the PDF; it is only absent from the ToC list.

> The `{ .toc-omit }` attribute also shows as literal text in Obsidian's
> preview. Only this exporter consumes it.

## Heading anchors

Each listed heading gets an auto-generated id (slug) used for the clickable
link — lowercase, spaces become hyphens, e.g. `## Full Setup` → `#full-setup`.
Duplicate heading texts get numeric suffixes (`-1`, `-2`) so links stay unique.

## How it works

Backed by python-markdown's built-in `toc` extension plus a small project
extension (`src/toc_scope.py`) that implements the scoping rules. The scope
extension hides excluded headings from the toc collector before it runs, then
restores them so they still render. No syntax beyond standard Markdown and
`attr_list`.

Relevant files:

- `src/html_converter.py` — enables `toc`, `attr_list`, and `TocScopeExtension`
- `src/toc_scope.py` — below-marker + `toc-omit` scoping
- `src/constants.py` — `TOC_MARKER`, `TOC_OMIT_CLASS`
