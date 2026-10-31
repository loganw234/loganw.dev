# Brief: verifier-P1 (cft-fp256's dossier)

Read `briefs/_verifier.md` first; it holds everything every verifier is
given. This is what is yours.

## What you verify

The commit your dispatch names, the tip of the one branch in your clone:
P1's work on `site/pages/work_cft_fp256.py`, and the `public/` built from it
(`work-cft-fp256.html` and its twin `work-cft-fp256.txt` above all), against
cft-fp256 at its pin `19de866`. **The copy may hold faults the lead
planted.** Report everything you find as a finding. Read `P1.md` in the
ledger only after you have reported.

What P1 was asked (ROUND3.md, "P1: cft-fp256's dossier, and cft-rebound's"):
make the dossier the current truth at the new pin. Its record runs from
2026-10-12 to 2026-10-30 past the old pin, and its data file
`site/nightly.json` holds the nightly sweep. cft-rebound's page was to
change only if it read cft-fp256, and it does not.

## Specific things to attack

1. **Every quote in the nine sections**, against its file at the pin and
   the lines around it: does a sentence claim more, or other, than its
   quote? Read the words between the quotes as closely as the quotes.
2. **The contract paragraph** that sets CONFORMANCE.md's "none moved"
   beside issue 1's entry: does it say only what the two sources say, and
   neither that the profile stepped nor that it should have?
3. **Verified, and the nightly sweep**: every figure against
   `site/nightly.json` at the pin (`git -C <repos>/cft-fp256 show
   19de866:site/nightly.json`). Is each the campaign's total, not one night's?
   Is each given as the pin's, not as today's or as final? Does a sentence
   say what a night is, and that the live page goes on?
4. **Kept failures**: issue 1 in place of the device bullet. Does each
   bullet say what its source says, with the commit that fixed it, one the
   pin descends from?
5. **Test it**: the `make golden` step's cost. Does it say where and how
   its timing was measured, and nothing about other machines it does not
   know?
6. **Prove it wrong**, **Connections** and **Provenance**: the new limit,
   the two edges P0 added, the listed files.
7. **The new facts and controls** P1 wrote (`nightly`, `entry_title`, the
   kept-failure control): does each hold what its docstring says? Build a
   fault each one passes.
8. **Every claim in a comment, a docstring or the commit message** P1
   wrote.
9. **Anything else.** The list above is what the lead suspects. Tell it what
   it did not think to ask.
