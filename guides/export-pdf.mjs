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
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { fileURLToPath, pathToFileURL } from "node:url";
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

/** @type {ReadonlyArray<{ family: string; weight: number; style: string; file: string }>} */
const FONT_SPECS = [
  { family: "Sarasa UI SC", weight: 400, style: "normal", file: "SarasaUiSC-Regular.ttf" },
  { family: "Sarasa UI SC", weight: 600, style: "normal", file: "SarasaUiSC-SemiBold.ttf" },
  { family: "Sarasa UI SC", weight: 700, style: "normal", file: "SarasaUiSC-Bold.ttf" },
  { family: "Sarasa Mono SC", weight: 400, style: "normal", file: "SarasaMonoSC-Regular.ttf" },
  { family: "Sarasa Mono SC", weight: 700, style: "normal", file: "SarasaMonoSC-Bold.ttf" },
  { family: "Fira Code", weight: 400, style: "normal", file: "FiraCode-Regular.ttf" },
  { family: "Fira Code", weight: 700, style: "normal", file: "FiraCode-Bold.ttf" },
];

async function pathExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function resolveFontDir() {
  const candidates = [
    process.env.PDF_EXPORT_FONT_DIR,
    "/mnt/c/Users/Sum/AppData/Local/Microsoft/Windows/Fonts",
    path.join(os.homedir(), ".local/share/fonts"),
    "/usr/share/fonts/truetype",
  ].filter(Boolean);

  for (const dir of candidates) {
    if (await pathExists(path.join(dir, "SarasaUiSC-Regular.ttf"))) {
      return dir;
    }
  }
  return null;
}

async function buildFontFaceCss() {
  const fontDir = await resolveFontDir();
  if (!fontDir) {
    console.warn("warn: Sarasa/Fira fonts not found; PDF may lack proper bold weights");
    return "";
  }

  const rules = [];
  for (const spec of FONT_SPECS) {
    const fontPath = path.join(fontDir, spec.file);
    if (!(await pathExists(fontPath))) {
      continue;
    }
    const src = pathToFileURL(fontPath).href;
    rules.push(`@font-face {
  font-family: "${spec.family}";
  font-style: ${spec.style};
  font-weight: ${spec.weight};
  src: url("${src}") format("truetype");
}`);
  }

  if (rules.length) {
    console.log(`Using fonts from ${fontDir} (${rules.length} @font-face rules)`);
  }
  return rules.join("\n\n");
}

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

async function mdToHtmlDocument(mdText, cssText, fontFaceCss) {
  const body = marked.parse(prepareMarkdown(mdText));
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>Guide Export</title>
  <link rel="stylesheet" href="${KATEX_CSS}">
  <style>${fontFaceCss}${fontFaceCss ? "\n\n" : ""}${cssText}</style>
</head>
<body>
${body}
</body>
</html>`;
}

async function exportPdf(mdPath, pdfPath) {
  const [mdText, cssText, fontFaceCss] = await Promise.all([
    fs.readFile(mdPath, "utf8"),
    fs.readFile(CSS_FILE, "utf8"),
    buildFontFaceCss(),
  ]);
  const htmlDoc = await mdToHtmlDocument(mdText, cssText, fontFaceCss);

  await fs.mkdir(path.dirname(pdfPath), { recursive: true });

  const browser = await puppeteer.launch({
    headless: true,
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--font-render-hinting=medium",
      "--allow-file-access-from-files",
    ],
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
