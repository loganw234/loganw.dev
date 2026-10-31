# Brief: verifier-I (the integration: the lead's merges, restates and records)

Read `briefs/_verifier.md` first; it holds everything every verifier is
given. This is what is yours.

## What you verify

The lead's own work on the branch `round3` after the seam: from `6eff67b`,
where the lead took verifier-P0's notes on the seam commit, to the tip your
dispatch names. It is the lead's, so it goes past you like a parcel's. You
work in a clone of loganw.dev at that tip. There are no planted faults in
this work. The parcels' own commits and their verifiers' reports are not
yours to redo; the lead's handling of them is.

In order on `round3` (`git log --oneline 6eff67b..<tip>`):
- `dffc6cc`, the merge of P3's `9d26d4f`, and `5ff7379`, the lead's restates
  for verifier-P3's first pass;
- `e6665a2`, the merge of P2's `2cbcc82`;
- `c301dcd`, the lead's restates for verifier-P3's second pass;
- `e03b3bc`, the lead's restates for verifier-P2's first pass. It also adds
  "Makefile" to build.SOURCE_PATHS, a seam change of the lead's;
- `775bf59`, the merge of P1's `7e576fd`;
- `cbb78e0`, the lead's restates for verifier-P1's first pass;
- `2bfafe1`, for verifier-P2's second pass;
- `ffdcbb1`, for verifier-P1's second pass;
- then the commits your dispatch names: the round's entry in
  `docs/VALIDATION.md`, and any after it.

`lead.md` records each verifier's report, the lead's check of each finding
at its source, and its decision. Read it before you read the commits. Each
verifier's own file holds its reports, and `keys/` holds the plants, now
that every planted-copy verifier has reported.

## Specific things to attack

1. **Each merge, made again.** For each of the three merges, rebuild what
   it should hold from its parents with `git merge-tree --write-tree
   <first parent> <second parent>`, and compare with the merge's tree for
   every path outside `public/`. Every path changed on one side only must
   equal that side's, and nothing may be lost. `public/` conflicted at each
   merge and was rebuilt, never merged as text, so hold it to a build
   instead: `python site/build.py --check` at the merge commit must pass.
2. **Each merge took the parcel's own commit**, by its SHA, never its
   planted copy. Search the tree at the tip for each plant's new text in
   `keys/`.
3. **Each restate:**
   - Is its new sentence true at its pin, and does it answer the finding
     `lead.md` says it answers, and only that?
   - Did any restate change a word of Logan's: a `stated()` text, About,
     the front page, a thread's door, Corrections' signature row or rules
     of engagement, a spec choice?
   - Does `e03b3bc`'s new source path name a file at cft-fp256's pin, and
     does every label that names it cite a line that holds the quote?
4. **The records:**
   - `docs/VALIDATION.md`'s new entry, sentence by sentence, against
     `lead.md`, the commits and the sources it names. Its account of the
     push of `797f588` and of the 2026-10-31 cleanup is to be read against
     `<repos>/loganw-dev-resume-ledger/lead.md`.
   - Every figure in the entry, against the command that gives it: the pins,
     the counts, 5 of 6, the gate's figures, and the cost table against
     `tools/round_metrics.py`'s own output.
   - `docs/SPEC.md`'s decisions 47 to 56, against `lead.md`'s record of
     Logan's words.
   - The merge and restate commits' messages, claim by claim.
5. **The findings the lead did not send back.** `lead.md` records the
   findings the lead restated, those it left, and the side-notes step
   (its entry headed 10:14:15). Do you agree with each that it left? Name
   any you would have sent back.
6. **The whole site at the tip, as a reader meets it.** Read the published
   text of every page the round changed, and look for a sentence that two
   merges together made false: one page saying what another contradicts.
   Look in particular at:
   - Verify, cft-fp256's dossier and the resume, which give make golden's
     cost and the nightly figures;
   - the Determinism thread, Corrections and the dossier, which tell of
     issue 1;
   - Method, About and the front page, which name the AI collaborators.
7. **The gate.** Run `bash verify/run.sh --require-all` yourself on the tip,
   from clean, but only after the lead's message says its own gate on the
   tip has ended. Two gates side by side each take several times as long
   (CLAUDE.md trap 19). Read its log.
8. **Anything else.** Tell the lead what it did not think to ask.

## Your ledger file

`verifier-I.md`. Write your report once, to a scratch file, and append
that file to your ledger file by a command, under a stamp from the clock.
The ledger's copy is the record. Your final message to the lead gives the
report too; if it differs from the ledger's copy, say so in it.
