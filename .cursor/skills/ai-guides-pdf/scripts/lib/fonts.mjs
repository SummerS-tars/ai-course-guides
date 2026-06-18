import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const SKILL_DIR = path.resolve(__dirname, "../..");
export const FONTS_DIR = path.join(SKILL_DIR, "fonts");

/** @type {ReadonlyArray<{ family: string; weight: number; style: string; file: string }>} */
export const FONT_SPECS = [
  { family: "Sarasa UI SC", weight: 400, style: "normal", file: "SarasaUiSC-Regular.ttf" },
  { family: "Sarasa UI SC", weight: 600, style: "normal", file: "SarasaUiSC-SemiBold.ttf" },
  { family: "Sarasa UI SC", weight: 700, style: "normal", file: "SarasaUiSC-Bold.ttf" },
  { family: "Sarasa Mono SC", weight: 400, style: "normal", file: "SarasaMonoSC-Regular.ttf" },
  { family: "Sarasa Mono SC", weight: 700, style: "normal", file: "SarasaMonoSC-Bold.ttf" },
  { family: "Fira Code", weight: 400, style: "normal", file: "FiraCode-Regular.ttf" },
  { family: "Fira Code", weight: 700, style: "normal", file: "FiraCode-Bold.ttf" },
];

export const REQUIRED_FONT_FILES = FONT_SPECS.map((spec) => spec.file);

async function pathExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

export async function fontsAreComplete(fontDir = FONTS_DIR) {
  const checks = await Promise.all(
    REQUIRED_FONT_FILES.map((file) => pathExists(path.join(fontDir, file))),
  );
  return checks.every(Boolean);
}

export async function resolveFontDir() {
  if (await fontsAreComplete(FONTS_DIR)) {
    return FONTS_DIR;
  }

  const override = process.env.PDF_EXPORT_FONT_DIR;
  if (override && (await fontsAreComplete(override))) {
    return override;
  }

  return null;
}

export async function buildFontFaceCss() {
  const fontDir = await resolveFontDir();
  if (!fontDir) {
    console.warn(
      "warn: bundled fonts missing; run: npm install --prefix .cursor/skills/ai-guides-pdf",
    );
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
