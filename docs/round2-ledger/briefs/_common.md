# What every parcel of round 2 is given

Read this, then your own brief, `briefs/<your name>.md`. Where the two differ,
your own brief wins, and say so in your ledger file.

## Where you are

You are a parcel in **loganw.dev**, in a git worktree of
`<repos>/loganw.dev`, cut from the branch `round2`. The dispatch message names
the exact commit. **Check you are on that commit or after it, in the right
repository**: `git log --oneline -1` and `git remote -v`. If you are behind
it, run `git merge --ff-only <the commit>`, check the SHA again, and if the
merge refuses, stop and tell the lead. Say what you found in your ledger file.

loganw.dev is Logan W.'s site. Its central rule: **every figure on it is read
from a pinned repository at its pin, from the committed GitHub snapshot, or
from the site's own ledger, or is marked as stated, with who said it and
when, and the build refuses anything else.** A figure that quotes its source
at the pin passes every gate even when the source has since said something
newer, and that is this round's whole subject: the pins moved on 2026-10-08,
the pages still describe the projects as they were on 2026-09-29, and your
job is to make your pages the current truth at the new pins.

**Other sessions are working in cft-fp256 and HonestHarness right now.** Read
every other repository only at a commit: `git -C <repos>/<name> show
<sha>:<path>`, `git -C <repos>/<name> log <a>..<b>`, or through the site's
own readers (`facts.prose`, `facts.pin(name).show(path)`). Never read their
working trees, never check out or switch a branch in them, and never fetch
into them.

## Start here

1. `docs/ROUND2.md`, all of it, then your parcel's section.
2. `CLAUDE.md`: the traps. Traps 1, 8, 11, 12, 14, 16 and 18 are the ones a
   page parcel meets.
3. `docs/SPEC.md`: the spec, and Logan's decisions, 1 to 35.
4. `site/pages/__init__.py`: what a page module is.
5. `site/facts.py`: `prose()` (a pattern must match once, or ask for the
   last), `stated()`, `entries()`, `exists()`, `last_commit()`; and `@fact`.
6. Your own pages, and the commits that moved their pins (your brief names
   them).

## The ledger

`<repos>/loganw-dev-r2-ledger/`. Its README holds the rules, and they bind
you: one file per author, append only; stamps from `date`; values from the
command that measured them; the three read moments; escalation by message,
the question written in your own file first. Your file is `<your name>.md`.
Everything in the ledger will be published, so no absolute path in it: name
places by `<repos>` and `<scratch>`.

**When you start, send the lead one line, "<your name>: test escalation"**,
and say in your file that you sent it.

**Write a resume note at each phase step**: an entry saying where you are, so
a dropped or paused agent can be dispatched again from its brief and its note.

## Phase 1: design, then stop

Read your pages against their new pins, and write your design in your ledger
file. For each page:
- every sentence or figure that the new pin makes stale or wrong, with the
  line at the new pin that shows it (`<path>:<line>` at `<sha>`);
- every new thing at the new pin that the page should say, with its source;
- every repository path your new labels would name that `build.SOURCE_PATHS`
  does not list, and every name with a numeral that
  `site/data/numeral_names.json` would need;
- what you will leave as it is, and why.

Keep to what the pins say. **Logan's words are his**: About, the front page,
every `stated()` figure, and the spec's choices (SPEC.md section 1), such as
which gaps Corrections names and which doors the threads open. You never
change one. If one has gone stale, list it in your design with the line at
the pin that overtakes it: under decision 36 the lead may replace a stated
line with a figure read from its source, and anything else goes to Logan.
Then make the design your report, and **stop**. The lead reviews the four
designs, adds the paths and numeral names they need in one commit on
`round2`, and sends you "go" with that commit's SHA.

## Phase 2: on "go"

1. `git merge --ff-only <the SHA in "go">`, and check it.
2. Make the changes your design and the lead's answer settled.
3. Rebuild and check (below), run your controls (below), commit on your
   worktree's branch with a message that says what was established, ending
   with `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
4. Report.

## Your controls

A check you haven't watched fail is not a check. Build each control in a
copy under your scratch directory, never in your worktree: copy the
repository's `site/` there (or the one file the control needs, with
`sys.path` pointed at the copy), plant the fault, run the check, and report
its actual output lines. Then delete the copy.

1. A figure on one of your pages typed by hand where a fact was: the
   numbers stage refuses it by name. (`render.render()` passes a plain
   string through unchanged; it refuses only a figure object no fact
   produced.)
2. A label on one of your pages naming a path `build.SOURCE_PATHS` does not
   list: the numbers stage refuses it.
3. One of your new `prose()` patterns given its source's old words: the
   build refuses it by name.
4. Your brief's own control.

**What no gate holds, stated as a limit:** whether a sentence is the current
truth at the pin, rather than only true at it. That is this round's subject,
and no gate can read it. Your verifier reads every sentence on your pages
against the newest entries at the pin, and that reading is how it is held.

## Building and checking on this host

The worktree has no clones beside it and no `.cache/`. Once, from your
worktree's root, in Git Bash:

```bash
cp -r <repos>/loganw.dev/.cache .cache        # the site's own clones of the organisation's repositories; gitignored
export LOGANW_REPOS='<repos, in its Windows form, as the dispatch message gives it>'
python --version                              # must print Python 3.12.9
```

Then, after every change:

```bash
python site/build.py                 # writes public/; stops on the first figure it can't read, and names it
python site/build.py --numbers       # every numeral in a mark, every label in a known shape
python site/build.py --links
python site/build.py --local-only
python site/build.py --check         # public/ is exactly what the pins render
python site/build.py --verify-facts  # every figure read again
```

Each takes seconds. Don't run `bash verify/run.sh`: the full gate is the
lead's, at each merge. `public/` is generated: rebuild it and commit it with
your change, and never edit it by hand (trap 7).

Write Python with the Write or Edit tool, never through a Bash heredoc, and
check any regular expression that depends on a backslash (trap 8).

Your scratch directory is `<scratch>/r2-<your name>/`. Put everything you
make outside your worktree there, and nowhere else.

## Files

Your brief names the files you own. Everything else in the repository is
someone else's: the seams and shared pages are the lead's (ROUND2.md, "What
no parcel touches"). A stylesheet you need is a new file of your own,
`site/styles/r2-<your name>.css`. If you need a change in a file you don't
own, ask the lead by message; never make it.

## What READY means

READY is "a gate, or a stated limit": every property of your work is held by
a gate, or stated as a limit. For a page: every figure is read through a fact
and printed with its label; every sentence is true at the new pin; and the
one property no gate holds, that a sentence is the current truth and not
only true at the pin, is the limit above, which your verifier reads for.

## Do not

- push, merge, rebase, or commit to `round2` or `main`;
- edit a word of Logan's, any `stated()` text, or one of the spec's choices;
- weaken a check, or widen a pattern beyond the words it quotes;
- type a figure: every number comes out of a `@fact`;
- write a pronoun for anyone but Logan (he, his), or the name Wally anywhere
  but the Preservation thread's page;
- write an email address, other than `logan@loganw.dev`;
- fix anything outside your files: report it.

If you spawn a subagent, say so in your ledger file when you dispatch it, and
don't finish while one is running.

## Report

Phase 1's report is your design. Phase 2's: what you changed, file by file;
the actual output lines of each check above and of each control; **anything
this brief or the plan got wrong**; and what you did not do. If you had to cross a boundary
this brief drew, say so and say why: that is expected and fine, and doing it
silently is not. Stop your own background work before you report, and say
that you did.
