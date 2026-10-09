# Brief: verifier-P2 (the two methods)

Read `briefs/_verifier.md` first; it holds everything every verifier is
given. This is what is yours.

## What you verify

Parcel **P2**'s work: the commit the dispatch message names, in your own
clone, `<scratch>/r2-verifier-P2/loganw.dev`. **It may hold faults the lead
planted.** Read `git show <the commit>`, `briefs/P2.md` (P2's brief), and
`docs/ROUND2.md`'s P2 section. Read `P2.md` in the ledger only once you have
formed your own view.

P2's job: make the pages about the two methods the current truth at their
pins: ParcelRound moved from `8767e23` to `f42242e` (its round 6: METHOD.md
brought to the method as practised, ADOPTION.md, the gate
`tools/check_method.py`, the templates, case studies 5 and 6); HonestFramework
did not move (`65447fd`). Its files: `site/pages/work_parcelround.py`,
`site/pages/work_honestframework.py`, `site/pages/method.py`,
`site/pages/propose.py`. The lead's answers to its design are in `lead.md`
(the entry after 15:58): the Method page's section III retitled, with items
for case studies 5 and 6, each with its limit and models; a new fact,
`adoption_state`, counting ADOPTION.md's rows; the gate's threat model
quoted; a third kept failure; three items that were never true removed; no
paragraph on HonestHarness.

## Specific things to attack

1. **Every sentence of the pages' own words** against the sources at their
   pins. Does any claim more than its source, in tense, scope or quantity?
   Does any figure or statement describe a different set of case studies or
   rounds than the sentence around it says (P2's brief names this as its
   likeliest regression)?
2. **Every quotation, and where it is cut**, against the case studies,
   METHOD.md, ADOPTION.md and `tools/check_method.py` at `f42242e`.
3. **`adoption_state`**: re-count ADOPTION.md's rows by status yourself, by
   a method of your own, and compare. Build a copy of ADOPTION.md with one
   row's status changed or a row added: does the fact read it, or refuse a
   shape it doesn't know?
4. **The gate's claims**: run `python tools/check_method.py` and `--control`
   in a clone of ParcelRound detached at `f42242e`, in your scratch; does
   the page say what they say, and no more?
5. **The models and the plants** the Method page states for rounds 5 and 6,
   against the case studies' own words.
6. **What was removed**: the three never-true items and "under a second".
   Is anything left that sends a reader to a source for something the
   source doesn't hold?
7. **Logan's words**: the ratio, the co-authorship statement, the method
   door, every `stated()` line, and the three thread doors propose.py
   renders: unchanged.
8. **P2's controls**: re-run at least two of its four from copies; each must
   fail for the reason it was written for.
9. **Scope**: `git diff --stat <parent> <commit>` against P2's brief; and the
   commit message's claims, one by one.
10. **Anything else.** Tell the lead what it did not think to ask.
