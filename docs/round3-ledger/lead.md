# lead.md - the lead's file, round 3

## 2026-10-31 05:03:37 -0700 - the round is asked for; the cleanup; the survey of what moved; the trial; Logan's six decisions

Measured:
- **Logan's request**, in chat at 2026-10-31 04:22:42 -0700 (the transcript's own timestamp), verbatim:
  > Go ahead with the cleanup, then we will update the site with a couple new projects, a bootstrap kit and a muse-softfloat hackathon project, as well as updating the cft information (it has a new nightly page which shows quite a bit about a nightly case sweep, as well as a separate project which found an issue in the golden model that can go to the corrections page)
- **The cleanup** came first, at that word: the resume work's leftover branches, plant worktrees and verifier clones. It is recorded in the resume work's own ledger at 04:26:59. loganw.dev now holds main alone, at `797f588`, which is GitHub's main.
- **What moved**, by `gh api repos/<owner>/<name>/compare/<pin>...<default branch>` for every pin in pins.json, run from 05:01:31 to 05:02:18 (an earlier run that morning gave the same counts):
  - cft-fp256: `ab51655` to `19de866`, 646 commits ahead;
  - QRO-Crate: `8858978` to `8fe0268`, 10 ahead;
  - Mercenaries-Fan-Build/mercs2-modkit: `9acb750` to `1d2c536`, 45 ahead;
  - Mercenaries-Fan-Build/mercs2-wad-simulator: `d18af76` to `13d96ed`, 1109 ahead;
  - Mercenaries-Fan-Build/notes-on-the-released-game: `dac773d` to `1fcc294`, 204 ahead;
  - the other 16 pins: identical.
- **New on the account** (`gh repo list loganw234`, against the 2026-10-15 snapshot's list):
  - softfloat-bootstrap, public, created 2026-10-24T23:55:59Z. Its PublicEvent is at that same second, so it has been public from its creation. Its main is `a23a0ff`. It has 3 commits, each authored "Claude", each with a `Co-Authored-By: Claude Opus 5.5` trailer, and no workflows. Its README at `a23a0ff` calls it "the builder of the bootstrap kit for Logan's Meta AI hackathon, 2026-10-26 to 2026-11-04", and says it "stays private".
  - muse-softfloat, public, created 2026-10-26T16:37:32Z. Its main is `a2241fc`. It has 185 commits, every one with the trailer `Co-Authored-By: Muse Code (muse-wonder-full-1.0)`. Its two workflows:
    - "Library CI (Linux gate)", `ci.yml`: `tools/run.sh smoke`, `standard` and `sanitize`, and the host example's build and diff;
    - "Deploy demo site to GitHub Pages", `pages.yml`.
  - Two private repositories the site does not read are new too. The snapshot leaves them out, as it leaves out every private repository the site does not read, and nothing in this round names them.
- **cft-fp256 at `19de866`.** `git diff ab51655 19de866 -- docs/VALIDATION.md` adds 90 headings. Among them:
  - 2026-10-22, the nightly progress page (parcel NP): `hw/card_stress_progress.py` reduces the long run's record to `site/nightly.json`, and `site/nightly.html` shows it;
  - 2026-10-29, the page redesigned;
  - the newest, 2026-10-30, "issue 1, the first outside report: exp2m1(emax + 1) toward zero raised overflow, in the golden model, the C, the vectors and the WebAssembly module; ...". Its entry says the report came "from a clean-room audit of loganw234/muse-softfloat (binary16/32/64), cross-tested against this library and an exact arbiter". The fix merged as `48e2aa22`.
  - GitHub's issue 1 on cft-fp256 was opened 2026-10-31T03:06:33Z and closed 11:20:42Z, both by the owner's account.
  - `site/nightly.json` at `19de866` is 216,831 bytes. Its totals: 10 nights, the first starting 2026-10-19 19:36:47, the newest (night 10) starting 2026-10-29; 6,135 slices, 20,759,013,456,650 cases, 0 disagreements; 8,645 legs, 8,505 pass, 0 fail, 140 skipped.
  - The page is live at https://loganw234.github.io/cft-fp256/nightly.html (HTTP 200 when read).
  - cft-fp256's workflows are still `gates` and `pages`, as pins.json classes them.
- **The trial**, in a scratch worktree of main at `797f588` (`<scratch>/r3-trial`):
  - The pins were moved: cft-fp256 to `19de866`, and softfloat-bootstrap at `a23a0ff` and muse-softfloat at `a2241fc` added with no `dir`, read from the site's own clones, which were fetched into the trial's `.cache/`.
  - A snapshot was taken there at 04:59 (`sources/github-2026-10-31-0459.json`, 66 repositories; its private names are only the ones the site reads). `check_workflows` and `check_pins` pass.
  - Each page was rendered on its own (`<scratch>/r3-trial-pages.py`); each stops at its first refusal, so the trial sees one refusal a page. 16 of 19 pages render, and 3 refuse:
    - pages.resume: cft-fp256's README.md, "(The published set is\s+\*\*[\d,]+\*\* cases)";
    - pages.verify: docs/VERIFICATION.md, the `gate` budget's sentence;
    - pages.work_cft_fp256: CONFORMANCE.md, "Profile 3, 2026-10-05".
  - Of the figures the 16 read, 8 read a different text than public/facts.json at `797f588`:
    - the snapshot's date;
    - Map & Ledger's newest cft-fp256 entry, now dated 2026-10-30, with the subject "issue 1, the first outside report";
    - CLAUDE.md's quick and gate budgets, "31 of 53 stages" and "45 of 53";
    - cft-fp256's last verified, 2026-10-30;
    - its agent-credited count, 2052/2106;
    - the Record's count of cft-fp256 entries, 258.
- **Logan's decisions**, through the question tool. The first four were answered by 04:40:32 -0700 and the last two by 04:55:59 (each stamp from `date`, taken right after the answer). Verbatim, question then answer, each answer the option he chose in the words the lead wrote for it:
  1. "softfloat-bootstrap's README says the repository "stays private" (only the zip goes to the Meta directories), but GitHub has shown it public since it was made, 2026-10-24 23:55 UTC. Is public what you want?" - "Public is right": "Keep it public. The site carries it like any public pin and never quotes the README's 'stays private' line, which is now stale."
  2. "How should the site carry softfloat-bootstrap and muse-softfloat in this round?" - "Rows and nodes now (Recommended)": "Pin both at GitHub's main. Each gets a Map & Ledger row and a map node in the Determinism lane, with edges quoting their own files. Dossiers wait until the hackathon closes on 2026-11-04."
  3. "cft-fp256's ledger calls issue 1 "the first outside report". It was filed from your own account, by a clean-room audit of muse-softfloat. On Corrections, does it retire the signature row ("first outside correction — pending")?" - "Own row; signature stays (Recommended)": "A new row read from cft-fp256's ledger at the new pin: found by 'a clean-room audit of loganw234/muse-softfloat', fixed in 48e2aa22. The signature row stays pending until a stranger files one."
  4. "All 185 of muse-softfloat's commits credit "Muse Code (muse-wonder-full-1.0)" in their Co-Authored-By line. The site's agent-credited rule counts only Claude or Gemini, so it would read 0 of 185. How should Muse be counted?" - "Count Muse, name it on Method (Recommended)": "The rule counts Claude, Gemini or Muse (185 of 185). SPEC's definition says so, and Method's co-authorship section adds a sentence read from muse-softfloat's trailers. Your statement there is unchanged."
  5. "Besides cft-fp256 and the two new pins, three more pins trail GitHub: QRO-Crate is 10 commits ahead, with a round of its own running today, and the organisation's three Preservation repositories are 45, 1,109 and 204 ahead. Which move in this round?" - "cft-fp256 and the new two (Recommended)": "QRO-Crate, mid-round, and the three Preservation repositories stay at their pins for a later update. Their pages are unchanged."
  6. "How should the work be split, and on which models?" - "Sonnet parcels, Haiku verifiers (Recommended)": "As in round 2. The lead does P0: pins, snapshot, rows, nodes and the Muse rule. Then Sonnet parcels take the cft-fp256 pages, Corrections and Method. Each parcel is verified on a planted copy on Haiku, and the lead's own work on Haiku too."

Believed:
- "QRO-Crate ... with a round of its own running today", in question 5, rests on today's push to its main and on the times of its worktrees and its ledger directory under `<repos>`, not on reading them.
- Logan's "a separate project which found an issue in the golden model" is the clean-room audit that cft-fp256's entry names. No repository of that audit was found, so the site cites cft-fp256's record of the report.

Decided:
- This is round 3, on the branch `round3`, cut from main at `797f588`. Its plan of record is `docs/ROUND3.md`.
- Every agent of this round is described "R3 <name>: ...", so `tools/round_metrics.py` finds it. The lead's own session is counted from the request at 04:22:42.
- **The push waits on Logan's word.** Decision 33, "Push when verified", was round 2's.

For: verifier-plan, the parcels, the round's record

## 2026-10-31 05:06:21 -0700 - Logan's seventh decision: About names Muse beside Claude and Gemini

Measured:
- About says, in the lead's words of round 1 (site/pages/about.py, coauthors_block): "The AI collaborators are named here: Claude and Gemini." Asked through the question tool, "About says "The AI collaborators are named here: Claude and Gemini." Once muse-softfloat is on the site, that list leaves out Muse. Should About name Muse too?" - his answer, by the stamp above: "Name Muse too (Recommended)": ""The AI collaborators are named here: Claude, Gemini and Muse." Only that list changes; the rest of About stays as you approved it."

Decided:
- About's list is the lead's, in P0, since about.py is a shared page; SPEC.md keeps the answer as decision 53.

For: verifier-plan, P0, P3

## 2026-10-31 05:06:35 -0700 - a correction to the 05:06:21 entry: About's sentence is P5's, not the lead's

Measured:
- The 05:06:21 entry calls About's "The AI collaborators are named here: Claude and Gemini." the lead's words of round 1. `git log -S` on site/pages/about.py finds it first in d445b42, "Merge 07b1526 (lead's control and gate fixes) and P5: Method and About": it is round 1's parcel P5's. The question put to Logan did not say whose it was, so his answer stands.

For: verifier-plan

## 2026-10-31 05:11:58 -0700 - the gate's Python is gone from the desktop; Logan's eighth decision moves the gate to 3.12.15

Measured:
- `python` on this desktop is now Miniconda's 3.12.15 (Git Bash and PowerShell alike). The py launcher lists a 3.12 install whose python.exe no longer exists; the only other Python is 3.13.5. .python-version says 3.12.9, so `bash verify/run.sh` refuses to run, and no gate has run here since 2026-10-16.
- Asked through the question tool, "The gate runs only under Python 3.12.9 (.python-version), and this machine no longer has it. ... How should I get 3.12.9 for the round's gates?" - his answer, at 05:11 by `date` taken after it: "Move the gate to 3.12.15": "Change .python-version to 3.12.15, so the desktop and CI both run 3.12.15, recorded in the ledger. Python's HTML parser reads edge cases differently between releases, so the gate itself would need checking first."
- CI can follow: actions/python-versions' manifest lists 3.12.15 as stable, with python-3.12.15-linux-24.04-x64.tar.gz. Miniconda's Python holds markdown-it-py 4.2.0 and mdurl 0.1.2, and no tinycss2 or webencodings; verify/requirements.txt pins markdown-it-py 3.0.0, mdurl 0.1.2, tinycss2 1.5.1 and webencodings 0.5.1 by hash.

Decided:
- The gate's Python is a venv of Miniconda's 3.12.15 at `<repos>/loganw-dev-venv`, holding verify/requirements.txt installed by hash, so Miniconda's own packages are left as they are. Every gate this round runs with PYTHON set to it.
- First, the full gate runs on main's tree with .python-version alone changed, to see what 3.12.15's parser does to it. The change lands in P0 only once that gate passes, and SPEC.md keeps the answer as decision 54.

For: anyone who runs a check this round; verifier-plan; P0

## 2026-10-31 05:14:32 -0700 - the plan, draft 1, at a19355a on round3; verifier-plan dispatched on Haiku

Measured:
- `docs/ROUND3.md`, draft 1, committed at `a19355a` on the branch `round3`, parent `797f588` (main). `python site/build.py --docs`: 0 problems in 9 documents. verifier-plan's brief: `briefs/verifier-plan.md`. Its worktree, `<scratch>/r3-verifier-plan/loganw.dev`, is a detached worktree of loganw.dev at `a19355a`, with the site's `.cache/` copied in.

Decided:
- **verifier-plan** is dispatched now, model requested: haiku, described "R3 verifier-plan: ...". Its scratch is `<scratch>/r3-verifier-plan/`. The full gate on main's tree under 3.12.15 (decision 54) is running in `<scratch>/r3-py`, so the brief tells it to run no gate.

For: verifier-plan, the round's record

## 2026-10-31 05:17:04 -0700 - verifier-plan's test escalation arrived as a runtime message

Measured:
- The line "verifier-plan: test escalation" reached the lead through the runtime's agent messages while P0's snapshot was being taken. A verifier on Haiku in this runtime can message the lead, as in round 2.

For: every later brief

## 2026-10-31 05:21:25 -0700 - the full gate passes on main's tree under 3.12.15; .python-version moves in P0's first commit

Measured:
- In `<scratch>/r3-py`, a detached worktree of main at `797f588` with only .python-version changed (3.12.9 to 3.12.15), `PYTHON=<repos>/loganw-dev-venv/Scripts/python.exe bash verify/run.sh --require-all`, run 20261031-051240-797f588-dirty, from 05:12:39 to 05:21:00: VERDICT: PASS, nothing skipped; passed 11; build 43 published files exactly what the pins render; facts 2084 read again and the same, 60 stated, 0 skipped; numbers 3544 marks; privacy 0 problems, with 2 private repositories the site does not read looked for in 164 files; github 21 pins; controls 485 caught, 0 did not fail, 0 skipped.
- The controls stage took 387 s. P0's page renders and its snapshot ran beside it, so that time is not the stage's alone (trap 19).

Decided:
- `.python-version` moves to 3.12.15 in a commit of its own on round3, before the rest of P0 is committed.

For: verifier-P0, every verifier that runs a gate

## 2026-10-31 05:45:05 -0700 - verifier-plan's report on draft 1: NOT READY, four defects, each true at its source; P0 committed at 2f52525 and its full gate running

- **P0** is commit `2f52525` on `round3`, parent `0e87fc2` (the gate's Python). Its message lists every change. Before it was committed: `python site/build.py`, 43 files from 23 pins, 2462 figures; `--check`, `--numbers` (4043 marks, 0 problems), `--links`, `--local-only`, `--docs` (9 documents) and `--manifest`, each 0 problems. Its full gate started at 2026-10-31 05:44:30 -0700.
Measured:
- **verifier-plan's report** on draft 1 (`a19355a`): NOT READY, four defects, 15 side notes, four items not determined. The runtime's figures: 72 tool uses, 1,540,590 ms; its "tokens", 459,808, is the context at the run's end. Its file is `verifier-plan.md`.
- **Each defect, checked at its source by the lead before acting:**
  - D1, true. The two private repositories the 05:03:37 entry and the plan call "new" were created on 2025-10-11 and 2026-04-18 (`gh repo list`'s createdAt, read at the survey). The snapshot leaves out every private repository the site does not read, so they were never in its list: they are not new. Corrected in the entry below and in draft 2.
  - D2, true. The 05:11:18 entry gives decision 8's question with "..." where the plan gives it whole. The whole question is in the entry below.
  - D3, true. `verify/run.sh` has no stage named connections: `links` holds each dossier's Connections to the map's edges (its line 210). The plan's "links, numbers and connections stages" is round 2's own wording, carried over.
  - D4, true. Draft 1 dropped round 2's "with the parcel's own message and parent", and names no branch. A single-branch clone carries its branch's name and its commit's message, author and date, so either could tell a verifier which commit holds the plants.
- **The side notes**, each read against its source:
  - taken in draft 2: S1 (build.SPEAKERS holds every statement to Logan), S2 (the ratio is decision 8's), S3 (SPEC.md gained decisions 47 to 54 in P0, `2f52525`, after the draft), S4 (a "Time and cost" section, as round 2's), S5 (question 5 said "three more pins" and listed four; Logan's answer keeps all four), S6 (the site calls the check "cft-fp256's own conformance replay, in the browser"), S7 (P2's thread quotes CLAUDE.md's two budget lines, which read new counts), S8 (P0's control is build.py's agent-rule), S9 (every page not on a parcel's list stays as it is), S13 (round_metrics.py counts only "R3 " agents in the lead's own subagent folder, and labels times at a fixed -0700, which is wrong after 2026-11-01 02:00), S14 (the 2026-10-16 entry left the push waiting on Logan's word, not the cleanup);
  - not taken: S10. The kit's "VERDICT: PASS, all five checks hold" is its kit gate's verdict, not its runner's. Its runner's passes ("17 of 17 stages passed, nothing skipped") sit in an entry headed "2026-10-23 to 2026-10-24", which the parser dates at its start, 2026-10-23, while both runs were made on 2026-10-24 (run ids 20261024-023330 and 20261024-025211). A declared form would print the newest pass a day early, so the row keeps its dash and says why;
  - S11, S12 and S15 confirm what the draft says.
- **Not determined by it:** the survey's times (`<scratch>/r3-survey-compare.txt` holds the run's own start and end lines); the venv's install by hash (`pip install --require-hashes` refuses a file whose hash differs, and the pip list after it showed the four pinned versions); QRO-Crate's "running today" (the plan's reading already marks it as resting on times, not content); the lead's model, which the round's script reads from the transcript at the round's end.

Decided:
- Draft 2 answers D1 to D4 and the side notes taken, and goes back to verifier-plan for its second pass, scoped to the diff from draft 1.
- No tracked file is edited while the full gate on `2f52525` runs, since its stages read the working tree.

For: verifier-plan, the round's record

## 2026-10-31 05:45:05 -0700 - a correction to the 05:03:37 entry, and the 05:11:18 entry's question whole (verifier-plan's D1 and D2)

Measured:
- **The 05:03:37 entry**, under "New on the account", says: "Two private repositories the site does not read are new too." That is wrong (verifier-plan's D1). Both were created before the 2026-10-15 snapshot, on 2025-10-11 and 2026-04-18, and are absent from every snapshot's list because the snapshot records a private repository only if the site reads it. The account now has 50 repositories, 40 public; the 2026-10-15 snapshot lists 46 of the owner's, 38 public and the 8 private ones the site reads. So the new public ones are softfloat-bootstrap and muse-softfloat, and nothing shows that any private one is new.
- **The 05:11:18 entry** gives decision 8's question with "...". The question, whole, as the question tool put it: "The gate runs only under Python 3.12.9 (.python-version), and this machine no longer has it. `python` is now Miniconda's 3.12.15, and the 3.12 install the py launcher lists is gone (perhaps in the 10-26 toolchain reinstall). How should I get 3.12.9 for the round's gates?" The three options offered: "conda env, conda-forge (Recommended)", "python.org installer", and "Move the gate to 3.12.15", which he chose.
- "perhaps in the 10-26 toolchain reinstall" in that question is the lead's guess, from cft-fp256's ledger entry "2026-10-26 (afternoon) - the lead's: the desktop's gate after its toolchains were reinstalled". It is not a measurement of when the install went.

For: verifier-plan, the round's record

## 2026-10-31 05:52:42 -0700 - the full gate on P0 (2f52525): PASS, nothing skipped

Measured:
- `PYTHON=<repos>/loganw-dev-venv/Scripts/python.exe bash verify/run.sh --require-all` on `2f52525`, clean, run 20261031-054430-2f52525, from 05:44:30 to 05:52:32, nothing else running: VERDICT: PASS, nothing skipped; passed 11; build 43 published files exactly what the pins render; facts 2402 read again and the same, 60 stated, 0 skipped; numbers 4043 marks; privacy 0 problems, 166 files and 1085 blobs; github 23 pins; controls 489 caught (main's 485 and the 4 agent-rule controls), 0 did not fail, 0 skipped, in 382 s.

For: verifier-P0, the round's record

## 2026-10-31 05:55:38 -0700 - draft 2 at 758411c; P0's third commit, f57c22e; verifier-plan resumed for its second pass, and verifier-P0 dispatched, both on Haiku

Measured:
- `f57c22e`: Map & Ledger's muse-softfloat row links its record, docs/RECORD.md, as draft 1's P0 section said it would and `2f52525` did not. `758411c`: draft 2 of the plan. Quick stages clean on both: `--check`, `--numbers` (4045 marks), `--links`, `--local-only`, `--docs` and `--manifest`, 0 problems.
- verifier-P0's brief: `briefs/verifier-P0.md`. Its worktree, `<scratch>/r3-verifier-P0/loganw.dev`, is a detached worktree of loganw.dev at `758411c`, with the site's `.cache/` copied in. The shared briefs `briefs/_common.md` and `briefs/_verifier.md` are written; so are P1's, P2's and P3's, for their dispatch after Logan approves the plan.

Decided:
- **verifier-plan** is resumed for its second pass, scoped to `git diff a19355a 758411c -- docs/ROUND3.md` and the ledger's entries since its report.
- **verifier-P0** is dispatched now, model requested: haiku, described "R3 verifier-P0: ...". Its scratch is `<scratch>/r3-verifier-P0/`.
- The full gate on `758411c` runs now; neither verifier runs one.

For: verifier-plan, verifier-P0, the round's record

## 2026-10-31 05:57:33 -0700 - Logan's ninth decision: the resume cites the card's long stress run and the nightly sweep, quoted; verifier-P0's test escalation

Measured:
- Asked through the question tool, by the stamp above: "Your resume quotes cft-fp256's binary256 soak: 541 passes in 70 minutes, 0 failures. At the new pin the record also states the card's long stress run (61 hours, 4,086 legs, 0 failures, 2026-10-19) and the nightly sweep (10 nights, 20,759,013,456,650 cases, 0 disagreements). Should the resume cite them too?" - his answer: "Add both, quoted (Recommended)": "Two short lines beside the soak, each quoted from cft-fp256's record at the pin with its file and line, as the resume's other lines are. The PDF and the text twin follow." The question's figures were the lead's reading: the 61 hours, 4,086 legs and 0 failures from the heading of cft-fp256's entry of 2026-10-19 at 19de866, and the nightly figures from site/nightly.json's totals there.
- The line "verifier-P0: test escalation" reached the lead through the runtime's agent messages.

Decided:
- The two lines are the lead's, on the resume, after the full gate on 758411c has finished (its stages read the working tree), as their own commit. SPEC.md keeps the answer as decision 55. verifier-P0 is told of the commit, scoped to it.

For: verifier-P0, the integration verifier, the round's record

## 2026-10-31 06:05:54 -0700 - the full gate on 758411c: PASS, nothing skipped

Measured:
- `PYTHON=<repos>/loganw-dev-venv/Scripts/python.exe bash verify/run.sh --require-all` on `758411c`, clean, run 20261031-055546-758411c, ending 06:05:04: VERDICT: PASS, nothing skipped; passed 11; build 43 files; facts 2404 read again and the same, 60 stated, 0 skipped; controls 489 caught, 0 did not fail, 0 skipped, in 444 s, with verifier-plan and verifier-P0 at work beside it (their quick modes only).

For: verifier-P0, the round's record

## 2026-10-31 06:11:34 -0700 - verifier-plan's second pass on draft 2: NOT READY on D5, true at its source; make_plant.py's branch guard fixed and watched to refuse

Measured:
- **verifier-plan's second pass**, on draft 2 (`758411c`): NOT READY on one defect, D5; D1 to D4 answered; ten side notes. The runtime's figures: 39 tool uses, 871,590 ms; its "tokens", 679,201, is the context at the run's end.
- **D5, checked at its source: true.** `tools/make_plant.py` refused only a branch name containing "plant", then ran `git branch -f <name> <planted>`. A key naming `round3`, `main` or any existing branch would have moved that branch onto the plants, unless it was checked out in a worktree. Now the tool refuses `round3`, `main` and any branch that exists, and creates its branch without `-f`. Its control, in a scratch repository under `<scratch>/plant-guard-test` holding `round3` and `r3-P9`, with keys naming round3, main, r3-P9 and r3-plant-P9:
  - "round3: the branch 'round3' is the round's or main; a copy goes on a branch of its own"
  - "main: the branch 'main' is the round's or main; a copy goes on a branch of its own"
  - "r3-P9: the branch 'r3-P9' exists already; a copy goes on a new branch of its own"
  - "r3-plant-P9: the branch 'r3-plant-P9' names a plant; name it as a parcel's own branch is"
  - and every branch is where it was.
- **Its side notes**, each read against its source:
  - taken in draft 3: SN-1 ("On 8" in the past tense), SN-2 (a drafted label is accepted too, "drafted from" his words), SN-3 (`site/snapshot_github.py` and `verify/` on the lead's list), SN-4 (decision 8's "perhaps in the 10-26 toolchain reinstall" was the lead's guess), SN-5 (decision 55), SN-6 (a page on no parcel's list keeps its module; its rendered page changes by what it reads), SN-7 (propose.py's control reads the Determinism door's word "workloads"), SN-8 (the clock changes at 02:00 PDT, 09:00 UTC on 2026-11-01), SN-10 (the kit's row does not quote "stays private");
  - SN-9 is true: the lead's message for the second pass listed the commits since the first pass without `0e87fc2`. The verifier found it.
- **Not determined by it:** the soak's figures in the ninth decision's question, which are the resume's own facts at `758411c` (its text twin: "541 passes in 70 minutes, each a resident run of a million elements at fma, add and mul [fact 1021], with 0 failures"); the survey's times; P2's budget-table line and P3's pinned readers, which are the parcels' to read; and the live deploy of `797f588`, which the round's entry records.

Decided:
- Draft 3 answers D5 and the side notes taken, and records decision 55 and the resume's change, `site/pages/resume.py`'s one new item.
- verifier-plan's third pass, its last under the three-pass rule, reads draft 3.

For: verifier-plan, the round's record

## 2026-10-31 06:14:42 -0700 - the resume's item for decision 55 at 2cbb7e7; draft 3 at e464d1d; verifier-plan resumed for its third pass, its last

Measured:
- `2cbb7e7`: the resume's one new item, "A 61-hour stress run of the card with no failure; then nightly sweeps: 10 nights, 20,759,013,456,650 cases, 0 disagreements, where the sweep's case totals add items whose tools count different things." (its text twin, three facts), and SPEC.md's decision 55. By printout.py's own measure, cft-fp256's block had 29 pt to spare on the PDF's page 1: two items took 43 pt and one item quoting the ledger's heading 41, each moving the block to page 2 and the PDF to three pages; this one takes 28, and the PDF stays at two (cft-fp256 280 pt in 281). Its first commit message said "two items took 41"; it was restated in place, unpushed and uncited, as `2cbb7e7`. `e464d1d`: draft 3. Quick stages clean on both.

Decided:
- **verifier-plan** is resumed for its third pass, its last, on `e464d1d`, scoped to `git diff 758411c e464d1d` and the ledger's entries since its second report.
- The full gate on `e464d1d` runs now. verifier-P0, still on its first pass at `758411c`, is told of `2cbb7e7` when it reports.

For: verifier-plan, verifier-P0, the round's record

## 2026-10-31 06:25:43 -0700 - verifier-plan's third pass, its last: NOT READY on D6, a stamp the ledger lacked; the stamp given, and a correction to the 05:45:05 entries

Measured:
- verifier-plan's third pass, on draft 3 (`e464d1d`): NOT READY on one record defect, D6; D5's fix confirmed by its own run of make_plant.py on five keys; no wrong answer left. The runtime's figures: 16 tool uses, 486,129 ms; its "tokens", 771,278, is the context at the run's end.
- D6, true. SPEC.md's round-3 block says the eighth answer came "by 05:11:18", and no heading here carries that stamp. Its source: the command the lead ran right after the answer opened with `S="$(date '+%%Y-%%m-%%d %%H:%%M:%%S %%z')"; echo "$S"`, which printed "2026-10-31 05:11:18 -0700"; it then read the gate's libraries and actions/python-versions. The entry that records the answer was written later, at 05:11:58, and says "at 05:11 by `date` taken after it". So SPEC's "by 05:11:18" stands, on the output quoted here.
- The two entries of 05:45:05 call that entry "the 05:11:18 entry"; it is the 05:11:58 entry.

Decided:
- Its notes: SN-B taken in draft 4 (decision 9's figures were the lead's reading of the record, as the 05:57:33 entry says); SN-C taken (make_plant.py's docstring names its guard); SN-D noted as a limit of the tool (a failed run leaves its worktree registered, and the next run refuses until it is removed). Its note for Logan, that decision 55 asked for two short lines and the resume prints one item of two printed lines, goes to him with the plan.

For: verifier-plan, the round's record

## 2026-10-31 06:26:21 -0700 - the full gate on e464d1d: PASS, nothing skipped; draft 4 at d9bf501; a slip of the lead's

Measured:
- `bash verify/run.sh --require-all` on `e464d1d`, run 20261031-061450-e464d1d, from 06:14:49 to 06:26:10: VERDICT: PASS, nothing skipped; passed 11; facts 2407 read again and the same; numbers 4054 marks; docs 0 problems in 9 documents; controls 489 caught in 532 s, verifier-plan's third pass running beside it.
- **A slip of the lead's:** at 06:25:46, during that run's controls stage, the lead edited docs/ROUND3.md (draft 4's one change), against its own rule of 05:45:05 that no tracked file is edited while a gate runs. The run's docs stage had passed on `e464d1d`'s text by 06:17:16, when the run's state directory was last written before the controls stage. No stage after it reads that file's words for a verdict, so the verdict stands for `e464d1d`; the change is draft 4's alone, and `--docs` passes on it.

For: the round's record

## 2026-10-31 06:44:54 -0700 - Logan approves the plan at d9bf501 and keeps the resume's one item; verifier-P0's report on P0: NOT READY, each finding checked; the parcels dispatched for their designs

Measured:
- **Logan approved the plan**, through the question tool, by the stamp above: "Round 3's plan is at draft 4 (docs/ROUND3.md, d9bf501). Its verifier ended its third pass on one record stamp, since fixed; no wrong answer remains. Approve it, and start the three Sonnet parcels on their designs?" - "Approve and start (Recommended)": "P1, P2 and P3 start their designs now, beside verifier-P0's check of P0. Each stops after its design, for the lead's review and a seam commit, before building."
- **And kept the resume's one item**: "Decision 55 asked for "two short lines beside the soak". The resume prints both as one item of two printed lines: two separate items push cft-fp256 to the PDF's page 2 and the printout to three pages. Keep the one item?" - "Keep one item (Recommended)": "...The PDF stays at two pages."
- **verifier-P0's report** on P0 (`0e87fc2`, `2f52525`, `f57c22e`) at `758411c`, and on `2cbb7e7` as asked: NOT READY, five defects and a minor one. The runtime's figures: 107 tool uses, 1,949,795 ms; its "tokens", 536,857, is the context at the run's end. Its test escalation reached the lead, addressed to "main".
- **Each finding, checked at its source by the lead:**
  - A, true. On the phone map, softfloat-bootstrap's label box covers muse-softfloat's marker. The lead's own browser check found it before the commit and judged it of the kind the live map already shows (seven labels over another node's marker there), but `2f52525`'s message says only that "the phone map's overlaps are the stacked lines the live map already has", which leaves it out. Restated here, and in the plan: one more label covers a marker, as seven already do on the live map; a known limit of the phone layout, which puts a label under its own marker and does not move it off a later one.
  - B, true, and P3's: Method's count sentence still says "credit Claude or Gemini". The plan gives it to P3, and P3's verifier reads for it.
  - C, true. The plan's P0 bullet says P0 adds to `build.SOURCE_PATHS`; P0 needed none, since every path its labels name was listed. Restated in the plan.
  - D, the resume's dropped clause "The published set is 1,068,915 cases": a change to what the resume claims, which the plan sends to Logan. It goes to him now, with the printout's fit measured.
  - E, the nightly totals carry no date on the resume, and grow each night after the pin. Also to Logan, with the fit.
  - The minor one is verifier-plan's D6, answered at 06:2x.
- **Its side notes, read against their sources:**
  - taken: a control case that only a case-insensitive rule passes; SPEC section 4 states the rule's limits (it reads names, so a person named Muse would be counted, and `Muse_Code` would not); resume.py's comment says the totals are cumulative to the newest night;
  - not taken: `design/experiments/` is round 1's unpublished design work, kept as it was, and says "Claude or Gemini" as round 1's rule did; the muse-softfloat edge's evidence, printed beside it under the map, says the audit cross-tested the two, so "verifies" stands with its words beside it.

Decided:
- P1, P2 and P3 are dispatched now, for their designs only, each in a worktree of its own cut from `round3` at `d9bf501`, model requested: sonnet, described "R3 P<n>: ...". Their branches are `r3-P1`, `r3-P2` and `r3-P3`.
- P0's follow-ups (the control case, SPEC's limits, the resume's comment, the plan's two restates) are the lead's next commit, for verifier-P0's second pass. They touch no parcel's file; each parcel takes them by its "go" fast-forward.

For: P1, P2, P3, verifier-P0, the round's record

## 2026-10-31 06:48:36 -0700 - Logan's word on verifier-P0's D and E: the published set stays out, and the nightly totals are dated; the parcels' test escalations

Measured:
- D: "The resume used to say "The published set is 1,068,915 cases, and that exact set was replayed on the card...". At the new pin the published set is 1,072,415, so the line now cites only the replayed 1,068,915-case set, which drops the published set's size. Restore it?" - "Leave it out (Recommended)": "The line keeps its claim about what the card replayed. Restoring "and the published set is 1,072,415 now" adds a printed line, which moves cft-fp256 off the PDF's first page and makes the printout three pages."
- E: "The nightly totals on the resume (10 nights, 20,759,013,456,650 cases, 0 disagreements) grow every night after the pin, so they carry no date as written. Date them?" - "Date them (Recommended)": ""...; nightly sweeps to 2026-10-29: 10 nights, ...", the date read from site/nightly.json's newest night at the pin. "then" is dropped so the item stays two printed lines, and the PDF stays two pages."
- The fits, by printout.py's own measure: the replay item is 3 printed lines, and 4 with D; the nightly item is 2, 3 with E as first worded, and 2 with "then" dropped (its last line 444 of 492 pt). site/nightly.json at 19de866 gives the newest night on its line 5: "newest": {"night": 10, "date": "2026-10-29", ...}.
- "P1: test escalation", "P2: test escalation" and "P3: test escalation" each reached the lead as a runtime message, addressed to "main". The 06:3x entry's "answered at 06:2x" means the 06:25:43 entry.

Decided:
- P0's follow-ups go in one commit: the date (site/nightly.json joins build.SOURCE_PATHS, which P1's design also needs), the agent-rule control's upper-case case, SPEC section 4's limits of the rule and decision 55's two further answers, resume.py's comment, and the plan's restates of A and C. Then verifier-P0's second pass, scoped to it.

For: verifier-P0, the integration verifier, the round's record

## 2026-10-31 06:48:46 -0700 - a correction to the entry before: two times it typed instead of reading

Measured:
- The entry before says "The 06:3x entry's "answered at 06:2x" means the 06:25:43 entry." Both of its first two times were typed. Read from the headings: the entry is the one headed 2026-10-31 06:44:54 -0700 ("Logan approves the plan at d9bf501 ..."), whose line "The minor one is verifier-plan's D6, answered at 06:2x" means the entry headed 2026-10-31 06:25:43 -0700.

For: the round's record

## 2026-10-31 06:51:47 -0700 - P0's follow-ups at c5e5e79; its full gate running; verifier-P0 resumed for its second pass

Measured:
- `c5e5e79` on round3, parent `d9bf501`: the resume's dated nightly item ("nightly sweeps to 2026-10-29 [fact 1246]: 10 nights, 20,759,013,456,650 cases, 0 disagreements [fact 1247] ..." in its twin; the PDF two pages, cft-fp256 280 pt in 281); site/nightly.json in build.SOURCE_PATHS; the agent-rule control's upper-case case; SPEC section 4's limits and decision 55's further answers; resume.py's comment; ROUND3.md's restates of verifier-P0's A and C. Quick stages clean: `--check`, `--numbers` (4057 marks), `--links`, `--local-only`, `--docs`, `--manifest`.

Decided:
- verifier-P0's second pass is scoped to `git diff 758411c c5e5e79 -- site docs/SPEC.md pins.json sources` and to ROUND3.md's P0 section as it now reads, with the ledger's entries after its report. The full gate on `c5e5e79` runs now; the three parcels are designing beside it, reading only.

For: verifier-P0, the round's record

## 2026-10-31 07:00:49 -0700 - the full gate on c5e5e79: PASS, nothing skipped

Measured:
- `bash verify/run.sh --require-all` on `c5e5e79`, clean, run 20261031-065144-c5e5e79, from 06:51:43 to 06:59:42: VERDICT: PASS, nothing skipped; build 43 files; facts 2408 read again and the same, 60 stated, 0 skipped; numbers 4057 marks; privacy 0 problems, 1161 blobs; github 23 pins; controls 490 caught (489 and the upper-case case), 0 did not fail, 0 skipped, in 359 s, with the parcels designing and verifier-P0 reading beside it.

For: verifier-P0, the round's record

## 2026-10-31 07:05:22 -0700 - P1's two findings across parcels, each true at 19de866; one is cft-fp256's own record disagreeing with itself

Measured:
- P1's 07:04 entry, finding 1: Verify's `make golden` cost quotes docs/VERIFICATION.md's table cells, "2.6 min at four workers" and "8 to 13 min", which `git log -S'min at four workers'` last changed at 291c431c (2026-09-08). The same row now counts "5,954 tests since parcel M2F2 (2026-10-30)" (line 354), and the ledger at 19de866 has the stage at "golden ok 3,385 s, 5,951 passed and 3 skipped" (VALIDATION.md:26127, a run on the build box).
- P1's finding 2: CONFORMANCE.md:338-339 says "**The tree is at profile 3.1** (2026-10-13), a minor step: cases added, none moved", and its rule at 281 says "**A major step** is a change to any recorded bit or flag". Issue 1's entry says of its fix: "The 8 that change are the rtz and rdn transcendental sets of each format, each by exactly one record, exp2m1(emax + 1): the same value, flags 20 to 16. ... those 8 records are the published ones moving" (VALIDATION.md:26179). CONFORMANCE.md at 19de866 names neither issue 1 nor a new profile, and GitHub's main is still 19de866 (`gh api .../compare/19de866...main`: identical).

Decided:
- Finding 1 is P2's: the page should not give the old cells as the current cost without what the record now measures. P2 is told.
- Finding 2 is P1's for the dossier, which quotes "none moved" since P0's requote, and touches P3's issue-1 row, whose "fixed" must not claim more than the entry. P3 is told. No page may say the profile stepped, since no file at the pin says so; a page may quote both lines.
- Finding 2 is a disagreement inside cft-fp256's own record, which the site can quote but not settle. It goes to Logan as a finding about cft-fp256, for the session that works there.

For: P1, P2, P3, their verifiers, Logan

## 2026-10-31 07:06:49 -0700 - verifier-P0's second pass: READY, with three restates and a note, made at 52983e0

Measured:
- verifier-P0's second report, on `c5e5e79`: READY, with R1 to R3 to restate and S1 to state; the upper-case control case closes the gap it found (its case-sensitive mutant now fails); the printout reproduced byte for byte from the twin, two pages by Ghostscript and pdftotext, cft-fp256's block on page 1. The runtime's figures: 42 tool uses, 812,318 ms; its "tokens", 703,717, is the context at the run's end. Its notes S2 (the date is the night's start, the record's own label) and S4 (design/experiments) stand as they are; B stays P3's.
- `52983e0` makes R1 to R3, S1 and S3. Quick stages clean.

For: the integration verifier, the round's record

## 2026-10-31 07:18:32 -0700 - P3's design reported; the lead's answers

Measured:
- P3's design (P3.md, 07:16:44 and its 07:17:20 correction): Corrections gains issue 1's row, every cell read from the one entry found by its whole heading (facts.entries: 1 of 258), its fix 48e2aa22 read from the entry's "merged as" line and checked as a merge the pin descends from; the caption restated; the gaps re-read at 19de866, none closed. Method's count sentence names "Claude, Gemini or Muse", and one sentence reads muse-softfloat's trailers, 185/185, the name only: every Muse trailer line also carries an email address, so no page prints the line. No seam need. The runtime's figures: 111 tool uses, 1,907,461 ms; its "tokens", 448,377, is the context at the run's end.

Decided:
- Every default P3 lists stands: the entry's line on the 8 moved records, two of its four known limits, no clause on whose repository muse-softfloat is, the row's word guard, the Muse sentence after the count sentence, and a stylesheet only if the browser shows the long cell needs one.
- P3's three gaps the record names and "where I'd attack first" does not list (DETERMINISM.md's departure from RISC-V on fma(inf, 0, quiet NaN), issue 1's known limits, and CONFORMANCE.md's "none moved" against VALIDATION.md:26179) are Logan's to add or not; they go to him with the round's other open items.
- P3's cross-page note: Map & Ledger's cft-fp256 row quotes the newest entry's subject, "issue 1, the first outside report", and Corrections' signature row says the first outside correction is pending. Both stand, each with its source: cft-fp256's "outside" is its own word for a report from outside its process, and decision 49 keeps the signature row until a stranger files one. It goes to Logan as a note.

For: P3, verifier-P3, Logan

## 2026-10-31 07:19:10 -0700 - P1's design reported; the lead's answers to its D1 to D5

Measured:
- P1's design (P1.md, 07:17:44; its cross-parcel findings 07:04:18; resume note 07:18:13). No seam need: site/nightly.json is in build.SOURCE_PATHS since c5e5e79. The runtime's figures: 133 tool uses, 1,970,603 ms; its "tokens", 583,077, is the context at the run's end.

Decided:
- D1, yes: issue 1 (VALIDATION.md:26149, fix 48e2aa22) is the third kept failure, in place of the device bullet (8b7dea1). The spec's "2-3" is its choice; which two or three is the dossier's, and round 1's P3 made the first choice.
- D2, yes: one paragraph quoting CONFORMANCE.md:338-339 beside VALIDATION.md:26179 and CONFORMANCE.md:281, which says neither that the profile stepped nor that it should have.
- D3, yes: the four rows and the nightly sweep's two paragraphs, every figure through the nightly fact, the pin's through night 10.
- D4, yes: Test it's `make golden` cost quotes VALIDATION.md:26127. P2's Verify quotes the same line, so the two pages agree; P2 is told.
- D5: no. O1, a sentence on cft-rebound's pinned libcft (ABI 0.12) beside the site's cft-fp256 pin, is declined: cft-rebound's pin did not move, the page reads nothing from cft-fp256, and the sentence would set the two side by side for a reader to compare.

For: P1, P2, verifier-P1, verifier-P2

## 2026-10-31 07:39:53 -0700 - P2's design reported; Logan's tenth decision (Verify keeps its order and drops "cheapest first"); the lead's answers; the seam commit to make

Measured:
- P2's design (P2.md, 07:30:25, corrected 07:35:56; resume note 07:36:14). Every quote on Verify and the Determinism thread has the same words at both pins but CLAUDE.md:9-10's counts; what moved is what they describe. Its one seam need: `bindings/wasm/README.md` in build.SOURCE_PATHS. The runtime's figures: 173 tool uses, 3,058,969 ms; its "tokens", 674,148, is the context at the run's end.
- Logan, through the question tool, by the stamp above: "Verify lists its checks "cheapest first": the browser replay, make golden, then make verify-quick. Its make golden cost will quote the record's newest timing, 3,385 s on the build box (one worker, 5,951 tests), no longer cheaper than verify-quick's documented ~20 min. Both of cft-fp256's own budget figures date from September. What should Verify do?" - "Keep order, drop the ranking (Recommended)": "The checks stay in their order, each with its cost and where and when it was measured; the lede no longer says "cheapest first", since no current figure ranks them on one machine." SPEC.md keeps it as decision 56.

Decided:
- D1, yes: VALIDATION.md:26127 with its entry's date and host, and no old cell. D2: as decision 56; the lede's change is P2's. D3: keep "what a pass proves". D4: yes, the three limits and the LIMIT sentence.
- D5: (a) and (c) yes. (b) yes, but not the subject "issue 1, the first outside report": the thread quotes what the defect was instead (the heading's own words after its subject, or the entry's line on it), so that "outside" is not printed on another page while Corrections' signature row says no outside correction has come. Map & Ledger's row quotes the subject as the newest entry's, and stays.
- D6, yes: the seam commit adds bindings/wasm/README.md to build.SOURCE_PATHS, with SPEC decision 56. verifier-P0 checks it, scoped, before "go".
- P2's F1 (cft-fp256's budget lines are September's, and the box's gates took 181 to 198 minutes) is a finding about cft-fp256, for Logan. F2 goes to P1 with its "go". F3 (threads.py's Determinism line) is not taken: the line names the thread's core, as it always has, not every node. F4 confirms the three pages quote the same lines of issue 1's entry.
- 

For: P1, P2, P3, verifier-P0, their verifiers, Logan

## 2026-10-31 07:41:31 -0700 - the seam commit at 90e36ef; a slip of the lead's, caught before it was committed

Measured:
- `90e36ef` on round3, parent `52983e0`: build.SOURCE_PATHS gains bindings/wasm/README.md, and SPEC.md gains decision 56. Quick stages clean: `--check`, `--numbers` (4057 marks), `--links`, `--local-only`, `--docs`, `--manifest`.
- **A slip of the lead's:** decision 56's text first carried "(2026-10-31, by 07:48.)", a time typed, not read. Before the commit it was replaced by the stamp of the entry that records the answer, 07:39:53, read from this file's heading.

Decided:
- verifier-P0 checks `90e36ef`, scoped to `git diff 52983e0 90e36ef`; then each parcel gets "go" with that SHA and its answers.

For: verifier-P0, the parcels, the round's record

## 2026-10-31 07:52:07 -0700 - verifier-P0 on the seam commit: no defect; its notes taken at 6eff67b; "go" to P1, P2 and P3 at 6eff67b

Measured:
- verifier-P0's scoped check of `90e36ef` (its file, 07:49:37): no defect; every label path the designs state is listed; decision 56 word for word; two cosmetic notes (the list's order, the preface's tenth stamp), both taken in `6eff67b`. The runtime's figures: 23 tool uses, 497,280 ms; its "tokens", 796,036, is the context at the run's end.

Decided:
- "go" goes to each parcel with `6eff67b`, which each takes by `git merge --ff-only 6eff67b` from `d9bf501`; no commit since d9bf501 touches a parcel's own files.
- P1's message carries its answers D1 to D4 yes, D5 no (see the entry on P1's design), and P2's F2: `make golden` runs four workers where pytest-xdist imports, so a single-worker timing is that host's, and the step says so.
- P2's message carries decision 56 and the answers of the entry on P2's design: D1 yes, D3 keep, D4 yes, D5 (a) and (c) yes and (b) without the subject "issue 1, the first outside report", D6 in 90e36ef.
- P3's message: every default stands, as the entry on its design says.

For: P1, P2, P3

## 2026-10-31 08:20:59 -0700 - P3 reported at 9d26d4f; its planted copy made, the key's SHA-256 recorded before verifier-P3's dispatch

Measured:
- P3's phase 2: `9d26d4f` on r3-P3, parent `6eff67b`; quick stages clean on its tree (its report, P3.md 08:16:45): 43 files, 2477 figures, numbers 4075 marks, verify-facts 2417 the same; its pages' controls 21 caught, 16 new. The runtime's figures: 71 tool uses, 1,493,537 ms; its "tokens", 608,946, is the context at the run's end.
- The planted copy, by tools/make_plant.py: `9bef3c6` on a branch of its own, with P3's message, author and dates and P3's parent; two plants, of kinds the plan names. **The key's SHA-256: `f3b84d8828fffac7e068a794142d24c6e4d27a09b4b463bd4240c47c3084a170`.** The key itself stays in `<scratch>` until the last planted-copy verifier has reported. The copy's full gate is running.

Decided:
- verifier-P3 is dispatched on Haiku once the copy's gate passes, in a clone made with `git clone --no-local --single-branch` from the copy's branch, which holds round3's history and the planted commit and not P3's own.

For: verifier-P3, the round's record

## 2026-10-31 08:31:24 -0700 - P3's planted copy passes the full gate; verifier-P3 dispatched on Haiku

Measured:
- The full gate on the planted copy `9bef3c6`, in its worktree under `<scratch>`, run 20261031-082055-9bef3c6, ending 08:31:12: VERDICT: PASS, nothing skipped; passed 11; numbers 4075 marks; facts 2417 the same; controls 506 caught (490 and P3's 16), 0 did not fail, 0 skipped. No stage points at a plant.
- verifier-P3's clone, `<scratch>/r3-verifier-P3/loganw.dev`, made with `git clone --no-local --single-branch` from the copy's branch, its origin removed: one branch, the planted commit on round3's history, and P3's own commit not in it. Its brief: `briefs/verifier-P3.md`.

Decided:
- **verifier-P3** is dispatched now, model requested: haiku, described "R3 verifier-P3: ...". Its scratch is `<scratch>/r3-verifier-P3/`. It reads P3.md only after it reports.

For: verifier-P3, the round's record

## 2026-10-31 08:32:57 -0700 - verifier-P3's test escalation

Measured:
- The line "verifier-P3: test escalation" reached the lead through the runtime's agent messages, addressed to "main".

For: the round's record

## 2026-10-31 08:40:08 -0700 - P2 reported at 2cbcc82; its planted copy made, the key's SHA-256 recorded before verifier-P2's dispatch

Measured:
- P2's phase 2: `2cbcc82` on r3-P2, parent `6eff67b`; quick stages clean on its tree (its report, P2.md 08:38:05): 43 files, 2500 figures, numbers 4119 marks, verify-facts 2440 the same; its controls caught, `replay-old-words` new in verify.controls(). It found the brief's control recipe short: a copy of site/ alone cannot build, since the site's own-commit facts need its history. The runtime's figures: 89 tool uses, 2,768,421 ms; its "tokens", 829,030, is the context at the run's end.
- The planted copy, by tools/make_plant.py: `8b397be` on a branch of its own, with P2's message, author, dates and parent; two plants, of kinds the plan names. **The key's SHA-256: `86c2cdf9a47dc0e45d757746f16b951a0b102bfe7590175dcc508ffbb35e2b31`.** The key stays in `<scratch>` until the last planted-copy verifier has reported. The copy's full gate is running.

Decided:
- verifier-P2 is dispatched on Haiku once the copy's gate passes, in a single-branch clone of the copy's branch.

For: verifier-P2, the round's record

## 2026-10-31 08:42:10 -0700 - P1 reported at 7e576fd; its planted copy made, the key's SHA-256 recorded before verifier-P1's dispatch

Measured:
- P1's phase 2: `7e576fd` on r3-P1, parent `6eff67b` (amended once from 9ae1242 before it reported, nothing sent); quick stages clean on its tree (P1.md 08:39:24): 43 files, 2504 figures, numbers 4162 marks, verify-facts 2444 the same; its module's controls 8 caught. Its four departures from the design: issue 1 cited by its date, not its heading ("outside" kept off the page, after the ruling for P2); the live page's "goes on" in the entry's own words; the contract paragraph self-contained; the golden step quoting verify/run.sh, not the Makefile, which SOURCE_PATHS does not list. It also fixed the kept-failure control, which had counted facts.Unavailable as a caught fault. The runtime's figures: 106 tool uses, 2,856,924 ms; its "tokens", 790,699, is the context at the run's end.
- The planted copy, by tools/make_plant.py: `c4c4e9b` on a branch of its own, with P1's message, author, dates and parent; two plants, of kinds the plan names. **The key's SHA-256: `c6050e7cf15136dba746097170c4709ef660e7fe90f684502f8e29b7fcb7f975`.** The key stays in `<scratch>` until the last planted-copy verifier has reported.

Decided:
- P1's four departures stand: each keeps a sentence to its source or the word "outside" off a page.
- The copy's full gate runs once the gate on P2's copy has ended (two gates side by side each take several times as long, trap 19); verifier-P1 is dispatched once it passes.

For: verifier-P1, the round's record

## 2026-10-31 08:50:08 -0700 - P2's planted copy passes the full gate; verifier-P2 dispatched on Haiku; P1's copy's gate started

Measured:
- The full gate on P2's planted copy `8b397be`, run 20261031-084005-8b397be, ending 08:49:51: VERDICT: PASS, nothing skipped; passed 11; numbers 4119 marks; facts 2440 the same; controls 491 caught (490 and P2's replay-old-words), 0 did not fail, 0 skipped. No stage points at a plant. verifier-P2's clone, `<scratch>/r3-verifier-P2/loganw.dev`: one branch, the planted commit on round3's history, P2's own commit not in it, its origin removed.

Decided:
- **verifier-P2** is dispatched now, model requested: haiku, described "R3 verifier-P2: ...". Its brief: `briefs/verifier-P2.md`; its scratch `<scratch>/r3-verifier-P2/`. It reads P2.md only after it reports.
- The full gate on P1's planted copy `c4c4e9b` starts now, alone among gates; verifier-P1 is dispatched once it passes. verifier-P2 and verifier-P3 run no gate.

For: verifier-P2, verifier-P1, the round's record

## 2026-10-31 08:50:53 -0700 - verifier-P2's test escalation

Measured:
- The line "verifier-P2: test escalation" reached the lead through the runtime's agent messages, addressed to "main".

For: the round's record

## 2026-10-31 08:53:04 -0700 - verifier-P2's note on keys/: the directory is empty

Measured:
- verifier-P2 noted that the ledger holds a keys entry and did not open it. `keys/` is a directory the lead made when it set the ledger up, for the keys' archive at the round's end, and it holds no file (`find keys -type f`: 0). The three keys are outside the ledger, in `<scratch>`, as the README says, until the last planted-copy verifier has reported; only their SHA-256s are here.

For: verifier-P1, verifier-P2, verifier-P3

## 2026-10-31 08:58:09 -0700 - a ruling on verifier-P3's question: a planted-copy verifier's findings stay out of this ledger until the last one has reported

Measured:
- verifier-P3 asked (its file, 08:57:43) whether its report, which describes faults in P3's copy, may go into the ledger now, while verifier-P2 is reading and verifier-P1 is not yet dispatched; its default was to hold it.

Decided:
- **Ruled: hold it.** The README keeps "keys, and any description of their plants" out of the ledger until the last planted-copy verifier has reported. A verifier's findings on a planted copy can describe plants as well as a key can, and verifier-P1 reads the whole directory before it starts. So each planted-copy verifier's report goes to the lead as its final message, and into its own file only after the last one, verifier-P1, has reported. Its file meanwhile says that a report is held, and nothing of what it found.
- This adds to the README's rule, as round 2's case study proposed of a parcel's design (its proposal 2). The round's record names it.

For: verifier-P1, verifier-P2, verifier-P3

## 2026-10-31 09:00:47 -0700 - verifier-P3 has reported, its report held; P1's planted copy passes the full gate; verifier-P1 dispatched on Haiku

Measured:
- verifier-P3 reported to the lead at the end of its first pass. Under the ruling of 08:58:09, the report is held out of this ledger until verifier-P1 has reported, and nothing of it is recorded here. The runtime's figures: 69 tool uses, 1,676,686 ms; its "tokens", 427,174, is the context at the run's end.
- The full gate on P1's planted copy `c4c4e9b`, run 20261031-085012-c4c4e9b, ending 09:00:02: VERDICT: PASS, nothing skipped; numbers 4162 marks; facts 2444 the same; controls 494 caught (490 and P1's 4), 0 did not fail, 0 skipped. No stage points at a plant. verifier-P1's clone, `<scratch>/r3-verifier-P1/loganw.dev`: one branch, the planted commit on round3's history, P1's own commit not in it, its origin removed.

Decided:
- **verifier-P1** is dispatched now, model requested: haiku, described "R3 verifier-P1: ...". Its brief: `briefs/verifier-P1.md`; its scratch `<scratch>/r3-verifier-P1/`. It reads P1.md only after it reports, and holds its report out of this ledger, as the 08:58:09 ruling says.
- The lead's restates arising from the reports held come after verifier-P1 has reported, at the merges.

For: verifier-P1, the round's record

## 2026-10-31 09:09:36 -0700 - P3 merged at dffc6cc and the lead's restates committed at 5ff7379, before verifier-P1's report; the full gate on 5ff7379 started; verifier-P1's test escalation

Measured:
- The line "verifier-P1: test escalation" reached the lead through the runtime's agent messages at 09:01:34, addressed to "main".
- P3's own commit `9d26d4f`, not its planted copy, was merged into round3 at `dffc6cc` (09:01:55), with no conflict. Every author's file in this ledger as it stood then had been read by the lead; the newest entry was verifier-P3's of 08:57:43.
- The lead's restates followed at `5ff7379` (09:05:33): `site/pages/corrections.py` and `site/pages/method.py`, with `public/` rebuilt from them. On its tree the build wrote 43 files with 2477 figures; `--check`, `--numbers` (4075 marks), `--links`, `--local-only`, `--docs` and `--manifest` each found 0 problems; the two pages' controls caught 11 and 11, and one of those 22 is new. What each restate answers stays out of this ledger with the report it answers, under the ruling of 08:58:09.
- The full gate on `5ff7379`, run 20261031-090810-5ff7379, started at 09:08:10, alone among gates. verifier-P1 and verifier-P2 run none.
- The files the three parcels changed, outside `public/`, are disjoint: P1 changed `work_cft_fp256.py`, P2 `verify.py` and `thread_determinism.py`, and P3 `corrections.py` and `method.py`.

Decided:
- **Two departures, recorded here.** The entry of 09:00:47 said the restates would come after verifier-P1 has reported, and ROUND3.md's step 5 runs the full gate after each merge and then the restates. P3 was merged, and its restates committed, while verifier-P1 and verifier-P2 read, and one gate covers the merge and its restates together.
- Why they stand: neither verifier can see either commit. Their clones were cut before both, with origin removed, and neither reads `<repos>/loganw.dev`. P3's files are none that P1 or P2 changed. The cost: if this gate fails, it does not say whether the merge or a restate failed it. In that case the merge's own tree is gated alone before anything else.
- P2 and P1 are merged one at a time after verifier-P1 has reported, each followed by its own full gate and then its restates, as step 5 says.

For: the round's record, the integration verifier

## 2026-10-31 09:16:58 -0700 - verifier-P2 has reported, its report held; the full gate on 5ff7379 passes

Measured:
- verifier-P2 reported to the lead at 09:09:59, at the end of its first pass. Under the ruling of 08:58:09 the report is held out of this ledger until verifier-P1 has reported, and nothing of it is recorded here. The lead has checked each of its findings at its source; those checks are held with it. The runtime's figures: 57 tool uses, 1,177,095 ms; its "tokens", 428,538, is the context at the run's end.
- The full gate on `5ff7379`, run 20261031-090810-5ff7379, ending 09:16:43: VERDICT: PASS, nothing skipped; passed 11; numbers 4075 marks; facts 2417 the same; controls 507 caught (the 490 before the round's parcels, P3's 16 and the lead's 1), 0 did not fail, 0 skipped. The departure of 09:09:36 costs nothing, then: the merge and its restates pass together.

Decided:
- P2 is merged next, once verifier-P1 has reported, then P1, each with its own full gate and then its restates.

For: the round's record

## 2026-10-31 09:20:08 -0700 - verifier-P3 resumed for its second pass, on 5ff7379, its report held as before

Measured:
- The lead fetched round3 into verifier-P3's clone as a second branch, `pass2`, at `5ff7379`, and checked it out; `r3-P3-1` stays at `9bef3c6`. In the clone's `site/`, `git diff 9bef3c6 5ff7379` touches `site/pages/corrections.py` and `site/pages/method.py` only.

Decided:
- **verifier-P3's second pass**, resumed by message (the brief's "You may be resumed"), is scoped to that diff and its two pages, and runs no gate. Its report comes to the lead as its final message and stays out of this ledger with the first, under the ruling of 08:58:09, until verifier-P1 has reported.

For: verifier-P3, the round's record

## 2026-10-31 09:26:22 -0700 - verifier-P1 has reported and the hold lifts; the keys are filed, each matching its recorded SHA-256; the plants' yield is 5 of 6; the lead's checks of the three first reports

Measured:
- verifier-P1 reported to the lead at 09:21:33, at the end of its first pass: NOT READY. The runtime's figures: 59 tool uses, 1,235,532 ms; its "tokens", 433,129, is the context at the run's end. It was the last planted-copy verifier, so the hold of 08:58:09 lifts.
- The keys, moved from `<scratch>`, are in `keys/`: `key-P1.json`, `key-P2.json` and `key-P3.json`. Each one's SHA-256 is the one this file recorded before its verifier was dispatched, in the entries of 08:20:59, 08:40:08 and 08:42:10.
- The plants, from the keys, against the reports:
  - P3's copy `9bef3c6`. First, Corrections' caption names cft-fp256's CONFORMANCE.md as the source of issue 1's row, whose cells are read from docs/VALIDATION.md. Second, Method says muse-softfloat's commits were "each written by Muse alone". verifier-P3 caught both (its items 2 and 5).
  - P2's copy `8b397be`. First, the Determinism thread says muse-softfloat's docs/RECORD.md records the report on the audit, which only cft-fp256's ledger records. Second, Verify says the browser module is "rebuilt with every change to the library", in the sentence that quotes the entry saying it was stale from 2026-10-22. verifier-P2 caught the first (its D1) and passed the second. Its item 3 calls "Rebuilt with every change" supported by bindings/wasm/README.md's "as every change to its sources requires", which says what a change requires, not that it was done.
  - P1's copy `c4c4e9b`. First, the contract paragraph says issue 1's fix "left every published record as it was", beside the entry's "those 8 records are the published ones moving". Second, the nightly paragraph calls night 10's totals "the campaign's final figures", where the record says the sweep goes on. verifier-P1 caught both (its D1 and D2).
  - **Yield: 5 of 6.** Every plant was of a kind no gate reads: the words around a quote.
- The lead checked each finding at its source before acting on it (decision 35). Below are the reports' real findings, the ones on what the parcels themselves wrote, as checked:
  - **verifier-P3, pass 1:** restates, all taken in `5ff7379` (entry of 09:09:36) except two. Item 9's first known limit and the copy's branch name go to the side-notes step.
  - **verifier-P2, pass 1:**
    - D2 holds. Verify gives the runner's golden-stage timing as `make golden`'s cost. `make golden` adds pytest-xdist workers (cft-fp256's Makefile:20, :22, :26 and :112 at 19de866); the runner's stage (verify/run.sh:639) adds none. The page cannot say so while the Makefile is no listed source path.
    - R1 holds. The nightly item sits in the list headed "What cft-fp256's own documents say their checks do not reach", and no document says it. Its words are the plan's own (ROUND3.md:413).
    - R2 holds. "report" is printed on the thread, so "no word of the heading's subject" is false; "outside" is not printed.
    - R3 partly holds. docs/VERIFICATION.md dates its own gate figure. CLAUDE.md's two budget lines, last written in 2124cc00 (2026-09-12, `git log -S`), name no machine and no date.
    - R4 holds. Verify's budget quote holds sentences, "382 s against 346 s" and "about ten minutes in WSL since 2026-10-22" among them, that no file has at ab51655 (`git grep` at both pins).
    - R5 is a gloss its sources do not contradict.
    - R6 is on lines P2 did not change; it goes to the side-notes step. The module docstring's source list omits verify/run.sh.
    - The verifier left the replay comment's "lapsed once" undetermined. The lead checked it: the record also shows a stale module in its ABI 0.12 entry (VALIDATION.md, about 10925 to 10952), so a count is not what it holds.
  - **verifier-P1, pass 1:**
    - D3 holds. nightly() takes the first key of the name after its parent's, so a same-named key with the same value in a sibling object would be cited in its place; the docstring says that never happens. At the pin each citation is right.
    - D4 holds and predates P1: Provenance omits vectors/SHA256SUMS and docs/COMPATIBILITY.md, which the page reads through facts.exists.
    - D5 holds: the entry records four known limits, and "Prove it wrong" quotes one.
    - D6 holds. The Verified rows end on 2026-10-20, and the record holds later verification entries (2026-10-26, 10-27 and 10-29). So "the verification events the record holds after 2026-10-06" overclaims. P1's design called the selection editorial (P1.md 07:17:44).
    - Its side notes hold:
      - "outside" is printed on the dossier, in 2026-10-20's heading ("three outside test sources");
      - "no file at the pin says so" holds for issue 1 only (docs/COMPATIBILITY.md:1002, docs/ROADMAP.md:6446);
      - "never says now" holds in the page's own voice;
      - kept_failure checks ancestry only;
      - the nightly totals are one run's nights, which the page does not say.
- verifier-P2's floor. At its three moments it read README.md, lead.md, verifier-P1.md and verifier-P3.md whole, and only grepped P1.md, P3.md, verifier-P0.md and verifier-plan.md (its report says so). The rulings are in lead.md, which it read whole, so its findings stand. The README's floor was not met.

Decided:
- The hold has lifted. Each verifier appends its own reports to its own file: verifier-P3 at the end of its second pass, as the lead's message told it, and verifier-P2 and verifier-P1 when each is resumed for its second. Until then, the lead's verbatim copies of the three first reports stay in `<scratch>`.
- P2's restates, after its merge and that merge's gate:
  - D2: `Makefile` goes into build.SOURCE_PATHS, and Verify quotes `make golden`'s own line;
  - R1: the nightly item comes out of that list and is said in the site's voice;
  - R2, R3, R5, the replay comment and the docstring's sources are restated;
  - R4 is answered in the restates' commit message.
- P1's restates, after its merge and that merge's gate:
  - D3's docstring is restated as a stated limit, and D4's two paths are listed;
  - D5, D6, and the side notes' "outside", "for issue 1" and "now" are restated.
- The `make golden` step on P1's page stands: verifier-P1 confirmed it, and it already calls the timing the runner's stage's.

For: verifier-P1, verifier-P2, verifier-P3, the round's record

## 2026-10-31 09:26:22 -0700 - corrections to this file, held until now with the reports they rest on

Measured:
- **Correcting 07:05:22.** That entry said "No page may say the profile stepped, since no file at the pin says so". That is false as written. At 19de866, docs/COMPATIBILITY.md:1002 says "The profile steps from 3 to 3.1, a minor step", and docs/ROADMAP.md:6446 says "the profile stepped to 3.1". The narrower claim holds: no file at the pin records a profile step for issue 1's fix. The rule for pages stands in that form. P3's comments were restated in `5ff7379`, and P1's is restated at its merge. The lead carried the same words into the parcels' briefs.
- **Correcting 07:39:53.** That entry recorded under Measured that "Every quote on Verify and the Determinism thread has the same words at both pins but CLAUDE.md:9-10's counts". That is false. P0 requoted the gate budget whole at 19de866, and the requoted text holds sentences ab51655 does not have. The lead recorded the design's claim without checking it.
- **Qualifying 07:39:53.** The lead's question to Logan for decision 56 said "Both of cft-fp256's own budget figures date from September". That is true of when the lines were written: VERIFICATION.md's in 74016c94 (2026-09-07) and CLAUDE.md's in 2124cc00 (2026-09-12). Neither CLAUDE.md line says when or where it was measured. Decision 56's words, "where and when that was measured where a source says", already cover that.
- **A slip.** The lead's message telling verifier-P3 that the hold had lifted gave verifier-P1's report a typed time, 09:25. It came at 09:21:33, and a second message corrected it.

For: the round's record, the integration verifier

## 2026-10-31 09:32:59 -0700 - P2 merged at e6665a2, its full gate running; verifier-P3's second pass, NOT READY on two wording points, each checked at its source

Measured:
- **P2 merged.** Before the merge, the lead read every author's file in this ledger; the entries new since its last reading were verifier-P1's three and verifier-P3's of 09:21:13. P2's own commit `2cbcc82`, not its planted copy, was merged into round3 at `e6665a2` (09:28). Its only conflicts were in `public/`, 18 files of fact numbers and of the pages both sides changed, and they were resolved by rebuilding, never by merging the text (CLAUDE.md trap 7).
  - The rebuilt tree: 43 files from 23 pins, 2509 figures.
  - `--check`, `--numbers` (4137 marks), `--links`, `--local-only`, `--docs` and `--manifest` each found 0 problems.
- **The merge's gate.** Its full gate, run 20261031-092848-e6665a2, started at 09:28:46.
  - A slip: the lead started it with the shell's `&` inside a foreground call, not as a tracked background run, so the runtime would not have said when it ends.
  - The run is alive (its bash and Python processes date from 09:28:46). A tracked background watcher waits for its "end" line.
- **verifier-P3's second pass.** It reported at 09:31:38: NOT READY. Both of pass 1's defects are fixed, and no restate broke what pass 1 confirmed. Its two reports are in its own file (09:30:35 and 09:31:22). The runtime's figures for the pass: 20 tool uses, 696,565 ms; its "tokens", 542,836, is the context at the pass's end.
- The lead checked both of its points at their sources:
  - **First point: holds.** `5ff7379`'s comment on `_NAME_BEFORE_ADDRESS` says an address "spelled another way" is the local-only stage's to refuse, and its message says "spelled any other way". CLAUDE.md trap 14 lists "an address spelled out for a person to reassemble" among what that stage cannot see, so the claim is too wide. `one_muse_name`'s docstring, which names only the ASCII "@", is right.
  - **Second point: holds.** P3's `9d26d4f` message says "Every cell is read from the one entry headed ...". `5ff7379`'s message called P3's message standing as written, and did not weigh this sentence.
- A slip in the lead's message for the pass: it named the two pages' ".txt twins", and Corrections and Method have none.

Decided:
- Both restates go into a commit of their own once the merge's gate has ended, followed by P2's restates in another, so that each verifier's next pass is scoped to its own files.
- **verifier-P3's third pass**, its last, is scoped to that commit. If it still finds a wrong answer, the lead records it and asks Logan before going on (ROUND3.md, "What READY means").

For: verifier-P3, the round's record, the integration verifier

## 2026-10-31 09:46:52 -0700 - P2's merge gate passes; the restates at c301dcd and e03b3bc; P1 merged at 775bf59, its gate running; verifier-P3's third pass and verifier-P2's second dispatched

Measured:
- **P2's merge gate.** The full gate on `e6665a2`, run 20261031-092848-e6665a2, ended at 09:39:38: VERDICT: PASS, nothing skipped; passed 11; numbers 4137 marks; facts 2449 the same; controls 508 caught (507 and P2's 1), 0 did not fail, 0 skipped.
- **`c301dcd` (09:41:10), the restates for verifier-P3's second pass.** It changes method.py's comment on `_NAME_BEFORE_ADDRESS` and `public/MANIFEST`, whose source hashes moved with it. Its message also weighs P3's "every cell is read". On its tree `--check`, `--docs` and `--manifest` found 0 problems; no published page changed.
- **`e03b3bc` (09:43:24), P2's restates**, as the entry of 09:26:22 decided: `Makefile` in build.SOURCE_PATHS; verify.py and thread_determinism.py; `public/` rebuilt.
  - On its tree: 43 files, 2511 figures.
  - `--check`, `--numbers` (4141 marks), `--links`, `--local-only`, `--docs` and `--manifest` each found 0 problems.
  - Verify's, the thread's and Method's controls, run in-process: 13 of 13 caught. The thread page has none of its own.
  - The rendered sentences, read as text: `make golden` "itself runs" its Makefile line (Makefile:112), "which adds pytest-xdist's workers" "only if this interpreter has it" (Makefile:22). The nightly sentence follows the list: "The card's nightly stress run is none of the checks above."
- **P1 merged.** Before the merge the lead read every author's file. The new entries were verifier-P3's filed reports, of 09:30:35 and 09:31:22. P1's own commit `7e576fd`, not its planted copy, was merged at `775bf59` (09:45:43).
  - Its only conflicts were in `public/`, and they were resolved by rebuilding.
  - On the rebuilt tree: 43 files and 2547 figures, which is 2511 and P1's 36.
  - `--check`, `--numbers` (4246 marks), `--links`, `--local-only`, `--docs` and `--manifest` each found 0 problems.
- **P1's merge gate.** Its full gate, run 20261031-094550-775bf59, started at 09:45:49 as a tracked background run.
- **verifier-P3's filed first report is not verbatim.** Its entry of 09:30:35 says "verbatim as sent". A word diff against the lead's copy of the message finds 12 small differences: words added in two places, one restate line added in item 8, and a clause reworded in item 7. The lead finds that none changes a finding.

Decided:
- **verifier-P3's third and last pass** is scoped to `git diff 5ff7379 c301dcd`, on a branch `pass3` at `c301dcd` in its clone. It also appends an entry correcting its 09:30:35 one. If the pass still finds a wrong answer, the lead records it and asks Logan before going on.
- **verifier-P2's second pass** is scoped to its two pages and build.py's one line, `git diff 8b397be e03b3bc`, on a branch `pass2` at `e03b3bc` in its clone.
  - First, it files its first report by copying it by command from the lead's copy, not by retyping it.
  - It may now read its key and P2.md, and it says in its file what let the plant it passed go by.
- P1's restates come after P1's merge gate, and then verifier-P1's second pass.
- Neither verifier runs a gate. The lead's gate on `775bf59` is the only one running.

For: verifier-P2, verifier-P3, the round's record, the integration verifier

## 2026-10-31 09:54:20 -0700 - verifier-P3's third pass: READY; the reports as sent, read exactly from the lead's transcript; a slip in the third pass's scope

Measured:
- verifier-P3 reported its third pass, its last, at 09:52:30: READY. Both of pass 2's points hold against their sources, and the restate is comment-only (method.py's syntax trees are equal at `e6665a2` and `c301dcd`). The runtime's figures for the pass: 16 tool uses, 354,522 ms; its "tokens", 615,628, is the context at the pass's end.
- **A slip in the lead's message for that pass.** It scoped the pass to `git diff 5ff7379 c301dcd` and said that diff touches method.py and MANIFEST. It touches 21 files, since `c301dcd`'s parent is P2's merge `e6665a2`. The restate is `e6665a2..c301dcd`. The verifier found this and checked the restate alone.
- **Every report as sent, now read exactly.** The runtime records each task notification in the lead's transcript. A script, `<scratch>/r3-extract-reports.py`, reads each one's result with only the runtime's escaping undone, one file per notification, into `<scratch>/r3-held/exact/`. Against those files, by a word diff:
  - the lead's held copies of verifier-P2's and verifier-P1's first reports are word for word what each sent;
  - the lead's copy of verifier-P3's first report is word for word the report, without the 41-word line before it ("The lead's ruling is at 08:58:09 ... Here is the report as my final message.");
  - verifier-P3's own entries: its correction of 09:52:21 lists the 12 differences of its 09:30:35 entry, as the lead counted them. Its 09:31:22 entry, the second report, differs from the message as sent in three small places: "once this" for "now that", and "pass 1" for "pass 1 and pass 2", in one sentence on a citation. It also drops the message's closing line on the ledger. Its pass-3 entry is the message word for word, but its first line.
  - None of these differences changes a finding.

Decided:
- verifier-P3 is done: READY on its third pass. Its two notes, on Corrections' section III header (the signature row's typed words are excepted only by the next sentence) and on `check_row_words`' "other words", go to the side-notes step with the rest.
- The exact copies stay in `<scratch>/r3-held/exact/` until the round's end, when the lead asks Logan where the ledger is archived. verifier-P2 files its first report from the lead's copy, which is word for word what it sent.

For: the round's record, the integration verifier

## 2026-10-31 10:00:36 -0700 - P1's merge gate passes; P1's restates at cbb78e0 and verifier-P1's second pass; verifier-P2's second pass, NOT READY on two errors in the lead's restates, answered at 2bfafe1; verifier-P2's third pass

Measured:
- **P1's merge gate.** The full gate on `775bf59`, run 20261031-094550-775bf59, ended at 09:55:23: VERDICT: PASS, nothing skipped; passed 11; numbers 4246 marks; facts 2487 the same; controls 512 caught (508 and P1's 4), 0 did not fail, 0 skipped.
- **`cbb78e0` (09:57:06), P1's restates**, as the entry of 09:26:22 decided. Before applying them, the lead checked that the checkout's work_cft_fp256.py was still P1's own.
  - On its tree: 43 files, 2549 figures (the two new Provenance paths).
  - `--check`, `--numbers` (4252 marks), `--links`, `--local-only`, `--docs` and `--manifest` each found 0 problems.
  - The dossier's 8 controls, run in-process: 8 of 8 caught.
  - Provenance renders eight files, docs/COMPATIBILITY.md and vectors/SHA256SUMS among them.
- **verifier-P1's second pass** is dispatched by message, scoped to `git diff c4c4e9b cbb78e0 -- site/pages/work_cft_fp256.py` and its two rendered files, on a branch `pass2` at `cbb78e0`. It first files its first report, copied by command from the lead's copy without the lead's two note lines.
- **verifier-P2's second pass** reported at 09:57:16: NOT READY, on two errors in the lead's restates; the rendered pages carry neither. It also says what let the plant it passed go by: it took the wasm README's standing rule, "as every change to its sources requires", as the module's history, without testing it against the lapse the same sentence quotes. The runtime's figures for the pass: 20 tool uses, 631,251 ms; its "tokens", 556,317, is the context at the pass's end. The lead checked both errors at their sources:
  - **The date: holds.** `e03b3bc`'s docstring said CLAUDE.md's two budget lines "were last written on 2026-09-12". `git log -L9,10:CLAUDE.md` and `git blame` at 19de866 show them last changed on 2026-10-22, in `f59b0adc`. The lead had used `git log -S`, which finds only the commits that change how often a string occurs. Every change to the lines since 2026-09-12 moved their stage counts. Their time figures, "~20 min" and "~2 h quiet", have not changed since `2124cc00`: the quick budget's "~20 min" was written when it chose 24 of 37 stages, and it chooses 31 of 53 at the pin.
  - **The attribution: holds.** `e03b3bc`'s message called the nightly item's words "the plan's own phrase (ROUND3.md)". ROUND3.md:413 has "a record a reader can look at rather than a check to run", and P2 put that idea in its own words.
- **`2bfafe1` (10:00:06)** restates the docstring, with `public/MANIFEST`; no rendered page changes. On its tree `--check`, `--docs` and `--manifest` found 0 problems. Its message corrects `e03b3bc`'s record:
  - the attribution;
  - "as both READMEs do", which was loose;
  - "stands as written" in three of the lead's messages, which means the message is left unamended, not that its claims hold.
- It also answers the pass's two other notes:
  - the cost of `make golden` does not call the timing one process's, since box_m2f2.sh is not in the repository at 19de866;
  - the nightly sentence keeps the `cap` style that the section's other sentences in the site's words use.
- **verifier-P2's third and last pass** is dispatched, scoped to `git diff cbb78e0 2bfafe1`, on a branch `pass3` at `2bfafe1`. It also corrects its 09:48:32 entry, whose last line is the lead's note of the runtime's figures. The lead's instruction to copy "from its line 3" carried that line in.

Corrections:
- **Correcting 09:26:22.** It said CLAUDE.md's two budget lines were "last written in 2124cc00 (2026-09-12, `git log -S`)", as above. Their time figures were written then, and the lines were last changed on 2026-10-22.
- **Correcting 09:26:22.** It said the nightly item's words "are the plan's own (ROUND3.md:413)". The plan's words differ, as above.
- **Narrowing the qualification of 07:39:53 (in the entry of 09:26:22).** "CLAUDE.md's in 2124cc00 (2026-09-12)" holds of the lines' time figures, not of the lines.
- **Correcting 09:54:20.** It described a difference in verifier-P3's 09:31:22 entry from a word diff, and the description is wrong. The entry has "once this pass and pass 1 are in", where the message has "now that pass 1 and pass 2 are in".
- **A slip.** The lead told verifier-P2 to copy its report "from its line 3", which carried the lead's own last line into verifier-P2's entry. verifier-P1's instruction excludes it.

For: verifier-P1, verifier-P2, the round's record, the integration verifier

## 2026-10-31 10:07:15 -0700 - verifier-P2's third pass: READY; it withdraws its second pass's attribution point; corrections to the lead's question for decision 56

Measured:
- verifier-P2 reported its third pass, its last, at 10:07:00: READY. Send-back 1 is fixed. `git log -L9,10:CLAUDE.md` gives 16 versions of the two lines from `2124cc00` to `f59b0adc`: the time figures are the same in all of them, and the counts change in every one. The message's claims hold. The runtime's figures for the pass: 12 tool uses, 391,695 ms; its "tokens", 627,740, is the context at the pass's end.
- It withdraws its second pass's send-back 2 in its own file (10:06:37). It had searched the plan for the unwrapped words, and ROUND3.md wraps them across lines 413 and 414: "a record a reader can look at rather than a check to" / "run;". The lead had already checked those lines when it took that point. It took the point as one about wording, since P2's words differ from the plan's, and corrected `e03b3bc`'s record to say so in `2bfafe1`. Both readings agree: the idea is the plan's and the words are P2's.
- It corrects its 09:48:32 entry in its own file (10:06:36): that entry's last line is the lead's note, not its words.
- It also notes that VALIDATION.md:26125 at the pin records the runner command for the gate run whose golden line Verify quotes. So `2bfafe1`'s "no file at the pin shows how the box ran it" holds of the box's script, and not of the run as a whole; the message's colon names box_m2f2.sh. No page claims either.

Decided:
- verifier-P2 is done: READY on its third pass. Its side notes (cardstress beside the nightly sentence, R6 and propose.py's control) go to the side-notes step.

Corrections:
- **Correcting 07:39:53.** The lead's question to Logan for decision 56 called the 3,385 s "one worker, 5,951 tests". The record's line is "golden ok 3,385 s, 5,951 passed and 3 skipped". No file at the pin says how many workers ran it, and the runner's line names no worker option. P2 said so in its report (P2.md 08:38:05), and the lead did not record it until now. Decision 56 rests on neither figure: it rests on the ranking.

For: verifier-P2, the round's record, the integration verifier

## 2026-10-31 10:10:10 -0700 - two slips of the lead's that this file had not recorded

Measured:
- **`2cbb7e7`'s message**, the resume's item for decision 55, first gave the two-item layout's height as 41 pt, where the printout's own measure gave 43. The commit was amended at 06:13:11 (`git reflog`: "commit (amend)"), before it went to any verifier or remote.
- **A message to verifier-P0**, on its scoped check of the seam commit, called the lead's own point a side note of verifier-P0's earlier pass: the point that SPEC's round-3 preface gave no stamp for the tenth answer. A second message, about 07:41:45, corrected it: verifier-P0's R1 had been about decision 55's later answers. verifier-P0's report of 07:49:37 judged the stamp on its merits.

For: the round's record, the integration verifier

## 2026-10-31 10:13:42 -0700 - verifier-P1's second pass: NOT READY on the Verified list; answered at ffdcbb1; its third pass dispatched

Measured:
- verifier-P1 reported its second pass at 10:10:28: NOT READY. It filed its first report at 10:00:13, byte-identical to lines 3 to 89 of the lead's copy, and this report at 10:10:13. The runtime's figures for the pass: 29 tool uses, 715,060 ms; its "tokens", 600,637, is the context at the pass's end.
- Every restate holds but one, R7 (cbb78e0's comment on Verified), and none breaks a first-pass confirmation. Its own finding sends the work back. The lead checked both at their sources:
  - **R7 holds.** The comment called the round's four rows "the ones P1's brief named". briefs/P1.md (lines 10 to 15) names milestones, not rows, and one of them has no row: "the math library's routines, built golden-first, to sin, cos and tan at all four formats". The comment's later dates also missed 2026-10-28 and 2026-10-30. The lead had taken the claim from P1's design ("they are the verification events the brief names", P1.md 07:17:44) without checking it against the brief.
  - **The finding holds.** The Verified rows ended on 2026-10-20 under "Last verified: 2026-10-30". That is the trap the brief names (lines 75 and 76), "'Verified' rows that end at 2026-10-06 pass every gate", at a later date. The record's entries after 2026-10-20, listed from its headings at 19de866, include 24164, 25104, 25753 and 26082, each a verification event. 26082 is the entry in which "sin, cos and tan are built at all four formats".
- **`ffdcbb1` (10:13:23)** adds those four rows, each its entry's heading whole, and restates the comment.
  - On its tree: 43 files, 2553 figures.
  - `--check`, `--numbers` (4264 marks), `--links`, `--local-only`, `--docs` and `--manifest` each found 0 problems.
  - The dossier's 8 controls caught 8 of 8 in-process.
  - The rendered list ends on 2026-10-30.

Decided:
- **verifier-P1's third and last pass** is scoped to `git diff cbb78e0 ffdcbb1 -- site/pages/work_cft_fp256.py` and its two rendered files, on a branch `pass3` at `ffdcbb1`. If it still finds a wrong answer, the lead records it and asks Logan before going on.
- Its side notes go to the side-notes step with the rest. Two paths, docs/COMPATIBILITY.md and vectors/SHA256SUMS, are not in build.SOURCE_PATHS, and the build takes them because an `exists()` label names no path.

For: verifier-P1, the round's record, the integration verifier

## 2026-10-31 10:14:15 -0700 - the side-notes step (ROUND3.md, step 6): each verifier's side note, and what the lead does with it

Measured:
- The side notes are those of verifier-P3's three passes, verifier-P2's three and verifier-P1's first two. Its third may add more, which an entry after it answers.

Decided:
- **Taken in the round:**
  - The dossier's Verified rows ran to 2026-10-20 under "Last verified: 2026-10-30" (verifier-P1's second pass). `ffdcbb1` adds the record's four later verifying entries.
- **For Logan's call.** Each is a choice of what a page says, and each page says now only what its source holds:
  - issue 1's first known limit, "the gate ran on the desktop, not on the box", which neither Corrections (whose row says "among its known limits") nor the dossier quotes (verifier-P3, verifier-P1);
  - the dossiers' shared opening "Cheapest first;" over their attack lists. It is the spec's own wording (SPEC.md:41), and decision 56 dropped the ranking from Verify alone (verifier-P1);
  - the Determinism thread's budget figures, "~20 min" and "~2 h quiet", which are CLAUDE.md's own and labelled so, and name no machine or date (verifier-P2's R6);
  - Verify's `cardstress` stage, listed just above the sentence that the card's nightly run is none of the checks; a clause to tell them apart would need a source to say it (verifier-P2).
- **Left as they read, with the reason:**
  - The section III header in corrections.py names Logan's signature words as typed in its next sentence (verifier-P3).
  - `check_row_words`' "other words" covers invisible and look-alike spellings; the docstring calls the check lexical (verifier-P3).
  - The Muse name prints with its label inside its quotation marks, and "185/185" reads as a fraction: the site's figure style, as the Gemini sentence already shows (verifier-P3).
  - The newest golden timing is the newest one stated; the desktop gate of 2026-10-30 states none (verifier-P1).
  - The dossier's nightly paragraph gives the data file's totals, and the long run's row gives that run's own figures. The page does not say that the totals leave out that run (verifier-P1).
  - docs/COMPATIBILITY.md and vectors/SHA256SUMS are read through `exists()`, whose label names no path, so build.SOURCE_PATHS does not list them (verifier-P1).
- **Known limits,** for the site's ledger entry:
  - `_dossier.kept_failure` checks that a commit exists and the pin descends from it, not that it is the fix (verifier-P1);
  - an entry of another repository's ledger, cited by its line, would be re-pointed silently if a pin's move put another heading on that line (verifier-P1).
- **Not round 3's:**
  - propose.py's control, which passes whenever "workloads" is in the door's text, is close to a tautology (verifier-P2). It goes to a later round.
- **For the method:**
  - make_plant.py names a copy's branch for its parcel (`r3-P3-1`); a neutral name would tell a verifier nothing (verifier-P3).
  - _verifier.md's "Read everything again before you write your report" meets the rule that a planted-copy verifier opens its parcel's file only after reporting; a brief should name the files it means (verifier-P1).
  - A verifier that files its report by retyping it changes it, by 12 small differences in verifier-P3's case. The report as sent should be copied by command, from the runtime's own record.
  - A resumed pass's range should start at the restate commit's parent, not at the verifier's previous commit, wherever a merge falls between them.
  - verifier-P2 did not read four files whole at its three moments (README's floor).

For: the round's record, Logan

## 2026-10-31 10:15:29 -0700 - a correction to the 09:26:22 entry's correction of 07:05:22: the profile claim reached the parcels by message and by this file, not by their briefs

Measured:
- The 09:26:22 entry says of the 07:05:22 claim, "No page may say the profile stepped, since no file at the pin says so": "The lead carried the same words into the parcels' briefs." That is false. No brief holds them (`grep` over `briefs/`). The briefs were written before 07:05:22.
- The words reached the parcels in two ways:
  - the 07:05:22 entry itself, which every parcel reads;
  - the lead's message to P3 at about 07:05:27, from the runtime's record of the lead's messages: "No file at the pin says the profile stepped."
- P1's and P3's comments, and P3's commit message, carried the words from there. Both comments are restated: P3's in `5ff7379`, P1's in `cbb78e0`.

For: the round's record, the integration verifier

## 2026-10-31 10:24:41 -0700 - verifier-P1's third pass: READY, with one comment to restate, done at 4bcc3d0; the full gate on 4bcc3d0 running

Measured:
- verifier-P1 reported its third pass, its last, at 10:21:43: READY. Its report is in its own file, at 10:21:31. The runtime's figures for the pass: 10 tool uses, 486,695 ms; its "tokens", 707,094, is the context at the pass's end.
- All eight Verified rows equal the plain text of their headings at 19de866, and each links to its heading's line. Nothing its earlier passes confirmed broke.
- One comment sentence is wrong, its S2: the record's other entries in the span are "on tools, studies and nights". The lead checked it: they include other gate runs, the math library's other routines and issue 1.
  - The lead's own count, from the dated headings at 19de866 (`grep -E '^## 2026-1[0-9]-[0-9]{2}'`), is 90 after 2026-10-06, so 82 besides the eight.
  - The verifier counts 88 dated headings from 2026-10-12 and 80 besides the eight. The two counts differ by two, and the comment gives the lead's, with the command.
- **`4bcc3d0` (10:24:22)** restates the comment; no rendered page changes. On its tree `--check`, `--docs` and `--manifest` found 0 problems. Its message also says that `ffdcbb1`'s "the record's four later verifying entries" are four of them, not all, as the verifier's side note says.
- Its new side note is for Logan's notes on cft-fp256: README.md:436-439 at the pin still calls sin, cos and tan "the next build", against the record's entries of 2026-10-26 to 10-30. The dossier does not quote that passage.
- **The full gate on `4bcc3d0`**, run 20261031-102436-4bcc3d0, started at 10:24:35, tracked, alone among gates.

Decided:
- All three planted-copy verifiers are READY, each on its third pass: verifier-P3 at 09:52:30, verifier-P2 at 10:07:00 and verifier-P1 at 10:21:43. No pass found a wrong answer that is left standing, so nothing goes to Logan under the three-pass rule.
- Next, the round's entry in docs/VALIDATION.md, given this gate's figures. Then the full gate on that commit, and the integration verifier on the lead's work.

For: verifier-P1, the round's record, the integration verifier

## 2026-10-31 10:35:24 -0700 - the gate on 4bcc3d0 passes; the round's entry in docs/VALIDATION.md at 33dc465, its gate running; verifier-I dispatched on Haiku

Measured:
- **The gate on `4bcc3d0`.** The full gate, run 20261031-102436-4bcc3d0, ended at 10:32:47: VERDICT: PASS, nothing skipped; passed 11; numbers 4264 marks; facts 2493 the same; controls 512 caught, 0 did not fail, 0 skipped.
- **The round's entry, `33dc465` (10:34:37).** docs/VALIDATION.md gains the entry headed "2026-10-31 - round 3: ...". It records:
  - the push of 797f588 and its deploy, read from the resume work's ledger (its entries of 08:42:10 to 08:59:54, 2026-10-16), and the cleanup (its entry of 04:26:59);
  - what Logan asked for, and what moved and changed;
  - the one correction to what the site had published;
  - what verified it, its limits and the lead's slips;
  - the cost table, from `tools/round_metrics.py` with the window 04:22:42 to 10:24:41;
  - what is left with Logan.
- On its tree: 43 files, 2553 figures. `--check`, `--numbers` (4264 marks), `--links`, `--local-only`, `--docs` and `--manifest` each found 0 problems. No page's own reading of the ledger was refused, and Method's figure for the newest entry's controls now reads "512 of 512", from this entry.
- **Its gate.** The full gate on `33dc465`, run 20261031-103446-33dc465, started at 10:34:45, tracked.
- **verifier-I's clone.** `<scratch>/r3-verifier-I/loganw.dev`: a clone of loganw.dev on `round3` at `33dc465`, its one branch, with origin removed and the site's `.cache/` copied in.

Decided:
- **verifier-I** is dispatched now, model requested: haiku, described "R3 verifier-I: ...", on the brief `briefs/verifier-I.md`: the lead's merges, restates and records from `6eff67b` to `33dc465`. It runs its own full gate only after the lead's message that the lead's gate has ended.
- Main moves to round3's tip only after both gates pass and verifier-I is READY. It is pushed only at Logan's word.

For: verifier-I, the round's record

## 2026-10-31 10:35:53 -0700 - verifier-I's test escalation

Measured:
- The line "verifier-I: test escalation" reached the lead through the runtime's agent messages at 10:35:37, addressed to "main".

For: the round's record

## 2026-10-31 10:43:20 -0700 - the full gate on 33dc465 passes; verifier-I told it may run its own

Measured:
- The full gate on `33dc465`, run 20261031-103446-33dc465, ended at 10:42:41: VERDICT: PASS, nothing skipped; passed 11; numbers 4264 marks; facts 2493 the same; controls 512 caught, 0 did not fail, 0 skipped.

Decided:
- verifier-I is told that the lead's gate has ended and that it may run its own. The lead starts no gate until verifier-I reports.

For: verifier-I, the round's record

## 2026-10-31 10:43:03 -0700 - a correction to the entry headed 10:43:20: its time was typed, not read

Measured:
- The entry headed "2026-10-31 10:43:20 -0700 - the full gate on 33dc465 passes; ..." carries a time the lead typed before reading the clock. It was appended at about 10:42:55, the time `date` printed just after the append, so its heading is later than the moment it was written. Its content stands.

For: the round's record, the integration verifier

## 2026-10-31 11:01:55 -0700 - verifier-I's first pass: NOT READY on one figure in the round's entry; answered by a new entry at 6b712df; its gate running; verifier-I's second pass

Measured:
- verifier-I reported at 10:58:24: NOT READY, on one figure in the round's entry (its item 4). Its items 1 to 3 and 5 to 7 are confirmed:
  - the three merges made again, with no path lost and `--check` passing at each;
  - no plant on `round3`, but the one the entry quotes in telling of it;
  - each restate at its source;
  - the push and cleanup account, every other figure, the cost table run again row for row, and SPEC's decisions 47 to 56 word for word;
  - the pages together, where no sentence is made false;
  - its own full gate on `33dc465`, run 20261031-104305-33dc465: VERDICT: PASS, nothing skipped; controls 512 caught.
  The runtime's figures: 83 tool uses, 1,383,929 ms; its "tokens", 447,010, is the context at the run's end.
- The runtime refused verifier-I a report file, so its file holds a short entry with the finding (10:58:05), and its message is the report. The lead's exact copy of that message, read from the runtime's record by `<scratch>/r3-extract-reports.py`, is `<scratch>/r3-held/exact/a76111680b469cb21-1.md`.
- The lead checked each point at its source:
  - **The figure: holds.** The entry cites "36 of 44 stages" to VALIDATION.md:20886, :21353, :21762 and :22643 at cft-fp256's pin. The minutes and the 36 are there, and the 44 is at :21354: "36 and 8 make the budget's 44". P2's F1 (P2.md) cited :21354 and :21763 for the stage counts, and the lead dropped :21354 when it wrote the sentence.
  - **"the build box": holds** as a naming point. VALIDATION.md:26110 and the pages name amd-arc-box.
  - **Not determined by it, checked by the lead.** The entry says each pin "was its repository's GitHub main when the snapshot was taken". The snapshot records repositories and pins' commits, not branches. This file's entry of 05:03:37 records the `gh api` reads, of 05:01 to 05:02, that each repository's main was the commit pinned, and the snapshot followed at 05:30.
  - **The record note: not taken.** It reads this file's 09:26:22 bullet as calling the docstring's list of sources "R6". That bullet holds two points in two sentences, R6 and then the docstring's list, so no correction is filed.
- **`6b712df` (11:01:14)** appends a new entry to docs/VALIDATION.md, headed "2026-10-31 - round 3's integration verifier: ...". The site's ledger corrects an earlier entry by a later one and never edits it (CLAUDE.md trap 15). The new entry:
  - gives what verifier-I read;
  - gives its one finding, with the lines that hold the figure;
  - restates the two phrases;
  - records its two notes as left.
  On its tree, `--check`, `--numbers` (4264 marks), `--links`, `--local-only`, `--docs` and `--manifest` each found 0 problems. Method's figure for the newest entry's controls, still 512 of 512, now cites the new entry.
- **The full gate on `6b712df`**, run 20261031-110125-6b712df, started at 11:01:24, tracked.

Decided:
- **verifier-I's second pass** is scoped to `git diff 33dc465 6b712df`, on a branch `pass2` at `6b712df` in its clone. It first files its first report by command from the lead's exact copy. It runs its own gate only if the lead's message says so, after the lead's has ended.

For: verifier-I, the round's record

## 2026-10-31 11:09:09 -0700 - the full gate on 6b712df passes; verifier-I told

Measured:
- The full gate on `6b712df`, run 20261031-110125-6b712df, ended at 11:08:55: VERDICT: PASS, nothing skipped; passed 11; numbers 4264 marks; facts 2493 the same; controls 512 caught, 0 did not fail, 0 skipped.

Decided:
- verifier-I is told that the lead's gate has ended. Whether it runs its own on `6b712df` is its call.

For: verifier-I, the round's record

## 2026-10-31 11:09:58 -0700 - verifier-I's second pass: NOT READY on one sentence of 6b712df's entry; the reads of the two new repositories' mains, recorded with their time

Measured:
- verifier-I reported its second pass at 11:09:03: NOT READY, on one sentence of the entry `6b712df` adds. The rest of that entry holds, and the round's entry read with it says nothing false. It filed its first report at 11:03:07 by command from the lead's exact copy, and changed one absolute path in it to `<repos>`, as the README requires; that entry says so. It withdraws its note on this file's 09:26:22 bullet. The runtime's figures for the pass: 15 tool uses, 435,458 ms; its "tokens", 555,529, is the context at the pass's end. The lead's exact copy of the message is `<scratch>/r3-held/exact/a76111680b469cb21-2.md`.
- **The sentence, checked by the lead: wrong for two of the three.** It reads "The lead read each repository's main with `gh api` from 05:01 to 05:02 that morning, and each was the commit pinned".
  - The 05:01 to 05:02 run compared the pins that pins.json then held with their default branches. cft-fp256's was `19de866`.
  - softfloat-bootstrap and muse-softfloat were not pins then. The lead read them at 04:30:17, by one command over both: `gh api repos/loganw234/<name>` for the default branch, then `gh api repos/loganw234/<name>/commits/HEAD --jq .sha`. That is the runtime's record of the lead's commands, its timestamp 11:30:17 UTC.
  - This file's 05:03:37 entry gives their mains, `a23a0ff` and `a2241fc`, without saying when or how they were read. They are recorded here.
- verifier-I also read GitHub's default-branch heads at its pass: `19de866`, `a23a0ff` and `a2241fc`, the pins.

Decided:
- The site's ledger corrects the sentence in a later entry, as before. verifier-I's third pass, its last, is scoped to that commit. If it still finds a wrong answer, the lead records it and asks Logan before going on.

For: verifier-I, the round's record

## 2026-10-31 11:11:54 -0700 - 38a91a9 corrects 6b712df's sentence in a later entry; its gate running; verifier-I's third pass

Measured:
- verifier-I's message at the end of its second pass, after the lead's gate on `6b712df` ended: its NOT READY stands. It ran no full gate on `6b712df`, whose diff is one ledger entry and generated files, and its quick stages pass there. Its file has an entry of 11:11:01. The runtime's figures for that resume: 19 tool uses, 563,446 ms; its "tokens", 569,851, is the context at its end.
- `38a91a9` (38a91a9 2026-10-31 11:11:33 -0700) appends to docs/VALIDATION.md an entry headed "2026-10-31 - round 3's integration verifier, its second pass: ...". It says when the two new repositories' mains were read, at 04:30, by `gh api repos/loganw234/<name>/commits/HEAD`, and that the 05:01 run compared the pins pins.json already held. `public/MANIFEST` changes with it, and no page changes. On its tree, `--check`, `--numbers` (4264 marks), `--links`, `--local-only`, `--docs` and `--manifest` each found 0 problems.
- Its full gate: start 2026-10-31 11:11:39 -0700 == run 20261031-111140-38a91a9 

Decided:
- **verifier-I's third and last pass** is scoped to `git diff 6b712df 38a91a9`, on a branch `pass3` at `38a91a9` in its clone. It runs no gate.

For: verifier-I, the round's record

## 2026-10-31 11:15:36 -0700 - verifier-I's third pass: READY

Measured:
- verifier-I reported its third pass, its last, at 11:27:05: READY. Each sentence of `38a91a9`'s entry holds against its sources. The entries of `6b712df` and `38a91a9`, read with the round's entry, say nothing false. Its report is in its file (11:14:51). The runtime's figures for the pass: 27 tool uses, 808,346 ms; its "tokens", 622,657, is the context at the pass's end.
- Its one note: "cft-fp256's was `19de866`" in that entry means cft-fp256's default branch, which "its default branch" would say without doubt. A wording note, not a send-back; the entry stands.
- It did not check the clock behind this file's heading "11:09:58", which it took for typed. The time was read: `date` printed "2026-10-31 11:09:58 -0700" in the call just before the lead wrote that entry.

Decided:
- Every verifier of the round is READY: verifier-plan (by Logan's approval after its third pass), verifier-P0, verifier-P3, verifier-P2, verifier-P1 and verifier-I. Main moves to round3's tip once the gate on `38a91a9` passes, and is pushed at Logan's word.

For: the round's record, Logan

## 2026-10-31 11:15:45 -0700 - a correction to the entry before: the time of verifier-I's third report was typed, and is wrong

Measured:
- The entry before says verifier-I reported its third pass "at 11:27:05". The lead typed that time instead of reading it. The runtime's record of the notification gives 18:15:16 UTC, that is 11:15:16 -0700, which `<scratch>/r3-extract-reports.py` printed as the first line of the lead's exact copy, `<scratch>/r3-held/exact/a76111680b469cb21-4.md`. The rest of that entry stands.
- This is the round's sixth time typed instead of read. The VALIDATION.md entry of round 3, written before it, counts four. The first slip after the entry is this file's heading "10:43:20", corrected at 10:43:03, and this is the second.

For: the round's record, the integration verifier

## 2026-10-31 11:19:55 -0700 - the full gate on 38a91a9, round3's tip, passes; the push goes to Logan

Measured:
- The full gate on `38a91a9`, run 20261031-111140-38a91a9, ended at 11:19:36: VERDICT: PASS, nothing skipped; passed 11; numbers 4264 marks; facts 2493 the same; controls 512 caught, 0 did not fail, 0 skipped.
- main is `797f588`, as origin/main is locally, and `round3` is 28 commits ahead of it: `git merge-base --is-ancestor main round3` holds, so main moves by a fast-forward.

Decided:
- The push goes to Logan now, through the question tool, with the ledger's archive, which ROUND3.md leaves to him at the round's end.

For: Logan, the round's record

## 2026-10-31 13:24:42 -0700 - Logan's word: push now, and archive the ledger in the repository

Measured:
- Logan, through the question tool, by the stamp above:
  - "Round 3 is done on round3's tip, 38a91a9: the full gate passed with nothing skipped, and every verifier is READY, the integration verifier included. Pushing fast-forwards main from 797f588 by 28 commits and deploys the site. Push now?" - "Push now (Recommended)": "Fast-forward main to 38a91a9 and push main only. Then watch the deploy, and check the live site byte for byte against the build."
  - "Round 3's ledger (the plan's briefs, every author's file, the six verifiers' reports and the three keys) sits outside the repository. Archive it in the repository as docs/round3-ledger/, as round 2's was archived as docs/round2-ledger/?" - "Archive it (Recommended)": "A follow-up commit copies the ledger into docs/round3-ledger/. A site-ledger entry records it, with the round's two later slips. It gets its own full gate and is pushed at your word."

Decided:
- main fast-forwards to `38a91a9` and is pushed now, main only. The lead watches the deploy and checks the live site byte for byte.
- The archive follows as its own commit and gate, and is pushed at Logan's word, as his answer says.

For: the round's record

## 2026-10-31 13:32:57 -0700 - pushed at Logan's word: main 797f588..38a91a9; the deploy passed on its first attempt; the live site is the build, byte for byte

Measured:
- `git ls-remote origin refs/heads/main` gave `797f588` just before the push, so GitHub's main had not moved. main fast-forwarded to `round3` (`git merge --ff-only`), and `git push origin main` printed "797f588..38a91a9  main -> main" at 13:25:00. main alone was pushed.
- The site's workflow, run 41238802159, on `38a91a9`: the gate job 20:25:05Z to 20:31:27Z, success; the deploy job 20:31:30Z to 20:32:02Z, success, on its first attempt.
- The live site, by `<scratch>/r3-live-check.py` against https://loganw.dev/ at 13:32:
  - BUILD reads "Deployed from 38a91a9fc1114416face589801409a030ea6fc8b";
  - 42 of 42 other published files are byte-identical to the build;
  - /resume serves the same bytes as resume.html;
  - resume.pdf is served as application/pdf;
  - 0 problems.

Decided:
- The round's end follows: the plant branches bundled into this ledger and deleted, the parcels' branches deleted (each is merged), and the worktrees and clones moved to the Recycle Bin, each checked first. Then the archive, as Logan's answer says.

For: the round's record, Logan

## 2026-10-31 13:34:42 -0700 - the round's end: the plant branches bundled and deleted, the parcels' branches deleted, the worktrees and clones to the Recycle Bin

Measured:
- **Checked first.** Every worktree had a clean tree except two of P0's trial worktrees:
  - `<scratch>/r3-py` held `.python-version` changed, which `0e87fc2` commits;
  - `<scratch>/r3-trial` held `pins.json` changed and its own trial snapshot, both superseded by `2f52525` and the 05:30 snapshot.
  The parcels' branches `r3-P1`, `r3-P2` and `r3-P3` are ancestors of main, and the plant branches `r3-P1-1`, `r3-P2-1` and `r3-P3-1` are not.
- **The bundle.** `plant-branches-r3-2026-10-31.bundle`, in this ledger, holds the three plant branches at `c4c4e9b`, `8b397be` and `9bef3c6`. `git bundle verify` says it is okay. It is 3,051,044 bytes, SHA-256 `06b0d6b9dd205fa2fb7eb8fdcd37e4f20f5697612103934c04629b2b847ea240`.
- **To the Recycle Bin, not deleted:**
  - the ten worktrees: the three planted copies, the three parcels', P0's two trials, and verifier-P0's and verifier-plan's;
  - the four verifier clones: verifier-P1's, P2's, P3's and I's.
  The verifiers' scratch scripts beside them stay. Emptying the Recycle Bin is Logan's.
- **Pruned and deleted.** `git worktree prune` cleared their records. `git branch -d` deleted the three parcels' branches, all merged, and `git branch -D` the three plant branches, after the bundle.
- loganw.dev now holds main, at `38a91a9`, and `round3`, at the same commit. The archive's commit goes on `round3`.
- The browser preview server the lead started at 05:31 for the map's checks is stopped.

For: the round's record, Logan
