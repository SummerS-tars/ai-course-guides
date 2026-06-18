#!/usr/bin/env node
/** Thin wrapper → ai-guides-pdf skill export script. */
import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const skillScript = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../.cursor/skills/ai-guides-pdf/scripts/export-pdf.mjs",
);

const child = spawn(process.execPath, [skillScript, ...process.argv.slice(2)], {
  stdio: "inherit",
});
child.on("exit", (code, signal) => {
  if (signal) {
    process.kill(process.pid, signal);
    return;
  }
  process.exit(code ?? 1);
});
