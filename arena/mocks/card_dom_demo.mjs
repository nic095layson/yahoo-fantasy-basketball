// Render the REAL page in headless Chromium at chosen owner turns of committed rooms and read the
// decision card rows (name, score, tags) — before/after a judgment-layer change. Usage:
//   node card_dom_demo.mjs <deck.html> <states_dir> <out.json> <mock:turn,mock:turn,...>
import fs from "node:fs"; import path from "node:path"; import os from "node:os"; import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)(process.env.PW_MODULE || "/opt/node22/lib/node_modules/playwright");
const [html, statesDir, outPath, spec] = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || "/opt/pw-browsers/chromium", args: ["--no-sandbox"] });
const out = { deck: html, turns: [] };
for (const item of spec.split(",")) {
  const [mock, turn] = item.split(":").map(Number);
  const st = JSON.parse(fs.readFileSync(path.join(statesDir, `draft_state_${mock}.json`), "utf8"));
  const trunc = { ...st, picks: st.picks.slice(0, turn - 1) }; delete trunc.cast;
  const page = await browser.newPage(); const errors = [];
  page.on("pageerror", e => errors.push(String(e)));
  await page.goto("file://" + path.resolve(html)); await page.waitForTimeout(300);
  const tmp = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "demo-")), "s.json"); fs.writeFileSync(tmp, JSON.stringify(trunc));
  await page.setInputFiles("#importFile", tmp); await page.waitForTimeout(1200);
  const rows = await page.evaluate(() => [...document.querySelectorAll("#recos > li")].map(li => ({
    rk: li.querySelector(".rk")?.textContent?.trim() ?? "", nm: li.querySelector(".nm")?.textContent?.trim() ?? "",
    sc: li.querySelector(".sc")?.textContent?.trim() ?? "", tags: li.querySelector(".tags")?.textContent?.replace(/\s+/g, " ").trim() ?? "",
    meta: [...li.querySelectorAll(".meta")].map(m => m.textContent.replace(/\s+/g, " ").trim()).join(" | "),
    scTip: li.querySelector(".sc")?.dataset?.tip ?? "", tips: [...li.querySelectorAll("[data-tip]")].map(e => e.dataset.tip).filter(t => /judgment|OWNER/i.test(t)).map(t => t.slice(0, 400)) })));
  const strip = await page.evaluate(() => document.getElementById("strip")?.textContent?.replace(/\s+/g, " ").trim() ?? "");
  const advice = await page.evaluate(() => document.getElementById("adviceline")?.textContent?.replace(/\s+/g, " ").trim() ?? "");
  out.turns.push({ mock, turn, picks: trunc.picks.length, strip, advice, rows, errors });
  await page.close();
}
await browser.close();
fs.writeFileSync(outPath, JSON.stringify(out, null, 1));
console.log(JSON.stringify(out.turns.map(t => ({ mock: t.mock, turn: t.turn, errors: t.errors.length, rows: t.rows.map(r => `${r.rk} ${r.nm} ${r.sc} [${r.tags}]`) })), null, 1));
