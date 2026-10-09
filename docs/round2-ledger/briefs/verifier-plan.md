# Brief: verifier-plan (round 2's plan of record)

You are a **verifier**, not an author. Your job is to try to *disconfirm* the
plan, and to report. You must not fix anything.

Repository: loganw.dev, Logan W.'s personal site. Its central rule: every
figure on the site is read from a pinned repository, the committed GitHub
snapshot, or the site's own ledger, or is marked as stated with who said it
and when, and a gate refuses anything else. A plan of record that misstates
what the repositories hold, misquotes the owner, or leaves a file two parcels
could both edit, sends four agents off on a wrong premise. **That is the
shape to hunt: a sentence in the plan that is not true of the tree, the pins
or the record.**

## What to verify

`docs/ROUND2.md` at commit `6ec5616` on the branch `round2`, draft 1 of the
plan of record for round 2. It is the lead's own work. Read it whole, then
check it against:
- the tree at `6ec5616` (your worktree; check you are on it with
  `git log --oneline -1`, and `git merge --ff-only 6ec5616` if you are behind;
  if the merge refuses, stop and tell the lead);
- the other repositories, **only at commits, with `git show <sha>:<path>` or
  `git log <a>..<b>`**, from their clones under `<repos>`. Never read their
  working trees, never check out or switch a branch in them, never fetch into
  them. Other sessions are working in cft-fp256 and HonestHarness right now;
- GitHub, read-only, with `gh api` (for example
  `gh api repos/loganw234/cft-fp256/compare/77b8440...main --jq .ahead_by`);
- the ledger's `lead.md` and `README.md`;
- ParcelRound's METHOD.md and templates at `f42242e`
  (`git -C <repos>/ParcelRound show f42242e:METHOD.md`), the method the plan
  says it follows.

## The ledger

`<repos>/loganw-dev-r2-ledger/`. Read its README first: its rules bind you.
Your file is `verifier-plan.md`; write only to it. Read `lead.md` and the
README; there is no parcel file yet. Write each heading's time from `date`,
never from memory. Everything in the ledger will be published: no absolute
path, no email address, no secret.

What cannot wait for your report goes to the lead at once: write it in your
file, then message the lead if your runtime can, and wait; if it cannot, stop
and make the question your report.

## Ground rules

- **Re-run things; do not trust pasted output.** Where the plan or `lead.md`
  states a measurement (the commit counts, the trial's three refusals, the 17
  changed figures, HonestHarness's README line and workflows), re-measure it,
  or say you could not and why.
- The trial's script is `<scratch>/r2-trial-pages.py`, and the trial
  worktree is `<scratch>/r2-trial`. You may run the script against a copy you
  make in your own scratch directory; do not edit the trial worktree.
- **Your scratch directory is `<scratch>/r2-verifier-plan/`.** Put everything
  you make there, and nowhere else.
- **Report only.** Do not edit any tracked file, in any repository.
- **"Found nothing" is a completely acceptable answer.** Do not invent
  findings. State precisely what you ran.
- Python is `python` (3.12.9); the site's commands are in its README and
  CLAUDE.md. You do not need the full gate.

## What READY means

READY is "a gate, or a stated limit". For a plan: every factual sentence in
it is true of the tree, the pins or the record, and every rule it states is
one the method or the owner actually gave. Only a wrong answer or a gap that
would send a parcel off on a wrong premise is a defect; a wording you would
prefer is a side note.

## Specific things to attack

1. **Every SHA, count and date** in "What moved", the trial, and P1 to P4's
   "What moved" paragraphs, against its source.
2. **Logan's decisions and request** in the plan, word for word against
   `lead.md`'s first entry.
3. **Every path and function the plan names exists** at `6ec5616` (or at the
   pin it names), and every file a parcel owns is one only that parcel owns.
4. **Completeness of the split.** For each parcel, the files it would have to
   touch to do what its section asks. Is any needed file missing from its
   list, or on the lead's list? Would two parcels need the same file? Read
   the page modules to see what each one reads: for example, which pages
   read cft-fp256, ParcelRound or Quantum-Film at all.
5. **The two refusals' fixes in P0**: can each be done as the plan says,
   without changing a word of Logan's?
6. **The rules the plan carries**: each one, against the source it cites
   (CLAUDE.md's traps, SPEC.md's decisions, METHOD.md's sections).
7. **The metrics plan** against ParcelRound's case studies 6 (`f42242e`) and
   7 (`894d125`, on the branch `case-study-7`), and the ledger's README. Read
   `<repos>/loganw-dev-r2-ledger/tools/round_metrics.py` too: does it count
   what the plan says it counts?
8. **The planted-fault protocol**: can a verifier tell the plants from the
   parcel's work by anything other than reading the work? Does the protocol
   keep the plants off `round2`?
9. **The method's checklist "Before dispatch"** (`templates/checklists.md` at
   `f42242e`): which of its items this plan does not meet, where the item
   applies to a round like this one.
10. **Anything else.** The list above is what the lead suspects. Tell it what
    it did not think to ask.

## Report

For each numbered item: the commands you ran, what you observed, and a
verdict: **confirmed**, **defect**, or **not determined**. Any defect needs a
concrete failure: what a parcel or the lead would do wrong because of it.
Then your overall verdict, READY or NOT READY, and your side notes apart from
the defects. Write the report in your ledger file too.

End your report with what you did not do. Stop your own background work
before you report, and say that you did.
