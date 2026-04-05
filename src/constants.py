APP_NAME = "obsidian-markdown-to-pdf"
APP_DESCRIPTION = "Convert Obsidian-flavored markdown files to PDF"

MSYS2_DLL_DIR = r"C:\msys64\ucrt64\bin"

RESOURCES_DIR = "_resources"

PAGE_BREAK_HTML = '<div class="page-break"></div>'

ERR_INPUT_NOT_FOUND = "Input file not found: {path}"
ERR_CONVERSION_FAILED = "Conversion failed: {error}"

CSS_TEMPLATE = """
@page {
    size: A4;
    margin: 2cm;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 12pt;
    line-height: 1.6;
    color: #1a1a1a;
}

h1, h2, h3, h4, h5, h6 {
    margin-top: 1.2em;
    margin-bottom: 0.4em;
    color: #111;
}

h1 { font-size: 1.8em; }
h2 { font-size: 1.5em; border-bottom: 1px solid #ddd; padding-bottom: 0.2em; }
h3 { font-size: 1.2em; }

img {
    max-width: 100%;
    height: auto;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}

th, td {
    border: 1px solid #ccc;
    padding: 8px 12px;
    text-align: left;
}

th {
    background-color: #f5f5f5;
    font-weight: 600;
}

tr:nth-child(even) {
    background-color: #fafafa;
}

.page-break {
    page-break-after: always;
}

p {
    margin: 0.6em 0;
}
"""
