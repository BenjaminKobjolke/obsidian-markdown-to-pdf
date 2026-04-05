import re

import markdown

from src.constants import CSS_TEMPLATE

WIDTH_ATTR_PATTERN = re.compile(r'(<img\b[^>]*)\bwidth="(\d+)"([^>]*/>)')

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{css}
</style>
</head>
<body>
{body}
</body>
</html>"""


def markdown_to_html(md_content: str) -> str:
    md = markdown.Markdown(
        extensions=[
            "tables",
            "sane_lists",
            "obsidian_media",
        ],
    )
    return str(md.convert(md_content))


def wrap_html(body: str) -> str:
    return HTML_TEMPLATE.format(css=CSS_TEMPLATE, body=body)


def width_attr_to_style(html: str) -> str:
    def _replace(match: re.Match[str]) -> str:
        before = match.group(1)
        width = match.group(2)
        after = match.group(3)
        before = re.sub(r'\bwidth="\d+"', "", before)
        return f'{before}style="width: {width}px; height: auto;"{after}'

    return WIDTH_ATTR_PATTERN.sub(_replace, html)


def convert(md_content: str) -> str:
    body = markdown_to_html(md_content)
    body = width_attr_to_style(body)
    return wrap_html(body)
