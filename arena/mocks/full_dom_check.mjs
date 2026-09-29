// Full-control integrity check of the REAL deck page in headless Chromium
// (system validation 2026-09-29). Exercises every interactive control the page
// has — setup fields, mode toggles, punt chips, Start, Daily sweep, Import
// (invalid / missing-keys / valid), Export (download), Copy, Reset (two-click),
// the feed (Log button + Enter + numbered fix), the live hint, Undo,
// Insert-at-#, Resync, all five tabs, every Best-available filter / lens /
// header sort / cat chip / row click, the Take buttons, the TARGET button, the
// head-to-head select, the tooltip, and a full MOCK run through "Draft them" —
// and cross-checks every number the page shows against the engine functions
// the page itself carries (availablePool, categoryRanks, rosterTotals,
// totalValue, rankCard(decwScores)). Usage:
//   node arena/mocks/full_dom_check.mjs <deck.html> <draft_state_54.json> <out.json>
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)(process.env.PW_MODULE || "/opt/node22/lib/node_modules/playwright");
const [html, statePath, outPath] = process.argv.slice(2);
const ST54 = JSON.parse(fs.readFileSync(statePath, "utf8"));
const TEAMS = 12, SIZE = 13, SLOT = 10;
const teamOfPick = (n, t) => { const r = Math.floor(n / t), i = n % t; return r % 2 === 0 ? i + 1 : t - i; };

const A = [];
function ok(id, cond, detail) { A.push({ id, ok: !!cond, detail: detail === undefined ? null : detail }); return !!cond; }
const errors = [];
const notes = {};

const browser = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || "/opt/pw-browsers/chromium", args: ["--no-sandbox"] });
// a harness crash must still leave the assertions it reached on disk
let harnessCrash = null;
process.on("uncaughtException", e => { harnessCrash = String(e && e.stack || e); writeOut(); process.exit(3); });
process.on("unhandledRejection", e => { harnessCrash = String(e && e.stack || e); writeOut(); process.exit(3); });
function writeOut() {
  const failed = A.filter(a => !a.ok);
  const out = { deck: html, at: new Date().toISOString(), assertions: A.length, failed: failed.length, harnessCrash,
    pass: failed.length === 0 && errors.length === 0 && !harnessCrash, pageErrors: errors, notes, failures: failed, all: A };
  fs.writeFileSync(outPath, JSON.stringify(out, null, 1));
  console.log(JSON.stringify({ assertions: A.length, failed: failed.length, pageErrors: errors.length, crash: !!harnessCrash, pass: out.pass, failures: failed.map(f => f.id) }));
  process.exitCode = out.pass ? 0 : 1;   /* a gate, not a report: DATA-PULL.md §7 step 5b (owner decision D6, 2026-09-29) */
}
async function newPage() {
  const ctx = await browser.newContext({ acceptDownloads: true });
  try { await ctx.grantPermissions(["clipboard-read", "clipboard-write"]); notes.clipboardGrant = "granted"; }
  catch (e) { notes.clipboardGrant = "grant failed: " + String(e.message || e); }
  const page = await ctx.newPage();
  page.on("pageerror", e => errors.push({ at: "pageerror", msg: String(e && e.message || e) }));
  page.on("console", m => { if (m.type() === "error") errors.push({ at: "console", msg: m.text() }); });
  await page.goto("file://" + path.resolve(html));
  return { ctx, page };
}
const stateOf = page => page.evaluate(() => { try { return JSON.parse(localStorage.getItem("draftdeck.v1")); } catch (e) { return null; } });
const picksOf = async page => ((await stateOf(page)) || { state: { picks: [] } }).state.picks;
const mirror = async page => (await page.locator("#mirror").innerText()).split("\n").map(s => s.trim()).filter(Boolean);
const strip = async page => (await page.locator("#strip").innerText()).replace(/\s+/g, " ").trim();
const hidden = (page, sel) => page.locator(sel).evaluate(el => el.classList.contains("hidden"));
const num = s => parseFloat(String(s).replace("−", "-").replace(/[^0-9.+-]/g, ""));
const nonIncreasing = xs => xs.every((v, i) => i === 0 || v <= xs[i - 1] + 1e-9);
const nonDecreasing = xs => xs.every((v, i) => i === 0 || v >= xs[i - 1] - 1e-9);
async function tableRows(page) {
  return page.locator("#bestRows tr").evaluateAll(trs => trs.map(tr => [...tr.cells].map(td => td.innerText.trim())));
}
async function topFive(page) {
  return page.locator("#recos li").evaluateAll(lis => lis
    .map(li => ({ rk: (li.querySelector(".rk") || {}).textContent || "", nm: (li.querySelector(".nm") || {}).textContent || "" }))
    .filter(r => /^[1-5]$/.test(r.rk.trim()))
    .map(r => r.nm.replace(/^🎯\s*/, "").replace(/[▲*]+$/, "").trim()));   /* ▲ = the risk flag the card appends to a name */
}
async function pinNames(page) {
  return page.locator("#recos .nm").evaluateAll(ns => ns.map(n => n.textContent).filter(t => t.startsWith("🎯")).map(t => t.replace(/^🎯\s*/, "").replace(/[▲*]+$/, "").trim()));
}
// the engine's own card ordering (what check_parity compares against hoops.py), over the owner pool (veto applied)
async function engineTop5(page) {
  return page.evaluate(() => {
    const d = JSON.parse(localStorage.getItem("draftdeck.v1")); const st = d.state;
    const veto = new Set((typeof JUDGMENT !== "undefined" && JUDGMENT.doNotDraft) || []);
    const rosters = buildRosters(st, PLAYERS);
    const mine = rosters[st.slot] || [];
    const opp = []; for (let s = 1; s <= st.teams; s++) if (s !== st.slot) opp.push(rosters[s] || []);
    const pool = availablePool(st, PLAYERS).filter(p => !veto.has(p.n));
    return rankCard(decwScores(pool, mine, opp)).slice(0, 5).map(x => x.p.n);
  });
}
const availCount = page => page.evaluate(() => { const st = JSON.parse(localStorage.getItem("draftdeck.v1")).state; return availablePool(st, PLAYERS).length; });
async function bestAvailByMkt(page) {
  return page.evaluate(() => { const st = JSON.parse(localStorage.getItem("draftdeck.v1")).state;
    const p = availablePool(st, PLAYERS).filter(p => p.mkt != null).sort((a, b) => a.mkt - b.mkt)[0]; return p ? p.n : null; });
}
async function feed(page, text, viaEnter) {
  await page.fill("#feed", text);
  if (viaEnter) await page.press("#feed", "Enter"); else await page.click("#logBtn");
}
async function exportState(page) {
  try {
    const [dl] = await Promise.all([page.waitForEvent("download", { timeout: 8000 }), page.click("#exportBtn")]);
    const p = await dl.path();
    return { filename: dl.suggestedFilename(), json: JSON.parse(fs.readFileSync(p, "utf8")) };
  } catch (e) { return { error: String(e.message || e) }; }
}
function tmpJson(name, obj) { const p = path.join(os.tmpdir(), name); fs.writeFileSync(p, JSON.stringify(obj)); return p; }

/* ============ S1: setup page, import, draft-complete state, export, reset ============ */
{
  const { ctx, page } = await newPage();
  ok("S1.setup-visible", !(await hidden(page, "#setup")) && (await hidden(page, "#draft")));
  ok("S1.echo-default", (await page.locator("#echo").innerText()) === "12 teams × 13 rounds = 156 total picks (last pick #156)", await page.locator("#echo").innerText());
  await page.fill("#cfgTeams", "10");
  ok("S1.echo-updates-on-input", (await page.locator("#echo").innerText()) === "10 teams × 13 rounds = 130 total picks (last pick #130)", await page.locator("#echo").innerText());
  await page.fill("#cfgTeams", "1"); await page.click("#startBtn");
  ok("S1.invalid-teams", !(await hidden(page, "#setupErr")) && (await page.locator("#setupErr").innerText()) === "Teams must be 2 or more.", await page.locator("#setupErr").innerText());
  await page.fill("#cfgTeams", "12"); await page.fill("#cfgSize", "0"); await page.click("#startBtn");
  ok("S1.invalid-rounds", (await page.locator("#setupErr").innerText()) === "Rounds must be 1 or more.", await page.locator("#setupErr").innerText());
  await page.fill("#cfgSize", "13"); await page.fill("#cfgSlot", "13"); await page.click("#startBtn");
  ok("S1.invalid-slot", (await page.locator("#setupErr").innerText()) === "Your slot must be between 1 and 12.", await page.locator("#setupErr").innerText());
  ok("S1.invalid-start-stays-on-setup", !(await hidden(page, "#setup")) && (await hidden(page, "#draft")));
  await page.fill("#cfgSlot", "10");
  await page.click("#modeMock");
  ok("S1.mode-mock-pressed", (await page.getAttribute("#modeMock", "aria-pressed")) === "true" && (await page.getAttribute("#modeLive", "aria-pressed")) === "false");
  await page.click("#modeLive");
  ok("S1.mode-live-pressed", (await page.getAttribute("#modeLive", "aria-pressed")) === "true" && (await page.getAttribute("#modeMock", "aria-pressed")) === "false");
  const chips = page.locator("#setupPunt button.chip");
  ok("S1.punt-chips-9", (await chips.count()) === 9, await chips.count());
  const ft = chips.filter({ hasText: /^FT%$/ });
  await ft.click(); ok("S1.punt-chip-toggles-on", (await ft.getAttribute("aria-pressed")) === "true");
  await ft.click(); ok("S1.punt-chip-toggles-off", (await ft.getAttribute("aria-pressed")) === "false");
  // Daily sweep panel
  await page.click("#pullBtn");
  await page.waitForFunction(() => document.getElementById("pullPanel").innerText.length > 0, null, { timeout: 3000 }).catch(() => {});   /* the panel fills after an awaited clipboard write */
  const panel = await page.locator("#pullPanel").innerText();
  ok("S1.sweep-panel-opens", !(await hidden(page, "#pullPanel")) && /Data is/.test(panel), panel.slice(0, 160));
  ok("S1.sweep-panel-names-last-sweep", /Last sweep \(2026-09-28\)/.test(panel));
  notes.sweepPanelPlacementsSentence = (panel.match(/re-verifies all [^,]+,/) || [""])[0];
  await page.click("#pullBtn");
  ok("S1.sweep-panel-closes", await hidden(page, "#pullPanel"));
  // Import: file chooser opens from the button
  const [fc] = await Promise.all([page.waitForEvent("filechooser", { timeout: 5000 }).catch(() => null), page.click("#importBtn")]);
  ok("S1.import-button-opens-chooser", !!fc);
  // invalid JSON
  await page.setInputFiles("#importFile", { name: "bad.json", mimeType: "application/json", buffer: Buffer.from("{not json") });
  await page.waitForTimeout(150);
  ok("S1.import-invalid-json", (await page.locator("#setupErr").innerText()) === "That file isn't valid JSON.", await page.locator("#setupErr").innerText());
  await page.setInputFiles("#importFile", { name: "keys.json", mimeType: "application/json", buffer: Buffer.from(JSON.stringify({ teams: 12 })) });
  await page.waitForTimeout(150);
  ok("S1.import-missing-keys", (await page.locator("#setupErr").innerText()) === "Missing keys — expected {teams, slot, size, punt, picks}.", await page.locator("#setupErr").innerText());
  // valid: the full committed mock-54 state (156 picks)
  await page.setInputFiles("#importFile", tmpJson("s54_full.json", ST54));
  await page.waitForSelector("#draft:not(.hidden)");
  const m = await mirror(page);
  ok("S1.import-valid-enters-draft", m.some(l => l === "Imported draft state: 156 picks, you are Team 10."), m.slice(-2));
  const s = await strip(page);
  ok("S1.draft-complete-strip", /Draft complete — 156 picks/.test(s) && /your roster: Team 10/.test(s) && /no punt/.test(s), s);
  ok("S1.draft-complete-countdown", (await page.locator("#feedCountdown").innerText()).trim().toLowerCase() === "(draft complete)");   /* the title row is CSS-uppercased */
  ok("S1.draft-complete-placeholder", (await page.getAttribute("#feed", "placeholder")) === "draft complete");
  ok("S1.draft-complete-card", (await page.locator("#recos").innerText()).includes("Draft complete."));
  ok("S1.draft-complete-roster-13", (await page.locator("#myRoster li:not(.empty)").count()) === 13, await page.locator("#myRoster li:not(.empty)").count());
  ok("S1.advance-hidden-in-live", await hidden(page, "#advanceBtn"));
  const ex = await exportState(page);
  ok("S1.export-download", ex.filename === "draft_state.json" && ex.json && ex.json.picks.length === 156 && ex.json.slot === 10 && !("cast" in ex.json), ex.error || { filename: ex.filename, picks: ex.json && ex.json.picks.length, keys: ex.json && Object.keys(ex.json) });
  ok("S1.export-logged", (await mirror(page)).some(l => /^Exported draft_state\.json/.test(l)));
  // Reset: two-click confirm
  await page.click("#resetBtn");
  ok("S1.reset-armed", (await page.locator("#resetBtn").innerText()) === "Click again to confirm reset" && !(await hidden(page, "#draft")));
  await page.click("#resetBtn");
  ok("S1.reset-clears", !(await hidden(page, "#setup")) && (await hidden(page, "#draft")) && (await stateOf(page)) === null && (await page.locator("#mirror").innerText()).trim() === "" && (await page.locator("#resetBtn").innerText()) === "Reset draft");
  ok("S1.reset-remembers-slot", (await page.inputValue("#cfgSlot")) === "10", await page.inputValue("#cfgSlot"));
  await ctx.close();
}

/* ============ S2: LIVE room replay of mock 54 with every control exercised ============ */
{
  const { ctx, page } = await newPage();
  await page.fill("#cfgTeams", String(TEAMS)); await page.fill("#cfgSize", String(SIZE)); await page.fill("#cfgSlot", String(SLOT));
  await page.click("#modeLive"); await page.click("#startBtn");
  await page.waitForSelector("#draft:not(.hidden)");
  ok("S2.start-log", (await mirror(page))[0] === "Draft started: 12 teams × 13 rounds = 156 picks; you are Team 10 · LIVE", (await mirror(page))[0]);
  ok("S2.feed-title-live", (await page.locator("#feedTitle").innerText()).toLowerCase() === "pick feed");
  ok("S2.advance-hidden", await hidden(page, "#advanceBtn"));
  {
    const s = await strip(page); const av = await availCount(page);
    ok("S2.strip-pick1", /Pick #1 · R1\/13/.test(s) && /Seat 1 on the clock/.test(s) && /your next: #10/.test(s) && /your roster: 0\/13/.test(s) && /no punt/.test(s) && s.includes(`${av} available`), { s, av });
    ok("S2.countdown-pick1", (await page.locator("#feedCountdown").innerText()).trim().toLowerCase() === "(9 until your pick)", await page.locator("#feedCountdown").innerText());
    ok("S2.placeholder-pick1", (await page.getAttribute("#feed", "placeholder")) === "Pick 1 — Team (1)", await page.getAttribute("#feed", "placeholder"));
  }
  const ownerTurns = []; let substitutions = 0; let targetSeen = 0, targetClicked = false, lastCallSeen = 0;
  const veto = await page.evaluate(() => (typeof JUDGMENT !== "undefined" && JUDGMENT.doNotDraft) || []);
  let sideDone = false;
  for (let n = 0; n < TEAMS * SIZE; n++) {
    const seat = teamOfPick(n, TEAMS);
    const before = await picksOf(page);
    if (before.length !== n) { ok(`S2.replay-desync-at-${n}`, false, before.length); break; }
    if (seat === SLOT) {
      const turn = { n, pickNo: n + 1 };
      const s = await strip(page);
      turn.onClock = /YOU are on the clock/.test(s) && (await page.locator("#feedCountdown").innerText()).trim().toLowerCase() === "(you're on the clock)"
        && (await page.locator("#feedCountdown").evaluate(el => el.classList.contains("onclocknow")))
        && (await page.getAttribute("#feed", "placeholder")) === `Pick ${n + 1} — Team (10 / YOU)`;
      const top5 = await topFive(page); const pins = await pinNames(page); const eng = await engineTop5(page);
      turn.top5 = top5; turn.pins = pins; turn.engineTop5 = eng;
      turn.cardMatchesEngine = JSON.stringify(top5) === JSON.stringify(eng);
      turn.onePin = pins.length === 1;
      turn.vetoAbsent = !top5.some(nm => veto.includes(nm)) && !pins.some(nm => veto.includes(nm));
      const recosText = await page.locator("#recos").innerText();
      if (/LAST CALL/.test(recosText)) lastCallSeen++;
      // live hint under the feed
      await page.fill("#feed", "my: " + top5[1]); await page.dispatchEvent("#feed", "input"); await page.waitForTimeout(60);
      const h2 = await page.locator("#feedHint").innerText();
      turn.hintOffCard = h2.startsWith(`off the card: ${top5[1]} ranks #2 (`) && h2.includes(`behind 🎯 ${top5[0]}`) && ((n + 1) > 8 * TEAMS ? h2.includes("round-9+ rule") : !h2.includes("round-9+ rule"));
      turn.hint2 = h2;
      await page.fill("#feed", "my: " + top5[0]); await page.dispatchEvent("#feed", "input"); await page.waitForTimeout(60);
      turn.hintPin = (await page.locator("#feedHint").innerText()) === `${top5[0]} is the 🎯`;
      await page.fill("#feed", ""); await page.dispatchEvent("#feed", "input");
      // TARGET / BOARD LEAN button
      const tb = page.locator("#deckmeta button.target");
      if (await tb.count()) {
        targetSeen++;
        if (!targetClicked) {
          turn.targetLabel = await tb.first().innerText();
          await tb.first().click(); await page.waitForTimeout(60);
          turn.targetClickSetsFitLens = (await page.inputValue("#bestSort")) === "fit" && (await hidden(page, "#bestChips"));
          ok("S2.target-button-click", turn.targetClickSetsFitLens, { label: turn.targetLabel, sort: await page.inputValue("#bestSort"), pos: await page.inputValue("#bestPos") });
          targetClicked = true;
          await page.click("#bestReset");
        }
      }
      // take the card's #1 via the Take button, then Log
      const take = page.locator("#recos li .take").first();
      turn.takeLabel = await take.innerText();
      await take.click();
      turn.takeStages = (await page.inputValue("#feed")) === "my:" + top5[0];
      const linesBefore = (await mirror(page)).length;
      await page.click("#logBtn");
      const after = await picksOf(page);
      const fresh = (await mirror(page)).slice(linesBefore);
      turn.logged = after.length === n + 1 && after[n].player === top5[0] && after[n].slot === SLOT;
      turn.noGapWarn = !fresh.some(l => l.includes("off the card"));
      turn.rosterShows = (await page.locator("#myRoster").innerText()).includes(top5[0].split(" ").slice(-1)[0]);
      ownerTurns.push(turn);
      ok(`S2.turn#${n + 1}`, turn.onClock && turn.cardMatchesEngine && turn.onePin && turn.vetoAbsent && turn.hintOffCard && turn.hintPin && turn.takeStages && turn.logged && turn.noGapWarn && turn.rosterShows, turn);
    } else {
      let name = ST54.picks[n].player;
      if (before.some(pk => pk.player === name)) { name = await bestAvailByMkt(page); substitutions++; }
      await feed(page, name, n === 0);
      const after = await picksOf(page);
      const good = after.length === n + 1 && after[n].player === name && after[n].slot === seat;
      if (!good) ok(`S2.opp-pick#${n + 1}`, false, { name, after: after[n], len: after.length });
      if (n === 0) ok("S2.enter-key-logs", good);
      if (n % 24 === 0 && n > 0) {
        const s = await strip(page); const av = await availCount(page);
        ok(`S2.strip-at-${n}`, s.includes(`Pick #${n + 2}`) && s.includes(`${av} available`) && s.includes(`your roster: ${after.filter(pk => pk.slot === SLOT).length}/13`), { s, av });
      }
    }
    /* ---- side features, once, with 24 picks on the board (pick #25, seat 1 on the clock) ---- */
    if (!sideDone && (await picksOf(page)).length === 24) {
      sideDone = true;
      const P = await picksOf(page); const names = P.map(pk => pk.player);
      // tabs
      for (const t of ["boardtab", "rosters", "matrix", "vs", "best"]) {
        await page.click("#tab-" + t);
        const sel = await page.getAttribute("#tab-" + t, "aria-selected");
        const others = await page.locator("[role=tabpanel]").evaluateAll((ps, t) => ps.filter(p => p.id !== "pane-" + t).every(p => p.classList.contains("hidden")), t);
        ok(`S2.tab-${t}`, sel === "true" && !(await hidden(page, "#pane-" + t)) && others);
      }
      // grid (snake) + tooltip
      ok("S2.grid-head", (await page.locator("#gridHead th").count()) === 13 && (await page.locator("#gridHead th").nth(10).innerText()) === "Seat 10 YOU");
      ok("S2.grid-rows", (await page.locator("#gridRows tr").count()) === 13);
      const r1c1 = await page.locator("#gridRows tr").nth(0).locator("td").nth(1).innerText();
      const r2c12 = await page.locator("#gridRows tr").nth(1).locator("td").nth(12).innerText();
      const r2c1 = await page.locator("#gridRows tr").nth(1).locator("td").nth(1).innerText();
      ok("S2.grid-snake", r1c1 === names[0] && r2c12 === names[12] && r2c1 === names[23], { r1c1, r2c12, r2c1 });
      await page.click("#tab-boardtab");
      await page.hover("#gridRows tr >> nth=0 >> td >> nth=1");
      await page.waitForTimeout(60);
      const tip = await page.locator("#tip").evaluate(el => ({ display: getComputedStyle(el).display, text: el.textContent }));
      ok("S2.tooltip", tip.display === "block" && tip.text === "#1 → Seat 1", tip);
      // rosters
      const rosterChk = await page.evaluate(() => {
        const st = JSON.parse(localStorage.getItem("draftdeck.v1")).state; const punt = new Set(st.punt);
        const R = buildRosters(st, PLAYERS); const out = [];
        document.querySelectorAll("#rosterGrid .roster").forEach((div, i) => {
          const s = i + 1; const exp = (R[s] || []).reduce((a, p) => a + totalValue(p, punt), 0);
          const got = parseFloat(div.querySelector(".tot").textContent.replace("kept-cat value ", "").replace("−", "-"));
          out.push({ s, exp: +exp.toFixed(3), got, ok: Math.abs(exp - got) <= 0.051, you: div.classList.contains("you"), h3: div.querySelector("h3").textContent, n: div.querySelectorAll("li").length });
        });
        return out;
      });
      ok("S2.rosters-12", rosterChk.length === 12 && rosterChk.every(r => r.ok) && rosterChk[9].you && rosterChk[9].h3 === "Team 10 — YOU" && rosterChk.filter(r => r.you).length === 1, rosterChk.filter(r => !r.ok));
      // matrix
      const matrixChk = await page.evaluate(() => {
        const st = JSON.parse(localStorage.getItem("draftdeck.v1")).state; const punt = new Set(st.punt);
        const { ranks, totals } = categoryRanks(st, PLAYERS); const CATS9 = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"];
        const rows = [...document.querySelectorAll("#matrixRows tr")]; const bad = [];
        rows.forEach((tr, i) => { const s = i + 1; const cells = [...tr.cells].map(td => parseFloat(td.textContent.replace("−", "-")));
          CATS9.forEach((c, j) => { if (Math.abs(cells[j + 1] - totals[s][c]) > 0.051) bad.push([s, c, cells[j + 1], totals[s][c]]); });
          const kept = CATS9.filter(c => !punt.has(c)).reduce((a, c) => a + totals[s][c], 0);
          if (Math.abs(cells[10] - kept) > 0.051) bad.push([s, "kept", cells[10], kept]); });
        const note = document.getElementById("matrixNote").textContent;
        return { rows: rows.length, bad, youRow: rows[9] && rows[9].className === "you", note, noteOK: note.startsWith("Your rank:") && (note.match(/\d+\/12/g) || []).length === 9, ranks };
      });
      ok("S2.matrix", matrixChk.rows === 12 && matrixChk.bad.length === 0 && matrixChk.youRow && matrixChk.noteOK, { bad: matrixChk.bad, note: matrixChk.note });
      // head-to-head
      const vsOpts = await page.locator("#vsTeam option").evaluateAll(os => os.map(o => o.value));
      ok("S2.vs-options", vsOpts.length === 11 && !vsOpts.includes("10"), vsOpts);
      await page.click("#tab-vs");
      await page.selectOption("#vsTeam", "1"); await page.waitForTimeout(50);
      const vsChk = await page.evaluate(() => {
        const st = JSON.parse(localStorage.getItem("draftdeck.v1")).state; const punt = new Set(st.punt);
        const R = buildRosters(st, PLAYERS); const a = rosterTotals(R[st.slot]), b = rosterTotals(R[1]);
        const CATS9 = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]; const bad = []; let w = 0, l = 0;
        [...document.querySelectorAll("#vsRows tr")].forEach((tr, i) => { const c = CATS9[i]; const cells = [...tr.cells].map(td => td.textContent.trim());
          const lead = a[c] > b[c] ? "you" : (b[c] > a[c] ? "them" : "tied"); if (!punt.has(c) && a[c] !== b[c]) { w += lead === "you"; l += lead === "them"; }
          if (Math.abs(parseFloat(cells[1].replace("−", "-")) - a[c]) > 0.0051 || Math.abs(parseFloat(cells[2].replace("−", "-")) - b[c]) > 0.0051 || cells[3] !== lead) bad.push([c, cells, a[c], b[c], lead]); });
        const mrow = [...document.querySelectorAll("#matrixRows tr")][st.slot - 1]; const mcells = [...mrow.cells].map(td => parseFloat(td.textContent.replace("−", "-")));
        const consistent = CATS9.every((c, j) => Math.abs(mcells[j + 1] - a[c]) <= 0.051);
        return { n: document.querySelectorAll("#vsRows tr").length, bad, note: document.getElementById("vsNote").textContent, expNote: `Kept categories: you lead ${w}–${l} vs Team 1`, consistent };
      });
      ok("S2.vs-table", vsChk.n === 9 && vsChk.bad.length === 0 && vsChk.note === vsChk.expNote && vsChk.consistent, vsChk);
      await page.click("#tab-best");
      // Best available: row click stages a pick for the seat on the clock (not the owner's turn: no "my:")
      const firstRowName = await page.locator("#bestRows tr").first().locator("td").nth(2).evaluate(td => td.childNodes[0].textContent.trim());
      await page.locator("#bestRows tr").first().click();
      ok("S2.row-click-stages", (await page.inputValue("#feed")) === firstRowName, { feed: await page.inputValue("#feed"), firstRowName });
      await page.fill("#feed", "");
      // position filter
      await page.selectOption("#bestPos", "C");
      const posRows = await tableRows(page);
      ok("S2.filter-pos-C", posRows.length > 0 && posRows.every(r => r[4].split(/[,/]/).map(s => s.trim()).includes("C")), posRows.slice(0, 3).map(r => r[4]));
      await page.selectOption("#bestPos", "");
      // search + Enter (drafted lookup)
      const q = firstRowName.split(" ").slice(-1)[0].slice(0, 4).toLowerCase();
      await page.fill("#bestQ", q);
      const qRows = await tableRows(page);
      ok("S2.filter-search", qRows.length > 0 && qRows.every(r => r[2].toLowerCase().includes(q)) && (await page.locator("#bestSummary").innerText()).includes(`matching “${q}”`), { q, n: qRows.length });
      const dq = names[0].split(" ").slice(-1)[0].toLowerCase();
      await page.fill("#bestQ", dq); await page.press("#bestQ", "Enter");
      ok("S2.search-enter-drafted", (await page.locator("#bestSummary").innerText()).includes(`${names[0]} — Drafted #1 (R1) by Team 1`), await page.locator("#bestSummary").innerText());
      await page.fill("#bestQ", "porz");
      const vetoRow = await tableRows(page);
      ok("S2.veto-row-marked", vetoRow.length === 1 && vetoRow[0][2].includes("⛔ DO NOT DRAFT"), vetoRow.map(r => r[2]));
      await page.fill("#bestQ", "");
      // show N
      await page.selectOption("#bestTop", "12");
      ok("S2.show-12", (await tableRows(page)).length <= 12, (await tableRows(page)).length);
      await page.selectOption("#bestTop", "25");
      // lenses
      await page.selectOption("#bestSort", "val");
      ok("S2.lens-val-sorted", nonIncreasing((await tableRows(page)).map(r => num(r[5]))));
      await page.selectOption("#bestSort", "decw");
      ok("S2.lens-decw-sorted", nonIncreasing((await tableRows(page)).map(r => num(r[6])).filter(v => !isNaN(v))) && (await page.locator("#thRoster").innerText()).startsWith("ΔECW"));
      await page.selectOption("#bestSort", "fit");
      ok("S2.lens-fit-header", (await page.locator("#thRoster").innerText()).startsWith("Fit") && nonIncreasing((await tableRows(page)).map(r => num(r[6])).filter(v => !isNaN(v))));
      await page.selectOption("#bestSort", "mkt");
      ok("S2.lens-mkt-sorted", nonDecreasing((await tableRows(page)).map(r => num(r[0])).filter(v => !isNaN(v))));
      // Mkt column equals the baked price rank
      const mktChk = await page.evaluate(() => { const st = JSON.parse(localStorage.getItem("draftdeck.v1")).state;
        const mr = marketRanks(PLAYERS.filter(p => p.av > 0)); const bad = [];
        [...document.querySelectorAll("#bestRows tr")].forEach(tr => { const name = tr.cells[2].childNodes[0].textContent.trim(); const shown = tr.cells[0].textContent.trim();
          const exp = mr.get(name); if (String(exp) !== shown.replace(/[^0-9]/g, "")) bad.push([name, shown, exp]); });
        return { checked: document.querySelectorAll("#bestRows tr").length, bad }; });
      ok("S2.mkt-column-matches-marketRanks", mktChk.checked > 0 && mktChk.bad.length === 0, mktChk);
      // cat lens via header clicks
      const th = c => page.locator("#bestHead th").filter({ hasText: new RegExp("^" + c.replace("%", "\\%") + "$") });
      await th("PTS").click();
      ok("S2.cat-lens-PTS", !(await hidden(page, "#bestChips")) && (await page.locator("#bestChips .catchip").count()) === 1 && (await page.inputValue("#bestSort")) === "" && nonIncreasing((await tableRows(page)).map(r => num(r[10]))));
      await th("REB").click(); await th("AST").click();
      ok("S2.cat-lens-3", (await page.locator("#bestChips .catchip").count()) === 3);
      await th("ST").click();
      ok("S2.cat-lens-cap", (await page.locator("#bestChips .catchip").count()) === 3 && (await page.locator("#bestChips").innerText()).includes("3-cat limit"));
      await th("PTS").click();
      ok("S2.cat-lens-drill", await page.locator("#bestChips .catchip").first().evaluate(el => el.classList.contains("drilled")) && nonIncreasing((await tableRows(page)).map(r => num(r[10]))));
      await page.locator("#bestChips .catchip").first().click();
      ok("S2.cat-chip-remove", (await page.locator("#bestChips .catchip").count()) === 2);
      await page.click("#bestReset");
      ok("S2.best-reset", (await hidden(page, "#bestChips")) && (await page.inputValue("#bestSort")) === "mkt" && (await page.inputValue("#bestPos")) === "" && (await page.inputValue("#bestQ")) === "" && (await page.inputValue("#bestTop")) === "25");
      // Undo, then re-log
      const lb = (await mirror(page)).length;
      await page.click("#undoBtn");
      const afterUndo = await picksOf(page);
      ok("S2.undo", afterUndo.length === 23 && (await mirror(page)).slice(lb).some(l => l.startsWith(`↶ undid: ${names[23]} (Seat ${P[23].slot})`)), (await mirror(page)).slice(lb));
      await feed(page, names[23], false);
      ok("S2.relog-after-undo", (await picksOf(page)).length === 24);
      // Insert-at-#
      await page.click("#insertToggle");
      ok("S2.insert-bar-opens", !(await hidden(page, "#insertBar")) && (await page.evaluate(() => document.activeElement && document.activeElement.id)) === "insNum");
      const lb2 = (await mirror(page)).length;
      await page.click("#insBtn");
      ok("S2.insert-empty-warns", (await mirror(page)).slice(lb2).some(l => l === "Insert needs a pick # and a player name."), (await mirror(page)).slice(lb2));
      const insName = await bestAvailByMkt(page);
      await page.fill("#insNum", "3"); await page.fill("#insName", insName); await page.click("#insBtn");
      const afterIns = await picksOf(page);
      ok("S2.insert-empty-warn-visible-after-next-render", (await mirror(page)).some(l => l === "Insert needs a pick # and a player name."));
      ok("S2.insert-shifts", afterIns.length === 25 && afterIns[2].player === insName && afterIns[3].player === names[2] && afterIns[24].player === names[23] && (await hidden(page, "#insertBar")), { len: afterIns.length, p2: afterIns[2], p3: afterIns[3] });
      // Resync: refuse empty, then rebuild the 24-pick board from a paste
      await page.click("#resyncBtn");
      ok("S2.resync-bar-opens", !(await hidden(page, "#resyncBar")));
      const lb3 = (await mirror(page)).length;
      await page.click("#resyncGo");
      ok("S2.resync-empty-refused", (await mirror(page)).slice(lb3).some(l => l.startsWith("RESYNC refused")) && (await picksOf(page)).length === 25);
      await page.fill("#resyncPaste", names.join("; ")); await page.press("#resyncPaste", "Enter");
      const afterRs = await picksOf(page);
      const rsLog = (await mirror(page)).slice(lb3);
      ok("S2.resync-empty-refusal-visible-after-next-render", (await mirror(page)).some(l => l.startsWith("RESYNC refused")));
      ok("S2.resync-rebuilds", afterRs.length === 24 && afterRs.every((pk, i) => pk.player === names[i] && pk.slot === P[i].slot) && rsLog.some(l => l.startsWith("RESYNC: cleared 25 pick(s); rebuilt 24")) && (await hidden(page, "#resyncBar")) && (await page.evaluate(() => localStorage.getItem("draftdeck.v1:preresync") !== null)), rsLog.slice(0, 2));
      // numbered correction through the feed, then restore
      const alt = await bestAvailByMkt(page);
      await feed(page, `24- ${alt}`, false);
      const afterFix = await picksOf(page);
      ok("S2.numbered-fix", afterFix.length === 24 && afterFix[23].player === alt, afterFix[23]);
      await feed(page, `24- ${names[23]}`, false);
      ok("S2.numbered-fix-restore", (await picksOf(page))[23].player === names[23]);
      // Copy + Export
      const lb4 = (await mirror(page)).length;
      await page.click("#copyBtn"); await page.waitForTimeout(100);
      const copyLine = (await mirror(page)).slice(lb4).find(l => /clipboard/i.test(l)) || "";
      let clipRead = null; try { clipRead = await page.evaluate(() => navigator.clipboard.readText()); } catch (e) { clipRead = "readText failed: " + e.message; }
      const copyOK = copyLine === "State JSON copied to clipboard." && (() => { try { return JSON.parse(clipRead).picks.length === 24; } catch (e) { return false; } })();
      ok("S2.copy-state", copyOK || copyLine === "Clipboard unavailable — use Export instead.", { copyLine, clipHead: String(clipRead).slice(0, 60) });
      notes.copyPath = copyOK ? "clipboard write + read-back verified" : copyLine;
      const ex = await exportState(page);
      ok("S2.export-24", ex.json && ex.json.picks.length === 24 && ex.json.teams === 12 && ex.json.slot === 10 && ex.json.size === 13, ex.error || ex.filename);
    }
  }
  const P = await picksOf(page);
  ok("S2.replay-complete", P.length === 156, P.length);
  const s = await strip(page);
  ok("S2.final-strip", /Draft complete — 156 picks/.test(s), s);
  ok("S2.final-card", (await page.locator("#recos").innerText()).includes("Draft complete."));
  ok("S2.final-roster-13", P.filter(pk => pk.slot === SLOT).length === 13 && (await page.locator("#myRoster li:not(.empty)").count()) === 13);
  ok("S2.owner-turns-13", ownerTurns.length === 13, ownerTurns.length);
  ok("S2.card-matches-engine-all-turns", ownerTurns.every(t => t.cardMatchesEngine), ownerTurns.filter(t => !t.cardMatchesEngine).map(t => ({ n: t.pickNo, top5: t.top5, eng: t.engineTop5 })));
  ok("S2.veto-never-on-card", ownerTurns.every(t => t.vetoAbsent));
  ok("S2.hint-late-rule-from-round-9", ownerTurns.filter(t => t.pickNo > 96).every(t => t.hint2.includes("round-9+ rule")) && ownerTurns.filter(t => t.pickNo <= 96).every(t => !t.hint2.includes("round-9+ rule")));
  notes.live = { substitutions, targetSeen, lastCallSeen, ownerTurns };
  await ctx.close();
}

/* ============ S3: punt declared at setup ============ */
{
  const { ctx, page } = await newPage();
  await page.fill("#cfgTeams", "12"); await page.fill("#cfgSize", "13"); await page.fill("#cfgSlot", "10");
  await page.locator("#setupPunt button.chip").filter({ hasText: /^FT%$/ }).click();
  await page.click("#modeLive"); await page.click("#startBtn"); await page.waitForSelector("#draft:not(.hidden)");
  ok("S3.start-log-punt", (await mirror(page))[0].includes("; punting FT% · LIVE"), (await mirror(page))[0]);
  ok("S3.strip-punt", (await strip(page)).includes("punting FT%"));
  for (const pk of ST54.picks.slice(0, 3)) await feed(page, pk.player, false);
  const mx = await page.evaluate(() => { const tr = document.querySelectorAll("#matrixRows tr")[0]; const td = tr.cells[2]; return { deco: getComputedStyle(td).textDecorationLine, note: document.getElementById("matrixNote").textContent }; });
  ok("S3.matrix-punted-struck", mx.deco.includes("line-through") && mx.note.includes("punted: FT%"), mx);
  ok("S3.vs-punted-label", (await page.locator("#vsRows tr").nth(1).locator("td").first().innerText()) === "FT% (punted)");
  const rchk = await page.evaluate(() => { const st = JSON.parse(localStorage.getItem("draftdeck.v1")).state; const R = buildRosters(st, PLAYERS);
    const exp = (R[1] || []).reduce((a, p) => a + totalValue(p, new Set(["FT%"])), 0); const got = parseFloat(document.querySelector("#rosterGrid .roster .tot").textContent.replace("kept-cat value ", "").replace("−", "-")); return { exp, got }; });
  ok("S3.rosters-kept-excludes-punt", Math.abs(rchk.exp - rchk.got) <= 0.051, rchk);
  await ctx.close();
}

/* ============ S4: MOCK room — the 11 league-mates draft against the card ============ */
{
  const { ctx, page } = await newPage();
  await page.fill("#cfgTeams", "12"); await page.fill("#cfgSize", "13"); await page.fill("#cfgSlot", "10");
  await page.click("#modeMock"); await page.click("#startBtn"); await page.waitForSelector("#draft:not(.hidden)");
  const m0 = await mirror(page);
  ok("S4.start-log", m0[0].endsWith("· MOCK — your 11 league-mates hold the other seats") && m0[1].startsWith("Cast: Seat 1:"), m0.slice(0, 2));
  ok("S4.auto-advance-to-owner", (await picksOf(page)).length === 9 && (await page.locator("#feedTitle").innerText()).toLowerCase() === "your pick #10" && !(await hidden(page, "#advanceBtn")), { n: (await picksOf(page)).length, title: await page.locator("#feedTitle").innerText() });
  ok("S4.cast-seated", (await stateOf(page)).state.cast.length === 11);
  const take = page.locator("#recos li .take").first();
  ok("S4.take-label", (await take.innerText()) === "Draft them", await take.innerText());
  const t5 = await topFive(page);
  await take.click(); await page.waitForTimeout(100);
  let P = await picksOf(page);
  ok("S4.draft-them-auto-advances", P.length === 14 && P[9].player === t5[0] && P[9].slot === 10 && (await page.locator("#feedTitle").innerText()).toLowerCase() === "your pick #15", { n: P.length, p9: P[9] });
  // typed pick with my: + Enter, then input memory across undo
  const t5b = await topFive(page);
  const typed = "my: " + t5b[1];
  await feed(page, typed, true); await page.waitForTimeout(100);
  P = await picksOf(page);
  ok("S4.typed-pick-logs-and-advances", P.length === 33 && P[14].player === t5b[1] && P[14].slot === 10, { n: P.length, p14: P[14] });
  const gapWarned = (await mirror(page)).some(l => l.includes(`off the card: ${t5b[1]} ranks #2`));
  ok("S4.gap-warn-on-off-card-pick", gapWarned);
  for (let i = 0; i < 19; i++) await page.click("#undoBtn");
  P = await picksOf(page);
  ok("S4.undo-x19-back-to-owner-turn", P.length === 14 && (await page.inputValue("#feed")) === typed, { n: P.length, feed: await page.inputValue("#feed") });
  await page.fill("#feed", ""); await page.click("#undoBtn");
  ok("S4.undo-owner-pick", (await picksOf(page)).length === 13);
  await page.click("#advanceBtn");
  ok("S4.advance-button", (await picksOf(page)).length === 14);
  // play it out through the card
  let guard = 0;
  while ((await picksOf(page)).length < 156 && guard++ < 20) { await page.locator("#recos li .take").first().click(); await page.waitForTimeout(80); }
  P = await picksOf(page);
  ok("S4.mock-complete", P.length === 156 && P.filter(pk => pk.slot === 10).length === 13 && new Set(P.map(pk => pk.player)).size === 156, { n: P.length, guard });
  ok("S4.complete-log", (await mirror(page)).some(l => l.startsWith("Draft complete — export the state")));
  const ex = await exportState(page);
  ok("S4.export-has-cast", ex.json && ex.json.picks.length === 156 && Array.isArray(ex.json.cast) && ex.json.cast.length === 11, ex.error || (ex.json && Object.keys(ex.json)));
  await ctx.close();
}

await browser.close();
writeOut();
