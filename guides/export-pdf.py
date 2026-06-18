#!/usr/bin/env python3
"""Export Markdown guides to PDF with inline LaTeX math ($...$).

Pipeline: Markdown → python-markdown + markdown-katex (KaTeX HTML/SVG)
→ WeasyPrint PDF.

Requires the project venv (see guides/requirements-pdf.txt):
  python3 -m venv .venv-pdf && .venv-pdf/bin/pip install -r guides/requirements-pdf.txt
  .venv-pdf/bin/python guides/export-pdf.py [input.md] [output.pdf]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown_katex.extension import KatexExtension
from weasyprint import CSS, HTML

GUIDES_DIR = Path(__file__).resolve().parent
DEFAULT_MD = GUIDES_DIR / "AI课程-14周内容梳理.md"
DEFAULT_PDF = GUIDES_DIR / "AI课程-14周内容梳理.pdf"
CSS_FILE = GUIDES_DIR / "pdf-export.css"


def prepare_blockquotes(text: str) -> str:
    """Insert blank blockquote lines before lists inside ``>`` blocks.

    python-markdown treats ``> intro:\\n> - item`` as one paragraph unless a
    blank ``>`` line separates the intro from the list.
    """
    lines = text.splitlines()
    result: list[str] = []
    bq = re.compile(r"^>\s?(.*)$")
    list_start = re.compile(r"^(\s*)([-*+]|\d+\.)\s")

    i = 0
    while i < len(lines):
        line = lines[i]
        match = bq.match(line)
        if match and i + 1 < len(lines):
            nxt = bq.match(lines[i + 1])
            if nxt:
                cur_content = match.group(1)
                nxt_content = nxt.group(1)
                cur_is_list = bool(list_start.match(cur_content))
                nxt_is_list = bool(list_start.match(nxt_content))
                if not cur_is_list and nxt_is_list and cur_content.strip():
                    result.append(line)
                    result.append(">")
                    i += 1
                    continue
        result.append(line)
        i += 1
    return "\n".join(result)


# Color emoji embed as raster images in WeasyPrint and leave green corner artifacts.
PDF_SYMBOL_REPLACEMENTS = {
    "✅": "✓",
    "🏖️": "〔休〕",
    "🏃": "〔运〕",
    "🔜": "→",
}


def prepare_pdf_symbols(text: str) -> str:
    """Replace color emoji with plain-text symbols safe for WeasyPrint."""
    for src, dst in PDF_SYMBOL_REPLACEMENTS.items():
        text = text.replace(src, dst)
    return text


def prepare_markdown_lists(text: str) -> str:
    """Normalize list markup for python-markdown.

    - Insert a blank line before a top-level list when it immediately follows prose
      (e.g. ``**核心内容**：`` + ``- item``), otherwise the list is parsed as a paragraph.
    - Expand 2-space nested list indents to 4-space (``  -`` → ``    -``).
    """
    lines = text.splitlines()
    prepared: list[str] = []
    list_line = re.compile(r"^(\s*)([-*+]|\d+\.)\s")

    for line in lines:
        match = list_line.match(line)
        if match and match.group(1) == "" and prepared and prepared[-1].strip():
            if not list_line.match(prepared[-1]):
                prepared.append("")
        prepared.append(line)

    normalized: list[str] = []
    for line in prepared:
        match = list_line.match(line)
        if match and match.group(1):
            level = len(match.group(1)) // 2
            normalized.append(" " * (4 * level) + line[len(match.group(1)) :])
        else:
            normalized.append(line)
    return "\n".join(normalized)


def convert_dollar_math(text: str) -> str:
    """Map $...$ / $$...$$ to markdown-katex fenced syntax ($`...`$)."""
    text = re.sub(
        r"\$\$([^\$]+)\$\$",
        lambda m: "\n```math\n" + m.group(1).strip() + "\n```\n",
        text,
    )
    text = re.sub(
        r"\$([^\$\n]+)\$",
        lambda m: "$`" + m.group(1) + "`$",
        text,
    )
    return text


def prepare_markdown(md_text: str) -> str:
    return prepare_pdf_symbols(
        prepare_markdown_lists(prepare_blockquotes(md_text))
    )


def md_to_html(md_text: str) -> str:
    body = markdown.markdown(
        convert_dollar_math(prepare_markdown(md_text)),
        extensions=[
            KatexExtension(no_inline_svg=True),
            TableExtension(),
            FencedCodeExtension(),
        ],
    )
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>Guide Export</title>
</head>
<body>
{body}
</body>
</html>"""


def export_pdf(md_path: Path, pdf_path: Path) -> None:
    md_text = md_path.read_text(encoding="utf-8")
    html_doc = md_to_html(md_text)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html_doc, base_url=str(GUIDES_DIR)).write_pdf(
        str(pdf_path),
        stylesheets=[CSS(filename=str(CSS_FILE))],
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export Markdown guide to PDF.")
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=DEFAULT_MD,
        help=f"Source Markdown (default: {DEFAULT_MD.name})",
    )
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        default=DEFAULT_PDF,
        help=f"Output PDF (default: {DEFAULT_PDF.name})",
    )
    args = parser.parse_args(argv)

    md_path = args.input.resolve()
    pdf_path = args.output.resolve()

    if not md_path.is_file():
        print(f"error: input not found: {md_path}", file=sys.stderr)
        return 1
    if not CSS_FILE.is_file():
        print(f"error: stylesheet not found: {CSS_FILE}", file=sys.stderr)
        return 1

    print(f"Exporting {md_path.name} → {pdf_path.name} …")
    export_pdf(md_path, pdf_path)
    print(f"Wrote {pdf_path} ({pdf_path.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
