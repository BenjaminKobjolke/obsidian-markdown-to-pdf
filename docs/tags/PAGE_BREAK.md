# `---` — Page break

Force a new page in the exported PDF.

## Usage

Put three dashes alone on a line where the next content should start on a new
page:

```markdown
End of chapter one.

---

# Chapter two
```

Leading/trailing whitespace on the line is allowed; anything else on the line
(e.g. `--- text`) is not a page break. Inline dashes and em-dashes are
untouched.

> In Obsidian's own preview `---` renders as a horizontal rule — only this
> exporter turns it into a page break.

## Notes

- Every `---` line becomes a page break, so there is no way to get a plain
  horizontal rule (`<hr>`) in the PDF.
- YAML frontmatter at the top of the file is stripped before this step, so its
  `---` delimiters never become page breaks.

## How it works

A text-level preprocessing step (`convert_page_breaks` in
`src/obsidian_parser.py`) replaces each `---` line with
`<div class="page-break"></div>`; the stylesheet gives that class
`page-break-after: always`, which WeasyPrint honors when rendering the PDF.

Relevant files:

- `src/obsidian_parser.py` — `PAGE_BREAK_PATTERN`, `convert_page_breaks`
- `src/constants.py` — `PAGE_BREAK_HTML`, `.page-break` CSS rule
