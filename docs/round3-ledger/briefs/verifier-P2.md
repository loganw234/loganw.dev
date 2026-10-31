# Brief: verifier-P2 (Verify and the Determinism thread)

Read `briefs/_verifier.md` first; it holds everything every verifier is
given. This is what is yours.

## What you verify

The commit your dispatch names, the tip of the one branch in your clone:
P2's work on `site/pages/verify.py` and `site/pages/thread_determinism.py`,
and the `public/` built from them, against cft-fp256 at its pin `19de866`,
and softfloat-bootstrap (`a23a0ff`), muse-softfloat (`a2241fc`) and
HonestHarness (`b69ed76`) at theirs. **The copy may hold faults the lead
planted.** Report everything you find as a finding. Read `P2.md` in the
ledger only after you have reported.

What P2 was asked (ROUND3.md, "P2: Verify and the Determinism thread";
SPEC.md, decision 56):
- Verify and the thread become the current truth at cft-fp256's new pin;
- Verify keeps its order, and its lede no longer says "cheapest first";
- the thread says what its lane now holds.

## Specific things to attack

1. **Every quote on both pages**, against its file at its pin, and the
   lines around it: does a sentence claim more, or other, than its quote?
2. **Verify's costs**: the `make golden` line, the quick and gate budgets.
   Each with where and when it was measured, as decision 56 says? Does any
   cost read as today's, or as everyone's, when its source says otherwise?
3. **The browser replay**: what it holds, what a pass proves, and the
   module's lapse and rebuild. Is each true at the pin, and does the page say
   which deploy a reader's browser will see?
4. **Section II, the limits**: issue 1, the digests limit, the nightly page.
   Does each say what its source says, and no more?
5. **The thread's new paragraph**: each project's words against its README
   at its pin; the audit's sentence against cft-fp256's ledger; anything a
   reader would take as said by a source that does not say it. Is the word
   "outside" kept off both pages, and is softfloat-bootstrap's "stays
   private" line never quoted (decision 47)?
6. **Logan's words**: the Determinism door, its "workloads" and
   "bit-identical everywhere" (decision 27): unchanged? Does propose.py's
   own control still pass?
7. **Every claim in a comment, a docstring or the commit message** P2 wrote,
   and its new control's: does it fail on the fault it names?
8. **Anything else.** The list above is what the lead suspects. Tell it what
   it did not think to ask.
