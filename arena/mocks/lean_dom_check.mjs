// Owner-reported 2026-10-14 (lock day): the card's "⚠ LEAN: 7G vs 2F" line on a
// six-man roster of four PG,SG guards and two forwards. Feeds a pick list into
// the REAL page in headless Chromium (LIVE mode, 12 × 13, seat 10) and prints the
// roster header's family census and every flag line the card shows, so the
// token-count bug can be seen on the old page and its absence on the new one.
// Usage: node arena/mocks/lean_dom_check.mjs <deck.html> <events.json> [teams size slot]
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)(process.env.PW_MODULE || "/opt/node22/lib/node_modules/playwright");
const [html, evPath, teamsA = "12", sizeA = "13", slotA = "10"] = process.argv.slice(2);
const events = JSON.parse(fs.readFileSync(evPath, "utf8"));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.resolve(html));
await page.fill("#cfgTeams", teamsA); await page.fill("#cfgSize", sizeA); await page.fill("#cfgSlot", slotA);
await page.click("#modeLive"); await page.click("#startBtn");
for (const ev of events) { await page.fill("#feed", ev.text); await page.click("#logBtn"); }
await page.waitForTimeout(100);
const census = (await page.locator("#rosterHead, #rosterTitle, .roster-head").first().innerText().catch(() => "")).trim();
const body = await page.locator("body").innerText();
const censusLine = (body.match(/G \(\d+\)\s+F \(\d+\)\s+C \(\d+\)/) || [census])[0];
const flags = (await page.locator("#flags").innerText()).split("\n").map(s => s.trim()).filter(Boolean);
const roster = (body.match(/YOUR ROSTER \((\d+)\/(\d+)\)/) || [])[0];
console.log(JSON.stringify({ deck: html, picks: events.length, roster, census: censusLine, flags, lean: flags.filter(f => f.includes("LEAN")) }));
await browser.close();
