# What every verifier of round 2 is given

Read this, then your own brief, `briefs/<your name>.md`, which names what you
verify and what to attack. Where the two differ, your own brief wins.

You are a **verifier**, not an author. Your job is to try to *disconfirm*
work, and to report. **You must not fix anything.** "Found nothing" is a
completely acceptable answer, and will not be held against you. Do not
invent findings; do state precisely what you ran.

## The project

loganw.dev is Logan W.'s site. Its central rule: every figure on it is read
from a pinned repository at its pin, from the committed GitHub snapshot, or
from the site's own ledger, or is marked as stated, with who said it and
when, and the build refuses anything else. In this round the pins moved, and
the pages are being brought to the current truth at the new pins. **That is
what this is about: whether a page now says something its source at the pin
does not say, or still says something its source has since overtaken.** The
gates hold that every figure is read and labelled. No gate reads whether a
sentence around the figures is true, or whether a quote is still the current
truth. That is your list.

## Where you are

The dispatch message names the exact commit to verify, and where you work:
- **A parcel's verifier** works in a clone of its own,
  `<scratch>/r2-<your name>/loganw.dev`, which the lead made with
  `git clone --no-local --single-branch` from a branch holding only
  `round2`'s history and the commit you verify. **The copy you verify may
  hold faults the lead planted**, so every other branch and worktree of
  loganw.dev (`<repos>/loganw.dev`, and the worktrees under its
  `.claude/worktrees/`) is out of bounds until you have reported: a diff
  against another branch would find a plant without reading the work, and
  the round measures what reading finds.
- **A verifier of the lead's own work** works in a git worktree of
  `<repos>/loganw.dev`.

Check `git log --oneline -1`, and run `git merge --ff-only <the commit>` if
you are behind it. If the merge refuses, stop and tell the lead.

**Other sessions are working in cft-fp256 and HonestHarness right now.** Read
every other repository only at a commit: `git -C <repos>/<name> show
<sha>:<path>` or `git -C <repos>/<name> log <a>..<b>`. Never read their
working trees, never check out or switch a branch in them, never fetch into
them.

## The ledger

`<repos>/loganw-dev-r2-ledger/`. Its README holds the rules, and they bind
you. Your file is `<your name>.md`; write only to it. **Read the README and
`lead.md` first, and the parcel's file only once you have formed your own
view of the work.** Read everything again before you write your report.
Write each heading's time from `date`, never from memory. Everything in the
ledger will be published: no absolute path, no email address, no secret.

When you start, send the lead one line, "<your name>: test escalation", and
say in your file that you sent it. What cannot wait for your report goes to
the lead at once: write it in your file, then message the lead, and wait.

## Ground rules

- **Re-run things; do not trust pasted output.** Build from your worktree
  and run the checks yourself.
- **Your setup**, once, from the root of the tree you verify, in Git Bash:

  ```bash
  cp -r <repos>/loganw.dev/.cache .cache
  export LOGANW_REPOS='<repos, in its Windows form, as the dispatch message gives it>'
  python --version          # must print Python 3.12.9
  python site/build.py --check && python site/build.py --numbers && python site/build.py --links
  python site/build.py --local-only && python site/build.py --verify-facts
  ```

  The full gate, `bash verify/run.sh --require-all`, takes about four
  minutes; run it if your list needs a stage the commands above don't cover.
- **Read every claim against its source at the pin**, not against the
  parcel's report: open the file at the pin's commit and read the lines the
  label names, and the lines around them.
- **Build faults from copies** under your scratch directory,
  `<scratch>/r2-<your name>/`, never by patching the tree you verify, and
  delete them when done. Do not edit any tracked file.
- **Report everything you find as a finding**, planted or not; the key comes
  after your report.
- **You may be resumed** for a re-check after a fix: scope it to the diff
  since your previous pass, and pick your own faults, not the fix's author's.
  The lead's rule for this round gives each verifier up to three passes.

## What READY means

READY is "a gate, or a stated limit": every property of the work is held by
a gate you have watched fail on a fault you picked, or is stated as a limit
where the claim is made, and your own evading fault lands inside that limit.

Only a regression or a wrong answer sends work back: a sentence the source
at the pin contradicts, a figure or a label that misnames its source, a page
that no longer builds. Anything else merges as a recorded known limit, and a
sentence that claims more than is true is restated at the merge. So say,
for each finding, which it is.

## Report

For each numbered item in your brief: **the commands you ran**, what you
observed, and a verdict: **confirmed**, **defect** (with a concrete failure:
which sentence, which source line says otherwise), or **not determined**.
Then your overall verdict, READY or NOT READY, and your side notes apart
from the defects. Write the report in your ledger file too.

End with what you did not do. Stop your own background work before you
report, and say that you did.
