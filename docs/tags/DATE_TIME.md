# `[date]` / `[time]` — Insert export date and time

Insert the date/time of the export (when the PDF is generated) into the
document.

## Usage

Put the tag anywhere in the text — it works inline:

```markdown
Created: [date] at [time]
```

With the defaults this renders as `Created: 16.07.2025 at 08:31`.

Custom format via a `format` attribute:

```markdown
Report [date format="YYMMDD"]
Generated [time format="HH:mm:ss"]
```

Tags are lowercase and case-sensitive: `[DATE]` stays literal text.
Both tags in one document use the same moment, so date and time always match.

> In Obsidian's own preview the tags show as literal text — only this exporter
> replaces them.

## Format tokens

Moment.js-style tokens (the Obsidian convention). Any other character
(`.`, `-`, `:`, `/`, space) passes through literally.

| Token  | Meaning              | Example   |
| ------ | -------------------- | --------- |
| `YYYY` | 4-digit year         | 2025      |
| `YY`   | 2-digit year         | 25        |
| `MMMM` | full month name      | July      |
| `MMM`  | short month name     | Jul       |
| `MM`   | 2-digit month        | 07        |
| `DD`   | 2-digit day          | 16        |
| `dddd` | full weekday name    | Wednesday |
| `ddd`  | short weekday name   | Wed       |
| `HH`   | 2-digit hour (24h)   | 08        |
| `hh`   | 2-digit hour (12h)   | 08        |
| `mm`   | 2-digit minute       | 31        |
| `ss`   | 2-digit second       | 05        |
| `A`    | AM/PM                | AM        |

Defaults: `[date]` = `DD.MM.YYYY`, `[time]` = `HH:mm`.

## Notes

- The replacement runs on the raw markdown text, so tags inside fenced code
  blocks are also replaced. Break the tag up (e.g. `[date ]`) if you need it
  literal in a code example.
- Tags inside `[NO-EXPORT]` sections are removed with the section and never
  rendered.

## How it works

A text-level preprocessing step (`convert_datetime_tags` in
`src/obsidian_parser.py`) replaces each tag with `datetime.now()` formatted
per the (translated) format string; it runs after `[NO-EXPORT]` stripping and
before image resolution.

Relevant files:

- `src/obsidian_parser.py` — `DATETIME_TAG_PATTERN`, `convert_datetime_tags`,
  `_moment_to_strftime`
- `src/constants.py` — `DATE_TAG`, `TIME_TAG`, `DEFAULT_DATE_FORMAT`,
  `DEFAULT_TIME_FORMAT`
