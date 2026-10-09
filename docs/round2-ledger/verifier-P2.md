
## 2026-10-08 17:21:48 -0700 - verifier-P2 starts; the test escalation went to the lead

Measured:
- I sent the lead "verifier-P2: test escalation" through SendMessage, to "main". The runtime queued it for the main conversation's next turn, so this runtime can message the lead.
- My clone is at 2093b9d on r2-plant-P2, with a clean tree. Python prints 3.12.9. The brief's setup passes: --check says the 39 published files are exactly what the pins render; --numbers 0 problems and 3061 marks; --links 0; --local-only 0; --verify-facts 1853 read again and the same, 54 stated, 0 skipped.

Believed:
- Nothing yet. I have read the README, lead.md and the two briefs. I have not read the parcel's file, P2.md, and will not until I have formed my own view.

For: the lead, the case study

## 2026-10-08 17:45:45 -0700 - verifier-P2's report on 2093b9d: NOT READY; two sentences the commit adds are contradicted by their sources at the pins

Measured:

Overall: NOT READY. The commit adds two sentences that their sources at the pins contradict: D1, a round label, and D2, a round scope. Both are regressions. Send back for D1 and D2. D3 and D4 are wrong labels that predate this commit; by the brief's rule a label that misnames its source sends work back, so the lead may send them back or restate them at the merge. S1 to S4 are restate or known-limit items, not send-backs.

Defects:
- D1, regression, send back. work_parcelround.py, Verified (work-parcelround.txt line 18): "The fifth round's case study records what that round added: 'a gate of its own, tools/check_method.py, and an adoption record, ADOPTION.md, one row per proposal.'" The quotation is CASE-STUDY-6.md:35-37, under "What was new against rounds 1 to 5", so it is the sixth round's record. The fifth round is CASE-STUDY-5.md, which predates the gate. The README's table names CASE-STUDY-6 "A sixth round".
- D2, regression, send back. method.py section III, item 8 (method.html): "Across its rounds, its planted faults: ten of ten caught, from the sources." The figure is round 6's alone: CASE-STUDY-6.md:152 heads round 6's planted faults (eight in the four wave-1 copies, two in wave 2). Round 4 counted its own planted faults as "equality with the authority passed 10 of 11 planted certificate faults" (CASE-STUDY-4.md:94), so the total across rounds is not ten of ten. The same block's note says "none is a total across rounds" (method.py:149-151), which this sentence contradicts.
- D3, wrong label, predates P2. method.py, ratio block (method.html): "The one measurement on record is ParcelRound's second round, where its own accounting puts the human-active time at 1 h 38 min against 23 h 40 min of API time across every agent." CASE-STUDY-2.md:34-36 says "the desktop app's own accounting puts the human-active time at 1 h 38 min against 23 h 40 min of API time". The accounting is the app's, not the round's. P2 did not change this block.
- D4, wrong label, predates P2. work_parcelround.py, Test it: "Try the method's own seam test on a codebase you already know: list every file each of several independent changes would touch, and see whether one file appears in several such lists at once." METHOD.md:118-120 is the P0 step ("Before dispatching anything, list every file each parcel would touch"). METHOD.md:1200-1202 uses "seam tests" for a test run at each merge that exercises two parcels together. The sentence names the listing a seam test.

Side notes (not send-backs):
- S1, restate. work_parcelround.py's Verified quotes check_method.py:10, "It reads structure and citations, never what a rule says", and omits lines 11-12: "A gate that reads a rule's wording is a stated limit, not a guarantee ... Checks 7 and 9 read text, and are such limits." Checks 7 and 9 do read text: the gate's run prints "29 loganw.dev patterns and 6 HonestFramework passages read". The quotation is exact, but its cut drops the source's own limit. Quote both sentences, or restate.
- S2, known limit, state it. adoption_state refuses an unknown status word and a file with no rows (V2 and V6 below). It does not refuse a status that begins with a known word (V3), and it drops a table row whose id is not CS, B, R or S (V4), with no refusal. Neither shape is at the pin. The docstring states only the status refusal. ParcelRound's own gate (check 3) refuses such a row; the fact does not.
- S3, restate the commit message. It says "every file other than the five of these pages differs in fact ids only". True of the 14 rendered pages and texts (my script: 14 of 14). Not true of MANIFEST and facts.json, which gain entries and new hashes.
- S4, restate, predates P2. method.html says "Mercenaries2's README credits substantial AI assistance." The README's line is "**Gemini** (Google) — substantial AI assistance throughout the project", so the sentence drops its subject.

Item 1 (every sentence of the pages' own words): defects D1 to D4; the rest confirmed.
- Commands: git diff 427900e 2093b9d on the four modules; read the rendered public/work-parcelround.txt, public/work-honestframework.txt and public/method.html; checked each sentence against ParcelRound at f42242e (git show f42242e:<path> for README.md, METHOD.md, ADOPTION.md, CASE-STUDY-2.md to CASE-STUDY-6.md, tools/check_method.py, templates/brief.md and templates/verifier.md), HonestFramework at 65447fd, Quantum-Film at 3a73823 (README.md:341-342) and HonestHarness at b310f82 (README.md:3-4).
- Observed: apart from D1 and D2, the new sentences say what their sources say at the pins, in tense, scope and quantity. The counts (item 3), the models and plants (item 5) and the removed items (item 6) are right. The Test it and Prove it wrong items point at things that exist: CASE-STUDY.md's worked example (line 110), CASE-STUDY-6.md's timeline heading (line 51), archive/round6-ledger.zip (present at the pin), the templates' tags "(§3)" and "(own)", README's "The clearest single argument for it" heading, and HonestFramework's check_claims.py, which checks links, the mechanism count and the case-study total (checks 1 to 3).
- No pronoun for a person other than Logan, and no Wally, in the five changed pages (trap 18). The only "their" are generic.

Item 2 (quotations and where they are cut): confirmed, with S1 and S4.
- Commands: as item 1. I copied the pinned files into scratch and searched each quoted passage in them.
- Every quotation is exact at its pin, as the build's prose() matches also show. The cuts are faithful except S1 and S4. Quantum-Film's composite "credits AI collaborators (...) as contributors equal to the human one" is faithful to README.md:341-342 at 3a73823. HonestFramework's paraphrase "the blinding was never verifiable from the record" is faithful to METHOD.md:689-691 at 65447fd.

Item 3 (adoption_state): confirmed at the pin; S2 is the shapes it does not refuse.
- Commands: my own count of ADOPTION.md at f42242e, by awk over its table lines: 123 lines starting with "|" (header, separator, 121 rows). Ids: CS 97, B 13, R 5, S 6. Status cells, before " at": adopted 87, adopted in part 8, pending 23, not adopted 3. The gate printed "121 ids in ADOPTION.md" and "95 adopted rows" (87 + 8).
- Variants, by a script under scratch (python -B adoption_test.py): the fact called through a stub pin on in-memory copies of the pinned file, nothing written to a repository. V0, the pinned file: "121 rows: 87 adopted, 8 adopted in part, 23 pending, 3 not adopted". V1, one pending row made adopted: 88, 8, 22, 3, read. V2, status "deferred until round 9": REFUSED by name. V3, status "adopted, partly at ...": counted as adopted (122 rows, 88 adopted), not refused. V4, a row with id X1: dropped (121 counted of 122 rows), not refused. V5, a CS9#3 pending row: counted (122 rows, 24 pending). V6, a file with no rows: REFUSED.

Item 4 (the gate): confirmed.
- Commands: git clone --no-local of my ParcelRound clone into scratch; git checkout --detach f42242e (HEAD confirmed f42242e); python tools/check_method.py, exit 0, "PASS: 10 of 10 checks hold"; python tools/check_method.py --control, exit 0, "controls: 50 of 50 caught".
- The page's account of the gate matches its docstring and README.md:29 word for word (checked check_method.py lines 5-8, 10, 14, 16, 23, 26, 31, 90-91, 145-146 and 157-158). "This page quotes the gate and does not run it" is true. The page prints neither count. The one cut is S1.

Item 5 (models and plants, rounds 5 and 6): confirmed, except D2.
- Round 5: "Planted controls caught 2 of 2, twice. The second could have been passed by a diff." (CASE-STUDY-5.md:158-159) and "The parcels and their verifiers ran on Sonnet 5" (:31). Exact.
- Round 6: "the lead and every verifier on Opus 5.5, the five parcels on Sonnet 5.5" (CASE-STUDY-6.md:48-49; the cost table at :305-319 agrees). "ten of ten caught, from the sources" (:152), round 6's own, eight plus two. "Of its 84 faults, 47 caught; of the 37 that passed, 25 lay outside every limit the gate stated" (:57). "no parcel went back; the round's one wrong answer was the lead's (obs 4)" (:131-132). All exact.

Item 6 (what was removed): confirmed.
- CASE-STUDY.md has no clock time (no hh:mm), no hex run of seven or more characters, and no "timeline" word, so the three never-true sentences are gone. "under a second" is not in any site/ file, and HonestFramework at 65447fd has no such timing (README.md, METHOD.md, CASE-STUDY.md and tools/check_claims.py searched). The quotation mark is closed.
- Nothing left points a reader at a source that lacks its content: each reference listed under item 1 resolves. D4 is the one wrong label left.

Item 7 (Logan's words): confirmed.
- git diff 427900e 2093b9d -- site/pages/method.py changes the page description, the lede, the section II gate sentences, section III's heading and items, and the render heading. No stated() call, STATEMENT_9, ONLY_HERE, ratio block or co-authorship block changed. propose.py has no diff; its LICENSE reads ("MIT License") are the same blob at 8767e23 and f42242e. The three thread doors are rendered from other parcels' pages, and this commit does not touch them.
- P2.md's watch item, "It will be measured from now on": no ParcelRound case study at f42242e records a human-active time (grep: CASE-STUDY-2.md:35, :36 and :532 only), so "one measurement on record" still holds.

Item 8 (P2's controls): confirmed. I ran all four, each in a copy with its edit made in the copy only.
- 1, a figure typed in place of adoption_state(NAME): build exit 0 ("1906 figures in facts.json"); --numbers exit 1 with ten problems: "PROBLEM work-parcelround.html: '121' is a numeral outside any figure's mark, in ..." and the same for 87, 8, 23 and 3, in the .html and the .txt. The same as P2's control 1.
- 2, the fact's label naming archive/round6-practice-survey.md, which SOURCE_PATHS does not list: build exit 0 ("1907 figures"); --numbers exit 1: "PROBLEM facts.json: fact 1733's label 'ParcelRound f42242e archive/round6-practice-survey.md' isn't one the build writes for a source". P2's own variant (ADOPTION.md taken off the list) gave three problems; I did not re-run that variant.
- 3, a prose() pattern with the README's old words "It's the only way to / correct a brief after dispatch" (gone at f42242e): build exit 2: "REFUSED: ParcelRound f42242e README.md: the pattern ... no longer matches".
- 4, a citation of CASE-STUDY-7.md through facts.exists: build exit 2: "REFUSED: ParcelRound f42242e has no CASE-STUDY-7.md". The same wording as P2's control 4.
- Each refusal is its own rule's message.

Item 9 (scope and the commit message's claims): confirmed, with S3 and the D2 contradiction.
- git diff --stat 427900e 2093b9d: 24 files. method.py 54 changed lines, work_honestframework.py 4, work_parcelround.py 160, and 21 under public/. The three modules total 186 added and 32 removed. No other site, docs, pins or propose.py change.
- The commit's line references all sit at the cited lines: README.md:29; check_method.py:10, 14, 16, 23, 26, 31 and 214; CASE-STUDY-6.md:36, 152, 163, 187 and 188; METHOD.md:3-6 and 569-572.
- In my clone: --check exact; --numbers 0 problems and 3061 marks; --links 0; --local-only 0; --verify-facts 1853 the same, 54 stated, 0 skipped. In a copy, a build writes "39 files from 20 pins; 1907 figures". The site's controls, run on an unmodified copy: "controls: 386 caught, 0 did not fail, 0 skipped by name" (exit 0).
- Overstated in the message: "differs in fact ids only" (S3), and "says none is a total across rounds" (contradicted by D2).

Item 10 (anything else):
- After forming my view I read the parcel's file, P2.md, and compared the commit's new text with the design its entry of 15:54:48 records. They match sentence for sentence except two, which are D1 and D2: the design says "The sixth round's case study records" and "Its sixth round's planted faults: ten of ten caught". I did not use the design to find D1 or D2.
- Gemini trailers, counted at all 20 pins through the site's own pin reader (scratch script gemini_trailers.py): one commit names Gemini, Mercenaries2's d66f97a, of its 46 commits. The page says so.
- The kept-failure commits f2a0483 and 42e76cc (CASE-STUDY-2's subjects) and 1dc5ed4 (the gate fix) are ancestors of f42242e, and their subjects match the page's descriptions.
- HonestHarness: its README's first sentence is the connection text ("A harness for running ParcelRound and HonestFramework on open-weight models", b310f82 README.md:3-4).

Believed:
- I have not identified any plant, and I do not know the key. The findings are for the lead to match.
- The quotations are as exact as the build's prose() matches make them. I read the Quantum-Film and Mercenaries2 passages only at the lines cited.

Not done (last, as the brief asks):
- I did not run the full gate (bash verify/run.sh --require-all). The lead runs it; its record for 2093b9d is in lead.md (386 caught).
- I did not re-read the full text of the other agents' files at this moment. I read the directory listing; lead.md's entries after 17:17, in full; P2.md, in full; the headings of P1.md, verifier-P1.md, P3.md and verifier-P3.md; and a search of the ledger for P2's name and commit. I did not open round 6's archive, and ParcelRound's case study 7 is not at the pin.
- I did not identify plants, did not look for the key, changed no tracked file, and pushed nothing.
- Background work: the site's control run (exit 0) completed before this report. No process of mine is running, and I started no subagent.
- Scratch: deleted the faulted and build copies (copy-A, copy-B and the gate's clone). Kept my clone at 2093b9d, the exports of pinned files (pin, pin-hf, pin-qf, pin-hh), the scripts (adoption_test.py, fact_ids_check.py, gemini_trailers.py) and the outputs.

For: the lead (the send-back for D1 and D2; the choice on D3 and D4; the restates S1 to S4), the case study
