#!/usr/bin/env node
/**
 * Export Markdown guides to PDF via Puppeteer (Chromium print).
 *
 * Pipeline: Markdown → marked (GFM) → HTML + KaTeX auto-render → page.pdf()
 *
 * Setup:
 *   cd guides && npm install
 *   node export-pdf.mjs [input.md] [output.pdf]
 */

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import { marked } from "marked";
import puppeteer from "puppeteer";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const GUIDES_DIR = __dirname;
const DEFAULT_MD = path.join(GUIDES_DIR, "AI课程-14周内容梳理.md");
const DEFAULT_PDF = path.join(GUIDES_DIR, "AI课程-14周内容梳理.pdf");
const CSS_FILE = path.join(GUIDES_DIR, "pdf-export.css");

const KATEX_VERSION = "0.16.11";
const KATEX_CSS = `https://cdn.jsdelivr.net/npm/katex@${KATEX_VERSION}/dist/katex.min.css`;
const KATEX_JS = `https://cdn.jsdelivr.net/npm/katex@${KATEX_VERSION}/dist/katex.min.js`;
const KATEX_AUTO_RENDER = `https://cdn.jsdelivr.net/npm/katex@${KATEX_VERSION}/dist/contrib/auto-render.min.js`;

marked.setOptions({ gfm: true, breaks: false });

function prepareBlockquotes(text) {
  const lines = text.split("\n");
  const result = [];
  const bq = /^>\s?(.*)$/;
  const listStart = /^(\s*)([-*+]|\d+\.)\s/;

  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i];
    const match = bq.exec(line);
    if (match && i + 1 < lines.length) {
      const nxt = bq.exec(lines[i + 1]);
      if (nxt) {
        const curContent = match[1];
        const nxtContent = nxt[1];
        const curIsList = listStart.test(curContent);
        const nxtIsList = listStart.test(nxtContent);
        if (!curIsList && nxtIsList && curContent.trim()) {
          result.push(line, ">");
          continue;
        }
      }
    }
    result.push(line);
  }
  return result.join("\n");
}

function prepareMarkdownLists(text) {
  const lines = text.split("\n");
  const prepared = [];
  const listLine = /^(\s*)([-*+]|\d+\.)\s/;

  for (const line of lines) {
    const match = listLine.exec(line);
    if (match && match[1] === "" && prepared.length && prepared.at(-1).trim()) {
      if (!listLine.test(prepared.at(-1))) {
        prepared.push("");
      }
    }
    prepared.push(line);
  }

  const normalized = [];
  for (const line of prepared) {
    const match = listLine.exec(line);
    if (match && match[1]) {
      const level = Math.floor(match[1].length / 2);
      normalized.push(" ".repeat(4 * level) + line.slice(match[1].length));
    } else {
      normalized.push(line);
    }
  }
  return normalized.join("\n");
}

function prepareMarkdown(mdText) {
  return prepareMarkdownLists(prepareBlockquotes(mdText));
}

async function mdToHtmlDocument(mdText, cssText) {
  const body = marked.parse(prepareMarkdown(mdText));
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>Guide Export</title>
  <link rel="stylesheet" href="${KATEX_CSS}">
  <style>${cssText}</style>
</head>
<body>
${body}
</body>
</html>`;
}

async function exportPdf(mdPath, pdfPath) {
  const [mdText, cssText] = await Promise.all([
    fs.readFile(mdPath, "utf8"),
    fs.readFile(CSS_FILE, "utf8"),
  ]);
  const htmlDoc = await mdToHtmlDocument(mdText, cssText);

  await fs.mkdir(path.dirname(pdfPath), { recursive: true });

  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  try {
    const page = await browser.newPage();
    await page.setContent(htmlDoc, { waitUntil: "networkidle0" });
    await page.addScriptTag({ url: KATEX_JS });
    await page.addScriptTag({ url: KATEX_AUTO_RENDER });
    await page.evaluate(() => {
      renderMathInElement(document.body, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "$", right: "$", display: false },
        ],
        throwOnError: false,
      });
    });
    await page.emulateMediaType("print");
    await page.pdf({
      path: pdfPath,
      format: "A4",
      printBackground: true,
      margin: { top: "20mm", right: "18mm", bottom: "20mm", left: "18mm" },
    });
  } finally {
    await browser.close();
  }
}

function parseArgs(argv) {
  const args = argv.slice(2);
  if (args.includes("-h") || args.includes("--help")) {
    return { help: true };
  }
  return {
    input: args[0] ? path.resolve(args[0]) : DEFAULT_MD,
    output: args[1] ? path.resolve(args[1]) : DEFAULT_PDF,
  };
}

async function main() {
  const { help, input: mdPath, output: pdfPath } = parseArgs(process.argv);
  if (help) {
    console.log(`Usage: node export-pdf.mjs [input.md] [output.pdf]

Default input : ${DEFAULT_MD}
Default output: ${DEFAULT_PDF}`);
    return 0;
  }

  try {
    await fs.access(mdPath);
  } catch {
    console.error(`error: input not found: ${mdPath}`);
    return 1;
  }
  try {
    await fs.access(CSS_FILE);
  } catch {
    console.error(`error: stylesheet not found: ${CSS_FILE}`);
    return 1;
  }

  console.log(`Exporting ${path.basename(mdPath)} → ${path.basename(pdfPath)} …`);
  await exportPdf(mdPath, pdfPath);
  const stat = await fs.stat(pdfPath);
  console.log(`Wrote ${pdfPath} (${stat.size.toLocaleString()} bytes)`);
  return 0;
}

main().then((code) => process.exit(code));
