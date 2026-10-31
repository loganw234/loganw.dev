# Brief: verifier-plan (round 3's plan of record)

You are a **verifier**, not an author. Your job is to try to *disconfirm* the
plan, and to report. You must not fix anything.

Repository: loganw.dev, Logan W.'s personal site. Its central rule: every
figure on the site is read from a pinned repository, the committed GitHub
snapshot, or the site's own ledger, or is marked as stated with who said it
and when, and a gate refuses anything else. A plan of record that misstates
what the repositories hold, misquotes the owner, or leaves a file two parcels
could both edit, sends three agents off on a wrong premise. **That is the
shape to hunt: a sentence in the plan that is not true of the tree, the pins
or the record.**

## What to verify

`docs/ROUND3.md` at the commit your dispatch message names, on the branch
`round3`: draft 1 of the plan of record for round 3. It is the lead's own
work. Read it whole, then check it against:
- the tree at that commit: your worktree, `<scratch>/r3-verifier-plan/loganw.dev`.
  Check you are on it with `git log --oneline -1`;
- the other repositories, **only at commits**, with `git show <sha>:<path>`
  or `git log <a>..<b>`:
  - cft-fp256, from its clone `<repos>/cft-fp256`;
  - softfloat-bootstrap and muse-softfloat, from the trial's own clones,
    `<scratch>/r3-trial/.cache/repos/<name>` (read-only), or through
    `gh api repos/loganw234/<name>/contents/<path>?ref=<sha>`.
  Never read a working tree of theirs, never check out or switch a branch in
  them, and never fetch into the owner's clones. Other sessions are working
  in cft-fp256 and QRO-Crate right now. The hackathon runs in
  `<repos>/Muse-Softfloat`, which is out of bounds;
- GitHub, read-only, with `gh api` (for example
  `gh api repos/loganw234/cft-fp256/compare/ab51655...main --jq .ahead_by`);
- the ledger's `lead.md` and `README.md`;
- ParcelRound's METHOD.md and templates at its pin `f42242e`
  (`git -C <repos>/ParcelRound show f42242e:METHOD.md`), the method the plan
  says it follows, and round 2's plan, `docs/ROUND2.md`, whose shape it
  says it keeps.

## The ledger

`<repos>/loganw-dev-r3-ledger/`. Read its README first: its rules bind you.
Your file is `verifier-plan.md`; write only to it. Read `lead.md` and the
README; there is no parcel file yet. Write each heading's time from `date`,
never from memory. Everything in the ledger may be published: no absolute
path, no email address, no secret.

**Two private repositories the site does not read are new on the account.
Never write their names anywhere**, in your file or your report. If you
list the account's repositories, do not copy the list out.

When you start, send the lead one line, "verifier-plan: test escalation",
if your runtime can message, and say in your file whether it could. What
cannot wait for your report goes to the lead at once: write it in your file,
then message the lead if your runtime can, and wait. If it cannot, stop and
make the question your report.

## Ground rules

- **Re-run things; do not trust pasted output.** Where the plan or `lead.md`
  states a measurement, re-measure it, or say you could not and why. That
  covers the commit counts, the 90 headings, the new repositories' dates,
  commits, trailers and workflows, the nightly.json totals, the trial's
  refusals and its 8 differing figures, and the Python facts.
- The trial's script is `<scratch>/r3-trial-pages.py`, and the trial
  worktree is `<scratch>/r3-trial`. You may run the script against a copy you
  make in your own scratch directory. Do not edit the trial worktree.
- **Your scratch directory is `<scratch>/r3-verifier-plan/`.** Put everything
  you make there, and nowhere else.
- **Report only.** Do not edit any tracked file, in any repository.
- **"Found nothing" is a completely acceptable answer.** Do not invent
  findings. State precisely what you ran.
- Python is `python`, Miniconda's 3.12.15 (decision 54 in the plan). **Do
  not run the full gate**: the lead's may be running, and two gates side by
  side each take several times as long (CLAUDE.md, trap 19). The quick
  modes, such as `python site/build.py --docs`, take seconds.

## What READY means

READY is "a gate, or a stated limit". For a plan: every factual sentence in
it is true of the tree, the pins or the record, and every rule it states is
one the method or the owner actually gave. Only a wrong answer or a gap that
would send a parcel off on a wrong premise is a defect. A wording you would
prefer is a side note.

## Specific things to attack

1. **Every SHA, count and date** in "What moved", "New on the account",
   "What cft-fp256's record holds now" and the trial, against its source.
2. **Logan's request and his eight decisions** in the plan, word for word
   against `lead.md`.
3. **Every path and function the plan names exists** at the plan's commit,
   or at the pin it names. Is every file a parcel owns owned by that parcel
   alone?
4. **Completeness of the split.** For each parcel, list the files it would
   have to touch to do what its section asks. Is any needed file missing
   from its list, or on the lead's? Would two parcels need the same file?
   Read the page modules to see which pages read cft-fp256 at all, and
   whether any such page is on nobody's list.
5. **P0's work as the plan states it**: the three refusals; the Muse rule
   (find every place the site states the rule's words: its code, its pages,
   its documents); About's list; the Record's choice of ledgers; the new
   rows' "last verified". Can each be done as the plan says, without
   changing a word of Logan's beyond decision 53's list?
6. **The lead's readings** of Logan's decisions: does any claim more than his
   answer gives?
7. **The rules the plan carries**: each one, against the source it cites
   (CLAUDE.md's traps, SPEC.md's decisions, METHOD.md's sections).
8. **The planted-fault protocol and the metrics**: can a verifier tell the
   plants from the parcel's work by anything other than reading the work?
   Does the protocol keep the plants off `round3`? Does
   `<repos>/loganw-dev-r3-ledger/tools/round_metrics.py` count what the plan
   says it counts?
9. **The Python move** (decision 54): does the plan state what was measured
   and decided? Does anything a parcel or a verifier will read still name
   3.12.9 as the gate's Python where that would mislead them?
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
