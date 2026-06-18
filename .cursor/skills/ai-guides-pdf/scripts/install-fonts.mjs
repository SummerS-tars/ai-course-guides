#!/usr/bin/env node
/**
 * Download Sarasa SC + Fira Code into skill-local fonts/ (gitignored).
 * Uses pinned URLs from fonts-manifest.json; extracts only required weights.
 */
import { execFileSync } from "node:child_process";
import fs from "node:fs/promises";
import { createWriteStream } from "node:fs";
import path from "node:path";
import { pipeline } from "node:stream/promises";
import { fileURLToPath } from "node:url";
import { path7za } from "7zip-bin";
import {
  FONTS_DIR,
  REQUIRED_FONT_FILES,
  fontsAreComplete,
} from "./lib/fonts.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = path.resolve(__dirname, "..");
const MANIFEST_PATH = path.join(SKILL_DIR, "fonts-manifest.json");
const CACHE_DIR = path.join(FONTS_DIR, ".cache");

async function ensure7za() {
  try {
    await fs.chmod(path7za, 0o755);
  } catch {
    // ignore if platform has no bundled binary
  }
}

async function pathExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function download(url, dest) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`download failed (${response.status}): ${url}`);
  }
  await fs.mkdir(path.dirname(dest), { recursive: true });
  await pipeline(response.body, createWriteStream(dest));
}

async function extract7z(archivePath, outDir, onlyFiles) {
  await ensure7za();
  await fs.mkdir(outDir, { recursive: true });
  for (const file of onlyFiles) {
    execFileSync(path7za, ["x", archivePath, `-o${outDir}`, file, "-y"], {
      stdio: "pipe",
    });
  }
}

async function findExtractedFiles(rootDir, filenames) {
  const found = new Map();
  async function walk(dir) {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        await walk(full);
      } else if (filenames.includes(entry.name) && !found.has(entry.name)) {
        found.set(entry.name, full);
      }
    }
  }
  await walk(rootDir);
  return found;
}

async function extractZip(archivePath, outDir, onlyFiles) {
  await fs.mkdir(outDir, { recursive: true });
  execFileSync("unzip", ["-o", archivePath, ...onlyFiles.map((f) => `ttf/${f}`)], {
    cwd: outDir,
    stdio: "pipe",
  });
}

async function stageFonts(sourceMap) {
  await fs.mkdir(FONTS_DIR, { recursive: true });
  for (const file of REQUIRED_FONT_FILES) {
    const src = sourceMap.get(file);
    if (!src) {
      throw new Error(`missing font after extract: ${file}`);
    }
    await fs.copyFile(src, path.join(FONTS_DIR, file));
  }
}

async function main() {
  if (await fontsAreComplete()) {
    console.log("Fonts already installed in", FONTS_DIR);
    return;
  }

  const manifest = JSON.parse(await fs.readFile(MANIFEST_PATH, "utf8"));
  await fs.mkdir(CACHE_DIR, { recursive: true });

  const uiArchive = path.join(CACHE_DIR, "SarasaUiSC.7z");
  const monoArchive = path.join(CACHE_DIR, "SarasaMonoSC.7z");
  const firaArchive = path.join(CACHE_DIR, "FiraCode.zip");
  const extractRoot = path.join(CACHE_DIR, "extract");

  console.log("Downloading Sarasa UI SC …");
  if (!(await pathExists(uiArchive))) {
    await download(manifest.sarasa.packages.ui, uiArchive);
  }
  console.log("Downloading Sarasa Mono SC …");
  if (!(await pathExists(monoArchive))) {
    await download(manifest.sarasa.packages.mono, monoArchive);
  }
  console.log("Downloading Fira Code …");
  if (!(await pathExists(firaArchive))) {
    await download(manifest.firaCode.url, firaArchive);
  }

  await fs.rm(extractRoot, { recursive: true, force: true });
  await fs.mkdir(extractRoot, { recursive: true });

  const sarasaUiFiles = manifest.sarasa.files.filter((f) => f.startsWith("SarasaUi"));
  const sarasaMonoFiles = manifest.sarasa.files.filter((f) => f.startsWith("SarasaMono"));

  console.log("Extracting Sarasa fonts …");
  await extract7z(uiArchive, extractRoot, sarasaUiFiles);
  await extract7z(monoArchive, extractRoot, sarasaMonoFiles);

  console.log("Extracting Fira Code …");
  const firaDir = path.join(extractRoot, "fira");
  await extractZip(firaArchive, firaDir, manifest.firaCode.files);

  const located = await findExtractedFiles(extractRoot, REQUIRED_FONT_FILES);
  for (const file of manifest.firaCode.files) {
    const alt = path.join(firaDir, "ttf", file);
    if (await pathExists(alt)) {
      located.set(file, alt);
    }
  }

  await stageFonts(located);
  console.log(`Installed ${REQUIRED_FONT_FILES.length} fonts → ${FONTS_DIR}`);
}

main().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
