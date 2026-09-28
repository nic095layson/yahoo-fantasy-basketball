// D54 behavioral check (2026-09-28) through the REAL deck page in headless Chromium.
//   A) replay the owner's mock-54 tool log (feeds, the raw UNKNOWN texts, inserts, undos,
//      numbered fixes) through the feed box and diff the resulting board against Yahoo's
//      recap — the D54-2 auto-fix should collapse the 13-position drift to the one
//      UNKNOWN the owner never fixed (#97); the strip must name it.
//   B) import the recap state at 134 picks, type "my: Ajay Mitchell" and read the hint
//      under the feed (D54-1), then Log it and read the log line; read the advisor line
//      for the dead-category trap sentence (D54-3).
// Usage: node arena/mocks/d54_dom_check.mjs <deck.html> <events.json> <truth.json> <state.json> <out.json>
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)(process.env.PW_MODULE || "/opt/node22/lib/node_modules/playwright");
const [html, evPath, truthPath, statePath, outPath] = process.argv.slice(2);
const events = JSON.parse(fs.readFileSync(evPath, "utf8"));
const truth = JSON.parse(fs.readFileSync(truthPath, "utf8")).picks.map(p => p.player);
const st0 = JSON.parse(fs.readFileSync(statePath, "utf8"));
const browser = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || "/opt/pw-browsers/chromium", args: ["--no-sandbox"] });
const errors = [];
const res = { deck: html };
// ---- A) tool-log replay
{
  const page = await browser.newPage();
  page.on("pageerror", e => errors.push({ at: "A", msg: String(e && e.message || e) }));
  await page.goto("file://" + path.resolve(html));
  await page.fill("#cfgTeams", "12"); await page.fill("#cfgSize", "13"); await page.fill("#cfgSlot", "10");
  await page.click("#modeLive"); await page.click("#startBtn");
  await page.waitForSelector("#draft:not(.hidden)");
  for (const ev of events) {
    if (ev.op === "feed") { await page.fill("#feed", ev.text); await page.click("#logBtn"); }
    else if (ev.op === "insert") {
      if (await page.locator("#insertBar").evaluate(el => el.classList.contains("hidden"))) await page.click("#insertToggle");
      await page.fill("#insNum", String(ev.P)); await page.fill("#insName", ev.text); await page.click("#insBtn");
    } else if (ev.op === "undo") { await page.click("#undoBtn"); }
  }
  const state = await page.evaluate(() => JSON.parse(localStorage.getItem("draftdeck.v1")).state);
  const board = state.picks.map(p => p.player);
  const diff = board.map((n, i) => n !== truth[i] ? [i + 1, n, truth[i]] : null).filter(Boolean);
  const mirror = await page.locator("#mirror").innerText();
  const strip = await page.locator("#strip").innerText();
  res.replay = { picks: board.length, positionsDiffering: diff.length, diff, fixedLines: (mirror.match(/fixed: UNKNOWN/g) || []).length,
                 stillOpenWarned: /still UNKNOWN/.test(mirror), stripNamesOpen: /UNKNOWN open: #97/.test(strip), strip };
  await page.close();
}
// ---- B) hint + log line + trap sentence at #135
{
  const page = await browser.newPage();
  page.on("pageerror", e => errors.push({ at: "B", msg: String(e && e.message || e) }));
  await page.goto("file://" + path.resolve(html));
  const tmp = path.join(os.tmpdir(), `d54-state-${process.pid}.json`);
  /* import at 129 picks (owner on the clock at #130) and feed #130-#134 through
     the box, so the advisor's two-turn hysteresis runs the way it did live */
  fs.writeFileSync(tmp, JSON.stringify({ ...st0, picks: st0.picks.slice(0, 129) }));
  await page.setInputFiles("#importFile", tmp);
  await page.waitForSelector("#draft:not(.hidden)");
  for (const pk of st0.picks.slice(129, 134)) { await page.fill("#feed", pk.player); await page.click("#logBtn"); }
  const advisor = await page.locator("#deckmeta").innerText();
  await page.fill("#feed", "my: Ajay Mitchell"); await page.dispatchEvent("#feed", "input"); await page.waitForTimeout(100);
  const hint = (await page.locator("#feedHint").innerText()).trim();
  const before = (await page.locator("#mirror").innerText()).length;
  await page.click("#logBtn"); await page.waitForTimeout(150);
  const after = await page.locator("#mirror").innerText();
  res.at135 = { hint, hintOffCard: /off the card: Ajay Mitchell ranks #\d+/.test(hint), hintLateRule: /round-9\+ rule/.test(hint),
                logLine: /off the card: Ajay Mitchell/.test(after.slice(before)), trapSentence: /AST is dead — don't reach/.test(advisor),
                advisorExcerpt: (advisor.match(/AST is dead[^.]*\./) || [null])[0] };
  await page.close();
}
await browser.close();
res.pageErrors = errors;
res.pass = res.replay.positionsDiffering === 1 && res.replay.diff[0][0] === 97 && res.replay.fixedLines >= 1 && res.replay.stillOpenWarned && res.replay.stripNamesOpen
        && res.at135.hintOffCard && res.at135.hintLateRule && res.at135.logLine && res.at135.trapSentence && errors.length === 0;
fs.writeFileSync(outPath, JSON.stringify(res, null, 1));
console.log(JSON.stringify({ pass: res.pass, replay: { positionsDiffering: res.replay.positionsDiffering, diff: res.replay.diff, fixed: res.replay.fixedLines, stillOpenWarned: res.replay.stillOpenWarned, stripNamesOpen: res.replay.stripNamesOpen }, at135: res.at135, pageErrors: errors.length }));
