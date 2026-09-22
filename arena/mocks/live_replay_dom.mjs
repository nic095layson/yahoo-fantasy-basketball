// Replay a live-room tool log through the REAL deck page in headless Chromium
// (mock 53 integrity test, 2026-09-22): every feed / insert / undo the owner
// sent, in order, asserting the deck's echo line, recording the on-the-clock
// text under the feed title and the status strip after each event, and
// capturing page errors. Usage:
//   node arena/mocks/live_replay_dom.mjs   (PW_MODULE=<path to playwright> if not /opt/node22/lib/node_modules/playwright) <deck.html> <events.json> <out.json> [teams size slot]
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
// the global playwright install (npm root -g); ESM ignores NODE_PATH, so resolve it explicitly
const { chromium } = createRequire(import.meta.url)(process.env.PW_MODULE || "/opt/node22/lib/node_modules/playwright");
const [html, evPath, outPath, teamsA = "12", sizeA = "13", slotA = "10"] = process.argv.slice(2);
const events = JSON.parse(fs.readFileSync(evPath, "utf8"));
const teams = +teamsA, size = +sizeA, slot = +slotA;
const teamOfPick = (n, t) => { const r = Math.floor(n / t), i = n % t; return r % 2 === 0 ? i + 1 : t - i; };
function expectedClock(nPicks) {
  if (nPicks >= teams * size) return { text: "(draft complete)", onClock: false };
  const onClock = teamOfPick(nPicks, teams) === slot;
  let next = null; for (let n = nPicks; n < teams * size; n++) if (teamOfPick(n, teams) === slot) { next = n + 1; break; }
  if (onClock) return { text: "(you're on the clock)", onClock: true };
  const left = teams * size - nPicks;
  return { text: next === null ? `(your roster is full — ${left} pick${left === 1 ? "" : "s"} left in the draft)` : `(${next - (nPicks + 1)} until your pick)`, onClock: false, next };
}
const browser = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || "/opt/pw-browsers/chromium", args: ["--no-sandbox"] });
const page = await browser.newPage();
const errors = [];
page.on("pageerror", e => errors.push({ at: "pageerror", msg: String(e && e.message || e) }));
page.on("console", m => { if (m.type() === "error") errors.push({ at: "console", msg: m.text() }); });
await page.goto("file://" + path.resolve(html));
await page.fill("#cfgTeams", String(teams)); await page.fill("#cfgSize", String(size)); await page.fill("#cfgSlot", String(slot));
await page.click("#modeLive"); await page.click("#startBtn");
await page.waitForSelector("#draft:not(.hidden)");
const mirror = async () => (await page.locator("#mirror").innerText()).split("\n").map(s => s.trim()).filter(Boolean);
let seen = (await mirror()).length;
const rows = []; let mismatches = 0, echoMiss = 0;
for (let k = 0; k < events.length; k++) {
  const ev = events[k]; const errBefore = errors.length;
  if (ev.op === "feed") { await page.fill("#feed", ev.text); await page.click("#logBtn"); }
  else if (ev.op === "insert") {
    if (await page.locator("#insertBar").evaluate(el => el.classList.contains("hidden"))) await page.click("#insertToggle");
    await page.fill("#insNum", String(ev.P)); await page.fill("#insName", ev.text); await page.click("#insBtn");
  } else if (ev.op === "undo") { await page.click("#undoBtn"); }
  const lines = await mirror(); const fresh = lines.slice(seen); seen = lines.length;
  const echoOK = fresh.some(l => l.includes(ev.expect));
  if (!echoOK) echoMiss++;
  // `deck` lives in the app closure; the saved state is in localStorage (the app's save()), read it there
  const nPicks = await page.evaluate(() => { for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); try { const v = JSON.parse(localStorage.getItem(k)); const st = v && v.state && v.state.picks ? v.state : (v && v.picks ? v : null); if (st && Array.isArray(st.picks) && st.teams) return st.picks.length; } catch (e) {} } return -1; });
  const countdown = (await page.locator("#feedCountdown").innerText()).trim();
  const onclockClass = await page.locator("#feedCountdown").evaluate(el => el.classList.contains("onclocknow"));
  const strip = (await page.locator("#strip").innerText()).replace(/\s+/g, " ").trim();
  const exp = expectedClock(nPicks);
  const ok = countdown.toLowerCase() === exp.text.toLowerCase() && onclockClass === exp.onClock;   /* the title row is CSS-uppercased */
  if (!ok) mismatches++;
  rows.push({ k, op: ev.op, text: ev.text ?? null, P: ev.P ?? null, expect: ev.expect, echoOK, fresh, nPicks, countdown, onclockClass, expected: exp.text, clockOK: ok, strip, newErrors: errors.slice(errBefore) });
}
const finalState = await page.evaluate(() => { for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); try { const v = JSON.parse(localStorage.getItem(k)); const st = v && v.state && v.state.picks ? v.state : (v && v.picks ? v : null); if (st && Array.isArray(st.picks) && st.teams) return st; } catch (e) {} } return null; });
await browser.close();
const summary = { deck: html, events: events.length, echoMisses: echoMiss, clockMismatches: mismatches, pageErrors: errors.length, finalPicks: finalState ? finalState.picks.length : null,
  firstMismatch: rows.find(r => !r.clockOK) ? { k: rows.find(r => !r.clockOK).k, ...rows.find(r => !r.clockOK) } : null };
fs.writeFileSync(outPath, JSON.stringify({ summary, rows, finalState, errors }, null, 1));
console.log(JSON.stringify({ ...summary, firstMismatch: summary.firstMismatch && { k: summary.firstMismatch.k, op: summary.firstMismatch.op, nPicks: summary.firstMismatch.nPicks, countdown: summary.firstMismatch.countdown, expected: summary.firstMismatch.expected } }));
