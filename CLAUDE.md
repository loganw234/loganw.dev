# Working on loganw.dev

This file is short on purpose. It only lists what isn't obvious and has
already cost time. The README says what the site is; this says what will
bite you.

## Start here: one command answers "does it still hold?"

```bash
bash verify/run.sh --require-all   # 7 stages, about 15 s on the desktop
bash verify/run.sh --list          # every stage, with * on the ones this invocation would run
```

**Run this before every push.** A push to main deploys the site, and that
has been the rule since the first push (Logan, 2026-09-29).

There is no cache across runs; each fresh run does everything again.
`--resume` continues the last run of the same tree.

## The authority

The source repositories are the authority, each read at the commit named in
`pins.json`. The site never states a figure it didn't read there.

- **Write figures through `@fact`.** A figure must come out of a function
  decorated with `@fact` (`site/facts.py`). The renderer refuses any figure
  that didn't, because `facts.json` couldn't read it again.
- **Put new facts in your own page module.** Re-derivation imports the module
  each fact was defined in, so a new fact never needs an edit to `facts.py`.
- **What a check proves.** A figure lifted from prose shows that the page
  quotes its source faithfully at the pin. It doesn't show the source's claim
  is true; the source's own gates do that. This is a stated limit.

## Traps

1. **Other repositories are read at their pins, never from their working
   trees.** Use `git show <sha>:<path>` through `Pin`. Other sessions work in
   those checkouts; on 2026-09-29 a revision-7 round was running in
   cft-fp256. Stay out of `cft-worktrees`, and never switch a branch in
   another repository.
2. **A slow build means a git read bypassed `Pin.git`.** The first build took
   76 s, because it spawned a git process for each CI run and for each
   repeated read. `Pin.git` memoises, and `is_ancestor` reads one `rev-list`.
3. **A ledger heading the parser doesn't recognise refuses the build.** A
   heading has to be dated at its start, dated in brackets at its end, or
   numbered. Anything else refuses by name. A numbered entry is dated by the
   commit that wrote its heading, because cft-rebound's entries 30 to 33
   carry no date anywhere.
4. **Count commits, not trailer lines.** Merc2Reborn has 20 agent commits but
   21 trailer lines, because `d66f97a` credits both Claude and Gemini. Our
   first figure there was wrong for this reason.
5. **A count over a fork's history counts its parent.** nextpnr-xilinx showed
   45 of 3397. A fork gets a dash, and the reason.
6. **Links must be relative.** The site is served at
   `loganw234.github.io/loganw.dev/` as well as at the root of loganw.dev, so a
   leading `/` breaks one of the two.
7. **Don't hand-edit `public/`.** It is generated, and `--check` fails on
   drift. If two branches conflict in `public/`, resolve it by rebuilding,
   never by merging the text.
8. **The Write tool on this desktop turns `\uXXXX` in code into the literal
   character** (observed 2026-09-29). That's harmless in a string, but check
   any regular expression that depends on the escape.
9. **A pin with no `dir` is read only from the site's own clone** under
   `.cache/repos/`. The Mercenaries-Fan-Build organisation's repositories are
   pinned at GitHub's main. Logan's clones of them were behind that, and one
   carried a commit GitHub never had. A fresh clone of this repository needs
   `LOGANW_FETCH=1` once for those pins; until then, `build` skips by name.
   Never fetch into Logan's own clones.

## The discipline that matters most here

A number that isn't read from its source doesn't appear on the site. If you
can't find where a figure comes from, don't print it. Either mark it
*stated*, with who said it and when, or leave it out.
