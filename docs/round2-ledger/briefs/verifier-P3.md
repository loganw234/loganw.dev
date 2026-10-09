# Brief: verifier-P3 (Quantum-Film and the Film thread)

Read `briefs/_verifier.md` first; it holds everything every verifier is
given. This is what is yours.

## What you verify

Parcel **P3**'s work: the commit the dispatch message names, in your own
clone, `<scratch>/r2-verifier-P3/loganw.dev`. **It may hold faults the lead
planted.** Read `git show <the commit>`, `briefs/P3.md` (P3's brief), and
`docs/ROUND2.md`'s P3 section. Read `P3.md` in the ledger only once you have
formed your own view.

P3's job: make the Film & photography pages the current truth at their new
pins, and add one IBM hardware print to the Film thread's page (Logan's
decision 34: "The Film thread's own page"). Quantum-Film moved from
`a7f02db` to `3a73823`; its clone's folder is `<repos>/moth-quantum`.
StoryDocs, private, moved by one commit to `8548802`. Its files:
`site/pages/work_quantum_film.py`, `site/pages/thread_film.py`, and
`site/styles/r2-P3.css`. The lead's answers to its design are in `lead.md`
(the entries after 15:44): ibm_kingston's law-run print, with the page
saying both that it is first in the pre-registered order and that the
predictions ranked it first, and pointing to the other devices' runs; the
shortfall beside the print; a third kept failure; five permanent caption
controls; Last verified explained, not changed.

## Specific things to attack

1. **The print.** Its bytes against the pin (`git show
   3a73823:docs/prints/<file>`), byte for byte. Its caption: the device, the
   job and the rule, each against the records it names
   (`docs/records/2026-10-05/ibm/`, `docs/HARDWARE-RESULTS.md`, the ledger),
   not against the file's name. Is it the device's law run, and is that what
   the caption says?
2. **The choice of device.** Does the page say why this device, and is that
   reason what `docs/PREREGISTRATION.md` says, without making the chosen
   device look better than the record does?
3. **Agreement and shortfall.** Wherever the page reports what the hardware
   showed, does it give both halves `docs/HARDWARE-RESULTS.md` gives?
   Numbers: is any quoted figure one the ledger later corrected?
4. **Every sentence of the pages' own words** against the sources at their
   pins: tense, scope, quantity. Quantum-Film's README is stale in places at
   the pin ("Not on hardware yet"): does the page quote a stale line as the
   current truth?
5. **Every quotation, and where it is cut.**
6. **The caption controls** in `thread_film.controls()`: does each refuse
   what it says? Build one fault of your own they should catch, and one they
   might not.
7. **Logan's words**: the Film thread's door, unchanged. Map & Ledger's three
   prints are not P3's, and stay.
8. **P3's controls**: re-run at least two of its four from copies; each must
   fail for the reason it was written for.
9. **Scope**: `git diff --stat <parent> <commit>` against P3's brief; and the
   commit message's claims, one by one.
10. **Anything else.** Tell the lead what it did not think to ask.
