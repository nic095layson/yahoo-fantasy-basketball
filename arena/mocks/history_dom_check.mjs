// D59-1 (2026-10-01, mock 59): does the history box keep up with Insert-at-#?
// Replays a live-room tool log through the REAL page in headless Chromium (the
// live_replay_dom.mjs drive, minus the per-event clock bookkeeping) and then
// asserts the FINAL history text: every owner pick line reads its final number
// and "(YOU)", every standing UNKNOWN reads its final number, and each insert
// echo names the re-numbered range. Mock 59's room (161 events, four inserts):
// Queta fed at #105 before the #97 insert, Washington at #128 before the #121
// and #128 inserts, Hansen UNKNOWN at #125 before the #121 insert.
//   env -u TMPDIR node arena/mocks/history_dom_check.mjs <deck.html> <events.json> <state.json> <out.json> [teams size slot]
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)(process.env.PW_MODULE || "/opt/node22/lib/node_modules/playwright");
const [html, evPath, statePath, outPath, teamsA = "12", sizeA = "13", slotA = "10"] = process.argv.slice(2);
const events = JSON.parse(fs.readFileSync(evPath, "utf8"));
const truth = JSON.parse(fs.readFileSync(statePath, "utf8"));   // the room's final state (resync from the recap)
const teams = +teamsA, size = +sizeA, slot = +slotA;
const browser = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || "/opt/pw-browsers/chromium", args: ["--no-sandbox"] });
const page = await browser.newPage();
const errors = [];
page.on("pageerror", e => errors.push(String(e && e.message || e)));
await page.goto("file://" + path.resolve(html));
await page.fill("#cfgTeams", String(teams)); await page.fill("#cfgSize", String(size)); await page.fill("#cfgSlot", String(slot));
await page.click("#modeLive"); await page.click("#startBtn");
await page.waitForSelector("#draft:not(.hidden)");
for (const ev of events) {
  if (ev.op === "feed") { await page.fill("#feed", ev.text); await page.click("#logBtn"); }
  else if (ev.op === "insert") {
    if (await page.locator("#insertBar").evaluate(el => el.classList.contains("hidden"))) await page.click("#insertToggle");
    await page.fill("#insNum", String(ev.P)); await page.fill("#insName", ev.text); await page.click("#insBtn");
  } else if (ev.op === "undo") { await page.click("#undoBtn"); }
}
const lines = (await page.locator("#mirror").innerText()).split("\n").map(s => s.trim()).filter(Boolean);
const strip = (await page.locator("#strip").innerText()).replace(/\s+/g, " ").trim();
await browser.close();
// assertions from the final state: each owner pick's LAST history line must carry its final number and (YOU)
const checks = [];
const pickLine = (name) => [...lines].reverse().find(l => /^✓ \(R\d+\) #\d+: /.test(l) && l.includes(`: ${name} →`)) || null;
truth.picks.forEach((pk, i) => {
  if (pk.slot !== slot) return;
  const l = pickLine(pk.player);
  const ok = !!l && l.startsWith(`✓ (R${Math.floor(i / teams) + 1}) #${i + 1}: `) && l.includes("(YOU)");
  checks.push({ what: `owner pick #${i + 1} ${pk.player} reads its final number and (YOU)`, ok, line: l });
});
truth.picks.forEach((pk, i) => {
  if (!/^UNKNOWN #\d+$/.test(pk.player)) return;
  const l = [...lines].reverse().find(l => /^⚠ \(R\d+\) #\d+: UNKNOWN/.test(l)) || null;
  const ok = !!l && l.includes(`#${i + 1}: UNKNOWN`) && l.includes(`fix with: ${i + 1}- Name`);
  checks.push({ what: `standing UNKNOWN at #${i + 1} reads its final number in the history`, ok, line: l });
  checks.push({ what: `the status strip names the standing UNKNOWN by its final number (#${i + 1})`, ok: strip.includes(`#${i + 1}`) && strip.includes(`${i + 1}- Name`), line: strip });
});
for (const ev of events) if (ev.op === "insert") {
  const l = lines.find(l => l.startsWith("✎ inserted") && l.includes(`${ev.text} at #${ev.P}`)) || null;
  checks.push({ what: `insert echo for ${ev.text} at #${ev.P} names the re-numbered range`, ok: !!l && /re-numbered|shifted/.test(l), line: l });
}
const failed = checks.filter(c => !c.ok).length;
const out = { deck: html, events: events.length, lines: lines.length, checks: checks.length, failed, pageErrors: errors.length, pass: failed === 0 && errors.length === 0, detail: checks, errors };
fs.writeFileSync(outPath, JSON.stringify(out, null, 1));
console.log(JSON.stringify({ checks: checks.length, failed, pageErrors: errors.length, pass: out.pass }));
for (const c of checks) if (!c.ok) console.log("  FAIL  " + c.what + " — " + JSON.stringify(c.line));
