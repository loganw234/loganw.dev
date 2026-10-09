# Brief: verifier-I (the integration: the lead's merges, restates and records)

Read `briefs/_verifier.md` first; it holds everything every verifier is
given. This is what is yours.

## What you verify

The lead's own work on the branch `round2`, from `427900e` (the seam
commit, which verifier-P0 passed) to the tip the dispatch message names.
It is the lead's, so it goes past you like a parcel's (METHOD.md section 7).
You work in a git worktree of loganw.dev. There are no planted faults in
this work. The parcels' own commits and their verifiers' reports are not
yours to redo; the lead's handling of them is.

In order, on `round2` (`git log --oneline 427900e..<tip>`):
- `4d534df`, the merge of P4's `1e6b4ec`; `e349b1a`, the lead's restates;
- `e4c4a67`, the merge of P1's `bef03b0`;
- `0052634`, the merge of P2's `37d0609`; `7850d3a`, the lead's restates;
- `8b4973a`, the merge of P3's `583d3eb`; `a4a438c`, the lead's restates;
- `9b35773`, the round's entry in `docs/VALIDATION.md`, and Corrections'
  description.

`lead.md` records, for each verifier's report, the lead's check of each
finding and its decision; read it before you read the commits.

## Specific things to attack

1. **Each merge, made again.** For each of the four merges, rebuild what it
   should hold from its parents with `git merge-tree --write-tree <first
   parent> <second parent>`, and compare with the merge's tree: every path
   changed on one side only must equal that side's, and nothing may be
   lost. `public/` is regenerated at each merge, so compare `public/`
   against a build of the merge's `site/` instead: `python site/build.py
   --check` at the merge commit must pass. Is any source file different
   from what the merge of its parents gives?
2. **Each merge took the parcel's own commit**, by its SHA, never a planted
   copy. The planted branches are `r2-plant-P1` to `r2-plant-P4`; none of
   their plants (see `keys/` in the ledger, now that every planted-copy
   verifier has reported) may be on `round2`. Search the tree at the tip for
   each plant's new text.
3. **Each restate** (`e349b1a`, `7850d3a`, `a4a438c`, and the corrections.py
   line in `9b35773`): is the new sentence true at its pin? Does it answer
   the finding `lead.md` says it answers, and only that? Did any restate
   change a word of Logan's (a `stated()` text, About, the front page, a
   spec choice)?
4. **The records.** `docs/VALIDATION.md`'s new entry, sentence by sentence,
   against `lead.md`, the commits and the sources it names. Every figure in
   it (the pins, the counts, 8 of 8, 393 of 393, the passes) against the
   command that gives it. `docs/SPEC.md`'s decisions 31 to 36 and
   `docs/ROUND2.md`, against `lead.md`'s record of Logan's words. The four
   merge commits' and three restate commits' messages, claim by claim.
5. **The findings the lead decided not to send back.** `lead.md` records,
   for verifier-P1 to verifier-P4, which findings the lead restated at the
   merge and which it left as notes. Do you agree with each "not a wrong
   answer"? Name any you would have sent back.
6. **The whole site at the tip, as a reader meets it:** read the published
   text of every page a parcel changed (`public/*.html` and the `.txt`
   twins), and look for a sentence that two merges together made false,
   such as a page that now says something another page contradicts.
7. **The gate.** Run `bash verify/run.sh --require-all` yourself on the tip,
   from clean, and read its log.
8. **Anything else.** Tell the lead what it did not think to ask.
