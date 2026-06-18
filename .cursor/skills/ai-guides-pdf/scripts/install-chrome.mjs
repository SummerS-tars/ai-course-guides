#!/usr/bin/env node
/** Ensure Puppeteer-managed Chrome is present (npm may block puppeteer postinstall). */
import { execSync } from "node:child_process";
import puppeteer from "puppeteer";

try {
  puppeteer.executablePath();
} catch {
  console.log("Installing Chrome for Puppeteer …");
  execSync("npx puppeteer browsers install chrome", { stdio: "inherit" });
}
