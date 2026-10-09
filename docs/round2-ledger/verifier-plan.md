
## 2026-10-08 13:43:52 -0700 - the test escalation sent, the plan fast-forwarded to 6ec5616, the ledger read before starting

Measured:
- The test escalation: a message to the lead (the main conversation) with the line "verifier-plan: test escalation" returned success, "Message queued for the main conversation's next turn". So this runtime can message the lead.
- My worktree was one commit behind, at 43c36a2. A fast-forward-only merge to 6ec5616 advanced it, adding docs/ROUND2.md (307 lines). The worktree is clean.
- The ledger directory, read before starting: README.md, lead.md, briefs/verifier-plan.md, tools/round_metrics.py. No other file is in it.

Believed:
- Nothing yet.

For: the lead, for the escalation's result.

## 2026-10-08 13:59:40 -0700 - the plan's P0 fixes for the two refusals do not clear the build: Verify has two more patterns that fail at ab51655, one of them changed in its words

Measured:
- Re-ran the trial's page script (`<scratch>/r2-trial-pages.py`) on a copy of the trial worktree, in my scratch directory. The same three refusals: pages.home, pages.verify, pages.work. Seventeen lines OK, including check_workflows and check_pins.
- Surveyed every literal prose() pattern in site/pages at the pins the trial moved to. Three match nothing at the new pins, all in verify.py: line 27 (CONFORMANCE.md, the one the plan names), line 63 and line 68 (both docs/VERIFICATION.md). Patterns passed as variables are not surveyed; the trial covers those.
- The CONFORMANCE.md fix is only whitespace: at ab51655 the current pattern matches 0 times, and with each literal space made \s+ it matches once.
- In a copy with the plan's fixes applied (the Map & Ledger statement removed, the CONFORMANCE pattern made whitespace-tolerant), pages.verify refuses at line 63. Making every space in both docs/VERIFICATION.md patterns \s+ does not clear it. At ab51655 the words differ: the `quick` list names innerskips and ensurevectors, and no longer the GPU's photograph; the `gate` list reads "lint, formal, the C auditor's gate" where the pattern says "lint and formal)".
- The statement the plan removes is Logan's: site/pages/home.py calls S(...), which is facts.stated(text, "Logan", "2026-09-29", holds_at={"cft-fp256": "77b8440"}). Work reaches the same statement through home.rows().

Believed:
- The plan's P0 bullet ("the two refusals ... fixed only as far as the build needs") cannot be done as written. Verify needs two quotations restated, not reworded by whitespace, and the restatement changes what the page says. That is P1's text, but P0's gate needs the page to build.
- "No word of Logan's is changed or needed" is false for the Map & Ledger fix: removing the sentence changes his words, and the plan's own rule says they change only at his word.

For: the lead, for the plan's next draft and for P0.

## 2026-10-08 - the report: NOT READY; eight defects in draft 1 at 6ec5616; side notes; what I did not do

Measured:
Scope: docs/ROUND2.md at 6ec5616, draft 1, checked against the tree at that commit, the pins (read-only commit reads and gh api), the lead's files, and ParcelRound's METHOD.md and checklists at f42242e. Scripts and copies are in <scratch>/r2-verifier-plan/. No tracked file was edited.

Commands, in short: measure_pins.sh (gh api for the 20 pins, HonestHarness included); r2-trial-pages.py on a copy of the trial worktree; compare_text.py and compare_keys.py (trial facts against public/facts.json); survey_patterns.py (every literal prose() pattern in site/pages, at the old and the new pins); check_conformance.py; a trial-fixed copy (Map & Ledger's Logan sentence removed, the Verify patterns made whitespace-tolerant), page run again; check_quotes.py; check_names.py; round_metrics.py on the lead's session transcript from 2026-10-08T20:16:10Z; pin_dates.py.

VERDICT: NOT READY. Defects D1 to D8 below; side notes after them.

1. SHAs, counts and dates. DEFECT (D3) for the 17; all others CONFIRMED.
- The seven moved pins and counts match: cft-fp256 77b8440 to ab51655, 381; ParcelRound 8767e23 to f42242e, 37; Quantum-Film a7f02db to 3a73823, 171; StoryDocs 673148c to 8548802, 1; mercs2-modkit 3a4d888 to 9acb750, 5; mercs2-wad-simulator fdf3597 to d18af76, 409; notes-on-the-released-game b8c3958 to dac773d, 70. The other 12 pins equal their default branch.
- HonestHarness: created 2026-10-03, public, main b310f82, README "Status: research. There is no code yet.", zero workflows; GitHub has only main (the local clone also has r1-p1 to r1-p5 and round1).
- ParcelRound at f42242e has ADOPTION.md, tools/check_method.py, and CASE-STUDY-5 and -6 added in round 6. Case study 7 is on branch case-study-7 at 894d125 (GitHub agrees) and is not on main.
- The trial's pins diff is the seven pins plus the snapshot. Its three refusals reproduce: pages.home, pages.verify, pages.work. Fifteen page modules render, with check_workflows and check_pins OK.
- The 17 figures reproduce for the pages that render. But each page stops at its first refusal, and Map & Ledger and Work both stop at the Logan sentence. With that sentence removed in a copy, both pages render and five more numerals change: agent-credited counts cft-fp256 1030/1079 to 1408/1460, Quantum-Film 60/60 to 231/231, ParcelRound 86/86 to 123/123 (home.py:60); ParcelRound's CASE-STUDY file count 4 to 6 (home.py:108); METHOD.md's last change 2026-09-16 to 2026-10-03 (home.py:109). At least 22 figures change. Verify's facts after its quick refusal were not reached.
- P1: cft-fp256's ledger headings run from revision 7 (2026-09-29), through the certificate plan's steps, the fixes round, the language round, and step 6 (from 2026-10-02), to its closing records on 2026-10-06 with revision 8's first hardware image. ABI 0.15 to 0.18 (the trial's macros fact). CONFIRMED.
- P2: CONFIRMED. P3: the IBM devices are ibm_kingston, ibm_marrakesh and ibm_fez; "Heron r2" and the pre-registration are stated in the README and docs/HARDWARE-RESULTS.md; the paper (docs/chance-made-permanent.pdf), the poster and the web demo changed; StoryDocs 8548802 changes only projects/quantum-film. CONFIRMED. P4: CONFIRMED.

2. Logan's decisions and request, word for word against lead.md's first entry. CONFIRMED. check_quotes.py: all 12 double-quoted passages in the decisions section appear verbatim in lead.md's first entry, and the request matches lead.md line 7 word for word. The lead's readings of decisions 3 and 4 are marked. The reading of "verifiers" is marked too, but it conflicts with SPEC decision 24 (D4).

3. Paths, functions and ownership. CONFIRMED. check_names.py: every backticked path exists at 6ec5616, except tools/round_metrics.py (in the ledger) and tools/check_method.py (at f42242e). build.SOURCE_PATHS exists (build.py:82). No file is on two parcels' lists.

4. Completeness of the split. CONFIRMED, with side notes; no file is missing, and no file needs writing by two parcels.
- ParcelRound's README is read by P1's thread_determinism.py (lines 38 to 40), which P1's "What moved" omits. The quoted sentence is unchanged.
- Quantum-Film's README is quoted by P2's method.py (lines 180 to 183). The quotes still match at 3a73823. P2's "What moved" omits Quantum-Film, and P3 does not own method.py.
- propose.py (P2) imports the three door() functions (P1, P3, P4 files). Its door-retyped control needs the word "workloads" in P1's Determinism door (lines 96 to 97 and 124 to 137). The doors are Logan's words and the P1 brief keeps them, so there is no conflict today; the plan does not say so.
- _p5.py is imported by method.py (P2) and about.py (the lead). It is in no list.
- The IBM print as the Film thread's own ASSETS is feasible: build.py:216 reads ASSETS from every page module, so thread_film.py can declare it, and home.py needs no edit.
- The ParcelRound "check it" link is in home.py:110, the lead's file. Feasible.

5. The two refusals' fixes in P0. DEFECT (D1 and D2).
(a) Map and Ledger. The statement is home.py:86: S("a revision-7 round is under way off main", holds_at={"cft-fp256": "77b8440"}). S is facts.stated(text, "Logan", "2026-09-29") (home.py:34 to 35): Logan's word. Work reaches it through home.rows() (work.py:38), so one fix clears both pages, which the plan does not say. The plan says no word of Logan's is changed or needed. Removing the sentence changes his word, and the replacement figure is not named.
(b) Verify. The CONFORMANCE fix works: check_conformance.py finds 0 matches for the current pattern at ab51655, and 1 match when every literal space is replaced by backslash-s-plus (and 1 at 77b8440). But two more patterns on the same page fail at ab51655: verify.py:63 (docs/VERIFICATION.md, "quick is ...") and verify.py:68 ("gate adds ..."). With the plan's fixes applied to the copy, pages.verify still refuses at the quick pattern. Making every space into backslash-s-plus in both does not clear it, because the words changed at ab51655: quick now names innerskips, ensurevectors and the language's compiler, with no GPU photograph; gate runs on past "lint, formal" to the C auditor's gate. So P0 cannot pass its gate as the plan describes.

6. The rules the plan carries. DEFECTS D4, D5, D6; the rest CONFIRMED against their sources:
- Full gate before every push; a push to main deploys (CLAUDE.md, "Run this before every push ... (Logan, 2026-09-29)"; SPEC decision 7).
- Only main is pushed (CLAUDE trap 17). Shared core first, then a verifier, then the round (SPEC decision 18, verbatim).
- Seams, merges and records go past a verifier before main moves (METHOD section 7). Agents test quickly and hand large runs back: the owner's rule of 2026-09-29, quoted in METHOD section 7.
- Send-back: only a regression or a wrong answer sends work back (METHOD section 6). That owner's rule is dated 2026-09-27 in METHOD; the plan gives no date.
- He and his (CLAUDE trap 18; SPEC decision 28). Email only logan@loganw.dev (trap 14). Wally only on the Preservation thread's page (trap 16; SPEC decision 16); build.py's ONLY_IN also allows facts.json.
- Planted faults "can be light" (SPEC decision 20, verbatim). A re-check is scoped to the diff (METHOD section 6: "The scoped re-check after a fix is the default").
- READY is "a gate, or a stated limit" (METHOD sections 3 and 6). The plan's added clause, a gate the verifier has watched fail on a fault it picked, follows METHOD sections 5 and 6.

D4 (models). DEFECT. SPEC decision 24: "Every parcel, and each parcel's own verifier, is dispatched on Sonnet. The verifier of the shared core, which is code, stays on the lead's model." The plan reads Logan's request as Haiku for every verifier, the shared core's included, and calls that the lead's reading. It never mentions decision 24, and its P0 bullet adds decisions 31 to 35 ("the models") beside it. P0 commit 05413b2 does exactly that: decision 24 is unchanged, decisions 31 to 35 are added, and decision 35 ("every verifier of the round included") sits under "His answers to the lead's questions, verbatim", though it is the lead's reading of the request. The record now holds two conflicting model rules, and moving the shared core's verifier off the lead's model overrides a standing owner rule.

D5 (three passes; asks Logan). DEFECT. The plan's "What READY means": "Each verifier has up to three passes. ... If a third pass still finds a wrong answer, the lead records it and asks Logan before going on." Searched and not found in METHOD.md (the words "three passes" occur once, as a case-study observation at line 945), templates/verifier.md, ROUND1.md, SPEC.md, CLAUDE.md, README.md, or HonestFramework at 65447fd. The lead's shared brief (briefs/_verifier.md, lines 75 to 76) says "You have up to three passes" without the Logan step. The nearest source is HonestHarness round 1's brief ("Two full passes at most", its briefs/_verifier.md lines 82 to 85); its third pass was granted by Logan on 2026-10-06 (its lead.md line 441). So the rule is the lead's.

D6 ("Logan's own words change only at his word"). DEFECT. Stated in the plan's rules with no date and no source; not in SPEC.md, CLAUDE.md, METHOD.md, ROUND1.md or README.md. It conflicts with corrections.py's docstring (lines 1 to 6: the "where I'd attack first" gaps "are Logan's") and with P1's trap, which requires a closed gap to change; P1's brief settles this by treating the gaps as record-derived. It also conflicts with P0's removal of Logan's sentence (D2). The plan's header says each rule carries the date it was given; this one has none.

7. The metrics plan. CONFIRMED, with notes. round_metrics.py on the lead's transcript, window 13:16:10 to 13:58:02 -0700, prints per agent: model from its own transcript, runs, minutes, tool uses, messages, output, fresh tokens (input, cache writes, output), cache reads, and context at end; then class totals. My row reads claude-haiku-5-5, running. The lead reads claude-opus-5-5. The columns match the plan and case study 7's table (tool uses, cache reads, fresh tokens, minutes). Case study 7, line 471, says a notification's "tokens" is the agent's context size at the run's end; the script prints that as "context at end". Notes: case study 7 omits the lead's session and case study 6 counts it, so the plan should say which it follows. The script does not produce the wall-clock split or the planted-fault yield by model; label those as hand work. The script has an "other" class the plan does not name. The requested model is in lead.md, not the script.

8. The planted-fault protocol. DEFECT (D7). A verifier can tell the plants from the work by means other than reading. (a) If the copy's public/ and MANIFEST are not rebuilt, the drift stage catches the plant unread: build.py --check exits 1 when public/ differs from a fresh render (build.py line 5; the drift control at build.py:3224 to 3241). (b) If they are rebuilt, the copy differs from the parcel's own commit in exactly the plant places, and a diff finds them when the parcel's commit is readable from the verifier's repository (any branch). The plan does not say the copy is isolated or that public/ is rebuilt. Case study 6 records the reference-copy lesson: a verifier who reads the design first finds plants by comparison alone (lines 160 to 165). The ledger README's read order protects the design, not the parcel's commit. So the planted-fault yield by model would measure diffing, not reading. The plants do not reach round2 if the lead merges the parcel's own commit by SHA; I checked only the plan's text for that.

9. The Before-dispatch checklist (templates/checklists.md at f42242e). Applicable items not met:
- DEFECT (D8): names its specific negative control and asks for its output. No parcel names one. Also DEFECT (D8): names the trap and what will be measured at verification; the traps are named, the measurements are not.
- Each value names the measurement that would falsify it: met for the table, not for P1 to P4's "What moved" values.
- Behaviour-preserving P0: P0 changes outputs by design (pins, the HonestHarness row, two quotations). The plan does not list the expected changes.
- Most likely regression per parcel ("own"): not in the plan. Expected small edits outside files: P0's verify.py edit is named; the cross-reads in item 4 are not.
- Base commit with the exact tip and a fast-forward check: "cut from round2 at P0's tip", with no check (the shared brief has it). Host build traps as verbatim commands: the .cache copy and LOGANW_REPOS are in the shared brief, not the plan. A scratch directory per agent: in the briefs, not the plan.
- The lead reads every author's file before each merge and at each wave boundary: not in the plan; the README's read moments include no merge.
- A seam changed mid-round is checked against every open branch: the plan's step 3 adds the seam commit after the parcels are cut. The shared brief has parcels fast-forward to the "go" SHA; the plan does not.
- A seam test per merge, and verifiers' side notes getting a step: neither is in the plan.
- The owner's decisions kept as given, with the lead's reading marked: not met for decision 35 in P0 and for decision 24's omission (D4).
Met: owned and forbidden files, with owners (the lead for every forbidden file); the documents among forbidden files; the escalation channel (lead.md records my test escalation at 13:41:56); the ledger's location and rules; the owner asked what he wants to see first (decision 3).

10. Anything else.
- D8 in full: Wave 1 says each parcel "runs the checks below", and the plan has none. The build's own controls (386 in the gate) run only in the lead's full gate, since the shared brief tells parcels not to run it. No parcel watches a check fail, and sentence-level claims have no gate or stated limit in the plan.
- HonestHarness's row asks for "last verified" and "a check". SPEC section 4 says a repository with neither a CI run nor a ledger line shows a dash with its reason. HonestHarness at b310f82 has no workflows and no VALIDATION ledger (14 files: research and round documents). The plan should say the cell is a dash with its reason, and define "a check" for a repository with no gate.
- P0 at 05413b2 already differs from the plan's text: it removes Logan's sentence (D2), rewrites two quotations (D1), and adds decisions 31 to 35 beside an unamended decision 24 (D4). Draft 2 should carry these.
- The trial paragraph's "the round's real work is not the build's refusals" is contradicted by D1: the refusals hid text changes.
- "The pages describe the projects as they were on 2026-09-29": the pins' committer dates run from 2026-06-30 to 2026-09-29. The pins were set on 2026-09-29; the sentence should say so.
- StoryDocs is private on GitHub (P3's brief says so); the plan does not, and SPEC decision 5 requires the "private for now" mark.
- docs/VALIDATION.md, the site's own ledger read by facts.own_prose(), is not mentioned; if the round appends entries, trap 15 applies (rebuild before committing; MANIFEST).
- _p5.py is shared by P2's method.py and the lead's about.py: list it. Wally is also allowed in facts.json (ONLY_IN).
- The lead's shared brief says "Logan's own words never change", and P0 removed one. The brief and the commit disagree.

Defects, each with its concrete failure:
- D1 (item 5b): after the plan's fix, Verify still refuses at the quick pattern, and whitespace-only fixes cannot clear it because the quoted words changed. A parcel or the lead would believe the refusals were fixed and find the gate red. P0 (05413b2) rewrote the two quotations, which the plan does not describe.
- D2 (items 5a, 6): the plan's Map and Ledger fix removes a sentence that is Logan's stated word, while the plan says no word of his changes. Under its own rule, removal needs his word. P0 (05413b2) removed it, and lead.md records no word from Logan for it.
- D3 (item 1): the 17 is a partial census. At least 22 change on the pages the trial can render once refusals are cleared, five of them on Map and Ledger. A review built on the 17 misses them.
- D4 (item 6): decision 24 is contradicted by the plan's model reading and is not mentioned. P0 records two conflicting rules and presents the lead's reading as Logan's verbatim answer. The shared core's verifier moves off the lead's model, which overrides a standing owner rule; Logan should be asked about that part by name.
- D5 (item 6): "up to three passes" and "asks Logan" have no source, and the lead's shared verifier brief already carries "up to three passes" to every verifier.
- D6 (item 6): "Logan's own words change only at his word" has no source and conflicts with P1's attack-first work and with P0's removal. A parcel cannot tell whether a "where I'd attack first" gap is Logan's to change.
- D7 (item 8): the planted-fault yield would measure diffing, not reading. The protocol needs an isolated copy, a rebuilt public/ and MANIFEST, and the parcel's own commit kept out of the verifier's reach.
- D8 (items 9, 10): no parcel names a negative control, and Wave 1 refers to checks the plan does not contain. Parcel reports would show build output only, with no property watched failing. The plan needs a control and a measurement per parcel.

Side notes: the list in item 10, and the item-9 checklist items the briefs carry and the plan does not.

Not done: I did not run the full gate; the lead's record of its pass at 05413b2 is in lead.md at 13:58:01, and verifier-P0 has the P0 checks. I did not verify P0 beyond the points that touch the plan (the removed sentence, the SPEC decisions, the pin and snapshot counts). The survey covers the 89 literal prose() calls; the 85 non-literal calls are covered only by the trial's rendering, and Verify's figures after quick were not reached. I did not check the P3 print's PNG chunks or the records path P3's brief cites. I did not read the lead's transcript beyond running the metrics script on it. I started no background processes, so none to stop. The cloudflare and runpod connectors need authorisation through /mcp or the claude.ai connector settings before their tools work; I used neither, and this report does not need them.

Believed:
- Draft 2 of the plan needs D1 to D8, and P0 at 05413b2 must be reconciled with it: several points are already in P0 and in the briefs.
- For D2, D4 and D6 the owner's answer decides the outcome; the lead should ask Logan, not infer it.

For: the lead (draft 2 of the plan; reconciling P0 at 05413b2; questions to Logan on decisions 24 and 35, and on the Map and Ledger sentence).

## 2026-10-08 14:15:26 -0700 - correction to the report entry headed "2026-10-08": its heading had no time or zone, which the README requires

Measured:
- The report entry above (its heading begins "## 2026-10-08 - the report: NOT READY") was typed without the time from date. Its stamp is this entry's time, the time the report was appended; its content is unchanged.

For: the lead, when reading the report by heading.

## 2026-10-08 14:39:06 -0700 - pass 2 of up to 3 on draft 2 at b6c7560: the checks, measured

Measured:
- My worktree was fast-forwarded to b6c7560 (6ec5616 is an ancestor). The range includes P0 at 05413b2. Draft 2's own commit changes only docs/ROUND2.md and docs/SPEC.md; no code changed in draft 2.
- Read docs/ROUND2.md in full (413 lines) and the SPEC.md diff: decisions 31 to 36 added; decision 24 unchanged. Read the revised briefs (_common.md, _verifier.md, P1 to P4, verifier-P0) and lead.md to its last entry (14:22:22). Nothing in the directory changed after 14:22.
- The lead's point on docs/VERIFICATION.md line 382: at ab51655 the quick sentence names "the GPU's photograph" (a grep for the phrase gives line 382). I agree with the lead. My pass-1 statement that quick "no longer" names the GPU photograph was wrong: I had read lines 377 to 380 only. The built Verify page quotes the whole quick sentence, GPU photograph included (verify.py line 66).
- Logan's answers at 14:18:37 are verbatim in lead.md: each quoted passage in ROUND2 lines 92 to 104 is found once there. SPEC decisions 35 and 36 match the answers, with one gloss inside decision 35 (see D4 below).
- Full build in a scratch copy of the tree at b6c7560: 39 files from 20 pins, 1864 figures (the lead recorded the same). Page run: 18 pages OK, no refusals.
- Census by unique method and arguments (the build's facts.json against the committed one at 43c36a2): changed text 27, gone 5, added 77. The plan's figures are right. Counted as calls: changed 220, added 134, gone 7. My pass-1 figure "at least 22" came from a page-run script, which does not log footer facts, so it undercounted.
- Controls run in scratch copies. P3 (a tEXt chunk added before IEND in ibm-kingston-pauli-4x4-print.png, passed to build.check_asset): refused by name, "a PNG chunk no check reads: tEXt"; the unmodified print is accepted. P4 (an address other than the contact, and the name Wally, planted in about.html, then build.check_local_only): both refused by name.
- Controls read but not run. P2's citation of CASE-STUDY-7.md: facts.exists raises "has no CASE-STUDY-7.md". P1's _entry_at: raises "no ledger entry heading at line N". The shared hand-typed-figure control: verify.py plants a hand count and check_numbers must catch it, and it is among the gate's controls. The shared prose() control: refused by construction (the trial showed "no longer matches"). The SOURCE_PATHS label control: a label whose path is not listed does not fit the label shapes in check_numbers.
- P3's brief claim: all 18 docs/prints/ibm-*.png at 3a73823 hold only IHDR, IDAT and IEND chunks (measured by reading each file's chunk types). Confirmed.
- The pins re-measured at 14:3x with the same hosting-service command: unchanged. cft-fp256 ab51655 (381 ahead); ParcelRound f42242e (37); Quantum-Film 3a73823 (171); StoryDocs 8548802 (1); modkit 9acb750 (5); wad-simulator d18af76 (409); notes dac773d (70); HonestHarness b310f82, identical.
- HonestHarness's row as built: last verified is a dash with the pin label, and the page's glossary says a dash means neither a CI run nor a ledger line. Its check cell links Research/open-weight-harness-requirements.md at b310f82, a document rather than a check.
- The Verify gate sentence as built reads "... lint, formal - those need make verify-gate", which presents the list as complete. P1 owns the wording.

## 2026-10-08 14:39:54 -0700 - pass 2: each of my eight defects, and each side note, answered or not

Measured (status against draft 2 at b6c7560 and the revised briefs):
- D1 (Verify's refusals were not all named in P0): ANSWERED. The P0 bullet names all three (CONFORMANCE whitespace; quick requoted as the page now writes it; gate quoted to "lint, formal"), and P0 at 05413b2 does it (verify.py lines 64 to 72). P1 owns the wording. My correction on the GPU photograph is above; the substance stands, because a whitespace fix could not clear quick once three items were added.
- D2 (Logan's sentence removed, with "no word of Logan's changed"): ANSWERED. Logan's answer 2 (14:18:37) allows a stated line that a pin overtakes to be replaced by a figure read from its source, recorded in the ledger. Decision 36 records it (ROUND2 lines 126 to 132; _common.md). The "no word of Logan's" sentence is gone from the plan. The replacement reads the newest heading of cft-fp256's docs/VALIDATION.md at ab51655 (line 18544, dated 2026-10-06, "step 6's closing records, part two"), which is the last heading in the file. Work is cleared by the same change (work.py line 38 reads the rows).
- D3 (census understated): ANSWERED. ROUND2 lines 56 to 61 now give 27, 5 and 77, which the full build reproduces by unique method and arguments. The unit is worded as "fact call" (side note below).
- D4 (decision 24 against the Haiku reading; decision 35 misattributed): ANSWERED by Logan's answer 1 (14:18:37): every verifier on Haiku, the lead's work included, and decision 24 stays as round 1's rule. Decision 24's text is unchanged. PARTLY: SPEC decision 35 still ends with an unmarked gloss inside Logan's verbatim list ("With the request's ..., round 2's parcels are on Sonnet and every one of its verifiers on Haiku."). It is accurate, so it is a marking point, not a wrong answer.
- D5 (three passes and asks Logan, unsourced): ANSWERED by marking. ROUND2 lines 396 to 402 call it "the lead's own rule for this round, not the method's", with its reason; _verifier.md says the same. PARTLY: its stated rationale is wrong on the record (new defect D-B below).
- D6 (Logan's words rule unsourced; conflict with P1's attack-first work): ANSWERED. The rule is sourced to decision 36 and Logan's answer 2. P1's brief separates the gap names (Logan's: not to be dropped or renamed) from the quotes beneath them (cft-fp256's: to be re-read), and sends a closed gap to Logan through the lead. Side: CLAUDE trap 12 supports only the mechanism of stated().
- D7 (plants detectable by drift or by diff): ANSWERED, with the limit stated. The copy's public/ is rebuilt and must pass the full gate before dispatch, so the drift stage does not point at it. The verifier's clone is made from one branch holding round2's history and the plant, so the parcel's own commit is not in it. _verifier.md puts every other branch and worktree out of bounds. The remaining route, a verifier who leaves its clone, is a stated limit, and the yield is read with it (ROUND2 "The limit"). Side: the plant branch's removal after the key is published is not stated.
- D8 (no controls; "checks below" with nothing below): ANSWERED. The checks are listed (ROUND2 lines 224 to 226). Each parcel runs three shared controls (lines 228 to 235; _common.md) and one of its own (P1 to P4). The limit for sentence truth is stated (lines 237 to 241). Run: P3 and P4. Read: P1 and P2 (see Measured above). The SOURCE_PATHS control is read from the label checks, which refuse a fact label that fits neither the source shape nor this site's own path.
- Side notes from pass 1, status: HonestHarness's "last verified" dash: ANSWERED (ROUND2 lines 196 to 198; the built row); "a check": PARTLY (a document link, which the plan does not say). P0 against the plan's text: ANSWERED. "The real work is not the build's refusals": ANSWERED, but see D-A. "As they were on 2026-09-29": ANSWERED (reworded to round 1's pins). StoryDocs is private: ANSWERED (ROUND2 line 36; P3 lines 288 to 291). The site's VALIDATION entry: ANSWERED (ROUND2 lines 160 to 162). _p5.py: ANSWERED (What no parcel touches; the P2 brief). Wally in facts.json: ANSWERED (ROUND2 lines 136 to 137).
- Checklist items from pass 1: behaviour-preserving P0 with its changes listed: ANSWERED (the census and P0 section). Each value naming its falsifying measurement (P1 to P4's What moved): NOT ANSWERED (the sections give no command). Most likely regression per parcel: NOT ANSWERED. Cross-reads as expected edits: ANSWERED. Fast-forward to the base commit before building: ANSWERED (shape step 3; _common.md Phase 2). Host traps and scratch directories: ANSWERED (_common.md). The lead reads every author's file before each merge: ANSWERED (shape step 5). A seam changed mid-round: ANSWERED (shape step 3, the go SHA). A seam test per merge: ANSWERED (shape step 5, the full gate). Verifiers' side notes: ANSWERED (shape step 6). The owner's decisions with the lead's reading marked: PARTLY (decision 35's gloss). Subagent disclosure: NOT ANSWERED (not in the briefs). Boundary crossings: ANSWERED (_common.md, Report).
- Metrics notes from pass 1: the lead counted in case study 6 and not 7: ANSWERED (ROUND2 lines 359 to 362). Wall clock and yield by hand: ANSWERED (lines 374 to 378). The script's "other" class: NOT ANSWERED (trivial). The requested model: ANSWERED (lines 364 to 365).

## 2026-10-08 14:40:01 -0700 - pass 2: the new faults I found in draft 2 and the briefs

Measured:
- D-A (defect, low; ROUND2 lines 59 to 61). The sentence reads: "the pages describe the projects as round 1's pins had them, and every quote on them still stands, so every gate passes." It is false of the move: two lines earlier the same section says the trial refused Verify at its CONFORMANCE pattern and that P0 "met two more on Verify", and my pass-1 survey found three Verify quotes matching nothing at ab51655. It is true only after P0 requoted them. Concrete failure: a parcel or Logan reads that the move broke no quote, so the Verify quotes look settled, though P1 must still re-read them. Fix: "every quote stands once P0 has requoted the three Verify quotes".
- D-B (defect, low; ROUND2 line 399). The sentence reads: "round 1's front page took eight versions to READY." ROUND1.md never mentions a front page. The front-page commit 43c36a2 follows the round's close commit 80c9f32. The record, the 2026-09-30 front-page entry in docs/VALIDATION.md, lists seven verdicts, each NOT READY, from "verifier-front"; the seventh is followed by fixes and a gate pass ("11 passed"); no READY verdict is recorded. Concrete failure: Logan approves the three-pass rule on a rationale the record does not support. Fix: cite the entry and say what it shows, or drop the round and the count.
- B1 (brief error; verifier-P0.md). It says: "the commit after the plan's draft 2 restates SPEC.md's decisions 35 and 36." No commit follows b6c7560 (it is the tip), and draft 2 is itself the restatement. Concrete failure: the verifier looks for a commit that does not exist. Fix: name b6c7560 as the tip.
- B2 (brief error; P2.md). It says: "METHOD.md brought to the method as practised (698 lines added)." The change from 8767e23 to f42242e is 674 lines added and 24 removed (698 is the total changed). Fix the figure.
- B3 (brief omission; P1.md and ROUND2 lines 254 to 258). The spec names four "where I'd attack first" gaps (SPEC.md section 1: clause readings in COMPLIANCE; cross-device determinism; the transcendental refusal cap; the reduction tree shape). The page names three and leaves out the COMPLIANCE gap, with a code comment: "checked, not found" (corrections.py lines 46 to 52). At ab51655, docs/COMPLIANCE.md has its conformance statement (line 130) and no "clause reading" text, so the omission still holds as far as a literal search shows. P1's brief should name the four and list the omission's basis among its re-checks. Under decision 36 a dropped spec gap goes to Logan if the basis is overtaken. This is a side note, not a defect, because the claim holds at the pin.
- Record slip (the lead's record, not the plan). lead.md's 14:18:57 entry says Logan's two answers "become decisions 36 and 37". SPEC has them as 35 and 36, and the commit message says 35 and 36. A correction entry is needed.
- Side notes: ROUND2 line 231 names fig() for the hand-typed-figure control, and _common.md names render. The census wording in ROUND2 line 57 says "fact call"; the counts are unique facts (calls are 220 changed, 134 added, 7 gone). CLAUDE trap 12 is cited for "every stated() figure is his statement"; the trap supports the mechanism, and the built site satisfies the claim (13 stated() calls name Logan; the one "Someone Else" is a control in _settled.py; the two D() wrappers are unused). The HonestHarness check cell is a document link. The plant branch's removal after the key is published is not stated.

## 2026-10-08 14:40:08 -0700 - pass 2 verdict on draft 2 at b6c7560: NOT READY, two one-sentence defects; the eight of pass 1 answered

Measured:
- Verdict: NOT READY. Draft 2 has two defects, D-A and D-B, each a single sentence that is not true of the record. Both have one-sentence fixes. The brief errors B1 and B2 must be fixed before verifier-P0 and P2 rely on their briefs. B3 is a side note for P1's brief.
- The eight defects of pass 1 are answered: D1, D2, D3, D6, D7 and D8 fully; D4 and D5 with the marking points listed above. The lead's point on VERIFICATION.md line 382 is agreed, and my pass-1 statement on it is withdrawn.
- Scope of pass 3, if the lead wants one: the diff since b6c7560 in docs/ROUND2.md and docs/SPEC.md, the revised briefs named in the lead's entry of 14:22:22, and the correction entries for lead.md's "36 and 37" slip and for D-B.

Believed:
- The plan's architecture now answers pass 1: the Verify fixes, decision 36 for stale lines, the census, the models decided by Logan, the three-pass cap marked as the lead's, the planted copy and its clone, and the controls per parcel.
- If D-A and D-B are corrected and B1 and B2 are fixed, I expect READY on pass 3, which is the last pass allowed by the lead's rule. Whether to take the side notes is the lead's call.

For: the lead (the two sentences, the two brief fixes, the P1 brief's list of four gaps, and the lead.md correction).

Not done:
- I did not run the full gate (verifier-P0 has it). I ran the full site build and the page run in a scratch copy only.
- I ran the controls for P3 and P4 and read those for P1 and P2. I did not run the SOURCE_PATHS label control.
- I did not check every decision in SPEC against lead.md beyond the four answers of 14:18:37 and the two quoted in the plan (verifier-P0's item 7 covers the rest).
- I did not verify the P3 brief's bundle counts, or P2's METHOD section citations beyond the line count.
- I did not read the lead's transcript.
- No background process was started, so there is nothing to stop. The cloudflare and runpod connectors remain unused and still need authorisation.

## 2026-10-08 14:50:57 -0700 - pass 3 (the last under the lead's rule) on draft 3 at 10b6b17: the checks, measured

Measured:
- My worktree was fast-forwarded to 10b6b17; b6c7560 is an ancestor. The range changes docs/ROUND2.md (31 insertions, 10 deletions) and docs/SPEC.md (5 lines). No code, pins, public, sources or verify files changed.
- Read the whole diff of the plan and SPEC. Read the four changed briefs (_common.md, P1.md, P2.md, verifier-P0.md) in full or at the changed parts; the rest of P2 was read too, and its only change is the line count. Read lead.md from its 14:22 entry to the 14:43:12 entry and its correction of 36 and 37.
- Survey of the literal quote patterns against the draft-3 pins, on a scratch copy of the tree: 92 literal calls match once, none fails; 85 non-literal calls are skipped, as before.
- Parcel-level checks on the scratch copy: --check (39 published files exactly as the pins render), --numbers (0 problems; 2941 marks), --links (0 problems), --local-only (0 problems), --verify-facts (1810 read again and the same; 0 different; 54 stated; 0 skipped by name).
- The committed public/facts.json at 10b6b17 is byte-identical to a scratch build's output, so the census's "after P0" comparison holds.
- Control 1, tested: render.render() accepts a numeral typed into a string ("reads 4 checks by hand" comes back unchanged; a list of segments with a bare 4 also passes). The numbers stage refuses the same planted count in a copy of verify.html: "'4' is a numeral outside any figure's mark".
- Control 2, tested: a fact's label changed to name docs/NOT-LISTED.md, which build.SOURCE_PATHS does not list, is refused by the numbers stage: fact 40's label "isn't one the build writes for a source", and the page's own source text is flagged too.
- Dates: the round's close commit 80c9f32 is 2026-09-30 06:30 -0700; the front-page commit 43c36a2 is 2026-09-30 22:11 -0700. ROUND1.md has no front page.
- The four spec gap names (SPEC.md line 51) are quoted exactly in P1's brief. The page shows three: "Cross-device determinism", "The transcendental refusal cap" and "The reduction tree's shape" (corrections.py lines 57, 61 and 64). The third label is not the spec's words, which are "the reduction tree shape".
- Commit subjects in the ranges carry the values the new paragraph cites: ParcelRound 20 subjects mention ADOPTION, check_method, templates or case studies; cft-fp256 30 mention ABI; Quantum-Film 6 mention Heron, pre-registration, poster or paper.
- The three organisation repositories: the new pins 9acb750, d18af76 and dac773d are absent from the clones in the repos directory (mercs2-modkit, mercs2-wad-simulator, notes-on-the-released-game): commit lookup fails there. They are present in the site's own clones under .cache/repos (the modkit, wad-simulator and notes clones, the last under Mercenaries-Fan-Build--notes-on-the-released-game).
- METHOD.md, ParcelRound 8767e23 to f42242e: 674 lines added, 24 removed.
- method.py's round statistics read CASE-STUDY-2.md, -3.md and -4.md (lines 33, 102, 105, 107 and 110). It reads no CASE-STUDY.md, so case study 1 is not among them.

## 2026-10-08 14:51:05 -0700 - pass 3: D-A, D-B, B1, B2, B3 and the side notes, against draft 3 and the briefs

Measured (status):
- D-A, "every quote on them still stands, so every gate passes": ANSWERED. The sentence now reads "once P0 had requoted Verify's three, every quote on them stands at the new pins". The literal survey (92 match, none fails), the five parcel-level checks, and the committed facts file all agree. "Stands" here means still matches its source; the round's subject is that a matching quote can be overtaken, so "still matches its source" would say it more exactly (side note).
- D-B, "round 1's front page took eight versions to READY": ANSWERED. The reason now reads "the front page of 2026-09-30, made after round 1 had closed, went past its verifier seven times NOT READY before its push (docs/VALIDATION.md, its entry of that date)". Checked: the round's close commit is earlier (06:30) and the front-page commit later (22:11) on the same day; ROUND1.md has no front page; the entry records seven NOT READY verdicts from verifier-front, each on a version not pushed.
- B1 (verifier-P0.md named a commit after draft 2 that does not exist): ANSWERED. The brief now names draft 2 and the dispatch's tip. Residual: the brief still says decisions 35 and 36 "are P0's records"; decision 36 is not in P0 (05413b2 has 31 to 35). Side note B4 below.
- B2 (P2.md's "698 lines added"): ANSWERED. The brief says 674 lines added and 24 removed, and gives the numstat command, which I re-ran.
- B3 (P1.md names three gaps, and leaves out the fourth): ANSWERED. P1's brief now names all four in the spec's words, says the page shows the last three, gives the code comment's basis for the omitted COMPLIANCE gap, and asks P1 to re-check that basis at ab51655. I checked the basis as far as a literal search goes: docs/COMPLIANCE.md has its conformance statement at line 130 and no "clause reading" text. Residual: the page's third label differs from the spec's words (side note B6 below).
- Side notes from pass 2: the census unit is ANSWERED (ROUND2 line 56 now says "Every fact ... matched by its method and arguments"). The HonestHarness check is ANSWERED (a link to its requirements document, stated as its check, since it has no gate). The most likely regression per parcel is ANSWERED (a bullet for each of P1 to P4). The plant branches' end is ANSWERED (local, never pushed, deleted at the round's end). Decision 35's marking is ANSWERED (italic "The lead's reading"). Subagent disclosure is ANSWERED (_common.md, the line on spawning a subagent). The lead's 36-and-37 slip is ANSWERED by the lead's correction at 14:43:12. The "What moved" commands are ANSWERED in part (see the new faults below). The fig() naming is answered WRONGLY (see D-E). Not changed: the CLAUDE trap 12 citation for "every stated() figure is his statement"; the metrics script's "other" class.

## 2026-10-08 14:51:18 -0700 - pass 3: the new faults I found in draft 3 and the briefs

Measured:
- D-E (defect, low; ROUND2 control 1, and _common.md's control 1, which says "render"). The plan says the numbers stage, or render.render(), refuses a figure typed by hand. render.render() does not refuse a numeral typed into a string: tested, it prints it unchanged. Only the numbers stage refuses it, by name. Concrete failure: a parcel runs control 1 as the text says, sees render pass, and either reports a broken control or, if it only tests render, reports a held control that does not hold. Fix: name the numbers stage alone in both files, or, if render is meant, state it as a separate control on a figure object that no fact produced.
- D-F (defect, low-moderate; the "What moved" paragraph, ROUND2 lines 223 to 228). It says every "What moved" value was read by the repository log and the diff of docs/VALIDATION.md, run in the clone at <repos>/<clone>. For the three organisation repositories, which pins.json lists with no dir, that clone is Logan's own. Those clones lack the new pins (tested: the commit lookup fails for 9acb750, d18af76 and dac773d). The site's own .cache/repos clones have them, and P4's brief uses those. Trap 9 says a pin with no dir is read only from the site's own clone. Concrete failure: a P4 parcel or verifier runs the paragraph's command in the repos directory, gets an unknown revision, and either drops the measurement or reaches for a clone that is behind. Fix: say the three organisation repositories are read in the site's own .cache/repos clones, as P4's brief says.
- B4 (side; verifier-P0.md): "decisions 35 and 36, which are P0's records": decision 36 is not in P0 (05413b2 has 31 to 35). Also "the approved draft": Logan has not yet approved the plan (ROUND2 "The shape", step 1). Say "draft 3" or "the current draft".
- B5 (brief error; P2.md, and its trap sentence): "Today they come from case studies 1 to 4" and "a statistic still true of case studies 1 to 4". method.py reads 2, 3 and 4 and not 1 (lines 33, 102, 105, 107 and 110). Fix to "2 to 4" in both places.
- B6 (side; P1.md and corrections.py line 64): the brief says the gap names are Logan's words, and the page's third label reads "The reduction tree's shape" where the spec says "the reduction tree shape". Say whether the label is to change; under decision 36 a change to one of the spec's choices goes to Logan.
- D-C (side; the "What moved" paragraph): the paragraph says every value was read by those two commands. The commands show commit subjects and ledger headings, and most of the values do appear in the subjects (ParcelRound 20, cft-fp256 30, Quantum-Film 6). But the README sentence in P1, the ABI number from cft.h, and the device names from the README are read from files. Say which values come from files.
- Side: SPEC decision 36's second paragraph (the first use of the stated-line rule) is the lead's narration, and sits unmarked in the list headed "verbatim", as decision 35's gloss did before draft 3. The narration is accurate.
- Side: the CLAUDE trap 12 citation for "every stated() figure is his statement" (unchanged) supports only the mechanism. The metrics script's "other" class is still not named in the plan.

## 2026-10-08 14:51:25 -0700 - pass 3 verdict on draft 3 at 10b6b17: NOT READY, two wrong answers in the plan; the lead's rule sends them to Logan

Measured:
- Verdict: NOT READY. The third pass finds two wrong answers in the plan's text: D-E (the control names render.render() as a refuser it is not) and D-F (the "What moved" paragraph sends the organisation repositories to Logan's own clones). Both have small fixes. The brief errors B4, B5 and B6, and the side notes, are for the lead to take or decline.
- D-A, D-B, B1, B2 and B3 are answered, with the checks above.
- Under the lead's rule (ROUND2 lines 415 to 421): "If a third pass still finds a wrong answer, the lead records it and asks Logan before going on." This is that case. The lead records D-E and D-F here, and asks Logan before going on.

Believed:
- Once D-E and D-F are corrected, and the lead answers the side notes it wants, I would expect READY on the checks I ran. The plan's architecture now answers all of pass 1 and pass 2.
- The third pass was the last allowed under the lead's rule. Nothing in my remaining checks is left undone that would change the verdict.

For: the lead, and through it Logan (the two wrong answers, the brief fixes, and the side notes).

Not done:
- I did not run the full gate; verifier-P0 has it. The parcel-level checks ran on a scratch copy only.
- I did not check P0's SPEC decisions word for word beyond the plan's references (verifier-P0's item 7).
- I did not check the wording of the regression bullets beyond the one about the Verify quote.
- I started no background process, so nothing to stop. The cloudflare and runpod connectors remain unused.
- Scratch copies, scripts and outputs are in the scratch directory for this pass; nothing is in the ledger but this report and the earlier entries.
