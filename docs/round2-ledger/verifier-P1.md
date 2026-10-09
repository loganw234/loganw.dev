
## 2026-10-08 17:18:51 -0700 - verifier-P1 starts: test escalation sent; the clone is at 9a5449d; the README, lead.md and the directory read, P1.md not yet

Measured:
- The test escalation, "verifier-P1: test escalation", went to the lead with the runtime's SendMessage, addressed "main" as the earlier verifiers did. The tool answered: "Message queued for the main conversation's next turn". So this runtime can message the lead. I have no reply yet.
- My clone, `loganw.dev` in my scratch directory, is on branch r2-plant-P1 at 9a5449d, its working tree clean. Its one-line log subject is the P1 subject, which the lead's entry of 16:43:56 says a planted copy keeps from the parcel's own commit.
- I have read README.md, lead.md (all of it), and the directory listing. I have not read P1.md, the parcel's own file, until I have formed my own view of the commit.

Believed:
- The planted copy is the commit I verify; its two plants, if any, are in its tree and not in the lead's log.

For: the lead (the test escalation), anyone resuming verifier-P1

## 2026-10-08 17:43:05 -0700 - verifier-P1's environment facts: the Bash guard refuses `source` and a loop whose program is built at run time; plain commands with inline variables run

Measured:
- Refused, each with "runs ... inside a construct too complex to verify ... Refusing to run it": (a) a command that chained `source <scratch>/env.sh` with `cp -r`, `echo` and `python site/build.py`; (b) a `for n in ...; do printf ...; sed -n "${n}p" ...; done` loop. The refusal text says a worktree-isolated agent's git operations "must target its own worktree", and tells the agent to run the commands from its start worktree. The verifier brief puts that worktree out of bounds, so I ran nothing there.
- Ran: `cd <clone> && LOGANW_REPOS='<repos>' python site/build.py <mode>`, one mode per call, with the variable written inline (shell state does not persist between calls, and `source` is refused); `cp -r <repos>/loganw.dev/.cache <clone>/.cache`; `git -C <repos>/cft-fp256 show ab51655:<path> > <scratch>/<file>` (the redirect into scratch); `git -C <repos>/cft-fp256 grep -n <pattern> ab51655 -- <paths>`; `git -C <repos>/cft-fp256 merge-base --is-ancestor <a> <b>`; `git -C <repos>/cft-fp256 diff --stat <a> <b> -- <paths>`; a plain `for f in ...; do echo ...; done` loop; `sed -E` and `grep` on local files.
- Disk: the C: drive had 38 GB free of 1.9 TB (99% used) at 17:4x (`df`).

Believed:
- The guard refuses what it cannot parse: `source` of a file it cannot read, and a loop whose program is computed at run time. The same operations written inline pass.

For: the lead; every other agent that hits the guard

## 2026-10-08 17:43:05 -0700 - verifier-P1's report on 9a5449d: NOT READY, on two sentences the pin does not support; the other items confirmed, or not determined

Verdict: **NOT READY.** Two sentences in the commit claim what cft-fp256 at ab51655 does not say, and both are in the built pages.

Measured (my clone, `LOGANW_REPOS` set inline, Python 3.12.9):
- `build.py --check`: "check: 39 published files are exactly what the pins render".
- `--numbers`: "numbers: 0 problem(s); 3009 marks tied to their own facts in 39 files; allowed as part of a name: none".
- `--links`: "links: 0 problem(s) in 39 published files". `--local-only`: "local-only: 0 problem(s) in 39 published files".
- `--verify-facts`: "verify-facts: 1837 read again and the same, 0 different, 54 stated, 0 skipped by name".
- `--docs`: "docs: 0 problem(s) in 7 documents".
- Not run by me: the full gate, `--control` (the lead's full gate on 9a5449d reports 386 caught), the separate full build.

**DEFECT D1.** `site/pages/work_cft_fp256.py:58`: "The contract is versioned, and no step so far has moved a recorded bit." Published at `public/work-cft-fp256.html:4` and `public/work-cft-fp256.txt:18`. At ab51655 it is wrong: `CONFORMANCE.md:334-335`, "The tree is at profile 3 (2026-10-05), a major step: recorded bits moved"; `CONFORMANCE.md:347-353`, "Four recorded cases moved ... `vectors/SHA256SUMS` moved by four lines". The same paragraph quotes "recorded bits moved" two sentences later. P1's design (P1.md, 15:56:27, section 1, D2) has no such clause: "The contract is versioned. CONFORMANCE.md opens with its profile ...". Fix: strike ", and no step so far has moved a recorded bit".

**DEFECT D2.** `site/pages/thread_determinism.py:36`: "The same repository also holds a language, the one atlas-engine's plates are now written in:". Published at `public/thread-determinism.html:4`. Nothing at ab51655 supports it, and the source says otherwise. `docs/LANGUAGE.md` never mentions atlas-engine (`git grep`, none). `docs/ATLAS.md:3-4` says atlas-engine is "a language for platonography whose programs ... are evaluated" by the tile, so it is atlas-engine's own language. `docs/ROADMAP.md:4284` says "atlas-engine lowers pinned GLSL to binary32 tile programs". `README.md:441-443` says the plates atlas-engine evaluates are the PrettyCloud atlas. The account's own first paragraph says so: `thread_determinism.py:21-22`, "Its shapes wanted a language of their own: A language for platonography". The commit message says the language and certificates sentences come from `docs/LANGUAGE.md` and `docs/CERTIFICATES.md` at line 3; the atlas clause does not. P1's design (P1.md, section 4, T3) has "The same repository also holds a language: ...; and certificates: ...". Fix: restore that sentence.

Every other new sentence I compared matches its source, or matches P1's design. The two above are the only differences I found between the rendered sentences and the design (P1.md sections 1, 2 and 4).

**Side notes (not defects; the lead's calls)**
- **S1.** The commit message cites `CONFORMANCE.md` lines 312 and 316 for the digests quote. The quoted sentence is at lines 317-319; line 316 is inside the sentence before it.
- **S2.** The commit message says "The docstring and a comment record that the three gap quotes were re-read". Only the comment does; P1's own correction (P1.md, 16:34:27) says so.
- **S3. The fourth Corrections gap, for Logan.** The comment's basis, "calls no clause reading ... open to dispute ... checked, not found", is literally true of `docs/COMPLIANCE.md`, which is identical at both pins. But row 9.2 (`COMPLIANCE.md:109`) says Table 9.1 is "correctly rounded in every format and attribute with exact flags", and the 2026-10-05 entry (`VALIDATION.md:18203-18219`, the four moved cases at `:18212` and the four ties at `:18219`) shows that was false at four arguments until the fix. P1 flagged it (P1.md, 15:58:05), and lead.md has it for Logan under decision 36. I change nothing.
- **S4.** Verified rows. The two added rows are right (`VALIDATION.md:18245` and `:18544`, both 2026-10-06). Whether to carry more is a selection question: the 2026-10-05 wave-3 heading (`VALIDATION.md:17700`) ends "the card legs on revision 7's quad" and is not in the list.
- **S5.** The kept-failure row says "pow's and pown's exact branches always did"; `CONFORMANCE.md:341-342` says pow, pown, powr and compound. A subset, not an overclaim.
- **S6.** The "A major step is ..." quote ends at a colon (`CONFORMANCE.md:279-281` goes on: "an image that loaded and is refused, or one whose run moves by a bit"). The definition is complete; the page shows a dangling colon. No claim is enlarged.
- **S7. Not determined.** The golden item's "2.6 min at four workers when quiet" is an undated table cell (`VERIFICATION.md:330-332`), and the same row counts 3,370 tests, up from 2,075 in its own history. I did not re-measure. Whether the quiet figure is still current is the "Test it step whose cost changed" the brief warns of; I cannot say it is wrong.
- **S8. Not determined.** The Verify page and its docstring say "cheapest first". The site's own check comes last and the page gives it no cost.
- **S9. Supported, not a fault.** The ABI sentence says "checked by make verify-quick ... and make verify-gate". The quick budget's remote stage includes refusals (`verify/run.sh:1464-1484`), and `host/tests/remote_test.c:246-251` refuses an ABI one minor version away; the gate's libcft stage compares the macros in `host/tests/api_test.c:718`. I did not run either stage.
- **S10.** The card line "which needs the FPGA and its toolchain" is the page's own inference from "A device" (`CONFORMANCE.md:252`). It is consistent with the source.

**Items in my brief**

1. **Every sentence against its source at the pin: DEFECT D1 and D2.** The connecting words in P1.md section 8(c): "The contract is versioned" (the source supports the profile, not "no step"; D1); "by the recipe CONFORMANCE.md gives" (`CONFORMANCE.md:307-311`, confirmed); "The record says this is a check no gate makes" (`:312`, confirmed); "The record names one it lacks" (`VALIDATION.md:18237`, confirmed); "it does not run what make verify-gate adds" (`VERIFICATION.md:384-392`, confirmed); "The record shows a defect of that kind" (`VALIDATION.md:18206` and `:18219`, with `CONFORMANCE.md:344`, confirmed); "The same repository also holds a language ... and certificates" (the certificates clause and the language clause without the atlas clause: confirmed; the atlas clause is D2). Commands: `git -C <repos>/cft-fp256 show ab51655:<path>` into scratch, then `grep -n` and `sed -n` on those copies; `git -C <repos>/cft-fp256 grep -n ... ab51655 -- <paths>`. Verdict: defect.

2. **Quotations and where they are cut: confirmed, with S6.** Each pattern matched once (the build passes). I read the source lines and the words after each cut. The lede (`CONFORMANCE.md:8-12`) is a complete sentence. The golden item (`VERIFICATION.md:37-40`, `README.md:273-278`) is complete. The quick and gate lists (`VERIFICATION.md:377-393`) are exact, each ending where its sentence ends. The limits quotes: `VERIFICATION.md:83-89` ends at "this one would not", and the next words add negative controls, with no change in claim; `VALIDATION.md:18206` and `:18219` are cut before a clause that gives the mechanism, with no change in claim; the MPFR quote (`VALIDATION.md:18237`) ends at a sentence end. The exp2 quote (`CONFORMANCE.md:336-339`) is cut at a colon. "Step 6's design study M1 ..." (`CONFORMANCE.md:344`) omits ", and Logan decided the fix on 2026-10-05": an omission only.

3. **The new Verified rows and the third kept failure: confirmed.** `sed -n` on `VALIDATION.md` at 7161, 13913, 18203, 18237, 18245 and 18544, and `grep -n '^## 2026-10'`. Headings: 7161 "2026-09-08 - card day: first light ..."; 13913 "2026-09-23 - the U50 single closes 145 MHz ..."; 18203 "2026-10-05 - the golden model's exp2 tie fixed ..."; 18245 "2026-10-06 - step 6's closing records, part one ..."; 18544 "2026-10-06 - step 6's closing records, part two ...". `git -C <repos>/cft-fp256 merge-base --is-ancestor ca43695 ab51655`: yes. `git show -s` of ca43695: "exp2's tie at emin - p rounded as IEEE 754 rounds it, and profile 3 - ...", which matches the row. S4 and S5 apply.

4. **"Test it" and "Prove it wrong": confirmed.** `README.md:273-278` (the self-tests, then `pip install pytest mpmath`, then `make golden`); `Makefile:111-112` (golden runs pytest); `Makefile:117-122` (vectors runs `gen_vectors.py` at 3000, 4000 and 200, the profile's counts, so `make vectors` is the profile's regeneration); `CONFORMANCE.md:307-319` (the recipe and the limit); `VALIDATION.md:18237` (the pool gap is still open: the only later mention, `:18387`, is a verifier's note about closing it). I did not run `make golden` or `make vectors`; the brief allows reading.

5. **Logan's words: confirmed unchanged, none overtaken.** The diff does not touch the door (`thread_determinism.py`, `door()`), the rules and signature row (`corrections.py`, `engagement()` and `SIGNATURE`), the gap names or the third label (`attack_first()`). The door's "workloads" word is kept, as `propose.py`'s control needs it (`verifier-plan.md:54`). The cross-device half is still unshown: `DETERMINISM.md:1411-1413` (unchanged file), and `VALIDATION.md:18470` says the lead's ledger records no other card run on a revision-8 tile.

6. **The gap quotes at ab51655: all three stand, none closed.** `git -C <repos>/cft-fp256 diff --stat 77b8440 ab51655` lists none of DETERMINISM.md or COMPLIANCE.md. Cross-device: `DETERMINISM.md:1411-1413` is unchanged, and a search of the entries after 2026-09-29 for second, two, another or other card, and for K325T, A200T and Z020, finds one line (`:18470`). Cap: `TRANSCENDENTALS.md:413-415` ("Reaching the cap is loud.") has the same wording as `:350-351` at 77b8440; the entries after 09-29 change how often the sweep escalates (`VALIDATION.md:16576-16584`), and none changes what the cap does. Tree shape: `HOSTAPI.md:686` is the same paragraph at both pins, and no entry after 09-29 mentions the tree. The fourth gap: S3.

7. **P1's controls: controls 1 and 4 re-run from copies of 9a5449d; both fail for their written reason.** The base copies pass (numbers: 0 problems). Control 1 (`"2.6 min at four workers"` typed in place of the golden-cost `prose()` in `verify.py`): the build wrote 39 files and 1890 figures; `--numbers` printed "PROBLEM verify.html: '2.6' is a numeral outside any figure's mark, in 'in a clone of cft-fp256. Cost: 2.6 min at four workers when quiet,'", the same for "four" as a number word, and "numbers: 2 problem(s); 3007 marks ..."; exit 1. The same lines as P1.md, 16:26:09. Control 4 (the Verified row's 18245 moved to 18244): "REFUSED: cft-fp256 docs/VALIDATION.md: no ledger entry heading at line 18244"; exit 2. Controls 2 and 3 were not re-run.

8. **Scope: confirmed.** `git diff --stat 427900e 9a5449d`: 23 files, 1896 insertions, 1207 deletions, the four page modules and 19 files under `public/`. `git diff --numstat 427900e 9a5449d -- site/`: 168 insertions, 36 deletions, as P1 reported before committing. Not in the diff: `work_cft_rebound.py`, `build.py`, any stylesheet. Twelve public files differ only in fact ids: `thread-film`, `thread-preservation`, `threads`, `work`, `work-honestframework`, `work-parcelround`, `work-quantum-film` (each html and txt) and `work-cft-rebound.txt`. Each is identical to its parent after `sed -E 's/data-f="[0-9]+"/data-f=N/g; s/fact [0-9]+/fact N/g'` on both. The five others (`corrections.html`, `verify.html`, `thread-determinism.html`, `work-cft-fp256.html` and `.txt`) differ beyond fact ids, as P1 says.

9. **The commit message, claim by claim.** Confirmed: the lede from `CONFORMANCE.md` line 8; the two make golden lines (`README.md:273-277`, `Makefile:111-112`); the recipe at 307-311 and the limit at 312; `VALIDATION.md:18237`; the two Verified rows and their headings; ca43695 an ancestor; the gate and quick lists to `VERIFICATION.md:392`; the `CLAUDE.md` figures at lines 9 and 10; the golden loaded cost at `:332` (the header at `:330` names "quiet" and "loaded"); "19 files change" and the twelve fact-only files; "work_cft_rebound.py reads nothing from cft-fp256" (its one mention is a quote from cft-rebound's README, and its `NAME` is "cft-rebound"); the two `SOURCE_PATHS` entries (`build.py:85-86`); and the checks listed, each re-run by me with the same output. Not re-run by me: "1891 figures" and "--control 386 caught". Wrong or too broad: (a) "from the definitions docs/LANGUAGE.md and docs/CERTIFICATES.md open with (line 3 of each)" is false for the atlas clause (D2); (b) S1; (c) S2.

10. **Anything else.** (i) The account contradicts itself: `thread_determinism.py:21-22` says atlas-engine's language is its own, and `:36` says its plates are written in cft-fp256's text language (D2). (ii) S7 and S8. (iii) The commit's source-line counts equal P1's own pre-commit counts, so the two defects are in-line edits of existing sentences, not added lines; a diff-stat check would not have caught them.

Overall: **NOT READY** on D1 and D2. Each is a sentence the pin contradicts or does not support; each is in the commit and in the built page. Nothing else needs a send-back. S3 is for Logan under decision 36. S7 and S8 are not determined.

Believed:
- With D1 and D2 corrected to the design's text, every other check in this report stands; I have not re-run the build after such a correction.

What I did not do:
- I did not run the full gate, `--control`, `make golden` or `make vectors`, or controls 2 and 3. I did not run the separate full build (`--check` compares its output).
- I read P1.md in full, and the directory's entries after line 417 of lead.md (17:18:35 to 17:30:38), `verifier-P2.md` and `verifier-P3.md` in full. For `P2.md`, `P3.md`, `P4.md`, `verifier-plan.md`, `verifier-P0.md` and `verifier-P4.md` I searched for mentions of P1's pages and of the shared modules my pages use (facts, render, `_dossier`, build), and found no change to them that bears on P1's pages. I did not re-read those six files line by line before this report.
- I opened no other branch or worktree of loganw.dev, and did not look for any key or plant description. I did not check the deployed web page. I did not push, merge or commit, and changed no tracked file.
- I started no background process, so none needed stopping. The control copies and the extracts of cft-fp256 documents under my scratch directory are deleted; my clone stays.

For: the lead (the two sentences and their fixes, the merge, the side notes); verifier-P1 if resumed; Logan, through S3
