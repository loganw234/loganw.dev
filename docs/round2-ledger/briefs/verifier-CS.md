# Brief: verifier-CS (round 2's case study and its archived ledger)

Read `briefs/_verifier.md` first; it holds everything every verifier is
given. This is what is yours.

## What you verify

`docs/ROUND2-CASE-STUDY.md` and `docs/round2-ledger/` at the commit the
dispatch message names, on the branch `round2-close` of loganw.dev, in a
worktree of your own. It is the lead's own record, written after the round
from its ledger and the session's transcripts, so it goes past you like a
parcel's work. There are no planted faults in it.

Ten of round 2's eleven earlier agents' reports, and the lead's record of
each, are in the ledger, `<repos>/loganw-dev-r2-ledger/` (the archive in
the commit is a copy of it as it stood then; the ledger has grown since).
The lead's session transcript is
`<the lead's transcript, as the dispatch message names it>`; you may read it
only to check a figure the case study takes from it, and you quote none of
it beyond what the case study already does.

## Specific things to attack

1. **The timeline**, row by row, against the ledger's own stamps and the
   commits' times. A row that says what happened at a time must have an
   entry or a commit that shows it.
2. **Every figure in the observations**: 8 of 8, 27, 5 and 77, the passes
   and their defect counts, the 31 minutes, the eleven agents, the five
   times Logan was asked, the three wrong claims of verifiers in two of
   twelve reports. Re-derive each from the ledger, the commits or a command,
   by a method of your own.
3. **The cost section.** Run `python <repos>/loganw-dev-r2-ledger/tools/round_metrics.py <the lead's transcript> 2026-10-08T20:16:10Z 2026-10-09T01:56:43Z`
   and compare its tables with the case study's, cell by cell. Then check
   the claims made from them (the shares, the comparisons with ParcelRound's
   case studies 6 and 7, at `f42242e` and `894d125`), and whether the
   method paragraph says what the script does: read the script.
4. **The plants' table** against `keys/` in the archive and the four
   verifiers' reports in the ledger and in `lead.md`.
5. **Each "the lead's slip"** against the ledger entry that records it.
6. **The proposals**: each is labelled as the owner's to settle, and each
   rests on something the round recorded; name any that claims more than
   the round showed.
7. **The archive**: every file in `docs/round2-ledger/` at the commit, byte
   for byte, against the ledger's file as it stood then (the ledger's later
   entries are appended after the commit; say whether any earlier byte
   differs). No secret, no address but the site's contact and the co-author
   trailer's, no absolute path but the elided one the case study's
   verifier-P0 entry flags. Run `python site/build.py --privacy` yourself.
8. **The README rows and CLAUDE.md's trap 19**, against what they describe.
9. **The gate.** Run `bash verify/run.sh --require-all` on the commit
   yourself, from clean (no other gate is running while you do), and read
   its log.
10. **Anything else.** Tell the lead what it did not think to ask.
