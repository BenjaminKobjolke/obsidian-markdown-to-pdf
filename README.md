# Obsidian Markdown to PDF

Convert Obsidian-flavored markdown files to PDF with support for wiki-link images, frontmatter stripping, and page breaks. Includes an Obsidian plugin for one-click export from the command palette.

## Features

- Converts `![[image.png|width]]` wiki-link embeds to sized images
- Strips YAML frontmatter from output
- Treats `---` as page breaks
- Supports GFM tables
- Resolves images from `_resources/` subdirectory, same directory, and vault-level `_resources/`
- Automatically detects the Obsidian vault root via `.obsidian/` directory
- Respects image width settings (e.g. `![[image.png|400]]` or `![400](image.png)`)

## Prerequisites

- Python 3.12
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager
- [MSYS2](https://www.msys2.org/) with GTK3/Pango (required by WeasyPrint)

### Installing MSYS2 and GTK3

1. Download and install MSYS2 from https://www.msys2.org/ (default path: `C:\msys64`)
2. Open **MSYS2 UCRT64** terminal and run:
   ```
   pacman -S mingw-w64-ucrt-x86_64-gtk3
   ```
3. The `start.bat` script automatically adds `C:\msys64\ucrt64\bin` to PATH at runtime

## Installation

```
install.bat
```

## Usage

### Command line

```
start.bat --input "path/to/note.md"
start.bat --input "path/to/note.md" --output "output.pdf"
```

#### Output path rules

| Argument | Behavior |
|---|---|
| No `--output` | PDF saved next to the markdown file with `.pdf` extension |
| `--output filename.pdf` | PDF saved in the same directory as the markdown file |
| `--output path/to/file.pdf` | PDF saved at the specified path |

### Obsidian plugin

An Obsidian plugin is included at `tools/obsidian-markdown-to-pdf-helper/` for exporting directly from within Obsidian.

#### Plugin installation

1. Build the plugin:
   ```
   cd tools\obsidian-markdown-to-pdf-helper
   npm install
   npm run build
   ```
2. Copy the `obsidian-markdown-to-pdf-helper` folder into your vault's `.obsidian/plugins/` directory
3. In Obsidian, go to **Settings > Community plugins** and enable **Markdown to PDF**

#### Plugin settings

| Setting | Description |
|---|---|
| **Python tool path** | Path to the `obsidian-markdown-to-pdf` directory (where `start.bat` is located) |
| **Export folder** | Folder where exported PDFs are saved |

#### Exporting a file

1. Open a markdown file in Obsidian
2. Press `Ctrl+P` to open the command palette
3. Search for **"Export markdown to PDF"**
4. The PDF is saved to the configured export folder

### Image resolution order

For wiki-link images (`![[image.png]]`), the tool searches for the file in this order:

1. `_resources/` subdirectory relative to the markdown file
2. Same directory as the markdown file
3. `_resources/` in the Obsidian vault root
4. Obsidian vault root directory

## Development

### Run tests

```
tools\run_tests.bat
```

### Update dependencies

```
update.bat
```
