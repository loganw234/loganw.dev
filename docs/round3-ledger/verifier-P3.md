
## 2026-10-31 08:33:10 -0700 - verifier-P3 starts; the test escalation is sent to main

Measured:
- Read, in order: `briefs/_verifier.md`, `briefs/verifier-P3.md`, the ledger's `README.md` and `lead.md`. Not read: `P3.md`, which waits until this verifier has reported.
- The clone, `<scratch>/r3-verifier-P3/loganw.dev`: HEAD is `9bef3c6` (P3's commit), its parent is `6eff67b`, the tree is clean, it has no remote, and its one branch is named `r3-P3-1`. `python --version` prints Python 3.12.15 there.
- The test escalation: "verifier-P3: test escalation" was sent to "main" with SendMessage, and the runtime answered "Message queued for the main conversation's next turn". So this runtime can message the lead.
- The runtime's `update_plan` and `wrap_up` tools refuse a subagent ("Do not call update_plan or wrap_up"), so this verifier keeps no pinned task list. Other verifiers will meet the same refusal.

Believed:
- Nothing else yet. The verdicts come in the report.

For: the lead, every verifier that starts after this one (the refusal of `update_plan`)

## 2026-10-31 08:57:43 -0700 - verifier-P3: the report is held out of this ledger under the README rule; the question is for the lead

Measured:
- The README says: "Keys, and any description of their plants, stay out of this ledger until the last planted-copy verifier has reported." My brief says to write my report into this file before I finish.
- Planted copies exist for P3 (lead.md 08:20:59), P2 (08:40:08) and P1 (08:42:10). verifier-P1 is not yet dispatched (lead.md 08:50:08 dispatches it once P1's gate passes). So the last planted-copy verifier has not reported.
- My report describes faults in P3's copy. I have not written those descriptions, verdicts or fault kinds here. This entry holds no finding.
- The full report (each item's commands, observations and verdicts; READY or NOT READY; side notes; what I did not do) goes to the lead in my final message.

Believed:
- Writing the report into this ledger now could show verifier-P1, which reads the whole directory before it starts, what kinds of fault to look for in a planted copy. The README's rule exists to prevent that.

Question for the lead: may the report go into this ledger now, or only after verifier-P1 reports? My default is to hold it until then. I have sent the lead a message saying so.

For: the lead; verifier-P1 and verifier-P2, who read this directory

## 2026-10-31 09:21:13 -0700 - verifier-P3 pass 2 started on 5ff7379; its report is held

Measured:
- Pass 2 started on `5ff7379`, the lead's restates, in the clone's branch `pass2`. Its report is held out of this file, by the lead's ruling of 08:58:09 and the coordinator's message. Nothing of what pass 2 found is written here.

Believed:
- Nothing yet.

For: the lead

## 2026-10-31 09:30:35 -0700 - verifier-P3: pass-1 report, verbatim as sent (the final message after the 08:58:09 ruling)

**verifier-P3, pass 1, on `9bef3c6` (parent `6eff67b`). Verdict: NOT READY.** Two defects send the work back: items 2 and 5. The report is held out of my ledger file by the lead's ruling of 08:58:09 (`lead.md`), so this message is its only copy until verifier-P1 has reported.

**1. Issue 1's row, cell by cell: confirmed.**
- Commands: `git -C <repos>/cft-fp256 show 19de866:docs/VALIDATION.md` (copied into `<scratch>`), `sed -n '26149,26231p'`, the `facts.entries` count at the pin (258 entries; one headed as issue 1), `git rev-list --parents -n 1 48e2aa22`, and `git merge-base --is-ancestor` of 48e2aa22 against 19de866 and ab51655. Also the rendered `corrections.html` text.
- Observed: the date comes from the heading at 26149 (2026-10-30). The claim at 26152 matches verbatim, and "found by" at 26151 matches with no "outside". The disposition's vectors sentence at 26179 matches. The oracle and neighbour-counter bullets (26224, 26225) sit under "Known limits, recorded:" (26222). The fix is "merged as 48e2aa22" (26172): a merge of f68c6301 and b9d60ebc, an ancestor of 19de866 and not of ab51655. "Fixed" is the entry's own word, used ten times. Every cell except the date is read through a pattern confined to the entry's span. The date comes from the same heading but has no pattern guard (see item 7).
- Verdict: confirmed. Side note: the row shows two of the entry's four known limits (see item 9).

**2. The caption: defect.**
- Commands: read `LEDGER_CAP` in `corrections.py`; the rendered caption.
- Observed: the caption says "each of its cells is read from cft-fp256's CONFORMANCE.md at its pin". The cells come from `docs/VALIDATION.md` (`CFT_LEDGER`), and the rendered labels cite that file at 26149, 26151, 26152, 26179, 26224 and 26225. The fix check is accurate. "Each of its cells is read" also overstates, because the disposition's framing words ("fixed; the entry also records", ", and, among its known limits,") are typed.
- Failure: a published label names the wrong source. Sent back. Name `docs/VALIDATION.md`, and say the framing words are typed.

**3. "found by": confirmed.**
- Commands: the rendered row; `git diff` of `corrections.py`, where no hunk touches `SIGNATURE`.
- Observed: the cell reads "a clean-room audit of loganw234/muse-softfloat (binary16/32/64), cross-tested against this library and an exact arbiter", the entry's own words, with no "outside". The signature row is unchanged: "first outside correction — pending — this row is here so you can watch me remove it" (stated by Logan, 2026-09-29).

**4. The gaps: confirmed.**
- Commands: each quoted sentence matched at 19de866 and at ab51655 (`git show` and `grep -n`); `git log ab51655..19de866 -- docs/COMPLIANCE.md` (no commits); the paragraphs around the other three quotes at both pins (identical); the added lines of the ledger diff for "second card", "cross-device", "cap", "Ziv" and "tree shape"; COMPLIANCE rows 9.3 and 9.4.
- Observed: each quote matches once at 19de866. No new entry closes a gap. The two "second device" hits are record-merge laws in the 2026-10-19 store entry. The two "Ziv" lines concern a missing mpmath. "Above is refused" concerns an MPFR constant's count. No tree-shape text changed.

**5. Method's two sentences: count and figures confirmed; "each written by Muse alone" is a defect.**
- Commands: `facts.AGENT` (`^Co-Authored-By:.*\b(?:claude|gemini|muse)\b`); `git -C .cache/repos/muse-softfloat log a2241fc` counts; author and committer names with `@` masked; the rendered `method.html`; an exact-match count of trailer addresses against `public/`, with nothing printed.
- Observed: "Claude, Gemini or Muse" is the rule's word set, and `check_count_words` refuses a no-break-space variant. The figure 20/46 is `facts.agents("Mercenaries2")` under the same rule. The Muse figure, 185/185, and the name are correct: 185 commits, 185 Co-Authored-By lines naming "Muse Code (muse-wonder-full-1.0)", each with an address. But all 185 commits have "Logan" as author and as committer. "Each written by Muse alone" claims authorship the commits do not show. The lead's design (lead.md 07:18:32) and decision 50 both describe the sentence as trailer-only ("the name only"). No Muse trailer address appears in `public/`. The non-contact matches of a naive grep were binary files and hash fragments.
- Verdict: defect. Sent back. Restate to the trailer count and name.

**6. Logan's words: confirmed unchanged.**
- Commands: `git diff 6eff67b 9bef3c6` on both pages; SPEC decision 9.
- Observed: no hunk touches `engagement()`, `SIGNATURE`, `STATEMENT_9`, `ONLY_HERE`, `ratio_block` or `home.AI_USE`. `STATEMENT_9` matches SPEC decision 9 word for word. Decision 50's "your statement there is unchanged" holds.

**7. The new readers and controls: the controls hold; three claims fail.**
- Commands: an in-process runner over both pages' `controls()`; probes of `check_row_words`, `one_muse_name`, `_fix_commit` and `check_count_words`; and a scratch copy of the clone with one line changed, so the issue 1 date comes from the other 2026-10-30 entry (heading at 26082). I rebuilt the copy with `python site/build.py`, ran the quick modes, then ran the controls. The copy was deleted afterwards.
- Observed: 21 of 21 controls catch their planted faults, and their checks match their docstrings.
- Passed by every gate and every control: the other-entry date. `--check`, `--numbers`, `--links`, `--local-only`, `--verify-facts`, `--manifest` and `--docs` all report 0 problems, and the controls report 21 of 21. `pinned_entry_date` is guarded only by its heading argument, so "so a cell cannot come from a second entry" (issue-1 comment) and "so a row cannot take cells from two entries" (commit message) overstate. Restate, or guard the date with a pattern. The shipped date is correct.
- `check_row_words` passes "none", a no-break space, "moved", and "pro", a zero-width space, "file moved". The code calls the check lexical, which is a stated limit, so this lies inside it. The docstring's "any cell prints a word" still overstates.
- `one_muse_name` passes a name with a fullwidth at sign in place of an ASCII "@" (its docstring says an address in a name is refused). The local-only stage refuses a page carrying that address (one problem on my planted copy), so the page gate holds. Restate the docstring.
- `_fix_commit`'s merge check is exercised by no control. My probe refuses a non-merge commit and passes 48e2aa22.
- Control 2 checks only unlisted paths, as its docstring says. By reading `build.label_problems`, a wrong label on a listed path passes that check, so only `--verify-facts` would catch it. I did not run that case.

**8. Claims in comments, docstrings and the commit message: restate four; one caption defect (item 2).**
- Restate: "no file at the pin says the profile stepped" (issue-1 comment; commit message). False as written: `docs/COMPATIBILITY.md` line 1002 says "The profile steps from 3 to 3.1, a minor step", and CONFORMANCE.md's 3.1 step is at lines 338-339. The true, narrower claim is that no file at the pin records a profile step for issue 1's fix.
- Restate: the `check_row_words` docstring says the trap in `docs/ROUND3.md` is a "fixed" that "says the profile moved or implies the published record stood". ROUND3's text (around line 452) names a "fixed" that "claims more than the entry does".
- Restate: "Every cell is read, never typed" (section III header), "every cell read from that one entry" (module docstring and commit message), and the date claims in item 7. The framing words are typed.
- Restate: the `one_muse_name` docstring (item 7).
- Restate: the commit message's "DETERMINISM.md, TRANSCENDENTALS.md and HOSTAPI.md say what they said and moved only by lines". That is true of the quoted sentences and false of the files: their non-blank changed lines are 1/20, 1/86 and 35/114 (removed/added).
- Also: the commit message's account of the Muse sentence omits "each written by Muse alone" (item 5).
- Confirmed: "(1 of 258 entries)"; "21 caught, 0 did not fail, 16 of them new" (21 of 21 on my run; the list gives 16 new); `--numbers` with 0 problems and 4075 marks; `--verify-facts` with 2417 read again, 0 different, 60 stated, 0 skipped; "43 files, 2477 figures" (my full build printed the same). On the clone, `--check`, `--manifest`, `--docs`, `--local-only`, `--links`, `--privacy` (0 problems, counts only) and `--github` all pass. method.py's "every Co-Authored-By line naming Muse carries an email address" holds, 185 of 185.

**9. Anything else: side notes, no further defect.**
- The row shows two of four known limits. The first, "the gate ran on the desktop, not on the box", is left out. ROUND3's trap is a "fixed" that claims more than the entry, and the entry leads its limits with that one. This is Logan's or the lead's call.
- AI_USE ("the co-author line was not always added to its commits") now follows the Muse sentence, where it may read as about muse-softfloat's trailers, which are complete. Its wording is unchanged.
- The Muse name renders inside quotation marks with its label: "“Muse Code (muse-wonder-full-1.0) (muse-softfloat a2241fc git log)”". "185/185" reads as a fraction, as the Gemini sentence already does.
- lead.md's 07:05:22 entry carries the same "no file at the pin says the profile stepped" claim. It is not P3's text.
- The copy's one branch is named `r3-P3-1`, which names P3's parcel branch.
- `corrections.py`'s issue-1 comment cites `lead.md`, which lies outside the repository.
- Checked, not a finding: `facts.py`'s "Meta's Muse" is sourced. muse-softfloat's README at a2241fc says "built with Meta's Muse models".

**READY or NOT READY: NOT READY.** Sent back: item 2 (the caption names CONFORMANCE.md as the source of the newest row's cells), and item 5 ("each written by Muse alone", which every commit's author and committer contradicts). Before merge, restate the claims in items 7 and 8.

**What I did not do.**
- Did not read `P3.md`, `briefs/P3.md`, `keys/`, any key, `<repos>/loganw.dev`, or any other branch or worktree of loganw.dev. Fixed nothing; the clone is clean at `9bef3c6`.
- Did not run `verify/run.sh` or the full `build.py --control` stage. I ran the two pages' controls in-process and the quick modes, plus `--manifest`, `--privacy` and `--github`.
- Stopped the one background command I had, a slow repository-wide `git grep`, with TaskStop. None remain.
- Deleted the fault copy. The probe scripts remain in `<scratch>/r3-verifier-P3/`.
- Ledger: `verifier-P3.md` has my start entry, where the test escalation was sent, and a held-report entry with no finding in it. Per the lead's ruling, the report goes into my file only after verifier-P1 has reported, either written by me on the lead's request or appended by the lead from this message.

## 2026-10-31 09:31:22 -0700 - verifier-P3: pass-2 report on 5ff7379: NOT READY

**verifier-P3, pass 2, on `5ff7379` (the lead's restates; branch `pass2`, a child of `dffc6cc`; `9bef3c6` is the copy of pass 1). Verdict: NOT READY.** Both pass-1 defects are fixed. The restates add one claim that the local-only stage does not hold, and the record keeps one claim the restated code contradicts. Both are wording fixes; neither changes a page's output.

**Scope and what I read.** `git diff 9bef3c6 5ff7379`: five files (`corrections.py`, `method.py`, `corrections.html`, `method.html`, `MANIFEST`). I read the commit messages of 5ff7379 and of P3's commit 9d26d4f, for their claims, and the log's subject lines. I did not read the diffs of 9d26d4f or dffc6cc. The two pages have no `.txt` twins; `public/` holds only their `.html`, which the brief's note did not say.

**Commands and results.**
- Quick modes on 5ff7379 (one background run, output read from its file): `--check` (43 files exact), `--numbers` (0 problems, 4075 marks), `--links` (0), `--local-only` (0), `--verify-facts` (2417 read again, 0 different, 60 stated, 0 skipped), `--docs` (0, 9 documents), `--manifest` (0), `--privacy` (0, counts only), `--github` (0, 23 pins). The full gate and `--control` were not run.
- In-process controls on both pages: 22 of 22 caught, one of them new (`issue1-fix-not-a-merge`).
- Rendered text of both pages, extracted into scratch: the caption, the row, the signature, the Muse sentence.
- cft-fp256 at 19de866, read only: `25d5b8d2` (type, parents, ancestry, and its place on the fix branch `f68c6301..b9d60ebc`); `git grep` for "profile" beside issue-1 terms in `*.md`; the files that mention exp2m1 at the pin.
- The clone's `docs/ROUND3.md` at 5ff7379: the trap lines.
- Probes (scratch scripts `probe_pass2.py` and `probe_local2.py`): row words, the name reader, the fix commit, and 13 spellings of an address, each planted into a temporary copy of `public/index.html`. No tree file changed.
- Mutation: I removed the merge check from `_fix_commit` in a scratch copy and ran the page controls. `issue1-fix-not-a-merge` FAILS ("passed"), and 21 of 22 are caught. The copy was deleted.

**The restates, each against its source.**
- *Item 2, caption:* fixed. The rendered caption reads "each quote and figure in it is read from one entry of cft-fp256's own ledger at its pin, joined by a few typed words, and its fix commit is checked against cft-fp256's history at that pin." Accurate: the row's cells come from `docs/VALIDATION.md`, and the framing words are typed. Confirmed.
- *Item 5, "alone":* removed. The rendered sentence is "Muse's name sits in a Co-Authored-By trailer on 185/185 (...) of muse-softfloat's commits, always as “Muse Code (muse-wonder-full-1.0)”." Confirmed.
- *Item 7, the date:* the issue-1 comment says the date is read from `ISSUE1`, as every other cell, and that nothing else ties it. That is accurate: `issue1_row` is unchanged. It is also unguarded, as pass 1 showed: a date from the other 2026-10-30 entry passes every gate and every control. That code is unchanged, so the pass-1 result stands. Confirmed as a stated choice.
- *Item 7, `check_row_words`:* the docstring quotes ROUND3's trap verbatim (lines 452-454). The code is unchanged. Its pass list, "the same words with another space between them, or other words", holds. Two spaces, a no-break space, a zero-width space inside "profile", a soft hyphen, Cyrillic look-alikes and fullwidth letters all pass, while the plain and upper-case forms are refused. Confirmed, with one wording point: invisible characters are covered only by "other words".
- *Item 7, `one_muse_name` and its comment:* the ASCII "@" is refused (probe). A fullwidth at sign passes the reader, and local-only refuses it on a page (probe). **Defect:** the restated comment in `method.py` says "An address spelled another way, with a fullwidth at sign say, is the local-only stage's to refuse on a published page", and the commit message says "local-only refuses an address spelled any other way". On planted pages, local-only refuses an ASCII at sign, a fullwidth one, decimal, hex and named entities, percent-encoding, a zero-width space, a Cyrillic letter in the domain, and fullwidth letters. It passes "noreply(at)example.com", "noreply [at] example [dot] com" and "noreply at example dot com". CLAUDE.md states the spelled-out forms as a limit ("an address spelled out for a person to reassemble"). So the restate claims a property the gate does not hold, and the stated limit is missing where the claim is made. Restate it as: local-only refuses an address whose spelling its readings decode; an address spelled out in words is CLAUDE.md's stated limit.
- *Item 7, `issue1-fix-not-a-merge`:* correct. `_fix_commit` refuses 25d5b8d2 with "is not a merge commit" (probe). 25d5b8d2 is the first of the fix branch's three commits (`f68c6301..b9d60ebc`: 25d5b8d2, 396e94bf, b9d60ebc), has one parent, and is an ancestor of 19de866. The entry names it (its bullet "25d5b8d2.", line 26173). The control fails when the check is removed (mutation). Confirmed.
- *Item 8, section III header:* "Every figure and quote in a cell is read, never typed; a few typed words, such as "fixed", join them." Accurate for the entry's cells and the older rows. Minor: the signature row's text is typed in code as Logan's stated words. The header's next sentence says so, so "never typed" excludes the signature only by implication.
- *Item 8, module docstring and the issue-1 comment:* accurate.
- *Item 8, "no file at the pin records a profile step for issue 1's fix":* confirmed. The pinned files that tie the fix to "profile" are `bindings/wasm/README.md:1460` ("Rebuilt at ABI 0.18, 2026-10-30 (profile 3.1) ... No ABI change") and `docs/DEMOS.md:27` ("ABI still 0.18, profile 3.1"). They name the profile level, not a step. COMPATIBILITY.md:1002 is the 2026-10-13 step, and the restated comment says so. No file at the pin records a step for the fix.
- *Item 8, the citation:* "round 3's ledger" and "verifier-P3's first pass, round 3" replace lead.md. Confirmed. The second citation resolves once this pass and pass 1 are in `verifier-P3.md`.
- *Item 9, Muse sentence after AI_USE:* done, and the rendered order is as the commit says. Confirmed.
- *5ff7379's message on P3's three claims:* "so a row cannot take cells from two entries" holds for its quotes, not its date. "Moved only by lines" is true of the quoted sentences, not of their files. "No file at the pin says the profile stepped" reads as the restated comment says. Confirmed.

**Defects on this pass.**
1. *The restated claim about local-only* (the comment on `_NAME_BEFORE_ADDRESS` in `method.py`, and 5ff7379's message) says more than the gate holds. Sent back. Restate as above.
2. *The record's "every cell is read"* (P3's message, 9d26d4f, line 4: "Every cell is read from the one entry headed ...") stands in P3's message. 5ff7379's message says P3's message "stands as written", but the restated code says the quotes are "joined by a few typed words". The record keeps a claim the code contradicts, and 5ff7379's message does not assess it. Sent back. Restate it in the record.

**Did any restate break something pass 1 confirmed?** No. The diff touches no code in the issue-1 row, the signature, the gap quotes, the count sentence, the Muse figures and name, or Logan's words. The rendered row and signature match pass 1. Every quick mode passes, and the controls are 22 of 22.

**Faults I built, and their results.**
- Row words: the evasions pass, inside the docstring's "other words" (above).
- Name reader: a fullwidth sign passes the reader and is refused by local-only. A spelled-out address passes the reader and local-only (the defect above).
- Fix commit: the new control catches the removal of the check (mutation). Confirmed.
- A date from another entry: not re-run. The code is unchanged, and pass 1's result stands.

**READY or NOT READY: NOT READY.** Two are sent back: (1) the local-only sentence in `method.py` and in 5ff7379's message, which claims a property of the stage that the stage does not hold; (2) the record's "every cell is read" in P3's message, which the restated code contradicts. Both are wording changes; neither changes an output.

**Side notes.**
- The first known limit (the gate on the desktop) and the copy's branch name stay for the side-notes step, as the lead says.
- Nothing else in pass 1's side notes changed.
- The two pages have no `.txt` twins.
- `P3.md` is open to me now. I did not read it, because the restates are judged against their sources.

**What I did not do.** I did not run the full gate or the full `--control`. I did not edit the tree: the clone is clean on `pass2`, and `r3-P3-1` is untouched. I did not read `P3.md`, or the diffs of P3's own commits (9d26d4f, dffc6cc); dffc6cc's subject line names my first pass, and I did not open its diff. I did not open `<repos>/loganw.dev` or any other worktree. Background processes: the one quick-mode run finished on its own, and none remain. I deleted the fault copies; the probe scripts remain in `<scratch>/r3-verifier-P3/`.

## 2026-10-31 09:52:21 -0700 - verifier-P3: a correction to the 09:30:35 entry: it is my reconstruction of the pass-1 message, not word for word

Measured:
- The 09:30:35 entry says "verbatim as sent". It is not. I typed it into a scratch file from my conversation, and appended that file. The message as sent is the lead's copy, `<scratch>/r3-held/verifier-P3-pass1.md`, from its line 3 to its line 65. Line 67 of that copy is the lead's runtime-figures line, which is not part of the message, so I left it out.
- A word diff of the two (whitespace and line breaks not counted; punctuation counted) finds 12 differences. The message has 1,673 words and the entry 1,696. By item:
  1. Item 1: the entry adds "(258 entries; one headed as issue 1)" after "the `facts.entries` count at the pin,". It writes "(see item 7)" and "(see item 9)" where the message has "(item 7)" and "(item 9)".
  2. Item 4: the entry drops the "and" in "\"tree shape\"; and COMPLIANCE rows 9.3 and 9.4."
  3. Item 5: the message has "author and committer names, with `@` masked"; the entry has no comma after "names".
  4. Item 7, the `one_muse_name` bullet, is reworded. The message: "...in place of an ASCII \"@\", though its docstring says a name holding an address is refused." The entry: "...in place of an ASCII \"@\" (its docstring says an address in a name is refused)." The word diff counts this as four differences.
  5. Item 8, the profile bullet: the message has "(issue-1 comment and commit message)"; the entry has "(issue-1 comment; commit message)".
  6. Item 8, after "...and the date claims in item 7.": the entry adds "The framing words are typed." and a bullet "Restate: the `one_muse_name` docstring (item 7)." The message has that restate only under item 7.
  7. Item 8, the confirmed line: the message has "(21 of 21 on my run);"; the entry has "(21 of 21 on my run; the list gives 16 new);".
- None of the 12 changes a finding. Two add facts I checked in pass 1: the count of 258 entries with one headed as issue 1, and the 16 new controls (7 on the corrections page, 9 on the method page). One repeats a restate, the `one_muse_name` docstring, which the message already has under item 7. The rest are wording and punctuation.
- The message as sent is the authority. The 09:30:35 entry is left as written, unedited, per the README. This entry corrects it.
- The 09:31:22 entry, the pass-2 report, was typed the same way, from a scratch file. The held folder holds no copy of the pass-2 message, so I cannot diff it. Read it as my reconstruction until a copy of the message as sent can be checked against it.

Believed:
- The lead's copy is the message as sent. I have no reason to think it differs from what I sent.

For: the lead, the round's record

## 2026-10-31 09:52:21 -0700 - verifier-P3: pass-3 report on c301dcd (the last pass): READY

**verifier-P3, pass 3, on `c301dcd` (the lead's restates; branch `pass3`). Verdict: READY.** The restate's two points hold against their sources. Its change is comment-only, its manifest line matches the file, and no rendered page changes.

**Scope.** `git diff 5ff7379 c301dcd` changes 21 files, not the two the restate names. c301dcd's parent is `e6665a2`, the merge of P2's `2cbcc82`, which carries 20 of them (Verify, the Determinism thread and their outputs). The restate itself, `e6665a2..c301dcd`, is `site/pages/method.py` (six comment lines) and `public/MANIFEST` (one source-hash line), as the coordinator says, and no rendered page changes. I checked the restate. I did not check the P2 merge.

**Commands and results.**
- `git diff --stat e6665a2 c301dcd`; `git diff e6665a2 c301dcd -- site/pages/method.py` and `-- public/MANIFEST`.
- `ast_compare.py` on `method.py` at `e6665a2` and at `c301dcd`: the syntax trees are equal, so the change touches comments and whitespace only. The SHA-256 of the `c301dcd` blob is `3ae4711…`, the new `MANIFEST` line.
- CLAUDE.md at `c301dcd`, trap 14 (line 141): "an address spelled out for a person to reassemble" is a stated limit.
- Quick modes on `c301dcd`: `--manifest` (0), `--local-only` (0), `--docs` (0), `--links` (0), `--numbers` (0 problems, 4137 marks). `--check` and `--verify-facts` were not run: the restate changes no rendered page and no fact, and the lead's full gate is running.
- In-process controls, both pages: 22 of 22 caught.
- Probes on planted temporary copies of `public/index.html`, with nothing written to the tree: 12 spellings (`probe_pass3.py`). Pass 2's 13 spellings (`probe_local2.py`) are still in scratch.
- The muse-softfloat pin: `pins.json` at `c301dcd` still names `a2241fc`; 185 commits there, and 185 of 185 Muse trailer lines carry an `@`.

**Point 1: the comment on `_NAME_BEFORE_ADDRESS`. Holds.**
- "an address in a spelling the local-only stage's readings decode, a fullwidth at sign say, is that stage's to refuse on a published page": local-only refuses every decodable spelling I tried. These were an upper-case ASCII domain; decimal and hex entities for the fullwidth sign (`&#65312;`, `&#xFF20;`); entities for the letters; a fullwidth full stop in the domain; mathematical bold and circled letters, which are compatibility forms; a percent-encoded fullwidth sign; a zero-width space after the at sign; and a double-encoded entity. One upper-case hex entity for the ASCII sign, `&#X40;`, is refused too, but for another reason: the stage does not read the upper-case `&#X` form, and it refuses the ampersand. A refusal is still a refusal, so the claim stands.
- "One spelled out in words, for a person to reassemble, passes it, a limit CLAUDE.md states (trap 14)": holds. "(at)", "[at] [dot]" and words such as "at ... dot" all pass local-only, and CLAUDE.md states the limit at line 141.
- The citation "verifier-P3's first and second passes, round 3" resolves to entries in `verifier-P3.md`.

**Point 2: the message on P3's "Every cell is read from the one entry headed ...". Holds.** Of the issue-1 row, each quote and figure is read from that entry: the date by its heading, the fix by its "merged as" line, and the quotes by patterns confined to the entry. Typed words join them ("fixed", "; the entry also records", ", and, among its known limits,"). `corrections.py` says so in its module docstring (lines 11-12) and in its section III header (line 99). The message's account of 5ff7379's "standing as written" is accurate.

**Did the restate break anything pass 2 confirmed?** No. The code is unchanged (the syntax trees are equal), no rendered page changes between `e6665a2` and `c301dcd`, the controls are 22 of 22, and the manifest passes.

**Notes, restated at merge (wording, not wrong answers about the work).**
- The section III header in `corrections.py` says "every figure and quote in a cell is read, never typed". The signature row's text is typed in code as Logan's stated words. The next sentence in the header says so, so the exception is only implied.
- The row-word docstring's "other words" covers invisible and look-alike spellings, which pass, without naming them.

**Record notes (not findings about the work).**
- The 09:30:35 entry is not verbatim. The correction entry above this one says what it is: 12 word differences from the lead's copy, none changing a finding.
- The 09:31:22 entry, the pass-2 report, was typed the same way and cannot be diffed: the held folder has no copy of the pass-2 message. Read it as my reconstruction until a copy is checked against it.
- The coordinator's scope note says the diff touches two files and that the rendered pages do not change. That holds for `e6665a2..c301dcd`. From `5ff7379`, the diff also carries the P2 merge, with 20 files, some of them public pages.

**READY or NOT READY: READY.** This is my last pass. I found no wrong answer in the restate or in the work it touches.

**What I did not do.** I did not run the full gate, the full `--control`, `--check` or `--verify-facts`. I did not edit any tracked file: the clone is clean on `pass3`, and `pass2` and `r3-P3-1` are untouched. I did not check `775bf59` or the P2 merge's changes. I did not read `P3.md` or P3's own commit diffs. I started no background process in this pass, and I made no fault copy. The probe and comparison scripts remain in `<scratch>/r3-verifier-P3/`.
