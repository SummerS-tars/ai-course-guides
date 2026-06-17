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


def md_to_html(md_text: str) -> str:
    body = markdown.markdown(
        convert_dollar_math(md_text),
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
