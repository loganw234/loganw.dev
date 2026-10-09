
## 2026-10-08 19:33:05 -0700 - verifier-CS starts at 35e0dd1: the test escalation went to the lead before any other step, and the runtime took it

Measured:
- The worktree was fast-forwarded from 7f2d51b to 35e0dd1 (`git merge --ff-only 35e0dd1`), and was clean before. `git log --oneline -1` reads 35e0dd1.
- The first step, before any reading of the case study, was the test escalation, "verifier-CS: test escalation", sent to the lead (the main conversation). The runtime answered "Message queued for the main conversation's next turn." So this runtime can message the lead. This entry is written late, at 19:33, and says so.
- Read before starting: the briefs `_verifier.md` and `verifier-CS.md`; the ledger's README; lead.md, in full.
- The live ledger holds 34 files. The archive at 35e0dd1 holds 33. The one it lacks is `briefs/verifier-CS.md`, written after the archive commit (19:06:30).

Believed:
- Nothing yet.

For: the lead, the case study's verifier chain

## 2026-10-08 19:35:01 -0700 - verifier-CS report on 35e0dd1: NOT READY; six wrong answers to send back, eleven restates, three decisions for the lead; the gate passes

Measured:

Setup, from the worktree, Python 3.12.9, LOGANW_REPOS set inline: `python site/build.py --check` ("40 published files are exactly what the pins render"); `--numbers` (0 problems, 3231 marks); `--links` (0); `--local-only` (0); `--verify-facts` (1922 read again and the same, 0 different, 54 stated). The site's own `.cache` was copied into the worktree (gitignored).

Item 1, the timeline. Commands: `git log --format` of the committer times from 35e0dd1 back to 43c36a2; the first and last `## ` headings of each agent's ledger file; lead.md's stamps. Observed: every row agrees with the stamps and commit times, to the minute, with three exceptions. (a) Line 83, the 18:33 row, says every merge made again with `git merge-tree` "is clean". verifier-I found conflicts in public/ at each merge (8, 16, 18 and 17 files), resolved by building it again; "clean" needs that qualifier. (b) Line 86, the 18:56 row, reports the live byte check, which lead.md records at 19:04:33; the deploy run for 7f2d51b concluded success (`gh run list`). (c) The 16:22 row groups verifier-P4's report (16:22:07) with its merge (4d534df, 16:25:38) and its restates (e349b1a, 16:26:55); each time is right, but they are three events. Verdict: confirmed; (a) and (b) are restates.

Item 2, the figures.
- 8 of 8: see item 4. Confirmed.
- 27, 5 and 77: `git show 43c36a2:public/facts.json` and `git show 05413b2:public/facts.json`, each call keyed by method and arguments (820 and 892 distinct calls; 815 matched). My own count: 27 matched calls read different text; 5 are gone (the stated line, Verify's three old patterns, and case study 4's existence check); 77 are new. Confirmed.
- Passes and defects: verifier-plan 8 defects at its first report (14:17:38, lead.md), then 2 at pass 2 (14:40:08) and 2 wrong answers at pass 3 (14:51:25); verifier-P0 1 defect (15:21:32), then READY at 15:32:02 and at 16:13:11. Confirmed.
- 31 minutes: P4's go at 15:42:36, the others' go after verifier-P0's READY on the seam commit at 16:13:11. Confirmed.
- Eleven agents: four parcels and seven verifiers. Confirmed as eleven. But lines 40 to 42 say "the eight verifiers on claude-haiku-5-5"; the case study's own cost table has seven verifier rows, and the ledger dispatches seven. Defect (W2).
- Five times Logan was asked: the lead's transcript has five question-tool calls in the round, asked at 13:28:16, 14:17:44, 14:53:25, 15:23:09 and 18:32:10, answered after 4.5, 0.9, 1.4, 0.9 and 1.6 minutes. Two more calls, on 09-29, are round 1's. I read only timestamps and option counts. Confirmed, including "within minutes".
- Three wrong claims of verifiers, in two of twelve reports. The twelve reports before the push: verifier-plan 3, verifier-P0 3, verifier-P1, -P2, -P3 and -P4 one each, verifier-I 2. The wrong claims: (i) verifier-plan's pass 1, that quick "no longer" names the GPU's photograph; cft-fp256's docs/VERIFICATION.md line 382 at ab51655 still does; withdrawn at pass 2. (ii) verifier-P1's "dangling colon" on the page; public/work-cft-fp256.txt line 18 at bef03b0 has none, the colon is the source's lead-in ("says of the tree:"). (iii) verifier-P1's S1: CONFORMANCE.md lines 312 and 316 are right; at ab51655 the quote starts at 312 and "A change that moves" begins at the end of 316. P1 was right. Confirmed: three, in two reports.
- Not determined: the seven pins' compare counts (381, 37, 171, 1, 5, 409, 70). Not re-run; GitHub's counts have moved since 13:16.

Item 3, the cost section. Command: `python -I round_metrics.py <the lead's transcript> 2026-10-08T20:16:10Z 2026-10-09T01:56:43Z`, run on the ledger's copy. Observed: both tables, the class totals and the three output shares (57.9, 32.7 and 9.4 per cent) equal the case study's cell by cell. The method paragraph matches the script: per-message usage, fresh = input + cache writes + output, cache reads apart, notifications as runs with repeats merged, the context figure shown and never summed, models from the transcripts, the lead from the request. One gap: the "messages" column is never defined; the script counts the distinct assistant message ids that carry a usage record (restate R9).
Claims checked:
- The lead's checking, 8 runs and 4.9 M fresh tokens (1.9 + 1.6 + 1.4), more than any parcel (the largest, 3.3 M), and more than the four parcels' verifiers together (2.8 M). Confirmed.
- "7.7 M against 7.8 M, as case study 7 found": ParcelRound's case study 7 (commit 894d125) says "Verifiers and parcels took about the same", 189.0 M against 193.4 M. Confirmed.
- "0.67 M to 0.75 M ... near the medians ... (805 k and 751 k)": case study 7's first-run medians, smaller model 805 k, larger 751 k. Confirmed.
- "248 k to 287 k": confirmed.
- "round 6's Opus verifiers wrote 45 k to 68 k each (case study 6)": ParcelRound's case study 6 (f42242e) gives 44,727 to 68,067 for its five parcel verifiers; its other Opus verifiers wrote 129,015 (verifier-P0), 114,138 (the plan's verifier) and 117,223 (verifier-I, wave 1). Defect (W4): "each" holds for the parcel verifiers only.
- "Haiku writes more than it reads": the table has no input-only column; a parcel verifier's cache reads are 21 to 32 M and its output 0.25 to 0.29 M. As written the sentence is false and compares nothing the table measures. What the figures support is output per run against round 6's parcel verifiers (248 to 287 k against 45 to 68 k). Defect (W3).
- The quotation from case study 6, "A verifier that read the design first could have found every plant by comparison alone": exact (f42242e, lines 163 to 165). Confirmed.
Verdict: the tables are confirmed; W3 and W4 are defects.

Item 4, the plants. Commands: `sha256sum` of the four keys; reading each key; reading verifier-P1 (lines 26 to 40), verifier-P2 (lines 13 to 20 and 74), verifier-P4 (lines 13 to 20 and 43), and lead.md's transcription of verifier-P3's report (17:54:05); the hashes lead.md records before dispatch (15:52:29, 16:43:56, 17:24:31). Observed: the four hashes equal the values recorded before dispatch (P1 caff9677..., P2 7b24bf25..., P3 f4c13982..., P4 11bc552a...). Each row of the table matches its key's file, kind and words, with one nuance: the P2 plant is the lead-in "Across its rounds, its planted faults: "; "ten of ten" is the page's own figure after it (restate R8). Each of the eight is answered by a finding in the named verifier's report, citing the source line: verifier-P4 D1 (the tense, README line 6 of the Mercenaries2 repository) and D2 (the person and pronoun); verifier-P1 D1 (CONFORMANCE.md lines 334 to 353) and D2 (thread_determinism.py lines 21 to 22 and 36); verifier-P2 D1 (CASE-STUDY-6.md lines 35 to 37) and D2; verifier-P3 D1 and D2, from lead.md's transcription. Each verifier made one pass. Confirmed.

Item 5, the lead's slips. Commands: greps across the ledger for slip, correction, trailer, Co-Authored and question tool; reading each cited entry. Observed: the seven listed slips each have an entry: the plan's first draft (14:17:38, eight defects); the key written through a heredoc (17:24:31); the second heredoc (18:10:46); the metrics script (17:30:16, P1 and P2 showed fewer runs); the gates at once (16:44:52, 877 s against about 190 s; 17:17:12, about 1,490 s); P0's commit subject (15:24:47, "two refusals" for one Map & Ledger line and three Verify patterns); the two wrong line numbers (17:45:48, and 18:32:03 "The lead's slip"). The co-author trailer item has no lead entry: P4 recorded it in its own correction (P4.md, 15:40:10), and grep of lead.md for "trailer" finds none. Unlisted, but recorded by the lead: 14:43:12 (the decision numbers in the 14:18:57 entry were 35 and 36, not 36 and 37); 15:24:47 (10b6b17's message says render.render() refuses a typed figure, which is false); 18:02:01 (the yield entry said three verifiers noted the design's difference; all four did, as the case study repeats; see W6); 19:12:36 (commit 2d4ae4a went in past a failing --docs check, and a carriage return was lost; both were amended into 35e0dd1). The list reads as complete and is not (restate R4). "Each went back to Logan" (lines 163 to 164) is wrong for the quote fix (b7879df), which the lead made without asking Logan; the owner items did go to him (restate R4).

Item 6, the proposals. Each is headed "(proposed; the owner's to settle)". Checked against the ledger: (1) "it was most of the work": no measure of the work by kind exists in the ledger or the cost tables, which count by agent; restate R5. (2) "A planted copy is reachable by comparison through the ledger": rests on three full reports (verifier-P1 line 42, verifier-P2 line 74, verifier-P4 line 43); verifier-P3's summary does not show it (W6). Restate. (3) "A smaller model can verify a content round": one round, four planted-copy verifiers, eight plants, no same-plant comparison with a larger model in this round, and the design-route limit the case study itself records. It claims more than this round showed; restate R6. (4) "Read the cost from every record the transcript keeps": rests on lead.md 17:30:16 and on case study 7; confirmed. (5) "Three at once cost each controls stage five to eight times its time": the record gives 877 s and 1,490 s against about 190 s, that is 4.6 to 7.8 times; restate R7.

Item 7, the archive. Commands: `git ls-tree -r --name-only 35e0dd1 -- docs/round2-ledger` (33 files); each file read with `git show 35e0dd1:<path>`; compared with the live ledger file by `cmp`, and by `cmp -n` for the archived length; the worktree's checked-out copies compared the same way; a carriage-return count; `python site/build.py --privacy` ("privacy: 0 problem(s)", 155 files, 874 blobs); and greps across docs/ for addresses, absolute paths and secret patterns. Observed: 32 files are byte-identical to the live ledger, and so are the worktree copies. lead.md's archived bytes are the first 78,660 bytes of the live file; the live file has 1,709 more, the 19:12:36 entry; no earlier byte differs. The live ledger has one file the archive lacks, briefs/verifier-CS.md, written after the archive commit. P4.md holds one carriage return, kept. Addresses in docs/: the site's contact, and the co-author trailer's address in P4.md line 589 and briefs/_common.md line 86. The privacy stage and my brief allow the trailer's address; the ledger's README does not (it allows no address but the contact). Absolute paths: verifier-P0.md line 16 holds the elided path fragment that its own 15:21:26 entry flags; nothing else in the archive has one. Secrets: none found. Verdict: confirmed, byte for byte; two decisions for the lead (D1, D2).

Item 8, the README rows and CLAUDE.md's trap 19. Command: `git diff 7f2d51b 35e0dd1 -- README.md CLAUDE.md .gitattributes`. Observed: the two new README rows (lines 217 and 218) name paths that exist and describe them, with one exception. "The briefs as dispatched" is not exact: the plan's verifier was dispatched at 13:40, and the shared briefs _common.md and _verifier.md were revised at 14:22 (lead.md, 14:22:22); the archive holds the revised versions (restate R10). `.gitattributes` gives `docs/round2-ledger/** -text`, as its comment says. Trap 19 (CLAUDE.md, lines 179 to 184): "about three minutes alone": my run's controls stage took 216 s, the lead's took 190 to 202 s. "Between 15 and 25 minutes": the record gives 877 s and 1,490 s. On concurrency: lead.md 17:17:12 says the 1,490 s stages ran "beside the gate on e349b1a", but that gate started at 16:26:56, and its 877 s controls stage (lead.md 16:44:52) would have ended near 16:43, before the planted gates started (16:44:11). The ledger does not settle whether three ran at once; the e349b1a gate's stage record would. Not determined (N1).

Item 9, the gate. Command: `LOGANW_REPOS` set inline, then `bash verify/run.sh --require-all` on 35e0dd1 from a clean tree, run alone after checking that no other gate was running; run 20261008-191852-35e0dd1; the log is in my scratch. Observed: build ok (15 s); manifest ok; facts ok (15 s); numbers ok; links ok; local-only ok; docs ok (8 documents); privacy ok (23 s); github ok (14 s, 20 pins); controls ok (216 s, "393 caught, 0 did not fail, 0 skipped by name"); runner-control failed as it must ("CAUGHT: index.html links to planted.html"). Summary: "passed 11, failed 0, skipped 0, cached 0"; "VERDICT: PASS, nothing skipped". Confirmed. The tree was clean before and after, apart from the ignored .cache/ and verify/state/.

Item 10, anything else.
- W1, lines 13 to 14. The intro says the case study "went past a verifier, on Haiku, before it was committed; the last section says what that verifier found." The record says otherwise: the commit is 35e0dd1 (committer time 19:07:06); this verifier was dispatched on it at 19:12:36 (lead.md); and the last section is the placeholder at lines 287 to 289, "(To be filled after the integration verifier, the push and the live check.)", although all three had happened by 19:04. Send back: the intro's account of its verification is false as committed, and the last section must be written.
- R1, lines 155 to 156, "The site's own ledger lists every correction the round made": not so. The Threads index's line in site/pages/threads.py (at 43c36a2, line 20: "everyone who has committed to it") was restated at 427900e (its message: "it names the contributors to the repositories it reads (P4's F6)"), and the round's entry in docs/VALIDATION.md (lines 2073 to 2098, "Corrections to what the site had published") does not list it.
- Checked and confirmed: the four links in the case study resolve; ParcelRound's CASE-STUDY.md at f42242e has no clock time and no commit hash of seven or more hex digits, as the P2 entry says; cft-fp256's README at ab51655 gives "pip install pytest mpmath" beside "make golden"; HonestHarness's README at b310f82 says "A harness for running" and "There is no code yet"; P1's rows stop at 2026-09-23 (P1.md line 45); P4's new commits are all by the two accounts (P4.md line 104); SPEC.md decisions 31 to 36 (lines 282 to 307) match the case study's summary, decision 35's wording included; `git ls-remote --heads origin` shows only main, at 7f2d51b (trap 17); the deploy run for 7f2d51b concluded success.
- Side note: lead.md's 18:00:18 yield entry and its 18:02:01 correction say verifier-P3 also noted the design's difference; the record of its report (lead.md 17:54:05) does not. The case study repeats it (W6).
- Side note: two headings in verifier-P1.md share the stamp 17:43:05 (its environment entry and its report). verifier-plan.md's report heading (line 29) has a date and no clock time, so "which every author wrote with date" (lines 16 to 17) is not quite so (restate R11).
- Side note: the keys and the plants' descriptions are now in the repository's docs (archived), and the planted branches are local only. A future round must not reuse these plants.

Decisions for the lead (not defects):
- D1: the co-author trailer's address in the archive (P4.md line 589, briefs/_common.md line 86). Either the README's rule is changed to the stage's rule, or the two occurrences are struck; striking breaks the archive's byte-for-byte claim.
- D2: verifier-P0.md line 16. Its 15:21:26 entry asks that the fragment be struck when the file is published, and lead.md's 15:33:01 entry says it "is struck in the published archive"; the archive keeps it byte for byte. Strike it, or record that the elided form stays.
- D3: after this report, rewrite the intro (W1) and write the last section.

Overall verdict: NOT READY. Send back, the wrong answers: W1 (lines 13 to 14, and the placeholder at lines 287 to 289); W2 (lines 40 to 42, "the eight verifiers"); W3 (lines 251 to 252, "Haiku writes more than it reads"); W4 (lines 252 to 253, "round 6's Opus verifiers wrote 45 k to 68 k each"); W5 (lines 118 to 120, "in P1's, two citations in its own commit message"); W6 (lines 111 to 112, "All four reports also note ..."). Restate at the merge, as claims that go past their sources: R1 to R11 as numbered above. The archive is byte for byte, the privacy stage passes, and the gate passes.

Not determined: N1, the concurrency of the gates behind trap 19 and line 197; N2, the seven pins' compare counts; N3, METHOD.md's 13 quotes, 3 of them ParcelRound's, not counted; N4, verifier side notes the lead did not check: verifier-P1's S4, S5 and S7 to S10, and verifier-P3's S1, S2, S4, S5 and S7 (S6 I checked: prose() returns the first capture group, and the numbers stage reads public/, so S6 is accurate).

Believed:
- The case study's tables and method are sound. Its defects are in its sentences about what happened, and they are few and checkable.

What I did not do:
- I did not re-run the seven compare counts against GitHub, or re-count METHOD.md's quotes; I did not read the lead's gate state files, nor any worktree other than my own; I did not check the live site's bytes again (the lead's 19:04 record stands, and the deploy run concluded success); I did not re-run any planted copy (the case study has none); I did not quote the lead's transcript beyond its timestamps, option counts and the script's output.
- Background work: the gate (task bb1fmjolx) completed. Nothing of mine is running.
- Scratch: the gate log, the metrics output, the census and the copies of ParcelRound's and cft-fp256's text are in my scratch directory. No build copies were made, and no tracked file was edited. The worktree holds the gitignored .cache/ and verify/state/ that the setup and the gate created.

For: the lead (the send-back list, the restates and D1 to D3), the case study

## 2026-10-08 19:36:30 -0700 - verifier-CS addendum to the report at 19:35:01: W5 and W6 are explained here; the report's list is otherwise unchanged

Measured:
- W5, lines 118 to 120, "in P1's, two citations in its own commit message", is wrong as written. Of the two items the case study means, one is verifier-P1's S1, which said that P1's commit cited CONFORMANCE.md lines 312 and 316 for a quote at 317 to 319. The citation is right (at ab51655 the quote starts at 312, and "A change that moves" begins at the end of 316), so S1 was a wrong claim, and the lead's merge record of 17:45:48 repeated it. The other item, S2, is not a citation: P1's message says the docstring and a comment record the gap quotes' re-reading, where only the comment does, and P1 corrected that itself at 16:34:27. So the case study has no two citation findings in P1's work.
- W6, lines 111 to 112, "All four reports also note that the parcel's design ... reads otherwise at the planted sentences", is supported by three reports and not by the fourth as recorded: verifier-P1 (verifier-P1.md line 42), verifier-P2 (line 74) and verifier-P4 (line 43) say it. verifier-P3's report survives only as the lead's short transcription (lead.md, 17:54:05), which says nothing of the design. The lead's entries of 18:00:18 and 18:02:01 assert that verifier-P3 noted it; the record does not show it. The count must read "three", or the fourth must be recorded from verifier-P3's own words.
- The report's other items stand as written.

Believed:
- Nothing beyond the above.

For: the lead, the case study

## 2026-10-08 19:58:44 -0700 - verifier-CS pass 2 on eb90939: NOT READY on three wording faults, each a small fix, and on one R10 claim the archive still contradicts; the gate passes; the archive and the stage times checked

Measured:

Setup. Worktree fast-forwarded from 35e0dd1 to eb90939 (`git merge --ff-only eb90939`); clean before and after. Diff: eight files (CLAUDE.md, README.md, the case study, VALIDATION.md, public/MANIFEST, and the archive's three new or changed files, briefs/verifier-CS.md, verifier-CS.md and lead.md).

The gate on eb90939, run alone after checking that no other gate or build was running (run 20261008-195154-eb90939; log in my scratch): "passed 11, failed 0, skipped 0, cached 0"; "VERDICT: PASS, nothing skipped"; controls 393 caught, 0 did not fail, 0 skipped by name (214 s); runner-control failed as it must. The lead's run (194233) agrees.

Item by item (W = my pass-1 wrong answers, R = my pass-1 restates):
- W1, lines 13 to 15 and 321 to 346: fixed. The opening no longer claims pre-commit verification; the last section is written and says what the verifier found. Confirmed.
- W2, lines 43 to 47: "the seven verifiers before the push, and this file's". Confirmed.
- W3, line 275: "Haiku's verifiers wrote more than round 6's", with the per-run figures (248 to 287 k against 45 to 68 k). Confirmed.
- W4, lines 275 to 278: round 6's five parcel verifiers wrote 45 to 68 k each; its three other Opus verifiers 114 to 129 k. Checked against case study 6's table (f42242e). Confirmed.
- W5, lines 127 to 129: "one clause of its own commit message, which P1 had already corrected itself". Confirmed against lead.md's 16:34:27 entry and bef03b0's message.
- W6, lines 118 to 126: "All four reports also note ...", now sourced to verifier-P3's report as the lead's 19:38:26 correction quotes it. The quoted design words match P3.md (line 68, "quoted whole"; line 86, "Below, one of the devices' prints"), so the design reference is real. Accepted, with the limit that the verbatim report exists only in the lead's file.
- R1, lines 164 to 166: "lists most ... has every one, with the line that shows it". One example checked: the threads.py restate has its line (P4.md line 510: "threads.py line 20 (F6)"; line 302 quotes it). The word "every" is not checked exhaustively. Confirmed for the example.
- R2, row 18:33 (line 87): "merges its source files without a conflict; only the generated public/ conflicted, and was built again each time". Confirmed against verifier-I's item 1.
- R3, rows 18:56 and 19:04 (lines 90 to 91): confirmed. The deploy run 37872192090 concluded success, and both its gate and deploy jobs did too (`gh run view`). The live site: 38 of 39 published files are byte-identical to eb90939's public/; the one difference is MANIFEST, because eb90939 changed public/MANIFEST (the VALIDATION.md hash). The live MANIFEST equals 7f2d51b's (`git show 7f2d51b:public/MANIFEST`), so "39 of 39" is true of the pushed build (see R-d). BUILD reads "Deployed from 7f2d51b...". The email domain occurs 0 times in the live facts.json (counted, not printed).
- R4, lines 196 to 226: partly. Added: the 14:43:12 numbering, b7879df's quote, the yield's first record, and the 19:12:36 slips; "Each went back to Logan" fixed in the owner's section. Not added: lead.md's 15:24:47 entry, which says 10b6b17's message wrongly says render.render() refuses a typed figure. Restate (R-a).
- R5, line 265: "it was most of the work" removed. Confirmed.
- R6, lines 305 to 313: the proposal now says "That is one round, of four parcels." Confirmed.
- R7, lines 318 to 319: "4.6 to 7.8 times its time alone". Confirmed: 877/190 = 4.6; 1,490/190 = 7.8.
- R8, line 109: the P2 plant is the lead-in; "ten of ten" is the page's own figure. Confirmed against key-P2.json.
- R9, line 232: "A message is one of the agent's model responses, counted once by its id." Confirmed against round_metrics.py (distinct message ids with a usage record).
- R10, README.md line 218: NOT fixed (S2 below).
- R11, lines 17 to 18: "one of verifier-plan's headings had no time, which its next entry corrects". Confirmed: verifier-plan.md line 125 is that correction, stamped 14:15:26.

N1, settled from the stage records.
- e349b1a's gate (`stages.jsonl` in its state directory, in the main checkout): build 22 s, manifest 1, facts 21, numbers 1, links 1, local-only 3, docs 2, privacy 42, github 71; those sum to 164 s, so controls ran from 16:29:40 for 877 s, to 16:44:17; runner-control took 7 s, to 16:44:24. Confirmed (the lead's 19:38:26 figures).
- The planted gates (lead's scratch, `gate-plant-P1.log` and `gate-plant-P2.log`; run ids 164411): the stages before controls sum to 307 s (9a5449d) and 306 s (2093b9d), so their controls began near 16:49:18 and 16:49:17, and ran 1,493 s and 1,491 s, to about 17:14. Confirmed.
- So the controls stages did not overlap: the planted controls began about five minutes after e349b1a's ended. But gate runs did overlap: from 16:44:11 (the planted starts) to 16:44:24 (e349b1a's runner-control), three full gate runs were in progress, for 13 seconds. The wording "no three gates ran at once" (VALIDATION.md heading, line 2168), "they had not" (case study lines 343 to 345), and "So three gates did not run at once" (lead.md 19:38:26) is therefore wrong as worded (S3). The controls stages are the correct subject.
- P2's three --control runs: "3 m 22 s, 3 m 31 s and 4 m 0 s" (P2.md line 288), with no times recorded, as the 19:41:33 correction says. Confirmed. Which parcel runs overlapped e349b1a's controls is not determined, also as that correction says.

The round's corrected entry (VALIDATION.md 2168 to 2188): its content checks against the stage records, except the heading (S3). The first version's list entry it corrects (line 2127 to 2128) is quoted exactly.

Trap 19 (CLAUDE.md lines 179 to 184): "about three minutes on a quiet machine" (my runs 216 s and 214 s, the lead's 190 s and 212 s), "about 15 minutes" (877 s) and "about 25 for each of two gates run side by side" (1,490 s). Consistent with the records. Confirmed.

The archive, retaken at 19:41:52: 35 files. Each equals the live ledger file byte for byte except lead.md, which is the archive plus 1,061 appended bytes, and the appended text is only the lead's entries after 19:41:52 (19:47:24 and the coordinator's message). No live-only or archive-only file. CR count: P4.md one, as before. Addresses in docs/: the same set as pass 1 (the site's contact, and the co-author trailer's address in P4.md and briefs/_common.md); none in the new files. Absolute paths in the archive: none; the elided form of the user directory (the fragment that verifier-P0.md's correction flags) occurs in verifier-P0.md and in the lead's 19:38:26 entry, both allowed. `python site/build.py --privacy` is inside the gate: 0 problems.

The post-push figures (lines 286 to 291), re-derived with round_metrics.py over 18:56:43 to 19:39:45: 43 minutes; verifier-CS 1 run, 24 minutes, 102 tool uses, 74 messages, 247 k output, 698 k fresh, 20.6 M cache reads; the lead 34 tool uses, 38 k output, 98 k fresh, 26.6 M cache reads. Confirmed.

Cleanup (lines 329 to 332). `git worktree list`: only the main checkout and my worktree remain. `git branch --list "r2-*"`: none, so no planted branch is left; `ls-remote --heads origin`: only main. Two other branches, verifier-P3-commit and verifier-P4-commit, point to round 1's commits (28082eb and 4d11e60 with their check commits), not to round 2's; not a finding. "No finished agent left a process running": not determined beyond the gate and build processes, none of which is running now.

Wrong answers, to send back (S):
- S1, line 93, the 19:37 row: "six wrong answers in this file (the last section)". The six were in the opening (lines 13 to 14), the setting (lines 40 to 42), the cost section (lines 251 to 253), and "What happened" (lines 111 to 112 and 118 to 120); only the placeholder was in the last section. The label misnames where they were. Fix: drop the parenthetical or list the sections.
- S2, README.md line 218: "the briefs as each stood when its agent was dispatched". False for verifier-plan's first pass: it was dispatched at 13:40, and the shared briefs _common.md and _verifier.md were revised at 14:22 (lead.md, 14:22:22), so the archived versions are not the ones it read. The parenthetical covers later passes only. Fix: say that verifier-plan's first pass read the shared briefs as they stood at 13:40, before the 14:22 revision, which lead.md records. The ledger has no history from which the 13:40 text can be restored.
- S3, VALIDATION.md heading 2168, case study lines 343 to 345 ("asked whether three gates had run at once, which the gates' own times answer: / they had not"), and lead.md 19:38:26 ("So three gates did not run at once"). Wrong as worded: for 13 seconds three full gate runs were in progress (16:44:11 to 16:44:24). Fix: "the controls stages never overlapped" (true by the stage records above).

Restates, to merge with the change (R-a to R-e):
- R-a, lines 196 to 226 and VALIDATION.md 2123 to 2130: the slip lists are partial. The case study's omits lead.md 15:24:47 (10b6b17's message, false about render.render()); the round's VALIDATION list is partial too, and the new entry does not extend it. Say the lists are partial, or add the item.
- R-b, line 190, "All twelve agents sent a test message": twelve subagents, eleven of the build plus verifier-CS (lead.md 19:13:14 counts twelve). The cost table's "12" counts the lead instead. Say which.
- R-c, line 68, the 14:17 row: the lead's receipt time (lead.md 14:17:38, "about 14:17"). verifier-plan's own stamp for its report is 14:15:26 (verifier-plan.md line 125, which says the report "was appended" then). The intro says the times come from the ledger's own stamps. Say which.
- R-d, line 327, "byte for byte the build (39 of 39)": name the build, 7f2d51b, since eb90939's public/MANIFEST differs from the live one by design.
- R-e, lines 329 to 330, "No finished agent left a process running": not verified; drop it or say what was checked.

Decisions and notes for the lead:
- The N1 settlement (lead.md 19:38:26 and 19:41:33) is right in substance; the stage records above support the controls-stage version. Only S3's wording needs changing.
- verifier-plan's first-pass briefs cannot be restored from the ledger, so the README must say the exception (S2).

Verdict: NOT READY, on S1 to S3, each a one-line fix. R-a to R-e merge with the change. Everything else in the diff holds: W1 to W6 answered; R1, R2, R3, R5 to R9 and R11 answered; N1 settled on the stage records; the trap, the corrected entry and the archive (35 files, byte for byte) check out; the gate passes.

Not determined: (1) whether any parcel's own control run overlapped e349b1a's controls stage (the lead's 19:41:33 correction says so); (2) the verbatim text of verifier-P3's report, which exists only as the lead's quotations, though the design words it quotes match P3.md.

Believed:
- The revision answers what pass 1 found, and the three wording faults are the only things a reader would act on wrongly.

For: the lead; the case study (S1 to S3, R-a to R-e); README.md (S2)
