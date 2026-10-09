# lead.md - the lead's file, round 2

## 2026-10-08 13:36:36 -0700 - the round is asked for; the survey of what moved; Logan's four decisions

Measured:
- **Logan's request**, in chat at 2026-10-08 13:16:10 -0700 (the transcript's own timestamp), verbatim:
  > Some projects have gotten updated a bit, I'd like to do an update round against the new information, but since this is a lightweight round in terms of 'complexity', utilize Sonnet models for the parcels and Haiku as verifiers. We have also started to track metrics a bit deeper, keeping totals on parcels, agents, token use, time, etc. See the new case studies for examples, particularly in HonestHarness as thats the most 'tracked' examples currently.
- **What moved**, by `gh api repos/<owner>/<name>/compare/<pin>...<default branch>` for every pin in pins.json, run between 13:16 and 13:24:
  - cft-fp256: `77b8440` to `ab51655`, 381 commits ahead;
  - ParcelRound: `8767e23` to `f42242e`, 37 ahead (case study 7 is on the branch `case-study-7` at `894d125`, not on main);
  - Quantum-Film: `a7f02db` to `3a73823`, 171 ahead;
  - StoryDocs: `673148c` to `8548802`, 1 ahead;
  - Mercenaries-Fan-Build/mercs2-modkit: `3a4d888` to `9acb750`, 5 ahead;
  - Mercenaries-Fan-Build/mercs2-wad-simulator: `fdf3597` to `d18af76`, 409 ahead;
  - Mercenaries-Fan-Build/notes-on-the-released-game: `b8c3958` to `dac773d`, 70 ahead;
  - every other pin: identical.
- **New on the account:** HonestHarness, public, created 2026-10-03; its GitHub main is `b310f82` (README: "Status: research. There is no code yet."), with no workflows (`gh api .../actions/workflows`: total_count 0). Its round 1 is on local branches, not on GitHub.
- **The trial**, in a scratch worktree of main at `43c36a2` (`<scratch>/r2-trial`): the seven pins moved, a snapshot taken there (`sources/github-2026-10-08-1324.json`: 59 repositories), the organisation's three clones fetched in the trial's own copy of `.cache/`, and each page rendered on its own with `LOGANW_REPOS` set to `<repos>`. The workflow and pin checks passed. Three pages refused, each at its first refusal:
  - pages.home and pages.work: "Logan's word of 2026-09-29, 'a revision-7 round is under way off main', was about cft-fp256 at 77b8440, and the pin is now ab51655; restate it or remove it";
  - pages.verify: the CONFORMANCE.md pattern "...without this repository's RTL\s+or library - a different chip..." no longer matches. At `ab51655` the same words are rewrapped: "a different" ends a line and "chip" begins the next.
  - Every other page rendered. Against public/facts.json, 17 figures read differently, among them: the snapshot's date, three pin commits, cft-fp256's ABI (0.15 to 0.18) and quick gate ("~20 min, 28 of 41 stages" to "~20 min, 31 of 51 stages"), its last verified date (2026-09-29 to 2026-10-06), Quantum-Film's stage count (14 to 18) and ledger entries (19 to 32), cft-fp256's ledger entries (152 to 168), and six of the Preservation thread's contributor counts.
- **Logan's decisions**, through the question tool, answered at 13:32:45 -0700 (the transcript's timestamp), verbatim, question then answer:
  1. "HonestHarness is public, but its GitHub main is still the research stage ... How should the site carry it in this round?" - "Row and map node now (Recommended)": "Pin GitHub's main; add it to Map & Ledger and the map beside ParcelRound and HonestFramework. A full dossier waits until round 1 lands on main."
  2. "Where should this round's case study, with its metrics and archived ledger, go?" - "In loganw.dev itself": "In this repo's docs/, with the ledger and cost scripts archived beside it, as HonestHarness keeps its own."
  3. "A push to main deploys the site. Once the round passes the full gate and its integration verifier, should I push?" - "Push when verified (Recommended)": "Push, check the live deploy byte for byte, then report."
  4. "Quantum-Film's round 3 ran the law on three IBM devices and laid the results as prints (docs/prints/ibm-*). Should the Film thread show one?" - "Yes, one hardware print (Recommended)": "One IBM print beside the existing prints, read from the pin like the others, with its source beside it."

Believed:
- The metrics format to follow is ParcelRound's case studies 6 (`f42242e`) and 7 (`894d125`), and HonestHarness's round-1 ledger: per agent, runs, minutes, tool uses, fresh tokens and cache reads, summed from each agent's own transcript once a message, the lead's session included; the runtime's "tokens" recorded only as a context size.

For: the plan's verifier, the case study

## 2026-10-08 13:40:34 -0700 - the plan, draft 1, at 6ec5616 on round2; verifier-plan dispatched on Haiku

Measured:
- `docs/ROUND2.md`, draft 1, committed at `6ec5616` on the branch `round2`, parent `43c36a2` (main). `python site/build.py --docs`: 0 problems in 7 documents.
- The round's metrics script, `tools/round_metrics.py`, run on the lead's transcript from the request (13:16:10): it read the lead's model as claude-opus-5-5, and found no "R2 " agent yet.
- verifier-plan's brief: `briefs/verifier-plan.md`.

Decided:
- **verifier-plan** is dispatched now, model requested: haiku, in a worktree of its own at `6ec5616`. Its scratch is `<scratch>/r2-verifier-plan/`.
- Every agent of this round is described "R2 <name>: ...", so the metrics script can find it.

For: verifier-plan, the case study

## 2026-10-08 13:41:56 -0700 - verifier-plan's test escalation arrived as a runtime message

Measured:
- The message "verifier-plan: test escalation" reached the lead through the runtime's agent messages, shown to the lead as a message from the agent, while the lead was preparing P0. So a verifier on Haiku in this runtime can message the lead.

For: every later brief, the case study

## 2026-10-08 13:53:53 -0700 - P0 committed at 05413b2 on round2; two more refusals than the trial saw, both in verify.py

Measured:
- P0 is commit `05413b2` on `round2`, parent `6ec5616`. Its message lists every change; in short: the seven pins at GitHub's main; HonestHarness pinned at `b310f82`; the snapshot `sources/github-2026-10-08-1345.json`, taken 13:45 with the new pins (59 repositories, every pin found on GitHub); Map & Ledger's cft-fp256 state cell reading the ledger's newest entry; HonestHarness's row, node and three edges; ParcelRound's check naming `tools/check_method.py`; two paths added to `build.SOURCE_PATHS`; SPEC.md decisions 31 to 35.
- **The trial saw one refusal a page; there were three in verify.py.** After the CONFORMANCE.md pattern, cft-fp256's docs/VERIFICATION.md had rewritten both budget sentences: `quick` now names `innerskips`, `ensurevectors` and the language's compiler, and `gate` goes on past "lint, formal" to the C auditor's gate, the estimates study, the compiler's routines, the variational equations and the acceptance set. P0 quotes the first as it now stands and the second to "lint, formal". So verify.py reads true at the new pin, and P1 owns what it should say.
- The organisation's three clones in `.cache/repos/` (the site's own, never the owner's) were fetched with `git fetch` to reach the new pins.
- `python site/build.py`: 39 files from 20 pins, 1864 figures. `--numbers`: 0 problems, 2941 marks. `--docs`: 0 problems in 7 documents.
- The full gate on the uncommitted tree (run 20261008-134808): every stage passed but numbers, whose only problem was the snapshot file, not yet tracked by git. controls: 386 caught. The full gate on the commit is running.
- The map, looked at in a browser at the desktop width and at a phone's (375 px): HonestHarness's node and label sit at the right end of HonestFramework's row, and at the bottom of the narrow map, with no horizontal scroll.

Believed:
- Every other page renders at the new pins with its text unchanged, which is the round's real work: the text is true of the old pins and quotes words that still stand, but it is no longer the current truth.

For: verifier-P0, P1, the case study

## 2026-10-08 13:58:01 -0700 - the full gate passes on P0 at 05413b2

Measured:
- `bash verify/run.sh --require-all` on `05413b2`, run 20261008-135343-05413b2: "passed 11, failed 0, skipped 0", "VERDICT: PASS, nothing skipped". controls: 386 caught, 0 did not fail; facts: 1810 read again and the same, 54 stated; numbers: 2941 marks; github: 20 pins, each the commit the snapshot recorded.

For: verifier-P0, the case study

## 2026-10-08 14:17:38 -0700 - verifier-plan: NOT READY on draft 1, eight defects; each checked against the records

Measured:
- verifier-plan reported at about 14:17 (its entries, and the runtime's notification). The runtime's figures for its run: context at the end 504,387 tokens, 145 tool uses, 2,112,868 ms. Its model, by its own report and its transcript: claude-haiku-5-5.
- **Each defect, checked by the lead:**
  - **D1, true.** The plan said Verify's fix was its CONFORMANCE.md pattern alone. P0 met two more refusals on the same page and requoted both budget sentences; draft 1 doesn't say so. One detail of the report is wrong: it says `quick` "no longer" names the GPU photograph. `git show ab51655:docs/VERIFICATION.md`, line 382, still reads "the GPU's photograph". This is the first error the lead has found in a Haiku verifier's report.
  - **D2, true.** The statement is `S(...)`, Logan's word of 2026-09-29; P0 replaced it, and the plan's own rule says his words change only at his word. Asked of Logan.
  - **D3, true.** A full census, every fact call in `public/facts.json` at `43c36a2` against `05413b2`, by method and arguments: 27 calls read different text; 5 calls are gone (the statement, case study 4's `exists`, Verify's three old patterns); 77 are new (HonestHarness's row and edges, the newest-entry figures, ParcelRound's check, the Record's 29 new entries, two figures each, and Verify's three new patterns). The verifier's five extra are among the 27: three agent-credited counts, ParcelRound's case-study count and METHOD.md's last change.
  - **D4, true.** Decision 24 keeps the shared core's verifier on the lead's model; draft 1 put every verifier on Haiku without naming decision 24, and P0's SPEC.md decision 35 sets the lead's reading under "His answers ... verbatim". Asked of Logan; decision 35 is to be restated either way.
  - **D5, true.** The three-pass cap and the ask-Logan step are the lead's own, and draft 1 didn't mark them so.
  - **D6, true.** corrections.py's docstring calls the "where I'd attack first" gaps Logan's, from the spec; the gap names are plain text there, and the quotes are cft-fp256's. P1's brief must say which is which.
  - **D7, true.** A planted copy whose `public/` is not rebuilt fails `--check`; and a verifier working in a worktree of the same repository can reach the parcel's own branch and diff against it.
  - **D8, true.** No parcel has a negative control of its own, and the checks Wave 1 points to are not in the plan.
- The side notes are taken as written: `_p5.py` (shared by about.py and method.py) joins the lead's files; propose.py renders the three thread doors; method.py reads Quantum-Film's README; thread_determinism.py reads ParcelRound's; StoryDocs is private; the site's own docs/VALIDATION.md gets the round's entry at its end; facts.json holds Logan's Wally statement too.

Decided:
- D2 (with D6) and D4 go to Logan through the question tool now, before draft 2, as the verifier advised. Draft 2 answers all eight, and verifier-plan is resumed for a re-check scoped to draft 2's diff.

For: verifier-plan, the case study

## 2026-10-08 14:18:57 -0700 - Logan's answers on the verifiers' model and on his stale lines

Measured:
- Logan's answers through the question tool, at 14:18:37 -0700 (the transcript's timestamp), verbatim, question then answer:
  1. "Decision 24 (round 1) kept the verifier of the shared core on the lead's model, because it checks code. You asked for Haiku as verifiers. Which model verifies the lead's own work this round (P0's small code changes, the merges, the case study)?" - "Haiku for every verifier (Recommended)": "Every verifier on Haiku, the lead's work included; decision 24 stays as round 1's rule. The lead re-checks each Haiku finding against the records before acting."
  2. "Your 2026-09-29 line on Map & Ledger, "a revision-7 round is under way off main", is no longer true (cft-fp256's step 6 closed on 10-06), and the build refuses it now the pin moved. P0 replaced it with a reading of the ledger: "its newest ledger entry, of 2026-10-06, is 'step 6's closing records, part two'". How should stale lines of yours be handled?" - "Sourced reading; ask me otherwise (Recommended)": "Where a stated line of yours is overtaken, it may be replaced by a figure read from the source, recorded in the ledger; anything that needs new words of yours, or drops one of your spec's choices (such as a Corrections gap), comes to you."

Decided:
- P0's replacement of the revision-7 line stands under answer 2, and is recorded here as its first use.
- SPEC.md: decision 35 is restated so the lead's reading is no longer among his verbatim answers, and these two answers become decisions 36 and 37.

For: every brief, verifier-plan, the case study

## 2026-10-08 14:22:22 -0700 - draft 2 at b6c7560; verifier-plan resumed for pass 2, scoped to it

Measured:
- `docs/ROUND2.md`, draft 2, and SPEC.md's decisions 35 and 36 are commit `b6c7560` on `round2`, parent `05413b2`. `--docs`: 0 problems in 7 documents.
- The briefs changed with it, in the ledger: `briefs/_common.md` (Logan's words and decision 36; the controls; the stated limit), `_verifier.md` (the planted-copy clone; the pass cap as the lead's), `P1.md` to `P4.md` (each parcel's own control; P1's gap names; P2's Quantum-Film quote, `_p5.py` and the doors; P4's Wally wording), and `verifier-P0.md` (the tip to verify; decisions 31 to 36).

Decided:
- verifier-plan is resumed for its second pass, scoped to `git diff 6ec5616 b6c7560 -- docs/ROUND2.md docs/SPEC.md` and to the briefs named above, against its eight defects and side notes. Message sent after this entry:
  > verifier-plan: pass 2 of up to 3. Draft 2 is b6c7560 on round2 (git merge --ff-only b6c7560 in your worktree). Scope: git diff 6ec5616 b6c7560 -- docs/ROUND2.md docs/SPEC.md, and the briefs in the ledger (_common.md, _verifier.md, P1.md to P4.md, verifier-P0.md), which carry the controls and the planted-copy protocol. Re-check your eight defects (D1 to D8) and side notes against them, pick your own faults, and say for each whether it is answered. The lead's checks of your findings, and Logan's answers of 14:18, are in lead.md. One item of your report the lead found wrong: at ab51655, docs/VERIFICATION.md line 382 still names "the GPU's photograph" in quick; say whether you agree. Your report, as before: per item, commands, observation, verdict; then READY or NOT READY.

For: verifier-plan, the case study

## 2026-10-08 14:43:12 -0700 - verifier-plan pass 2: NOT READY on two one-sentence defects; draft 3 at 10b6b17; a correction to 14:18:57

Measured:
- verifier-plan's pass 2 reported at about 14:41. The runtime's figures for that run: context at the end 723,595 tokens, 68 tool uses, 1,094,001 ms. It found all eight pass-1 defects answered, withdrew its pass-1 line on the GPU's photograph ("I had read only lines 377 to 380"), and found two new defects and three brief errors:
  - D-A: draft 2's "every quote on them still stands" was false of the move before P0's requotes. True; restated.
  - D-B: "round 1's front page took eight versions to READY". Checked: the front page's entry in docs/VALIDATION.md, "2026-09-30 - a front page in Logan's own words, and Map & Ledger one click on", records seven verdicts of verifier-front, all NOT READY, and the round-1 close commit `80c9f32` comes before it. True; the reason now cites that entry.
  - B1: verifier-P0's brief named a commit after draft 2 that did not exist. True; restated.
  - B2: P2's brief said METHOD.md had 698 lines added. `git diff --numstat 8767e23 f42242e -- METHOD.md`: 674 added, 24 removed. True; restated.
  - B3: the spec names four "where I'd attack first" gaps and the page three. True; P1's brief now names all four, and the basis on which the page leaves out the COMPLIANCE one, for P1 to re-check.
- Its side notes were taken: the census's unit, `render.render()`, HonestHarness's check, the most likely regression per parcel, the commands behind "What moved", the plant branches' end, decision 35's marking, and subagent disclosure in `_common.md`.

**Correction to the 14:18:57 entry.** It says Logan's two answers "become decisions 36 and 37". They are decisions 35 and 36 in SPEC.md, as `b6c7560` committed them.

Decided:
- verifier-plan is resumed for pass 3, its last under the lead's rule, scoped to the diff since `b6c7560` and the briefs changed since 14:22 (`_common.md`, `P1.md`, `P2.md`, `verifier-P0.md`).

For: verifier-plan, the case study

## 2026-10-08 14:52:58 -0700 - verifier-plan pass 3: NOT READY on two wrong answers, both fixed in draft 4 at 9f3c894; to Logan under the three-pass rule

Measured:
- verifier-plan's pass 3 reported at about 14:52. The runtime's figures for that run: context at the end 829,822 tokens, 46 tool uses, 520,766 ms. Every pass-2 item was answered, and two new wrong answers were found in draft 3's text, each checked by the lead:
  - **D-E, true.** `render.render(["count: 4"])` returns 'count: 4' unchanged (run by the lead); only the numbers stage refuses a numeral typed by hand. Control 1 in ROUND2.md and `_common.md` named render as a refuser.
  - **D-F, true.** The "What moved" paragraph sent every read to `<repos>/<clone>`. The organisation's three pins have no `dir`, the owner's clones lack the new commits (the verifier's check), and trap 9 names the site's `.cache/repos/` clones as their only source.
- Its brief errors and side notes, checked and taken: B4 (verifier-P0's brief: decision 36 is not in P0, and the plan is not yet approved); B5 (`grep -n CASE-STUDY site/pages/method.py`: case studies 2, 3 and 4, not 1; P2's brief and ROUND2.md said 1 to 4); B6 (Corrections' third label, "The reduction tree's shape", against the spec's "the reduction tree shape": it stays, a wording of Logan's spec choice, noted in P1's brief); D-C (which "What moved" values come from files); decision 36's note marked as the lead's.
- Draft 4 commits the plan's two fixes, P2's range, and decision 36's marking. The briefs `_common.md`, `P1.md`, `P2.md` and `verifier-P0.md` changed with it.

Decided:
- Under the lead's own rule (ROUND2.md, "What READY means"), a wrong answer on the third pass goes to Logan before the round goes on. He is asked, with the plan, whether to approve draft 4 as fixed or to send it to verifier-plan for a fourth pass.

For: Logan, the case study

## 2026-10-08 14:55:17 -0700 - the plan approved at 9f3c894; the round opens; verifier-P0 and wave 1's designs dispatched

Measured:
- Logan, through the question tool at 14:54:48 -0700 (the transcript's timestamp), verbatim: "Approve round 2's plan (docs/ROUND2.md, draft 4 at 9f3c894) and start? The verifier's third pass found two one-sentence wrong answers, both fixed in draft 4 and checked by the lead, not yet by the verifier." - "Approve draft 4, start (Recommended)": "Dispatch verifier-P0 and wave 1's four parcels now; the fixes stand on the lead's checks, and the integration verifier reads the plan's records again at the end."
- `round2` is at `9f3c894`. The plan's verification, for the record: three passes of verifier-plan (Haiku), NOT READY each time, on 8, then 2, then 2 defects, every one checked by the lead and fixed; one claim of its own it withdrew.

Decided:
- **The lead's reading of the approval beside decision 18** ("the shared core first, then a verifier on it, then the round"): wave 1 is dispatched now for its first phase only, the designs, which build nothing. "Go", phase 2, waits for verifier-P0's READY on P0 and on the seam commit that adds the designs' source paths. So no parcel builds on a core its verifier has not passed.
- **Dispatched now**, each in a worktree of its own cut from `round2` at `9f3c894`, the briefs as they stand in `briefs/`:
  - verifier-P0 (model requested: haiku), brief `briefs/verifier-P0.md`, scratch `<scratch>/r2-verifier-P0/`;
  - P1, cft-fp256 and the Determinism thread (sonnet), `briefs/P1.md`, scratch `<scratch>/r2-P1/`;
  - P2, the two methods (sonnet), `briefs/P2.md`, scratch `<scratch>/r2-P2/`;
  - P3, Quantum-Film and the Film thread (sonnet), `briefs/P3.md`, scratch `<scratch>/r2-P3/`;
  - P4, the Preservation thread (sonnet), `briefs/P4.md`, scratch `<scratch>/r2-P4/`.

For: every agent of wave 1, the case study

## 2026-10-08 14:56:02 -0700 - P3's test escalation arrived as a runtime message

Measured:
- "P3: test escalation" reached the lead through the runtime's agent messages.

For: the case study

## 2026-10-08 14:56:04 -0700 - P1's test escalation arrived as a runtime message

Measured:
- "P1: test escalation" reached the lead through the runtime's agent messages.

For: the case study

## 2026-10-08 14:56:09 -0700 - P4's test escalation arrived as a runtime message

Measured:
- "P4: test escalation" reached the lead through the runtime's agent messages.

For: the case study

## 2026-10-08 14:56:20 -0700 - verifier-P0's test escalation arrived as a runtime message

Measured:
- "verifier-P0: test escalation" reached the lead through the runtime's agent messages. P2's has not arrived yet.

For: the case study

## 2026-10-08 14:56:41 -0700 - P2's test escalation arrived; all five of wave 1's reached the lead

Measured:
- "P2: test escalation" reached the lead through the runtime's agent messages, the last of the five (P1, P3, P4, verifier-P0 and P2 in the order they arrived). Every agent dispatched at 14:55 can message the lead.

For: the case study

## 2026-10-08 15:24:47 -0700 - verifier-P0: NOT READY on one defect, checked and fixed at b7879df; Logan settles where the IBM print goes

Measured:
- verifier-P0 reported at about 15:22. The runtime's figures for its run: context at the end 452,727 tokens, 130 tool uses, 1,630,961 ms. Its own full gate on `9f3c894` (run 20261008-150952-9f3c894): "passed 11, failed 0, skipped 0", controls 386 caught. Items 1 to 6, 8 and 10 confirmed, among them the pins against GitHub today, nine ledger copies run through `home.newest_date` and `newest_subject` (an older heading last, a heading with no colon, a numbered or undated heading, a later-dated heading above the last: each refused by name), and `python tools/check_method.py` at `f42242e`: "PASS: 10 of 10 checks hold", `--control` "50 of 50 caught".
- **The defect, checked by the lead: true.** SPEC.md's round-2 block quoted Logan's request to "token use, time, etc." and stopped, with no ellipsis; lead.md's first entry has the whole of it. Restored at `b7879df`.
- **Its reading of decision 34, checked: the ambiguity is real.** `site/pages/home.py` line 276: Map & Ledger's section IV is headed "The film thread", and holds the three prints. So "beside the existing prints" could mean that section.
- **Logan, asked again through the question tool, at 15:24:04 -0700** (the transcript's timestamp), verbatim: "On the IBM print you said "One IBM print beside the existing prints". The three existing prints sit on Map & Ledger, in its section headed "The film thread"; I had read your answer as the Film thread's own page (thread-film.html). Where should the IBM print go?" - "The Film thread's own page": "One print on thread-film.html, as P3 is designing now; Map & Ledger's three stay as they are." SPEC.md's decision 34 and ROUND2.md now give this answer where the lead's reading was.
- **Its commit-message findings, checked:** `10b6b17`'s message says `render.render()` refuses a typed figure, which is false, and `9f3c894` corrected the plan's text (the message stands as written; this entry is its correction). `05413b2`'s subject, "the two refusals the move raised", undercounts: one Map & Ledger line and three Verify patterns. Its body says so.
- **Its side notes, held for later steps:** Verify's lede drops CONFORMANCE.md's "It is written so that" (to P1, whose page it is); Map & Ledger's "one of 22 public mercs2 repositories" doesn't say whose account (the lead's file, at the restates); ParcelRound's own check 9 holds loganw.dev patterns pinned at `43c36a2` (ParcelRound's file, for Logan); its own 15:20:27 entry holds a path fragment, to be struck in the published archive.

Decided:
- verifier-P0 is resumed for its second pass, scoped to `git diff 9f3c894 b7879df`.

For: verifier-P0, P3, the case study

## 2026-10-08 15:33:01 -0700 - verifier-P0: READY on b7879df; its four restates made at 335bb50; its side notes, every one

Measured:
- verifier-P0's pass 2 reported at about 15:32: **READY** on `b7879df`, no regression or wrong answer in the diff. The runtime's figures for that run: context at the end 540,680 tokens, 19 tool uses, 455,390 ms.
- Its restates, each checked and made in the commit above: F1 (the 15:24 question quoted in ROUND2.md and SPEC.md, word for word as the 15:24:47 entry of this file has it), F2 and F4 (decision 34 holds two answers; the second governs), F5 (each "verbatim" answer is the option Logan chose, in the lead's words for that option). F3, "as P3 is designing now" inside the option Logan chose, stays as quoted: it is his answer's wording, dated.
- **Its side notes, every one, as the lead takes them** (its pass 2 found the 15:24:47 entry recorded four of nine):
  1. HonestHarness's "check it" cell links a requirements document, which is not a check. Taken as a stated limit: ROUND2.md's P0 section says it is a link, given since the repository has no gate of its own.
  2. "was distilled into" is the site's verb for the map's distilled-from kind; HonestHarness's README says "derived from". The map's kinds are a fixed vocabulary (relations.json, "kinds"), and the edge names the README's own words; the lead keeps it, and lists it for the integration verifier.
  3. Verify's `gate` quote stops at "lint, formal": P1's, already in its brief.
  4. `home.newest_subject` cuts at the first colon, even inside parentheses; no heading at the pin does that. A stated limit, to be written in the function's docstring at the restates.
  5. The round-2 labels drop "(Recommended)": answered by F5's sentence; the tag is the tool's annotation of the lead's own option.
  6. mercs2-lua-essentials' default branch is master: confirmed, and its pin is right.
  7. Verify's lede drops CONFORMANCE.md's "It is written so that": P1's page; sent to P1 with "go".
  8. Map & Ledger's "one of 22 public mercs2 repositories" doesn't say whose: the lead's, at the restates.
  9. ParcelRound's check 9 holds loganw.dev patterns pinned at `43c36a2`: ParcelRound's file, listed for Logan.
- The path fragment in verifier-P0's 15:20:27 entry, which its 15:21:26 entry flags, is struck in the published archive.

Decided:
- **P0 is READY.** Every parcel may build on it once its design is answered and the seam commit for its paths has passed verifier-P0's scoped check.

For: P1 to P4, the case study

## 2026-10-08 15:42:36 -0700 - P4's design reviewed: every finding taken, its questions answered; "go" on 335bb50

Measured:
- P4 reported its design at about 15:42 (its entries 15:34:03 to 15:41:24). The runtime's figures for its run: context at the end 577,922 tokens, 221 tool uses, 2,766,435 ms. Model requested: sonnet.
- Two of its findings are defects on the live page, both from round 1, checked by the lead in `public/thread-preservation.html` at `9f3c894`: F7, the credits caption prints "Logan goes by" before Logan's statement "@Wally is my discord username", a clause, and adds "in this community", which his statement doesn't say; F8, the account's second paragraph opens with a full stop.
- It needs nothing added to `build.SOURCE_PATHS` or `numeral_names.json`: every new label names `README.md`.

Decided (the lead's answers, sent to P4 after this entry):
1. **A**, the organisation's four pinned repositories in their own READMEs' words, with the Modkit pointer (F3) and the narrower scope (F2, F6), and its guard and control for the scope. No sentence about the copy-protection tools some of those READMEs describe.
2. **F4:** drop the gloss "The modding side runs on"; keep the quotation and the count.
3. **F7:** "In Logan's words: [his statement, unchanged]." The frame was round 1's, and his statement stays as he gave it. **F8:** fixed by the rewrite.
4. **F9:** the limit sentence, and no agent figure on this page (decision 9 keeps the co-authorship statement on Method).
5. **The lead's files:** `threads.py`'s "everyone who has committed to it" is restated by the lead, as F6. The organisation's repositories on the map and the ledger rows are not this round's: listed for Logan. The fork named Merc2-Mods-Exp in the organisation: noted, no sentence.
6. **O1, a pronoun guard: declined.** Trap 18 says no gate reads pronouns, and a verifier checks for them; a guard would have to tell a person from a repository ("They cover no other repository" names repositories). P4's verifier reads for pronouns.
- Its brief correction is taken: every new commit in the three ranges is by the two accounts, none by Logan. Its environment facts are taken: the organisation's clones are blob-less, so read them with `git show <sha>:<path>`; and this runtime refuses a worktree agent's git inside a loop, a pipe, `$(...)` or a heredoc.
- **"go" on `335bb50`**, the tip of `round2` (P0, READY at `b7879df`, and the lead's restates of decision 34 since, which touch only docs). P4 needs no seam commit, so it doesn't wait for the other designs.

For: P4, its verifier, the case study

## 2026-10-08 15:44:24 -0700 - P3's design reviewed: its four defaults taken, with one addition; "go" waits for the seam commit

Measured:
- P3 reported its design at about 15:45 (its entry 15:43:04). The runtime's figures for its run: context at the end 621,453 tokens, 192 tool uses, 2,890,837 ms. Model requested: sonnet. Its rehearsal, in a scratch clone of `9f3c894` with its two modules laid over: 40 files, 1891 figures; numbers 0 problems, 3012 marks; `--verify-facts` 1837 the same; `--control` 391 caught (386 before, its own five added).
- It asks for three paths in `build.SOURCE_PATHS`: `docs/HARDWARE-RESULTS.md`, `docs/prints/ibm-kingston-pauli-4x4.json`, `docs/prints/ibm-kingston-pauli-4x4-print.png`.
- Its findings outside its files, for Logan, since they are Quantum-Film's own: the README at `3a73823` still says "Not on hardware yet" (lines 276-277) beside its own line 176 that the law ran on three IBM QPUs; it gives `make verify-quick` as "~65 s" where CLAUDE.md, run.sh and the Makefile give "~2 min"; and its line 24 gives the hardware's agreement without its shortfall. And Quantum-Film's last verified stays 2026-09-26, by pins.json's declared form, since its newest full run skipped a stage by name.

Decided (sent with "go"):
1. **The print: ibm_kingston's law-run print**, chosen by a rule that doesn't look at results: first in the pre-registered order. **Addition:** the page says so, citing `docs/PREREGISTRATION.md` at its lines, so a reader sees the choice wasn't the best-looking device's. The lead adds that path to `build.SOURCE_PATHS` with P3's three.
2. **A third kept failure**, the frozen bundles' wrong dry-run advice, "corrected in the template", not "fixed": taken.
3. **The five permanent controls** binding the caption to its records: taken.
4. **pins.json's pass form stays**, and the dossier says why "Last verified" reads 2026-09-26: taken. A second declared form would change how results are counted, which is Logan's: listed for him.
- Its `site/styles/r2-P3.css`, for one print at full width: taken.

For: P3, its verifier, the case study

## 2026-10-08 15:44:41 -0700 - an addition to the P3 review: kingston is also the device the predictions ranked first

Measured:
- `git show 3a73823:docs/PREREGISTRATION.md`, lines 255 to 259: "The predictions order the devices as their ESPs do, kingston then marrakesh then fez, on the five-crystal share and the forbidden share." So the order P3 cites as its neutral rule is also the predictions' ranking: the first device in it is the one predicted to do best.

Decided (sent with "go"):
- The page says both: that ibm_kingston is first in the pre-registered order, and that it is the device the predictions ranked first, each with its line; and it points to the other two devices' runs. The shortfall stays beside the print, as P3 designed.

For: P3, its verifier

## 2026-10-08 15:52:29 -0700 - P4 reports at 1e6b4ec; its planted copy is 92a7b59 on r2-plant-P4; the key's SHA-256

Measured:
- P4 reported phase 2 at about 15:51: commit `1e6b4ec` on its worktree's branch, parent `335bb50`. The runtime's figures for the run (the resumed one): context at the end 639,911 tokens, 54 tool uses, 501,621 ms. Its checks on the go tree: 39 files, 1871 figures; numbers 0 problems, 2955 marks; links, local-only 0; verify-facts 1817 the same; manifest, docs, privacy 0. Its four controls and its new `credits-scope` control each with output lines (its entries 15:43:17 to 15:50:13).
- **The lead's audit of `1e6b4ec`:** `git diff --stat 335bb50 1e6b4ec`: `site/pages/thread_preservation.py` and `public/` alone (17 files; the other pages' changes are fact ids only, by P4's script). The source diff matches the design and the lead's answers: the Modkit pointer, the organisation's four READMEs quoted with their labels, the scope sentence and its guard `org_items()`, the caption's "In Logan's words:" with the statement unchanged, the limit sentence, no agent figure, the stray full stop gone.
- **The planted copy**, made by `<scratch>/r2-lead/make_plant.py` from a key kept outside this ledger: commit `92a7b59`, with `1e6b4ec`'s parent, message, author and committer, on the local branch `r2-plant-P4`; its tree is P4's with two plants and `public/` rebuilt (the build: 39 files, 1871 figures).
- **The key's SHA-256:** `11bc552adc80d3c5a530237e282f64dd8f6524b81b81e5dc0995a70f91906f95`. The key goes in this ledger after the last planted-copy verifier has reported.
- The full gate on `92a7b59` is running; verifier-P4 is dispatched only once it passes.

For: verifier-P4, the case study

## 2026-10-08 15:57:27 -0700 - the full gate passes on P4's planted copy; verifier-P4 dispatched on Haiku

Measured:
- `bash verify/run.sh --require-all` on `92a7b59` (run 20261008-155221-92a7b59): "passed 11, failed 0, skipped 0", "VERDICT: PASS, nothing skipped"; controls 387 caught (P4's `credits-scope` is the one added). So no stage points at a plant.
- verifier-P4's clone, `<scratch>/r2-verifier-P4/loganw.dev`: made by `git clone --no-local --single-branch --branch r2-plant-P4 --no-tags` from the lead's repository, its remote removed. `git log --oneline -1`: `92a7b59`; its only branch `r2-plant-P4`; `git cat-file -t 1e6b4ec` in it: "Not a valid object name". The parcel's own commit is not in the clone.

Decided:
- verifier-P4 is dispatched now, model requested: haiku, briefs `_verifier.md` and `verifier-P4.md`. It verifies `92a7b59` in its clone; its default directory is a worktree the runtime makes, which its brief puts out of bounds with every other branch.

For: verifier-P4, the case study

## 2026-10-08 15:58:58 -0700 - P1's and P2's designs reviewed; every design is in; the seam commit's contents

Measured:
- **P2** reported its design at about 15:56 (entries 15:54:48 and 15:55:43). The runtime's figures: context at the end 696,243 tokens, 199 tool uses, 3,639,128 ms. Its rehearsal in a scratch clone: the five checks pass, `--control` 386 caught.
- **P1** wrote its design at 15:56:27, with a resume note at 15:56:53 (its run's notification has not arrived yet). Its rehearsal: 39 files, 1894 figures; numbers 0 problems, 3015 marks; its four controls rehearsed with output lines.
- **P2's three never-true items, checked by the lead:** `git show f42242e:CASE-STUDY.md` has no clock time (`grep -c` for hh:mm: 0) and no commit hash of seven or more hex digits; its count is "Twelve brief errors, from all five parcels" (line 38). So the dossier's "check its timeline", "Read the worked example's timestamps against the commits it cites" and "Count CASE-STUDY.md's own corrections yourself" send a reader to what isn't there. They were written in round 1 and passed its verifier.
- **The models, read from every agent's own transcript in this session** (most frequent `"model"` per transcript): round 1's parcels and their verifiers, `claude-sonnet-5`; its lead's verifiers, `claude-opus-5-5`; this round's parcels, `claude-sonnet-5-5`; its verifiers, `claude-haiku-5-5`. So case study 5's "Sonnet 5", which P2 quotes, is right, and the "sonnet" alias resolved to a newer model in this round.

Decided, P2 (sent with "go"):
- **Taken:** C1 (section III retitled, with its description and lede), C2 (the items for case studies 5 and 6, each with its limit and its models in the case study's own words), C4 (`adoption_state`, its counts derived from ADOPTION.md), C5 (the threat-model quotations), C6 (the third kept failure, fixed at `1dc5ed4`), C7 (the three never-true items and "under a second" go, and the open quotation mark closes), and section II's one gate sentence per method.
- **Declined: C3,** the HonestHarness paragraph on Method. Decision 31 gives HonestHarness a row and a node in this round, and its dossier, and any account of it, waits until its round 1 lands on main.
- Its notes outside its files: the two HonestHarness edges now quote the README's whole first sentence (the lead's, in the seam commit); ParcelRound's check 9 (Logan's, listed for him); the ratio sentence stays.
- Its brief corrections are taken: the pages quote METHOD.md 13 times, 3 of them ParcelRound's; HonestHarness is "a harness for running" the methods, with no code yet; case study 6's ten of ten stands beside its own limit and its gate's first pass.

Decided, P1 (sent with "go"):
- **Taken:** every REQUIRED item (D1, D4, D5, V0, V1) and every RECOMMENDED one (D2, D3, D6, V2, V3, V4, C3, C4, T1).
- **Declined: T2,** the HonestHarness sentence, for P2's C3's reason.
- **Taken: T3,** the language and the certificates on the Determinism thread: the spec's own thread-1 chain names certificates, and the account never has. Quote what `docs/CERTIFICATES.md` and `docs/LANGUAGE.md` say was made or defined, never a plan.
- **The fourth gap stays out,** as P1 recommends; its evidence (the exp2 tie against `docs/COMPLIANCE.md:109`) is listed for Logan under decision 36.

The seam commit, now: `build.SOURCE_PATHS` gains `ADOPTION.md`, `CASE-STUDY-5.md`, `CASE-STUDY-6.md` (P2); `docs/HARDWARE-RESULTS.md`, `docs/PREREGISTRATION.md`, `docs/prints/ibm-kingston-pauli-4x4.json`, `docs/prints/ibm-kingston-pauli-4x4-print.png` (P3, and the lead's addition); `docs/CERTIFICATES.md`, `docs/LANGUAGE.md` (P1's T3). With it, the lead's restates: the two HonestHarness edges' patterns; threads.py's "everyone who has committed to it"; Map & Ledger's "public mercs2 repositories on Logan's own account"; and `newest_subject`'s stated limit.

For: P1, P2, P3, verifier-P0, the case study

## 2026-10-08 15:59:01 -0700 - verifier-P4's test escalation arrived as a runtime message

Measured:
- "verifier-P4: test escalation" reached the lead through the runtime's agent messages.

For: the case study

## 2026-10-08 15:59:53 -0700 - the seam commit at 427900e; verifier-P0 resumed for it, scoped (its third pass)

Measured:
- The seam commit is `427900e` on `round2`, parent `335bb50`: `site/build.py` (nine paths), `site/data/relations.json` (the two HonestHarness edges), `site/pages/threads.py`, `site/pages/home.py`, and `public/` rebuilt. Its message lists each change and its reason. `python site/build.py`: 39 files from 20 pins, 1864 figures; numbers 0 problems, 2941 marks; links 0; local-only 0. The full gate on it is running.
- P1's run notification arrived after the lead had read its design in its file: context at the end 735,090 tokens, 292 tool uses, 3,816,863 ms. Its 15:58:05 entry corrects its own 15:56:27 note on the fourth gap: `docs/COMPLIANCE.md` does say how some clauses are met by a chosen mechanism (lines 92, 110, 111, 158 to 162), so whether to show the gap, quoting 110 and 111, is listed for Logan under decision 36 with the exp2 tie.

Decided:
- verifier-P0 is resumed for its third and last pass under the lead's rule, scoped to `git diff 335bb50 427900e`. Message after this entry:
  > verifier-P0: pass 3, the last under the lead's rule. The seam commit is 427900e on round2 (git merge --ff-only 427900e). Scope: git diff 335bb50 427900e. It adds nine paths to build.SOURCE_PATHS for the four designs' labels (lead.md's entry after 15:58 says which design asked for which), restates the two HonestHarness edges to quote its README's whole first sentence, and makes three restates of the lead's own (threads.py's Preservation line, Map & Ledger's mercs2 count's account, newest_subject's docstring). Check that each path names a file at its pin and that a label naming it is one a parcel's design actually needs; that the edges' words are the README's and the edge kinds still fit them; that each restate is true at the pin. Pick your own faults; report READY or NOT READY, in your ledger file too.
- "go" to P1, P2 and P3 follows its READY, on `427900e`.

For: verifier-P0, P1, P2, P3

## 2026-10-08 16:04:00 -0700 - the full gate passes on the seam commit 427900e

Measured:
- `bash verify/run.sh --require-all` on `427900e` (run 20261008-155946-427900e): "passed 11, failed 0, skipped 0", "VERDICT: PASS, nothing skipped"; controls 386 caught; facts 1810 read again and the same, 54 stated.

For: verifier-P0, the case study

## 2026-10-08 16:13:45 -0700 - verifier-P0: READY on the seam commit 427900e; "go" to P1, P2 and P3 on it

Measured:
- verifier-P0's pass 3 reported at about 16:13: **READY** on `427900e`. The runtime's figures for that run: context at the end 705,030 tokens, 58 tool uses, 816,777 ms. Its own full gate on it (run 20261008-160716-427900e): 11 passed, controls 386 caught. Every one of the nine paths exists at its pin and is needed by a design; both edges' pattern matches once, at README.md line 3; the three restates are true at the pins.
- Its merge-time check for P4: the Preservation page's own description must land with P4's merge, or it and the Threads index's restated line will disagree. P4's `1e6b4ec` changes it (`git diff 335bb50 1e6b4ec`), so the merge carries it; the lead checks it there.

Decided:
- **"go" on `427900e`** to P1, P2 and P3, with the answers recorded above (P3's at 15:44 and 15:46, P1's and P2's at 15:58).

For: P1, P2, P3, the case study

## 2026-10-08 16:24:43 -0700 - verifier-P4: NOT READY on the planted copy, four findings; the lead's answers, and P4's merge

Measured:
- verifier-P4 reported at about 16:24 (its file, three entries). The runtime's figures for its run: context at the end 431,329 tokens, 113 tool uses, 1,544,465 ms. Model: claude-haiku-5-5 (its transcript).
- Its findings on `92a7b59`: D1 (a sentence about the community Modkit, against Mercenaries2 README.md line 6), D2 (a sentence about a person, with a pronoun), D3 (the "one of 22 public mercs2 repositories" sentence doesn't say that the count leaves out Merc2-Mods-Exp, which is public, on Logan's account and matches the pattern), D4 (`org_items()` guards the organisation's repositories, and nothing guards the three other names the scope sentence gives), and three claims of the commit message.
- **Checked by the lead against P4's own commit `1e6b4ec`:**
  - D3: true. `facts.family("(mercs2-|merc2-|wad-simulator)", ["Merc2-Mods-Exp"])` is the sentence's figure (`site/pages/thread_preservation.py` line 194), and the exclusion is in its arguments, not its words. The sentence is round 1's (line 153 at `427900e`), and Map & Ledger's row (the lead's) says the same.
  - D4: true, and no wrong answer today: the three names are typed in the sentence, and `REPOS` holds them.
  - The message: its line 8 says the Modkit is the one "that all further mods are built around"; the README says "will be built around". True, and P4's own. Its "the threads and propose controls that call it" overstates: propose.py's control reads the Determinism door alone (verifier-P4's reading; taken).
  - D1 and D2: answered in the keys' record, after the last planted-copy verifier has reported (README, "Planted faults").

Decided:
- **No send-back.** D3 is a sentence that claims more than is true, and D4 a guard's reach, so both are restated at the merge (the send-back rule): the lead merges P4's own commit, `1e6b4ec`, by its SHA, and then restates, in a commit of its own: the sentence's count with its exclusion, the same on Map & Ledger's row, and the scope sentence's three names read from `REPOS`, so they can't drift from the credits.
- The commit message's two claims are corrected in the restate commit's message.
- The integration verifier checks the merge and the restates.

For: the integration verifier, the case study

## 2026-10-08 16:43:56 -0700 - P1 reports at bef03b0 and P2 at 37d0609; their planted copies, and the keys' SHA-256

Measured:
- **P2** reported phase 2 at about 16:31: commit `37d0609`, parent `427900e`. The runtime's figures for that run: context at the end 770,084 tokens, 55 tool uses, 995,044 ms. Its checks: 39 files, 1907 figures; numbers 0 problems, 3061 marks; links, local-only 0; `--check` exact; verify-facts 1853 the same; `--control` 386 caught. Its four controls each with output lines (P2.md 16:14:58 to 16:30:02).
- **P1** reported phase 2 at about 16:34: commit `bef03b0`, parent `427900e`. The runtime's figures for that run: context at the end 861,184 tokens, 90 tool uses, 1,283,677 ms. Its checks: 39 files, 1891 figures; numbers 0 problems, 3009 marks; links, local-only 0; `--check` exact; verify-facts 1837 the same; docs 0; `--control` 386 caught. Its four controls each with output lines (P1.md, its report at 16:33:08). Its own note: its commit message says the docstring and a comment record the gap quotes' re-reading, where only the comment does.
- **The lead's audit:** `git diff --stat 427900e bef03b0 -- site/ docs/ README.md CLAUDE.md pins.json`: P1's four page modules alone (corrections, thread_determinism, verify, work_cft_fp256), 168 lines added and 36 removed; the rest is `public/`. `git diff --stat 427900e 37d0609` on the same paths: P2's three (method, work_honestframework, work_parcelround), 186 added and 32 removed. Neither touches a file it doesn't own.
- **The planted copies**, made as P4's was: P1's is `9a5449d` on `r2-plant-P1`, P2's is `2093b9d` on `r2-plant-P2`, each with its parcel's parent, message, author and committer, two plants, and `public/` rebuilt.
- **The keys' SHA-256:** P1's `caff96773df43bd65b548be370894d2134c4d1a0dd0883126ea7229ca65f32da`; P2's `7b24bf25e458b3112286be8103b8dbdfd900f29e11d138a8825673cb0160f2d7`.
- The full gate on each planted copy is running; each verifier is dispatched once its copy passes.

For: verifier-P1, verifier-P2, the case study

## 2026-10-08 16:44:52 -0700 - the full gate passes on round2 after P4's merge and the lead's restates (e349b1a)

Measured:
- P4 merged at `4d534df` (parents `427900e` and `1e6b4ec`): no source conflict; `public/` conflicted in eight files and was resolved by building it again, `--check` exact. The lead's restates followed at `e349b1a`.
- `bash verify/run.sh --require-all` on `e349b1a` (run 20261008-162656-e349b1a): "passed 11, failed 0, skipped 0", "VERDICT: PASS, nothing skipped"; controls 387 caught (P4's `credits-scope` added). The controls stage took 877 s, against about 190 s alone: three gates were running at once.

For: the integration verifier, the case study

## 2026-10-08 17:17:12 -0700 - the full gate passes on both planted copies; verifier-P1 and verifier-P2 dispatched on Haiku

Measured:
- `bash verify/run.sh --require-all` on `9a5449d` (run 20261008-164411-9a5449d) and on `2093b9d` (run 20261008-164411-2093b9d): each "passed 11, failed 0, skipped 0", "VERDICT: PASS, nothing skipped", controls 386 caught. So no stage points at a plant in either. Each controls stage took about 1,490 s, run beside the other and beside the gate on `e349b1a`: a lesson for the lead, who runs gates one at a time from here.
- Each verifier's clone, made as verifier-P4's was, holds only its planted branch, with the remote removed; `git cat-file -t` of the parcel's own commit in it: "Not a valid object name".

Decided:
- verifier-P1 (`9a5449d`, clone `<scratch>/r2-verifier-P1/loganw.dev`) and verifier-P2 (`2093b9d`, clone `<scratch>/r2-verifier-P2/loganw.dev`) are dispatched now, model requested: haiku, briefs `_verifier.md` and their own.

For: verifier-P1, verifier-P2, the case study

## 2026-10-08 17:18:35 -0700 - verifier-P2's test escalation arrived as a runtime message

Measured:
- "verifier-P2: test escalation" reached the lead through the runtime's agent messages.

For: the case study

## 2026-10-08 17:18:46 -0700 - verifier-P1's test escalation arrived as a runtime message

Measured:
- "verifier-P1: test escalation" reached the lead through the runtime's agent messages.

For: the case study

## 2026-10-08 17:24:31 -0700 - P3 reports at 583d3eb; its planted copy is 9db24ff on r2-plant-P3; the key's SHA-256

Measured:
- P3 reported phase 2 at about 17:23: commit `583d3eb`, parent `427900e` (amended twice before it was shared). The runtime's figures for that run: context at the end 795,829 tokens, 124 tool uses, 4,144,313 ms. Its checks: 40 files, 1894 figures; numbers 0 problems, 3018 marks; links, local-only 0; `--check` exact; verify-facts 1840 the same; manifest, docs, privacy 0; `--control` 392 caught (386 and its six caption controls). Its controls each with output lines (P3.md, 17:22:25).
- Beyond the accepted design, disclosed: a sixth caption control (the five missed a record whose device and job were changed together, with a matching job line, under the record's own name); two sentences made exact ("last written by" commit `5fd6fff`; "one-paragraph summary"). Its boundary crossings, disclosed and undone: a gitignored `.claude/launch.json` made and removed in its worktree; the project's table command run on a scratch extract of the pin, in phase 1.
- **The lead's audit:** `git diff --stat 427900e 583d3eb` on the source paths: `site/pages/thread_film.py`, `site/pages/work_quantum_film.py` and the new `site/styles/r2-P3.css` alone (253 lines added, 25 removed); the rest is `public/`. The caption's device and job come from the print's own record, held by `check_print`; the device paragraph quotes `docs/PREREGISTRATION.md` for both the order and the predictions' ranking, as the lead asked.
- **The planted copy**, made as the others were, on `r2-plant-P3`: P3's parent, message, author and committer, two plants, `public/` rebuilt.
- **The key's SHA-256:** `f4c139823bfa74320c0caad875f7c8247152f19a4bc657e9fc9d509f86c531e6`.
- **A slip of the lead's, caught before it did harm:** the first attempt to write P3's key went through a Bash heredoc, and its doubled backslashes arrived single (CLAUDE.md trap 8: Python warned of invalid escapes, and the script failed before writing anything). The key was written by a script file instead.
- The full gate on the planted copy is running.

For: verifier-P3, the case study

## 2026-10-08 17:29:03 -0700 - the full gate passes on P3's planted copy 9db24ff; verifier-P3 dispatched on Haiku

Measured:
- `bash verify/run.sh --require-all` on `9db24ff` (run 20261008-172423-9db24ff): "passed 11, failed 0, skipped 0", "VERDICT: PASS, nothing skipped"; controls 392 caught, in 202 s (run alone). So no stage points at a plant.
- verifier-P3's clone, `<scratch>/r2-verifier-P3/loganw.dev`, holds only `r2-plant-P3`, its remote removed; `git cat-file -t 583d3eb` in it: "Not a valid object name".

Decided:
- verifier-P3 is dispatched now, model requested: haiku, briefs `_verifier.md` and `verifier-P3.md`, on `9db24ff`.

For: verifier-P3, the case study

## 2026-10-08 17:30:16 -0700 - a slip in the metrics script, found and fixed: notifications that arrive while the lead works are kept as "attachment" records

Measured:
- The mid-round run of `tools/round_metrics.py` gave P1 no runs and P2 one, where each had reported twice. In the lead's transcript, each missing notification is a record of type "attachment" (`attachment.type` "queued_command", the notification text in `attachment.prompt`, and `attachment.usage` with its totals), written when it arrived while the lead was busy. The script read only "user" records, and only their "message" field.
- Fixed: it reads "user" and "attachment" records, and every string in each; its `seen` key (task, tokens, duration) still counts each notification once. Run again: P1 2 runs, 85 minutes; P2 2 runs, 77 minutes; P3 2 runs, 117; P4 2 runs, 54. Every parcel's figures now agree with the notifications the lead recorded here.

For: the case study (the script is archived with it)

## 2026-10-08 17:30:38 -0700 - verifier-P3's test escalation arrived as a runtime message

Measured:
- "verifier-P3: test escalation" reached the lead through the runtime's agent messages. Every agent of the round has now sent one, and every one arrived.

For: the case study

## 2026-10-08 17:45:48 -0700 - verifier-P1: NOT READY on the planted copy, two findings; the lead's answers, and P1's merge

Measured:
- verifier-P1 reported at about 17:46 (its file, entries of 17:43:05). The runtime's figures for its run: context at the end 464,341 tokens, 140 tool uses, 1,673,945 ms. Model: claude-haiku-5-5 (its transcript).
- Its findings on `9a5449d`: D1 (a sentence on the contract's versions, against CONFORMANCE.md lines 334 to 353) and D2 (a sentence on the language, against docs/LANGUAGE.md, docs/ATLAS.md and the account's own first paragraph). Side notes S1 to S10.
- **Checked by the lead against P1's own commit `bef03b0`:**
  - D1 and D2: answered in the keys' record, after the last planted-copy verifier has reported (README, "Planted faults").
  - S1: the commit message cites CONFORMANCE.md lines 312 and 316 for the digests quote, which sits at 317 to 319: true; corrected in the merge's record.
  - S2: the message says the docstring and a comment record the gap quotes' re-reading, where only the comment does: true, and P1's own correction of 16:34:27; corrected in the merge's record.
  - S6, "the page shows a dangling colon" after the major-step quote: **not true of P1's page.** `git show bef03b0:public/work-cft-fp256.txt`, line 18, reads "A major step is “a change to any recorded bit or flag, or to an accepted image's result, flags, STATUS or acceptance [fact 1484].”" The colon is the source's, outside the quote. The second error the lead has found in a Haiku verifier's report.
  - S3 (the fourth gap and the exp2 tie) is listed for Logan, as P1 asked. S4, S5, S7, S8, S9 and S10 stand as notes: none says a sentence is wrong.

Decided:
- **No send-back.** P1's own commit holds no wrong answer verifier-P1 found; its message's two slips are corrected in the merge's record. The lead merges `bef03b0` by its SHA.

For: the integration verifier, the case study

## 2026-10-08 17:51:13 -0700 - the full gate passes on P1's merge; verifier-P2: NOT READY on the planted copy; the lead's answers, and P2's merge

Measured:
- P1 merged at `e4c4a67` (parents `e349b1a` and `bef03b0`): no source conflict; `public/` conflicted in sixteen files and was built again, 1898 figures, `--check` exact. `bash verify/run.sh --require-all` on it (run 20261008-174621-e4c4a67): "passed 11, failed 0, skipped 0", "VERDICT: PASS, nothing skipped"; controls 387 caught, in 195 s.
- verifier-P2 reported at about 17:48 (its file, 17:45:45). The runtime's figures for its run: context at the end 497,654 tokens, 121 tool uses, 1,768,640 ms. Model: claude-haiku-5-5. Its findings on `2093b9d`: D1 and D2 (sent back, it says), D3 and D4 (wrong labels, older than P2), S1 to S4. It ran ParcelRound's gate at `f42242e` itself: "PASS: 10 of 10 checks hold", `--control` "50 of 50 caught"; and recounted ADOPTION.md by a method of its own: 121 rows, 87, 8, 23 and 3, as the page says.
- **Checked by the lead against P2's own commit `37d0609` and the sources:**
  - D1 and D2: answered in the keys' record, after the last planted-copy verifier has reported (README, "Planted faults").
  - D3, true: `git show f42242e:CASE-STUDY-2.md`, lines 34 to 36: "the desktop app's own accounting puts the human-active time at 1 h 38 min". The Method page says "its own accounting", which names no accountant, or the round. Round 1's wording, kept by P2.
  - D4, true: METHOD.md at `f42242e`, lines 118 to 120, makes listing every file each parcel would touch P0's step; its "seam tests" (lines 1200 to 1203) are tests of two parcels together at a merge. The ParcelRound dossier's "Test it" called the first "the method's own seam test". Round 1's wording.
  - S1, true and a sentence that claims more than its source: `tools/check_method.py` lines 10 to 12 say "It reads structure and citations, never what a rule says", and two sentences on, "Checks 7 and 9 read text, and are such limits". The page quotes the first sentence alone.
  - S2, true as a limit: `adoption_state` counts a status that begins with a known word as that word, and skips a row whose id is not CS, B, R or S; neither occurs at the pin. Stated in its docstring at the restates.
  - S3: the message's "differs in fact ids only" holds for the pages and texts, not MANIFEST and facts.json: corrected in the merge's record. S4 stands as a note (round 1's wording, not wrong).

Decided:
- **No send-back.** D3, D4 and S1 are sentences that claim more than is true, restated at the merge; S2 a stated limit. The lead merges `37d0609` by its SHA, and restates in a commit of its own.

For: the integration verifier, the case study

## 2026-10-08 17:54:05 -0700 - verifier-P3: NOT READY on the planted copy; its report, which its runtime kept out of its own file; the lead's answers, and P3's merge

Measured:
- verifier-P3 reported at about 17:55. The runtime's figures for its run: context at the end 474,208 tokens, 123 tool uses, 1,402,806 ms. Model: claude-haiku-5-5. It writes: "The runtime refused my ledger copy of this report, because a subagent should return findings as text. So this message is the report. `verifier-P3.md` in the ledger holds only my start entry." So its findings are recorded here, as it returned them, in short:
  - Setup on `9db24ff`: `--check` exact (40 files); numbers 0 problems, 3018 marks; links, local-only 0; verify-facts 1840 the same.
  - Item 1, the print: byte-identical to the pin's (9,579 bytes); commit `5fd6fff` the only one to touch it; the record, the job line and HARDWARE-RESULTS.md line 14 agree on ibm_kingston and job `db1nn11b694s73dsidjg`; the rule quote is VALIDATION.md 1646 to 1647, verbatim. Confirmed.
  - Item 2: **D1**, a sentence on which device's print is shown, against HARDWARE-RESULTS.md (its XEB and Y0Y1 rows, lines 71 to 92: on those, marrakesh is nearer its prediction than kingston). The "why" paragraph itself: confirmed.
  - Item 3: **D2**, the thread page's summary quote, against HARDWARE-RESULTS.md line 5. The dossier's quote: confirmed.
  - Items 4 to 8: confirmed; P3's four controls re-run from copies, each refused for its own reason; the six caption controls each refused for its own reason.
  - Item 9: scope confirmed (`thread_film.py`, `work_quantum_film.py`, `r2-P3.css` and `public/`).
  - Side notes: S1 (a check that refused quotations not closed at a sentence's end would catch D2); S2 ("ESP" undefined on the page; PREREGISTRATION.md lines 36 to 42 give its basis); S3 ("half of the map's other projects": 8 of 17 by the arrows out of StoryDocs); S4 (kept failure 3's "the template", where `66d17c0` changes code and the README's advice: loose, not false); S5 (check_print's law-kind branch has no control); S6 (`--numbers` reads `public/`, so a copy's source edit needs a build first; `prose()` returns only the first capture group); S7 (the runtime's refusals); S8 (the dossier prints a README heading mid-sentence, capitalised, without quotation marks); S9 (thread_film.py's docstring says `first_prints.py --check` holds each print to its record's digests, where it compares arrays, not the PNG).
  - Its verdict: NOT READY, for D1 and D2.
- **Checked by the lead against P3's own commit `583d3eb`:**
  - D1 and D2: answered in the keys' record, below.
  - S3, true and a sentence that claims more than is true: the StoryDocs paragraph says it "touched half of the map's other projects, which the arrows out of it show", and the arrows out of it reach 8 of the 17 other nodes now that HonestHarness is one. Round 1's sentence. Restated.
  - S8, true: `site/pages/work_quantum_film.py` line 121 prints the README's heading "The negative control, and its twin" as words of the sentence. Restated with quotation marks and agreement.
  - S9, true: P3's own report says `tools/first_prints.py --check` compares array digests (its line 395), not the PNG. The docstring is restated.
  - S2, S4 and S5 stand as notes: none is a wrong answer.

Decided:
- **No send-back.** The lead merges `583d3eb` by its SHA, and restates S3, S8 and S9 in a commit of its own.

For: the integration verifier, the case study

## 2026-10-08 18:00:18 -0700 - the full gate passes on round2 with every parcel merged (a4a438c); the keys, and the planted-fault yield: 8 of 8 on Haiku

Measured:
- `round2` is at `a4a438c`: P4 merged at `4d534df`, P1 at `e4c4a67`, P2 at `0052634` and P3 at `8b4973a`, each by its parcel's own commit's SHA, each followed by the lead's restates (`e349b1a`, `7850d3a`, `a4a438c`; P1 had none). `bash verify/run.sh --require-all` on `a4a438c` (run 20261008-175524-a4a438c): "passed 11, failed 0, skipped 0", "VERDICT: PASS, nothing skipped"; controls 393 caught (386, P4's one and P3's six).
- **The keys**, now that the last planted-copy verifier has reported, are in `keys/` beside this file: `key-P1.json` to `key-P4.json`, each holding its plants' old and new text, their kind and why each is wrong. Each file's SHA-256 matches the hash this file recorded before its verifier was dispatched (P4 `11bc552a...`, P1 `caff9677...`, P2 `7b24bf25...`, P3 `f4c13982...`; `sha256sum`, each found once above).
- **The yield, plant by plant:**

| parcel | the plant | its kind | the verifier's finding |
|---|---|---|---|
| P4 | "says all further mods are now built around" | a tense its source doesn't have | verifier-P4's D1 |
| P4 | "which austinkregel founded and leads with his collaborators" | a claim about a person, with a pronoun no one stated | verifier-P4's D2 |
| P1 | "a language, the one atlas-engine's plates are now written in" | a relation no source states | verifier-P1's D2 |
| P1 | "and no step so far has moved a recorded bit" | a sentence the source contradicts | verifier-P1's D1 |
| P2 | "Across its rounds, its planted faults" | a round's figure as every round's | verifier-P2's D2 |
| P2 | "The fifth round's case study records" | a lead-in naming the wrong source | verifier-P2's D1 |
| P3 | the summary quote ending before its shortfall sentence | a quote cut short | verifier-P3's D2 |
| P3 | "the device whose run came closest to its noise model's prediction" | a selection reason no source gives | verifier-P3's D1 |

  **8 of 8 caught**, by four verifiers on claude-haiku-5-5, each on its first pass. Round 6's five Opus verifiers caught ten of ten (CASE-STUDY-6.md).
- **How they found them**, by their own reports: each finding cites the source line that contradicts it. verifier-P2 writes "I did not use the design to find them". verifier-P4, verifier-P1 and verifier-P3 each also noted, after forming their view, that the parcel's design in its ledger file reads otherwise at the planted sentences: so the parcels' designs in the ledger are a second route to a plant, by comparison, which the protocol's clone did not close (round 6's case study records the same shape: "A verifier that read the design first could have found every plant by comparison alone"). The yield is read with that limit.
- **Real findings the four verifiers made beside the plants:** in P4's work, the mercs2 count's unstated exclusion and the scope sentence's unguarded names; in P1's, two citations of its own message; in P2's, two wrong labels and a quote cut short, all round 1's but one; in P3's, a "half" that is 8 of 17, a heading printed as prose, and a docstring. Each was restated at its merge. And two claims of the verifiers' own were wrong (verifier-plan's GPU photograph, withdrawn; verifier-P1's dangling colon).

For: the integration verifier, the case study, Logan

## 2026-10-08 18:02:01 -0700 - a correction to the yield entry of 17:5x: all four verifiers noted the design's difference, not three

Measured:
- The yield entry says verifier-P4, verifier-P1 and verifier-P3 each noted that the parcel's design reads otherwise at the planted sentences. verifier-P2's report says so too: "The commit matches the design sentence for sentence except D1 and D2. I did not use the design to find them." So all four noted it. Which of the other three found its plants before reading the design, their reports don't say.

For: the case study

## 2026-10-08 18:07:47 -0700 - the full gate passes on the round's entry (9b35773); the side notes' step; verifier-I dispatched on Haiku

Measured:
- `9b35773` adds the round's entry to `docs/VALIDATION.md` and restates Corrections' description. `bash verify/run.sh --require-all` on it (run 20261008-180254-9b35773): "passed 11, failed 0, skipped 0", "VERDICT: PASS, nothing skipped"; controls 393 caught.
- **The verifiers' side notes, as a step of their own.** Every side note is answered in the entry that records its verifier's report: restated at a merge, stated as a limit, or left as a note with its reason. What is left is for Logan, and goes to him with the round's report:
  1. Corrections' fourth gap, "clause readings in COMPLIANCE", stays out; P1 and verifier-P1 put its basis and the exp2 tie (`docs/COMPLIANCE.md` line 109 against `CONFORMANCE.md` lines 336 to 338) to him under decision 36.
  2. Quantum-Film's own README, at `3a73823`, still says "Not on hardware yet" beside its line 176 that the law ran on IBM hardware, and gives `make verify-quick` as "~65 s" where its CLAUDE.md gives "~2 min" (P3). Quantum-Film's to fix.
  3. Quantum-Film's "Last verified" stays at 2026-09-26 by pins.json's declared pass form; a second form would change how results are counted, which is his.
  4. ParcelRound's own gate, check 9, holds loganw.dev patterns pinned at `43c36a2` (verifier-P0, P2). ParcelRound's to update.
  5. The organisation's repositories are on neither the map nor Map & Ledger, and the organisation now has a fork named Merc2-Mods-Exp (P4).

Decided:
- **verifier-I** is dispatched now, model requested: haiku, briefs `_verifier.md` and `verifier-I.md`, in a worktree of loganw.dev at `9b35773`, on the lead's merges, restates and records from `427900e`.

For: verifier-I, Logan, the case study

## 2026-10-08 18:08:51 -0700 - verifier-I's test escalation arrived as a runtime message

Measured:
- "verifier-I: test escalation" reached the lead through the runtime's agent messages.

For: the case study

## 2026-10-08 18:10:46 -0700 - a second trap-8 slip of the lead's, caught the same way; the planting scripts copied into tools/ for the archive

Measured:
- A Python heredoc meant to copy the planting scripts into `tools/` lost its doubled backslashes again (CLAUDE.md trap 8: "unicodeescape codec can't decode"), and failed before writing anything. Done instead by a script file that builds each backslash with `chr(92)`.
- `tools/` now holds `round_metrics.py`, `make_plant.py` and `write_key_P3.py`. The last two read the paths they were run with from the environment (`LOGANW_DEV`, `LOGANW_REPOS`); each of the three parses, and holds no absolute path.

For: the case study

## 2026-10-08 18:32:03 -0700 - verifier-I: NOT READY on the lead's integration, four findings; its report, kept out of its own file by its runtime; the lead's checks

Measured:
- verifier-I reported at about 18:33. The runtime's figures for its run: context at the end 470,281 tokens, 152 tool uses, 1,380,095 ms. Model: claude-haiku-5-5. Its runtime refused its report file ("Subagents should return findings as text"), so `verifier-I.md` holds its start entry, and its report is here, in short:
  - Item 1, each merge made again with `git merge-tree --write-tree`: every source path auto-merges, conflicts only in `public/` (8, 16, 18 and 17 files), and `--check` passes at all nine commits. Confirmed.
  - Item 2: the second parents are `1e6b4ec`, `bef03b0`, `37d0609` and `583d3eb`; no planted commit is an ancestor of the tip; none of the plants' texts is in the tree. Confirmed.
  - Item 3: each restate is true at its pin, and none changes a stated line, About, the front page or a spec choice. Confirmed, with D-I1 and D-I2 left.
  - Item 4: the round's ledger entry, SPEC.md's decisions 31 to 36 and ROUND2.md against this file and the commits: confirmed, but for D-I4.
  - Item 7: its own full gate on `9b35773` (run 20261008-181016-9b35773): "passed 11, failed 0, skipped 0", "VERDICT: PASS, nothing skipped"; controls 393 caught.
  - **D-I1:** the map's family label, "22 mercs2 repositories created 06-29 to 07-25", on Map & Ledger and each thread's map, leaves out Merc2-Mods-Exp, drawn beside it, without saying so: the same scope as verifier-P4's D3, restated in two sentences and not here.
  - **D-I2:** About says the Preservation thread credits "everyone who has worked on it directly"; the page now says no repository but those listed is covered. About is Logan's approved text, so this is his.
  - **D-I3:** the spec names four "where I'd attack first" gaps and Corrections shows three; under decision 36 a dropped spec choice is Logan's to settle.
  - **D-I4:** the merge `e4c4a67`'s message "corrects" P1's citation of CONFORMANCE.md lines 312 and 316 to 317 to 319; at `ab51655` the known-limit quote starts at line 312 and "A change that moves ..." at the end of line 316. So P1 was right, and this file's 17:45:48 entry accepted verifier-P1's S1 as true without reading the lines.
  - Side notes: the planted branches are still in the lead's repository (only main is pushed; they are deleted at the round's end); "ESP" is undefined on the Film thread (verifier-P3's S2 too); `7850d3a`'s "round 2" names ParcelRound's round 2, which a reader could take for this one; the cft-fp256 edge's "was distilled into" against the README's "derived from", which it calls acceptable.
- **The lead's checks:**
  - D-I4: true. `git show ab51655:CONFORMANCE.md`, lines 312 and 316 to 319, as verifier-I says. **The lead's slip:** this file's 17:45:48 entry called verifier-P1's S1 "true" without reading the source lines, and the merge message `e4c4a67` then put the wrong lines in the record. **Correction to the 17:45:48 entry:** S1 was not true; P1's message cited the right lines. The merge message stands as written, corrected here and in the case study. The third error the lead has found in a Haiku verifier's report, and the first the lead carried into the record.
  - D-I1: true. `site/data/relations.json`'s family has `"exclude": ["Merc2-Mods-Exp"]`, and its label is "mercs2 repositories". Restated by the lead.
  - D-I2 and D-I3: both Logan's, under decision 36 and the plan's rule that About is his approved text. Asked of him now, with the evidence.

For: Logan, the case study

## 2026-10-08 18:36:57 -0700 - Logan settles D-I2 and D-I3; the lead's restates for verifier-I's four findings

Measured:
- Logan, through the question tool, at 18:33:47 -0700 (the transcript's timestamp), verbatim, question then answer:
  1. "About says the game-community project "has its own thread, crediting everyone who has worked on it directly". The Preservation page now says its credits cover the seven repositories it reads, and no others: the organisation has more repositories, and their contributors aren't counted. About is your approved text. How should it read?" - "Narrow it to match (Recommended)": ""...has its own thread, crediting every contributor to the repositories it reads directly:" (only that clause changes)."
  2. "Your spec names four "where I'd attack first" gaps on Corrections; since round 1 the page shows three, leaving out "clause readings in COMPLIANCE" because COMPLIANCE.md calls none of its readings open to dispute. This round found that COMPLIANCE.md does state how some clauses are met by its own choices (9.3, 9.4), and that its claim of correct rounding for exp2 was false at four arguments until 2026-10-05. What should the page do?" - "Show it, with its evidence": "Add the fourth gap, quoting COMPLIANCE.md's clause readings (9.3, 9.4) at cft-fp256's pin; a lead's restate, checked like the others."
- The restates, in the working tree, built: `python site/build.py`: 40 files, 1976 figures; numbers 0 problems, 3231 marks; links, local-only 0; `--check` exact.
  - D-I2: `site/pages/about.py`, the one clause, as his answer gives it.
  - D-I3: `site/pages/corrections.py`, the fourth gap first, as the spec lists it: "Clause readings in COMPLIANCE: clause 9.3, ... ; and clause 9.4, ...", each clause number and each reading quoted from `docs/COMPLIANCE.md` at `ab51655`, lines 110 and 111; that path added to `build.SOURCE_PATHS`; the comment above `attack_first()` says why it is shown.
  - D-I1: the family's label in `site/data/relations.json` reads "other mercs2 repos". "other mercs2 repositories" was tried first and, on a 375 px screen, ran 16 px past the map's right edge (measured in the browser: the label's right at 375 against the map's at 359); "22 other mercs2 repos" ends at 354.
  - SPEC.md decisions 37 and 38; ROUND2.md notes them.
- D-I4 is corrected in this file's entry after 18:33, and in the round's ledger entry's follow-up and the case study.

For: verifier-I, the case study

## 2026-10-08 18:47:15 -0700 - the integration findings committed at 7f2d51b; the full gate passes on it; verifier-I resumed for pass 2

Measured:
- `7f2d51b` on `round2`, parent `9b35773`: About's clause (decision 37), Corrections' fourth gap (decision 38), the map's label, `build.SOURCE_PATHS` (`docs/COMPLIANCE.md`), SPEC.md decisions 37 and 38, ROUND2.md's note of them, and a follow-up entry in `docs/VALIDATION.md` that corrects the citation `e4c4a67`'s message got wrong.
- `bash verify/run.sh --require-all` on `7f2d51b` (run 20261008-184228-7f2d51b): "passed 11, failed 0, skipped 0", "VERDICT: PASS, nothing skipped"; controls 393 caught. The entry's "11 passed, nothing skipped" and "393 of 393" are this run's.
- Before the commit, the gate on the working tree (run 20261008-183730-9b35773-dirty) failed only its docs stage, on the case study's draft, untracked in `docs/` with links into an archive not yet made. The draft was set aside in the lead's scratch.

Decided:
- verifier-I is resumed for its second pass, scoped to `git diff 9b35773 7f2d51b`. Message after this entry:
  > verifier-I: pass 2 of up to 3. The lead's fixes are 7f2d51b on round2 (git merge --ff-only 7f2d51b). Scope: git diff 9b35773 7f2d51b. It answers your D-I1 (the map's label), and D-I2 and D-I3 at Logan's word of 18:33 (SPEC decisions 37 and 38), and corrects D-I4 in a new entry of docs/VALIDATION.md. lead.md's entries after 18:33 record the lead's checks and Logan's words verbatim. Check each against its source and pick your own faults in the diff; report READY or NOT READY. If the runtime refuses your ledger file again, make the report your final message.

For: verifier-I

## 2026-10-08 18:56:35 -0700 - verifier-I: READY on 7f2d51b; main moves to it and is pushed

Measured:
- verifier-I's pass 2 reported at about 18:52: **READY** on `7f2d51b`, all four findings answered at their sources, no regression. The runtime's figures for that run: context at the end 582,995 tokens, 47 tool uses, 537,363 ms. Its own full gate on `7f2d51b` (run 20261008-185013-7f2d51b): "passed 11, failed 0, skipped 0", "VERDICT: PASS, nothing skipped", controls 393 caught. It measured the map's label at 375 px itself: right edge 354.0 px, the map's 359.2 px.
- Its notes, none a defect: the new ledger entry quotes About's new clause without its last word, "directly" (exact to that point); `site/mapgen.py` line 390's comment still gives the old label as its example; one line of SPEC.md's round-2 paragraph is long; the commit subject's "says what it leaves out" says a little more than "other" does. All stand as notes.

Decided:
- **Logan's decision 33, "Push when verified":** the full gate has passed on `7f2d51b` (the lead's run 20261008-184228 and verifier-I's 20261008-185013), and the integration verifier's verdict is READY. `main` moves to `7f2d51b` by a fast-forward, and only `main` is pushed (trap 17). The planted branches stay local, and are deleted at the round's end.

For: Logan, the case study

## 2026-10-08 19:04:33 -0700 - pushed at 18:56:43; the deploy passes; the live site is byte for byte the build

Measured:
- `git push origin main`: "43c36a2..7f2d51b main -> main"; `git ls-remote origin refs/heads/main`: `7f2d51b68f0c43233a1025586d6e2ae42af00820`. The push's time, from the remote-tracking reflog: 2026-10-08 18:56:43 -0700.
- The workflow run for it, 37872192090 ("site", event push, `7f2d51b`): completed, success; its gate job and its deploy job, each success (`gh run view`).
- **The live site:** every published file but BUILD fetched from https://loganw.dev/ and compared with `public/` by `cmp`: 39 identical, 0 different. BUILD reads "Deployed from 7f2d51b68f0c43233a1025586d6e2ae42af00820". The author's email domain appears 0 times in the live `facts.json`.
- **The build phase's cost**, by `tools/round_metrics.py` from the request (13:16:10) to the push (18:56:43): 341 minutes of wall clock; 12 agents (4 parcels on claude-sonnet-5-5, 7 verifiers on claude-haiku-5-5, the lead on claude-opus-5-5) in 20 runs and 583 agent-minutes; 2,796 tool uses; 4.1 M output tokens, 16.7 M fresh, 978.3 M cache reads; the verifiers' share of output 57.9%, the parcels' 32.7%, the lead's 9.4%. The table is the case study's.

Decided:
- The round's last part: the case study and this ledger's archive, in loganw.dev's `docs/`, past a verifier on Haiku, then pushed (decisions 32 and 33).

For: the case study, Logan

## 2026-10-08 19:12:36 -0700 - the case study and the archive at 35e0dd1 on round2-close; two more slips of the lead's, both caught before anything was pushed; verifier-CS dispatched on Haiku

Measured:
- `35e0dd1` on `round2-close`, from `7f2d51b` (main): `docs/ROUND2-CASE-STUDY.md`; `docs/round2-ledger/`, 33 files, each staged blob compared with its ledger file, 33 of 33 the same; `.gitattributes` keeps that directory's bytes; CLAUDE.md trap 19; README's layout rows. `bash verify/run.sh --require-all` on it (run 20261008-190706-35e0dd1): "passed 11, failed 0, skipped 0", "VERDICT: PASS, nothing skipped"; controls 393 caught.
- **Two slips of the lead's, both on the local branch, fixed by amending its unpushed commit:**
  - the first commit, `2d4ae4a`, went in although `--docs` had just refused CLAUDE.md's new trap ("stages took 15" reads as a stage count): the command chain committed after a failing check. The trap is reworded, and `--docs` reads 0 problems.
  - `P4.md` holds one carriage return, and the repository's `* text=auto eol=lf` would have stored it without, so the archive was not byte for byte as the commit said. `.gitattributes` now stores `docs/round2-ledger/**` as `-text`.

Decided:
- **verifier-CS** is dispatched now, model requested: haiku, briefs `_verifier.md` and `verifier-CS.md`, in a worktree of loganw.dev at `35e0dd1`. The lead runs no gate while it works (trap 19).

For: verifier-CS, the case study

## 2026-10-08 19:13:14 -0700 - verifier-CS's test escalation arrived as a runtime message

Measured:
- "verifier-CS: test escalation" reached the lead through the runtime's agent messages: twelve agents, twelve test messages, each arrived.

For: the case study

## 2026-10-08 19:38:26 -0700 - verifier-CS: NOT READY on 35e0dd1; the lead's checks; three corrections to this file; two decisions on the archive

Measured:
- verifier-CS reported at about 19:37 (its file, with an addendum at 19:36:30). The runtime's figures for its run: context at the end 455,778 tokens, 102 tool uses, 1,452,553 ms. Model: claude-haiku-5-5. Its own full gate on `35e0dd1`, run alone (run 20261008-191852-35e0dd1): "passed 11", controls 393 caught. It re-ran `tools/round_metrics.py` over the window 13:16:10 to 18:56:43 and reproduced both tables cell by cell; 27, 5 and 77 from `facts.json` at `43c36a2` and `05413b2`; each key's hash; and the archive, 32 of 33 files byte-identical and `lead.md` the archive plus appended bytes.
- Its six wrong answers in the case study, each checked by the lead, each true: W1 (the opening says this file went past a verifier before it was committed, and the last section is a placeholder); W2 ("eight verifiers": seven before the push); W3 ("Haiku writes more than it reads", which the table contradicts: it reads far more than it writes); W4 (case study 6's 45 k to 68 k is its five parcel verifiers' range; its other Opus verifiers wrote 114 k to 129 k); W5 ("two citations in [P1's] own commit message": verifier-P1's S1 was wrong, so one, which P1 had corrected itself); W6 (the claim that all four verifiers noted the design's difference rests, for verifier-P3, on its report, which this file summarised without that note).
- Its restates R1 to R11 and its notes, each checked; all taken, R7 with N1's correction below.
- **N1, settled by the lead:** the gate on `e349b1a` started at 16:26:56; its stages before controls took 164 s and its controls stage 877 s, so that stage ran from about 16:29:40 to 16:44:17. The planted copies' gates started at 16:44:11. So three gates did not run at once: the gate on `e349b1a` ran its controls while P1, P2 and P3 ran the site's `--control` in their own copies (P2 recorded three such runs, of 3 min 22 s to 4 min 0 s), and the two planted copies' gates ran beside each other.

**Corrections to this file:**
- To the entry of 16:44:52: its "three gates were running at once" is wrong, as above.
- To the entry of 17:54:05 (verifier-P3's report, which its runtime kept out of its own file): the summary left out two of its notes, which verifier-P3's report gave, verbatim: under D1, "P3's design wrote "Below, one of the devices' prints" (`P3.md`, 15:43:04, section 4)"; under D2, "The design said "quoted whole" (`P3.md` 68), ROUND2's P3 section names this regression (lines 325-327), and the lead's 15:44:41 answer says the shortfall stays beside the print."
- To the entry of 15:33:01, its side note 9's last line: the path fragment in verifier-P0's entry of 15:20:27 is not struck in the archive. It is "/c/Users/...", elided, naming no user and no machine, and striking it would break the archive's byte for byte.

Decided:
- **D1, the co-author trailer's address in the archive** (P4.md, and the lead's own `briefs/_common.md`): kept. It is in every commit's trailer, the privacy stage allows it, and the case study lists the README's rule against it as broken by the lead's own brief.
- **D2:** the elided fragment is kept, as the correction above says.
- **D3:** the case study is revised for W1 to W6 and R1 to R11, its opening and its last section written; CLAUDE.md's trap 19 and README's row restated; the site's own ledger gets an entry correcting its "three full gates run at once"; the archive is taken again; verifier-CS is resumed for its second pass.

For: verifier-CS, the case study

## 2026-10-08 19:41:33 -0700 - a correction to the entry of 19:4x on N1: the parcels' control runs are not shown to overlap the gate's controls stage

Measured:
- The entry says the gate on `e349b1a` ran its controls "while P1, P2 and P3 ran the site's `--control` in their own copies". Their stamps don't show that. What is measured: that controls stage ran from about 16:29:40 to 16:44:17; P2 reported at 16:30 and P1 at 16:33, and P3 was in its phase 2 throughout; P2's three `--control` runs are recorded without their times. So the stage ran while parcels were building and checking in their own copies, and which of their runs overlapped it is not determined.

For: the case study

## 2026-10-08 19:41:52 -0700 - the case study's second version, and the archive taken again, for verifier-CS's second pass

Measured:
- The case study revised for W1 to W6 and R1 to R11; CLAUDE.md's trap 19 and README's archive row restated; a new entry in `docs/VALIDATION.md` adds the case study and the archive and corrects round 2's entry's "three full gates run at once". The archive is taken again from this directory as it stands at this entry, byte for byte.

For: verifier-CS

## 2026-10-08 19:47:24 -0700 - eb90939; the full gate passes on it, run alone; verifier-CS resumed for its second pass

Measured:
- `eb90939` on `round2-close`, parent `35e0dd1`. `bash verify/run.sh --require-all` on it (run 20261008-194233-eb90939), with no other gate or agent running: "passed 11, failed 0, skipped 0", "VERDICT: PASS, nothing skipped"; controls 393 caught, in 212 s.

Decided:
- verifier-CS is resumed for its second pass, scoped to `git diff 35e0dd1 eb90939`. Message after this entry:
  > verifier-CS: pass 2 of up to 3. The revision is eb90939 on round2-close (git merge --ff-only eb90939). Scope: git diff 35e0dd1 eb90939. It answers W1 to W6 and R1 to R11, settles N1 from the gate's stage times (lead.md, the entries after 19:37), corrects round 2's ledger entry in a new one, restates trap 19 and README's row, and retakes the archive (35 files). Check each against its source, pick your own faults in the diff, and report READY or NOT READY. The ledger has grown since eb90939 only by the lead's entries after it.

For: verifier-CS

## 2026-10-08 20:01:11 -0700 - verifier-CS's second pass: NOT READY on three one-line wrong answers; each checked, all taken; a correction to the entry of 19:38

Measured:
- verifier-CS's second pass reported at about 19:59 (its entry 19:58:44). The runtime's figures for that run: context at the end 627,968 tokens, 54 tool uses, 743,586 ms. Its own full gate on `eb90939`, run alone (run 20261008-195154-eb90939): 11 passed, controls 393 caught.
- **S1, true:** the case study's 19:37 row put its first findings "(the last section)", where they were in the opening, the setting, the cost section and "What happened"; the last section lists them.
- **S2, true in its conclusion:** the archive's shared briefs are their last versions; the plan's verifier read earlier drafts of them in its second and third passes (at 14:22 and 14:43), which are not kept. Its first pass, at 13:40, read only `briefs/verifier-plan.md`, unchanged since: the shared briefs did not exist then. README's row is restated to say so.
- **S3, true:** the gate on `e349b1a`'s stage record, rebuilt from its start, 16:26:56, and each stage's seconds: controls 16:29:40 to 16:44:17, runner-control 16:44:17 to 16:44:24. The planted copies' gates began at 16:44:11. So for 13 seconds three gate runs were in progress, and their controls stages never overlapped.
- R-a to R-e, each checked and taken: the slip of the `render.render()` claim added (the case study's list, and a site-ledger entry saying round 2's list there is partial); "twelve agents" said to be the lead aside; the 14:17 row restated to verifier-plan's own 14:15 stamp; "39 of 39" named as the `7f2d51b` build; "no finished agent left a process running" restated as what the lead checked (the machine's Python and Node processes, before the worktrees were removed).

**Correction to the entry of 19:38:** its "So three gates did not run at once" is too strong, as S3 shows. The controls stages never overlapped; three gate runs were in progress for 13 seconds.

Decided:
- The case study, README's row, and a new `docs/VALIDATION.md` entry (append-only: it corrects the previous entry's heading) are committed with the archive taken again; verifier-CS is resumed for its third pass, the last under the lead's rule.

For: verifier-CS

## 2026-10-08 20:07:31 -0700 - Logan's word on the ten items left open, in chat at 20:06:12

Measured:
- Logan, in chat at 20:06:12 -0700 (the transcript's timestamp), answering the lead's numbered list of what was open for him, verbatim, each beside the item it answers:
  1. The five proposals for ParcelRound's METHOD.md in the case study: "Include them in the case study doc and Ill bring them over"
  2. Quantum-Film's "Last verified", held at 2026-09-26 by pins.json's declared pass form: "Leave for now with the old proper verified run"
  3. The Mercenaries-Fan-Build organisation's repositories, on neither the map nor Map & Ledger: "Leave them off, older community work not what Im focusing on now"
  4. Method's sentence "This is the one place the site states it": "Keep it"
  5. Quantum-Film's own README, stale in three places: "Leave it"
  6. ParcelRound's check 9, holding loganw.dev patterns at `43c36a2`: "Leave for now"
  7. ParcelRound's case study 7, on a branch, not main: "Leave for now"
  8. HonestHarness's dossier, waiting until its round 1 lands on main: "Agreed"
  9. Round 1's ledger working copy (`<repos>/loganw-dev-ledger`), archived in ParcelRound: "Ok to delete"
  10. `git gc --prune=now` in loganw.dev, for round 1's P2 commits that hold the author address and this round's planted copies: "Clear to delete"

Decided:
- 2, 3 and 4 are decisions about the site: SPEC.md decisions 39, 40 and 41. 1 is recorded under the case study's proposals; 5 to 8 need no change; the case study's last section gives all ten.
- **9 and 10 are permanent deletions of data, which the lead does not perform itself, even when cleared.** The lead gives Logan the exact commands, after checking each target: round 1's ledger is in ParcelRound's `archive/round5-ledger.zip` on its main.

For: the case study, Logan

## 2026-10-08 20:13:15 -0700 - bfdda6c, with Logan's ten answers; the full gate passes on it, run alone; verifier-CS resumed for its third pass

Measured:
- `bfdda6c` on `round2-close`, parent `eb90939` (the commit `be62744`, never dispatched, amended to add Logan's answers of 20:06): the case study answering verifier-CS's second pass and recording all ten answers; SPEC.md decisions 39 to 41; README's archive row; a `docs/VALIDATION.md` entry correcting the previous entry's heading; the archive taken again, 35 of 35 byte for byte. `bash verify/run.sh --require-all` on it (run 20261008-200826-bfdda6c), alone: "passed 11, failed 0, skipped 0", controls 393 caught.

Decided:
- verifier-CS is resumed for its third pass, the last under the lead's rule, scoped to `git diff eb90939 bfdda6c`. Message after this entry:
  > verifier-CS: pass 3, the last under the lead's rule. The revision is bfdda6c on round2-close (git merge --ff-only bfdda6c). Scope: git diff eb90939 bfdda6c. It answers S1 to S3 and R-a to R-e, and adds Logan's answers of 20:06 on the ten items left open (lead.md's entries after 19:59, verbatim; SPEC decisions 39 to 41; the case study's last section). Check each against its source, pick your own faults in the diff, and report READY or NOT READY.

For: verifier-CS

## 2026-10-08 20:22:13 -0700 - verifier-CS's third pass: NOT READY on two one-line wrong answers; to Logan under the three-pass rule; the process listing and the commands for items 9 and 10, recorded

Measured:
- verifier-CS's third pass reported at about 20:24 (its entries 20:20:28 and 20:23:10). The runtime's figures for that run: context at the end 739,770 tokens, 48 tool uses, 493,258 ms. Its own full gate on `bfdda6c`, alone (run 20261008-201405-bfdda6c): 11 passed, controls 393 caught. It found Logan's ten answers verbatim in his message of 20:06:12, and withdrew its own pass-2 claim about what the plan's verifier read at 13:40.
- **SB-1, true:** the new `docs/VALIDATION.md` entry says the case study "lists every slip the round's ledger records", and two are not in its list: this file's entry of 19:38 claimed, and the lead corrected at 19:41:33 and 20:01:11, that the parcels' control runs overlapped the gate's controls stage and that three gates did not run at once.
- **SB-2, true:** the case study's item 10 says "round 1's unpushed commits that hold the author address", where the list Logan answered said P2's.
- R-1 to R-4, each checked and taken; R-1's records are this entry.
- **The process listing** before the worktrees were removed (19:39, the transcript's own record of the lead's command): Python and Node processes were the owner's UI server (`ui.py --port 8330`), the RunPod connector's servers, the lead's preview server (`http.server 8432`), and another session's HonestHarness gate (`tools/check.py --control`, and a `pytest` beside it). None was a round-2 agent's.
- **The commands for items 9 and 10**, for Logan to run once the case study is pushed. The lead runs neither: they delete data for good.
  - 9, round 1's ledger working copy (476 K; in ParcelRound's `archive/round5-ledger.zip` on its main, since `49a9266`): `rm -rf <repos>/loganw-dev-ledger`.
  - 10, in loganw.dev: `git reflog expire --expire-unreachable=now --all`, then `git gc --prune=now`. Its reach, measured by `git fsck --unreachable`: 25 unreachable commits with the reflogs set aside, 13 counting them. So it drops more than the list named: round 1's P2 commits and this round's planted copies, and also every commit amended or replaced before it was pushed. No branch's commit is touched.

Decided:
- Under the lead's rule (ROUND2.md, "What READY means"), a wrong answer on a third pass goes to Logan. The fixes are made in a commit after `bfdda6c`, and Logan is asked whether to push on the lead's checks or send it for a fourth pass.

For: Logan, the case study
