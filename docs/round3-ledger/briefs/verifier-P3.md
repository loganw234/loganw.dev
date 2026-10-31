# Brief: verifier-P3 (Corrections and Method)

Read `briefs/_verifier.md` first; it holds everything every verifier is
given. This is what is yours.

## What you verify

The commit your dispatch names, the tip of the one branch in your clone:
P3's work on `site/pages/corrections.py` and `site/pages/method.py`, and the
`public/` built from them, against cft-fp256 at its pin `19de866` and
muse-softfloat at its pin `a2241fc`. **The copy may hold faults the lead
planted.** Report everything you find as a finding. Read `P3.md` in the
ledger only after you have reported.

What P3 was asked (ROUND3.md, "P3: Corrections and Method"; SPEC.md,
decisions 49 and 50):
- Corrections' ledger gains issue 1's row, every cell read from cft-fp256's
  ledger at the pin, and the signature row stays;
- the ledger's caption is restated;
- the "where I'd attack first" quotes are re-read at the pin;
- Method's co-authorship section gains a sentence read from muse-softfloat's
  trailers, and its count sentence is restated to the rule as it now reads.

## Specific things to attack

1. **Issue 1's row, cell by cell**, against `docs/VALIDATION.md` at
   `19de866`, the entry headed "2026-10-30 - issue 1, the first outside
   report: ..." (`git -C <repos>/cft-fp256 show 19de866:docs/VALIDATION.md`).
   Is each cell what the entry says? Does any cell read from another entry?
   Does "fixed", with what stands beside it, claim more than the entry does?
   Is `48e2aa22` the fix, a commit the pin descends from?
2. **The caption** under the ledger: does it say truly what each row is read
   from, and where its fix is checked?
3. **"found by"**: does the row read as a stranger's report anywhere? The
   signature row must stay, and say what it said.
4. **The gaps**: each quote under "where I'd attack first" against its file
   at the pin, and the ledger's newer entries: does the record now say a gap
   was closed?
5. **Method's two sentences**: the count sentence's words against the rule
   that makes its figure (`facts.AGENT`); the Muse sentence's figures and
   name against muse-softfloat's commits at `a2241fc` (read its clone under
   `.cache/repos/`). Does any word around them claim more than the trailers,
   or the commits' authors, show? Does any published file print an email
   address from those trailers?
6. **Logan's words**: the rules of engagement, the signature row,
   decision 9's statement and its ONLY_HERE, the ratio, and his word on the
   trailers: unchanged?
7. **The new readers and controls** P3 wrote: does each hold what its
   docstring says? Build a fault each one passes.
8. **Every claim in a comment, a docstring or the commit message** P3 wrote.
9. **Anything else.** The list above is what the lead suspects. Tell it what
   it did not think to ask.
