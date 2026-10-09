# Brief: verifier-P1 (cft-fp256 and the Determinism thread)

Read `briefs/_verifier.md` first; it holds everything every verifier is
given. This is what is yours.

## What you verify

Parcel **P1**'s work: the commit the dispatch message names, in your own
clone, `<scratch>/r2-verifier-P1/loganw.dev`. **It may hold faults the lead
planted.** Read `git show <the commit>`, `briefs/P1.md` (P1's brief), and
`docs/ROUND2.md`'s P1 section. Read `P1.md` in the ledger only once you have
formed your own view.

P1's job: make five pages the current truth at cft-fp256's new pin,
`ab51655` (it was `77b8440`): `site/pages/work_cft_fp256.py` (the dossier),
`site/pages/verify.py`, `site/pages/thread_determinism.py`,
`site/pages/corrections.py`, and `site/pages/work_cft_rebound.py` (which it
was to leave unless it reads cft-fp256). The lead's answers to its design
are in `lead.md` (the entry after 15:58): every item it called REQUIRED and
RECOMMENDED was taken; no sentence on HonestHarness; the language and the
certificates added to the Determinism thread from `docs/LANGUAGE.md` and
`docs/CERTIFICATES.md`; the fourth Corrections gap left out.

## Specific things to attack

1. **Every sentence of the pages' own words** against the sources the pages
   cite, at their pins. P1's design lists its connecting words as claims for
   you; read them first. Does any claim more than its source, in tense,
   scope or quantity? Is any a plan stated as done (cft-fp256's
   `docs/ROADMAP.md`, `docs/SEQUENCER.md` and `docs/studies/` state plans)?
2. **Every quotation, and where it is cut.** A quote cut short can say more
   than the whole sentence: the gate budget, the lede, the MPFR pool, the
   major step. Open each source line and read the words after the cut.
3. **The new "Verified" rows and the third kept failure** against the ledger
   entries they cite: the heading lines, the dates, the commit the kept
   failure names (is it an ancestor of `ab51655`, and does it do what the
   row says?).
4. **"Test it" and "Prove it wrong"**: run, or read the Makefile and
   README for, each step as a reader would. Does `make golden` need what the
   page says? Does each check compare what the page says it compares?
5. **Logan's words**: the Determinism door, the rules of engagement, the
   signature row, the gaps' names (the spec's), and "The reduction tree's
   shape": unchanged. Is any line of his now overtaken by the pin?
6. **The gaps' quotes on Corrections**, re-read at `ab51655`: is any gap now
   closed by the record?
7. **P1's controls**: re-run at least two of its four from copies; each must
   fail for the reason it was written for.
8. **Scope**: `git diff --stat <parent> <commit>` against P1's brief.
9. **The commit message's claims**, one by one.
10. **Anything else.** Tell the lead what it did not think to ask.
