// Owner veto behavioral check (2026-09-28) through the REAL deck page in headless
// Chromium: import a draft state, then assert (1) no JUDGMENT.doNotDraft name is on
// the decision card, (2) the Best-available table still lists the name, marked
// DO NOT DRAFT, (3) a my: pick of the name logs the warning and Undo takes it back,
// (4) zero page errors. Usage:
//   node arena/mocks/veto_dom_check.mjs <deck.html> <draft_state.json> <out.json> [picksToKeep]
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)(process.env.PW_MODULE || "/opt/node22/lib/node_modules/playwright");
const [html, statePath, outPath, keepA] = process.argv.slice(2);
const st0 = JSON.parse(fs.readFileSync(statePath, "utf8"));
const keep = keepA ? +keepA : st0.picks.length;
const st = { ...st0, picks: st0.picks.slice(0, keep) };
const src = fs.readFileSync(html, "utf8");
const vm = src.match(/doNotDraft:\s*\[(.*?)\]/s);
const veto = vm ? [...vm[1].matchAll(/"([^"]+)"/g)].map(m => m[1]) : [];
const tmpState = path.join(os.tmpdir(), `veto-state-${process.pid}.json`);
fs.writeFileSync(tmpState, JSON.stringify(st));
const browser = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || "/opt/pw-browsers/chromium", args: ["--no-sandbox"] });
const page = await browser.newPage();
const errors = [];
page.on("pageerror", e => errors.push({ at: "pageerror", msg: String(e && e.message || e) }));
page.on("console", m => { if (m.type() === "error") errors.push({ at: "console", msg: m.text() }); });
await page.goto("file://" + path.resolve(html));
await page.setInputFiles("#importFile", tmpState);
await page.waitForSelector("#draft:not(.hidden)");
const texts = async sel => (await page.locator(sel).allInnerTexts()).map(s => s.trim());
const card = await texts("#recos li .nm");
const strip = (await page.locator("#strip").innerText()).trim();
await page.fill("#bestQ", "Porz");
await page.dispatchEvent("#bestQ", "input");
await page.waitForTimeout(200);
const bestRows = await texts("#bestRows tr");
const mirrorText = async () => (await page.locator("#mirror").innerText()).trim();
const before = await mirrorText();
await page.fill("#feed", "my: " + (veto[0] || "Kristaps Porzingis"));
await page.click("#logBtn");
await page.waitForTimeout(150);
const afterLog = await mirrorText();
await page.click("#undoBtn");
await page.waitForTimeout(150);
const afterUndo = await mirrorText();
await browser.close();
const cardHit = card.filter(n => veto.some(v => n.includes(v)));
const bestHit = bestRows.filter(r => veto.some(v => r.includes(v)));
const res = {
  deck: html, state: path.basename(statePath), picksLoaded: st.picks.length, veto,
  card, cardNamesVetoed: cardHit,
  bestRowsMatchingVeto: bestHit, bestRowMarked: bestHit.some(r => r.includes("DO NOT DRAFT")),
  warnLogged: afterLog.slice(before.length).includes("on your DO NOT DRAFT list"),
  undoLogged: afterUndo.slice(afterLog.length).includes("undid"),
  strip, pageErrors: errors,
};
res.pass = cardHit.length === 0 && bestHit.length >= 1 && res.bestRowMarked && res.warnLogged && res.undoLogged && errors.length === 0;
fs.writeFileSync(outPath, JSON.stringify(res, null, 1));
console.log(JSON.stringify({ pass: res.pass, card: res.card, cardNamesVetoed: cardHit, bestRowMarked: res.bestRowMarked, warnLogged: res.warnLogged, undoLogged: res.undoLogged, pageErrors: errors.length }));
