
## 2026-10-31 09:02:03 -0700 - verifier-P1 starts; test escalation sent

Measured: SendMessage to main with the line 'verifier-P1: test escalation' returned 'Message queued for the main conversation's next turn.' Read at start: briefs/_verifier.md, briefs/verifier-P1.md, README.md (105 lines), lead.md (486 lines).
Believed: The runtime can message, so the test escalation went out as the README asks. P1.md is not read until I have reported.
For: the lead

## 2026-10-31 09:19:48 -0700 - the brief's re-read rule and the planted-copy rule disagree; this verifier read README.md and lead.md again and opened no other parcel or verifier file

Measured: _verifier.md says 'Read everything again before you write your report'; the dispatch and verifier-P1.md say P1.md is not read until the report. Before the report I read README.md (105 lines) and lead.md (513 lines, through its 09:16:58 entry). I opened neither P1.md nor the other verifiers' files.
Believed: The two rules conflict only for a planted-copy verifier, who must not read P1.md before reporting; a brief that says read everything again should name the files it means.
For: the lead, for the briefs of later planted-copy verifiers

## 2026-10-31 09:19:48 -0700 - verifier-P1 has reported; its report is held, and no finding is recorded in this file

Measured: The report is my final message to the lead. Background processes of mine: none; every command ran in the foreground, so none is still running. My clone, at c4c4e9b, has a clean tree, and no tracked file was edited. My scratch copies of other files were removed; my check scripts remain in the scratch directory.
Believed: The report holds every finding; this file says only that it is held, under the ruling of 08:58:09.
For: the lead

## 2026-10-31 10:00:13 -0700 - verifier-P1's pass-1 report, filed at the lead's request now that the hold has lifted (it reached the lead at 09:21:33)

verifier-P1 report: held. The ledger file (`<repos>/loganw-dev-r3-ledger/verifier-P1.md`) says only that it is held, with no finding in it.

**Copy verified:** `<scratch>/r3-verifier-P1/loganw.dev` at `c4c4e9b` (parent `6eff67b`). Python 3.12.15, `LOGANW_REPOS='C:\Users\logan\source\repos'`. The tree is clean and I edited no tracked file.

**Quick modes** (all exit 0): `--check`: 43 files are exactly what the pins render. `--numbers`: 4162 marks, 0 problems. `--links` and `--local-only`: 0 problems in 43 files. `--verify-facts`: 2444 read again and the same, 60 stated, 0 skipped. `--docs`: 0 problems in 9 documents. I did not run `--control` or `verify/run.sh`.

## 1. Every quote in the nine sections: DEFECT (D1, sends back)

- **Commands:** read `public/work-cft-fp256.txt` and `site/pages/work_cft_fp256.py` in full. Read cft-fp256 at `19de866` with `git show` and awk line ranges: VALIDATION.md 18206, 21042, 21055, 21099, 22253, 23603, 24164, 25104, 25753, 26082–26232; CONFORMANCE.md 3–4, 15–33, 226–232, 254–257, 281–284, 316–317, 338–339, 394–405; README.md 3–10, 26–34, 40–42, 67–74, 326–330; verify/run.sh 638–639; CLAUDE.md 116–118.
- **Observed:** Every quoted passage matches its source word for word. One sentence does not. In the contract paragraph (module lines 164–166; twin line 20), the page says the ledger's newest entry "reports a fix that left every published record as it was". The quote that follows is VALIDATION.md:26179: "...so those 8 records are the published ones moving." The sentence says the opposite of its own quote and of the entry. A reader is told no published record moved; the entry says eight did.
- **Verdict:** defect D1, a sentence the source contradicts.

## 2. The contract paragraph: DEFECT (D1, the same)

- **Commands:** as item 1; `git log -3 19de866 -- CONFORMANCE.md` (last change `740e6acb`, 2026-10-15); `facts.last_change` (author date); profile.py:58.
- **Observed:** "as of its last change, 2026-10-15" is right. The paragraph does not say the profile stepped or should have. "The pin holds both" is right. profile.py reads `VERSION = (3, 1)`. The defect is D1, which makes this paragraph misreport the entry it sets beside CONFORMANCE's "none moved".
- **Verdict:** defect D1.

## 3. Verified and the nightly sweep: DEFECT (D2, sends back)

- **Commands:** `git show 19de866:site/nightly.json`; `check_nightly.py` (scratch, read-only) summing the nights against `totals`; `cite_check.py` on `public/facts.json`; the harness of item 7.
- **Observed:** Every printed figure equals its `totals` figure: 10 nights; first 2026-10-19; newest night 10 starting 2026-10-29; 6,135 slices; 20,759,013,456,650 cases; 0 disagreements; 8,645 legs = 8,505 pass + 0 fail + 140 skipped. Each `totals` figure equals the sum over the ten nights, so each is the campaign's total through night 10. All 15 citations land on their own key's line (lines 5, 7, 8, 744, 748–751, 754). The sentence on what a night is quotes `rules.night` exactly, and the live page is said to go on.
- **Defect:** the paragraph also says "These are the campaign's final figures, through night 10" (module line 228; twin line 37). The sweep is not final. Night 1030 launched on 2026-10-30 and "runs until Monday 2026-11-02 07:45" (VALIDATION.md:26090–26092). The same paragraph says the live page goes on past these figures.
- **Verdict:** defect D2, a figure framed as final, which the source contradicts.

## 4. Kept failures: CONFIRMED

- **Commands:** `git merge-base --is-ancestor` against `19de866` for `48e2aa22`, `f192bf0`, `ca43695`, `25d5b8d2`, `b9d60ebc`, `f68c6301` (all ancestors); `git log -1` subjects; `git cat-file -p 48e2aa22`; `git diff --stat` and `git diff` of transcend.py and mpfr_check.c against the first parent.
- **Observed:** Issue 1 is the third bullet and replaces the device bullet. `f192bf0` ("make sim reads its results") and `ca43695` (the exp2 tie) match their bullets. `48e2aa22` is the merge of `fix-exp2m1` at `b9d60ebc`, the commit the entry names (VALIDATION.md:26172). The description in the source record matches the diff: the shortcut now begins at `n > emax + 1`; the MPFR tool's second call passes the exponential pool; the WebAssembly module changed. The bullet's quotes match VALIDATION.md 26151–26168.
- **Side note:** `kept_failure` checks ancestry only. `f68c6301`, the fix's first parent, is accepted as a "fixed by" commit.

## 5. The `make golden` cost: CONFIRMED

- **Commands:** VALIDATION.md 26082–26127; `grep -n "golden ok"` over the pin; verify/run.sh 638–639; Makefile 26 and 111–112.
- **Observed:** The 3,385 s, 5,951 passed line (26127) is the M2F2 gate, which the entry says was measured on amd-arc-box (26110). The page says where and how, and says that what `make golden` takes elsewhere depends on the machine and on whether pytest is given workers. That is right: `make golden` adds `-n` when pytest-xdist imports (Makefile:26), and the runner's stage does not (verify/run.sh:639).
- **Side note:** "newest timing" means the newest stated time. The 2026-10-30 desktop gate (26192–26193) also ran golden, with 5,955 passed, but states no golden time.

## 6. Prove it wrong, Connections, Provenance: defect D4 (minor), the rest CONFIRMED

- **Commands:** VALIDATION.md 26168 and 26224; `git diff 797f588 6eff67b -- site/data/relations.json`, which shows P0's six edges, two touching cft-fp256: the muse-softfloat "verified-by" edge and cft-fp256's "built-on" edge to softfloat-bootstrap; softfloat-bootstrap's README at `a23a0ff` (27–29); the page's file at `797f588` and `6eff67b`.
- **Observed:** The new limit is quoted exactly (26224), and the "never been asked" point matches 26168. Both edges' evidence matches its source word for word.
- **Defect D4 (minor):** Provenance lists six files, each read and present. The page also reads `vectors/SHA256SUMS` and `docs/COMPATIBILITY.md` through `facts.exists` (module lines 309–317), and neither is listed, though `_dossier.provenance_block` says it lists the files the dossier read. The omission is also in `797f588` and `6eff67b`, so it is pre-existing, but this commit rewrote the list and kept it.

## 7. New facts and controls: defect D3 (latent), the rest CONFIRMED

- **Commands:** `python -I nightly_faults.py <clone> <data>` in scratch, which calls `nightly`'s raw function with the pin replaced by crafted text; `_dossier.kept_failure` on real commits; build.py's controls loop (2502–2520, and the page loop near 3824).
- **Observed:**
  - The real file gives the right values and lines: cases 20,759,013,456,650 at 750; first 2026-10-19 at 748; newest night 10 at 5.
  - Refusals behave as the docstring says: an absent key is refused by name, with the keys present; a `part` matching twice is refused by name; a value on the next line is refused; a same-named key with another value is refused.
  - **D3, the docstring's guarantee is false.** The docstring says "a figure is never cited at a neighbour's line" (module line 40). The input `{"totals": {"legs": {"cases": 5, "pass": 1}, "cases": 5}}` returns 5, cited at line 3 (the legs object), not line 4 (`totals.cases`). A per-night list ahead of `totals.cases` with the same value does the same. The search takes the first match after the parent key, and the line check accepts any line holding the same pair. At the pin every citation is right, so this is latent.
  - `entry_title`'s example holds: the 2026-10-20 heading (VALIDATION.md:22253) ends in `**...**`, and `md_plain` strips it.
  - The kept-failure control's mutated hash (`48e2aa23`) is refused by git, so the control catches it. A fault it passes is an ancestor that is not the fix (item 4).
  - build.py's loop skips a page's controls by name on `Unavailable`, as the docstring says.

## 8. Comments, docstrings, commit message: defects D5 and D6; side notes

- **D5 (comment, module lines 259–262):** "The entry's known limits are quoted in 'Prove it wrong', not hidden." The entry lists four known limits (26223–26226). The page quotes one (26224).
- **D6 (comment, module lines 199–201, and the commit message):** "the verification events the record holds after 2026-10-06, newest last". The four rows end at 2026-10-20. The record holds later verification events: a soak against MPFR (24164, 2026-10-26), clause5-soak's wide class modes (25104, 2026-10-27), program.c parity (25753, 2026-10-29), and the 2026-10-30 gates (26082, 26149). The page also prints "Last verified: 2026-10-30" above a list that ends on 10-20.
- **Side notes:**
  - "keeps that word off a page other than Map & Ledger's row": literally false. The twin prints "three outside test sources" (line 33), a different sense from "the first outside report". The ruling's intent holds.
  - "no file at the pin says so": true for issue 1. COMPATIBILITY.md:1002 and ROADMAP.md:6446 say the profile stepped to 3.1, so the comment should say "for issue 1".
  - "the page never says 'now'": true in the page's own voice. The twin's line 58 quotes the record's "the ten now see both".
  - SPEC.md:39 does say "Kept failures (2–3, fix hashes)", as the comment says.

## 9. Anything else (side notes)

- Other pages changed by renumbering only. After normalising `[fact N]`, the `.txt` twins of cft-rebound, HonestFramework, ParcelRound and Quantum-Film are identical to `6eff67b`, and their `.html` differ only in `data-f` numbers. cft-rebound's text did not change; its public files did.
- The nightly totals are `card-stress-1019`'s nights only (`source.run_ids`). The 2026-10-19 row's long run names `out /data/card-stress-1016` (VALIDATION.md:21055). Its 4,086 legs and 3,287 slices are not in the totals' 8,645 and 6,135, and the page does not say so.
- Line-cited ledger rows (`row()`, `entry_title`, `ledger_title`, `ledger_date`) are re-pointed silently by a pin move, since `entry_title` checks only that a heading sits at the line. CLAUDE.md trap 15 cites by heading text. This is pre-existing practice for foreign ledgers, and no gate would catch a move.
- The "Cheapest first;" lede is shared `prove_it_wrong_opening` text, unchanged, and nothing on this page measures the order.

## Verdict: NOT READY

- **Sends work back:** D1 and D2.
- **Restate at the merge:** D3 (the docstring's neighbour-line claim, latent), D5 and D6 (comment claims).
- **Minor:** D4 (incomplete Provenance list; pre-existing; a list P1 rewrote).

## What I did not do

- Did not run `--control`, `verify/run.sh`, or the page's `controls()` through the build. The nightly and kept-failure functions were called directly in a scratch harness.
- Did not open P1.md, the other verifiers' files, the parcels' designs, or the keys. Did not open `<repos>/loganw.dev` or any worktree, `cft-worktrees`, `Muse-Softfloat`, the private repositories, or cft-fp256's working tree. cft-fp256 was read only by `git show`, `log`, `cat-file`, `merge-base` and `diff` at commits. Nothing was fetched, checked out or written.
- Did not check the Corrections, Map & Ledger, Method or resume pages, or the `5ff7379` restates. This verification covers `c4c4e9b` only.
- Did not check the rendered HTML in a browser, the reducer (`hw/card_stress_progress.py`), or the card's data.
- Re-read README.md and lead.md before the report. lead.md's new entries (09:09:36 and 09:16:58) concern other parcels; I found no instruction for me in them.

**Background work:** none of mine is running; every command ran in the foreground. I removed my scratch copies (`out/`, `data/`). The clone and three check scripts (`check_nightly.py`, `cite_check.py`, `nightly_faults.py`) remain in `<scratch>/r3-verifier-P1/`.


## 2026-10-31 10:10:13 -0700 - verifier-P1's pass-2 report on the lead's restates at cbb78e0: NOT READY

Pass 2 of 3, at the coordinator's request. Copy: branch pass2 at cbb78e0 (the lead's restates, on 775bf59, the merge of P1's 7e576fd); the planted copy was c4c4e9b.

Verdict: NOT READY. The restated comment on the Verified section (R7) claims more than its sources hold, and the Verified section itself still lacks the brief's named sin, cos and tan milestone and ends at 2026-10-20 above a line that says last verified 2026-10-30. Every other restate holds.

Checks (no gate run):
- git diff 7e576fd c4c4e9b -- site/pages/work_cft_fp256.py is exactly the two plants: the contract paragraph's "reports a fix that left every published record as it was" (P1 wrote "reports a fix that changed published records") and the nightly paragraph's "These are the campaign's final figures" (P1 wrote "These are the pin's figures"). The restates restore P1's wording, and both originals hold at the pin: VALIDATION.md:26179 says "those 8 records are the published ones moving"; :26092 says the sweep runs past night 10.
- git diff 775bf59 cbb78e0 -- site/pages/work_cft_fp256.py: six hunks, each examined below.
- Rendered output: a token-level diff of the HTML (fact numbers normalised), c4c4e9b to cbb78e0, shows only the two restored sentences and the two Provenance items. The twin text shows the same. Make golden's paragraph is unchanged. Other pages changed by renumbering only.
- Quick modes on cbb78e0, all exit 0: --check (43 files exactly what the pins render), --numbers (4252 marks, 0 problems), --links and --local-only (0), --verify-facts (2489 read again, 0 different, 60 stated, 0 skipped), --docs (0), --manifest (0).
- Citations: the new facts file gives the 14 nightly figures this page prints, each at its own key's line (744, 748, 5, 5, 749, 750, 751, 754 four times, 7, 8, 5).
- The nightly harness on cbb78e0's code: layouts T1 and T5 still cite the sibling object's line, so the stated limit is accurate.

The restates:
R1, the nightly module comment (one run, resumed each night, not the run the 2026-10-19 row closes): CONFIRMED. The source's run ids are ["card-stress-1019"] only, and the 2026-10-19 long-run entry's driver names out /data/card-stress-1016 (VALIDATION.md:21055). The page's own voice never says "now"; the one "now" on the page sits inside the record's quote (twin line 58).

R2, the nightly() docstring (a stated limit, and at the pin each printed figure is cited at its own key's line): CONFIRMED. The limit matches the code: the search starts at the parent key and takes the first match, and the line check accepts any line holding the same pair. The harness reproduces it, and all fourteen figures are at their own key's line at the pin.

R3, Provenance (the whole list, and "every file of cft-fp256's that this page reads, quoted or only shown to exist"): CONFIRMED. The page reads README.md, CONFORMANCE.md, CLAUDE.md, docs/VALIDATION.md and verify/run.sh by prose(); site/nightly.json by the nightly fact; docs/COMPATIBILITY.md and vectors/SHA256SUMS by exists(); and CONFORMANCE.md's last change by git log only. The Connections edges quoting cft-fp256's files read README.md (atlas-engine's two edges) and docs/VALIDATION.md (muse-softfloat's edge). last_verified reads workflow records, since pins.json declares no ledger for cft-fp256. Nothing else of cft-fp256's is read.

R4, the profile comment (no file at the pin records a step for issue 1's fix; the step to 3.1 is of 2026-10-13): CONFIRMED. profile.py:58 reads VERSION = (3, 1), and host/include/cft.h:155-156 has CFT_PROFILE_MAJOR 3 and CFT_PROFILE_MINOR 1. COMPATIBILITY.md:988 and :1002 sit under "Profile 3.1 (2026-10-13...)", and ROADMAP.md:6444-6446 says "Done on 2026-10-13". The M1 study lines (docs/studies/M1-exp-log.md:1527 and :1793) and CONFORMANCE.md:452 concern the 2026-10-05 exp2 tie. A search of docs, CONFORMANCE.md, README.md and profile.py for profile-step wording near exp2m1, issue 1 or 3.2 found nothing.

R5, the "outside" comment (the word is printed on this page in another sense): CONFIRMED. The page prints "outside" only in the 2026-10-20 heading ("three outside test sources"; twin line 33). public/corrections.html links 48e2aa22, as the comment says.

R6, the kept-failure comment (one of the entry's four known limits is quoted; the date label links its heading): CONFIRMED. VALIDATION.md:26223-26226 lists four known limits, and the page quotes 26224. The date label links to docs/VALIDATION.md?plain=1#L26149.

R7, the Verified comment: DEFECT, to restate. Two claims fail.
(a) "the ones P1's brief named". briefs/P1.md names no rows. Its lines 30-31 say the old Verified rows "now stop at 2026-10-06"; its lines 10-15 list what the dossier must reflect, among them "the math library's routines, built golden-first, to sin, cos and tan at all four formats". The page never mentions sin, cos or tan (a search of the twin finds none). VALIDATION.md:26082 (2026-10-30) says "so sin, cos and tan are built at all four formats", and 25753 (2026-10-29) and 25994 (2026-10-30) are the same milestone.
(b) "the record holds later ones, of 2026-10-26, 10-27 and 10-29". The record also holds later verification events on 2026-10-28 (25657: verifiers VN7, VM2G2a, VM2G2b, VTP) and 2026-10-30 (26082: verifiers VM2F1 and VM2F2; the desktop gate run 20261030-211024 at 26191-26198, VERDICT PASS). The list is incomplete.

R8, the rendered output: CONFIRMED (see the checks).

Pass-1 items after the restates: items 1 to 3 (quotes and figures) are unchanged, and the two reverted sentences are P1's wording and hold at the pin. Items 4 to 6 (kept failures, make golden, Connections and the new limit) are unchanged in the rendered output. Item 7 (the nightly fact and the controls): controls() is unchanged, and the kept-failure and nightly controls keep their behaviour. Item 8 (comments): restated as above, and R7 is the one comment still wrong. No restate breaks anything the first pass confirmed.

My own finding, the Verified list the lead deferred: DEFECT, sends the work back. The Verified rows (VALIDATION.md 18943, 21042, 21275, 22253) end on 2026-10-20, and the page's "Last verified: 2026-10-30" line sits above them. Its source, the passing gates workflow run on 19de866, is correct. The brief names this trap: "'Verified' rows that end at 2026-10-06 pass every gate" (briefs/P1.md, lines 75-76). The rows are not the brief's list: the sin, cos and tan milestone is missing, and the record runs to 2026-10-30. The page states no selection or limit where the rows are; the only statement is in a code comment, and under the READY test a limit must be stated where the claim is made. To clear it, either add the 2026-10-26 to 10-30 verification events, including VALIDATION.md:26082, or state on the page that the list is a selection through 2026-10-20 and record that as a known limit.

Side notes (none is a defect):
- docs/COMPATIBILITY.md and vectors/SHA256SUMS are not in build.SOURCE_PATHS. The build accepts them, since their Src labels name no path ("cft-fp256 19de866"), so the brief's rule about a path a label names does not reach them. The lead should decide whether they belong in the list.
- kept_failure checks ancestry only; f68c6301, the fix's first parent, is accepted as a "fixed by" commit. Deferred, unchanged.
- The nightly totals are card-stress-1019's nights only, and the page does not say the 2026-10-19 run's 4,086 legs and 3,287 slices lie outside them. Deferred.
- The golden timing is the newest stated time. The 2026-10-30 desktop gate ran golden with no time stated. A precision point only.
- The shared "Cheapest first;" lede and the line-cited ledger rows: deferred, unchanged.

Not done: no gate, no --control, no verify/run.sh, and I did not run the page's controls() (it is unchanged in the diff). I did not fetch, check out or write in any repository, and I did not read P1.md, the key, the other parcels' files or the other verifiers' files. Background work: none; every command ran in the foreground. My scratch copies from this pass are removed. The clone (cbb78e0, clean) and the three check scripts remain in <scratch>/r3-verifier-P1/.

## 2026-10-31 10:21:31 -0700 - verifier-P1's pass-3 report on the lead's restates at ffdcbb1 (the last pass): READY, with one comment sentence to restate before merge

Pass 3 of 3, the last. Copy: branch pass3 at ffdcbb1 (checked out), on 2bfafe1 (the lead's restate of Verify's docstring, which touches site/pages/verify.py and public/MANIFEST, neither my file nor my pages) and cbb78e0.

Verdict: READY on the page, with one comment sentence to restate before merge (S2 below). The rendered page is right: each of the eight Verified rows says exactly what its entry says, the list runs to the newest verification date, and nothing an earlier pass confirmed has broken. S2 is a comment that misdescribes the record. By the rule passes 1 and 2 applied to comments, it is restated at merge and is not a wrong answer on the page, so I do not send the work back for it. If the lead counts a code comment as a page-level claim, S2 is the one item to record for Logan; my reading is that it is restated at merge.

Checks (no gate run):
- git diff cbb78e0 ffdcbb1 -- site/pages/work_cft_fp256.py: four rows added after row(22253), namely row(24164), row(25104), row(25753) and row(26082), and the Verified comment rewritten. Nothing else in the file changed.
- 2bfafe1 changed site/pages/verify.py and public/MANIFEST only. A normalised diff of the twin (fact numbers removed) from cbb78e0 to 2bfafe1 is empty, so the Verify commit changes nothing visible on this page.
- From 2bfafe1 to ffdcbb1 the twin and the HTML change by the four rows and by renumbering only. The comment is not rendered.
- Row check (row_check.py, in scratch): each of the eight Verified rows in the twin equals the plain text of its heading at 19de866, after the same two steps as facts.md_plain. Each links to docs/VALIDATION.md?plain=1#L<line>. 8 of 8 pass.
- Quick modes on ffdcbb1, all exit 0: --check (43 files exactly what the pins render), --numbers (4264 marks, 0 problems), --links and --local-only (0), --verify-facts (2493 read again, 0 different, 60 stated, 0 skipped; the four rows add four facts, from 2489), --docs (0), --manifest (0). I did not rerun the full build, which writes public/, so the lead's 2553 figures are the lead's; --check confirms the 43 files.
- The nightly citations are unchanged: 15 in the facts file, 14 of them on this page, each at its own key's line.

The four new rows, each the heading as the site prints it:
- 24164 (2026-10-26): "the wide division and square-root soak: thirty modes of divsqrt-soak at fp64, fp128 and fp256 against MPFR ..." is a soak against MPFR. PASS.
- 25104 (2026-10-27): "the wide class modes: twelve modes of clause5-soak at fp128 and fp256 ... (parcel HXb, Opus 5.5)". PASS.
- 25753 (2026-10-29): "program.c parity for sin, cos and tan: the 45 fragments of parcel M2G2a run through libcft's sequencer ..." PASS. Its heading also says nothing in the entry touched the card or amd-arc-box.
- 26082 (2026-10-30): "... so sin, cos and tan are built at all four formats (the lead; verifiers VM2F1 and VM2F2)". PASS. This is the milestone the brief names. The pin's roadmap agrees: docs/ROADMAP.md:6138 dates fp32's trig part to 2026-10-30 (parcel M2F2, merged at d6f5574).

The comment, sentence by sentence:
- "eight of the record's entries after 2026-10-06, newest last, each one that verifies": true. The eight are all after 2026-10-06, in date order, and each verifies.
- The list of the eight: true. Each name matches its row.
- "The record holds other entries in that span, on tools, studies and nights": FALSE as a classification (S2). The span has 88 dated headings from 2026-10-12 to 2026-10-30; 80 are not among the eight. By my reading of their headings, roughly 35 of the 80 are not tools, studies or nights. Examples: math-library routines (VALIDATION.md:19548, exp2 and expm1; :19753, log, log2 and log1p; :24732, the trigonometric reduction of sin, cos and tan in the golden generator); a documentation entry (:22792); a fix (:26149, issue 1, which the comment points to under Kept failures); and gate or verification entries (:24351, a desktop gate run; :25657, the night-7 check by verifiers VN7 and others). The sentence hides the routines strand and the verifying entries the selection leaves out. The restate should name those kinds, or say that the selection leaves out entries of other kinds.
- "the nightly sweep follows this list, and issue 1 is under Kept failures": true. The nightly paragraphs come after the rows, and issue 1 is under Kept failures.
- "The selection is editorial, and its newest row is of 2026-10-30, the date "Last verified" prints above it at the pin": true. Twin line 24 reads "Last verified: 2026-10-30". Its source is the passing gates run on 19de866, created 2026-10-31T06:30:18Z and dated 2026-10-30 on the pin's calendar (facts.json). The comment says only that the dates match.
- "Each row is its entry's heading whole, so the row says what the entry says": true, 8 of 8.
- "the fourth says in its own heading that none of it has touched the card or amd-arc-box": true. The fourth row is 22253, and its heading says so.

Did the change break anything earlier passes confirmed? No. The quotes, figures, nightly paragraph, kept failures, make golden, Connections, the eight-file Provenance and the controls are unchanged in the diff and in the rendered output. The restates confirmed in pass 2 (R1 to R6 and R8) are unchanged, and the two false claims of R7 (the "brief named" attribution and the three-date list) are gone.

Side notes (none is a defect on the page):
- The commit message of ffdcbb1 says "the record's four later verifying entries". As a count that is not true: the record's later verifying entries include 24351, 25657 and 26149 (issue 1, verifier VX1, a desktop gate). History is not restated; the lead decides whether to note it.
- The pin's README.md lines 436-439 ("What is planned ... sin, cos and tan (M2, docs/studies/M2-trig.md) are the next build") are stale against the 2026-10-26 to 10-30 entries and ROADMAP.md:6138. The dossier does not quote that passage, so the page agrees with its entries. But Provenance lists README.md, so a reader who checks the README will find the disagreement.
- docs/COMPATIBILITY.md and vectors/SHA256SUMS are not in build.SOURCE_PATHS (pass 2, unchanged).
- Kept as before, not reopened: kept_failure checks ancestry only; the nightly totals are card-stress-1019's nights only; the line-cited rows; the shared "Cheapest first;" lede.

Not done: no gate, no --control, no verify/run.sh. I did not run the page's controls() (the lead reports 8 of 8, and the diff does not touch controls()), and I did not run the full build. I did not read P1.md, the key, or any other parcel's or verifier's file, and I did not fetch, check out or write anything in any repository. Background work: none; every command ran in the foreground. The scratch copies from this pass are removed. The clone (ffdcbb1, clean) and the scripts remain in <scratch>/r3-verifier-P1/.
