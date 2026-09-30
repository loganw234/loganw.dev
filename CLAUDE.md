# Working on loganw.dev

This file is short on purpose. It only lists what isn't obvious and has
already cost time. The README says what the site is; this says what will
bite you.

## Start here: one command answers "does it still hold?"

```bash
bash verify/run.sh --require-all   # every stage; any skip fails
bash verify/run.sh --list          # the stages, with * on the ones this invocation would run
```

**Run this before every push.** A push to main deploys the site, and that
has been the rule since the first push (Logan, 2026-09-29).

There is no cache across runs; each fresh run does everything again.
`--resume` continues the last run, and only on a clean tree. `--require-all`
refuses `--only` and `--skip`.

## The authority

The source repositories are the authority, each read at the commit named in
`pins.json`. For the site's own history, the authority is its own
`docs/VALIDATION.md`, read from the commit being built. The site never states
a figure it didn't read there.

- **Write figures through `@fact`.** A figure must come out of a function
  decorated with `@fact` (`site/facts.py`). `fig()` refuses a figure that
  isn't exactly what its fact returned. The `numbers` stage refuses a
  numeral on a page outside a figure's mark, and any mark whose text isn't
  its own fact's. Digits straight after a letter are read as a name
  (cft-fp256), so "x3397" would pass; that is a stated limit.
- **Put new facts in your own page module.** Re-derivation imports the module
  each fact was defined in, so a new fact never needs an edit to `facts.py`.
- **What a check proves.** A figure lifted from prose shows that the page
  quotes its source at the pin. It doesn't show the source's claim is true;
  the source's own gates do that.
  - A paraphrase (`display=`) prints its source's words beside it, and can't
    add a numeral they don't have. Whether it keeps their meaning isn't
    checked.
  - These are stated limits.

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
   numbered. Anything else refuses by name. Headings inside code fences are
   not entries. A numbered entry is dated by the first commit that added its
   heading, because cft-rebound's entries 30 to 33 carry no date anywhere.
   A retitled heading is therefore dated at its retitling.
4. **Count commits, not trailer lines.** Merc2Reborn has 20 agent commits but
   21 trailer lines, because `d66f97a` credits both Claude and Gemini. Our
   first figure there was wrong for this reason. `facts.agent_credited` is
   the one rule, and `snapshot_github.py` uses it too.
5. **A count over a fork's history counts its parent.** nextpnr-xilinx showed
   45 of 3397. A fork gets a dash, and the reason.
6. **Links must be relative, and name a published file exactly.** The site
   has been served at `loganw234.github.io/loganw.dev/`, a subpath, and at
   the root of loganw.dev. It is also previewed from local folders. A
   leading `/` breaks every one of these except the root.
7. **Don't hand-edit `public/`.** It is generated, and `--check` fails on
   drift. If two branches conflict in `public/`, resolve it by rebuilding,
   never by merging the text.
8. **Backslashes don't survive every tool here.** The Write tool turned
   `\uXXXX` in code into the literal character (2026-09-29). Python sent
   through a Bash heredoc had its `\\` arrive as `\` the same day. Write code
   with the Write or Edit tool, and check any regular expression that
   depends on an escape.
9. **A pin with no `dir` is read only from the site's own clone** under
   `.cache/repos/`, fetched with `LOGANW_FETCH=1`. The Mercenaries-Fan-Build
   organisation's repositories are pinned at GitHub's main. Logan's clones of
   them were behind that, and one carried a commit GitHub never had.
   - At P0.1 no page reads those pins; their commits come from pins.json and
     the snapshot. So nothing needs the fetch yet. P2's credits will, and
     from then on a clone without the fetch skips `build` by name.
   - Never fetch into Logan's own clones.
10. **Moving a pin means taking a new snapshot.** The build refuses a pin that
    the snapshot didn't look up, and a pin that GitHub doesn't have.
    atlas-darkroom was pinned at a commit that existed only in Logan's clone.
    Point `pins.json` at the new snapshot by its exact name. `ls | tail`
    picked the wrong one once, because `-1554.json` sorts before `.json`.
11. **A pattern passed to `prose()` must match exactly once,** or it is
    refused. `last=True` asks for the last match, on purpose.
12. **`stated()` takes who and when.**
    - A statement about a repository takes `holds_at={name: commit}`, and
      refuses the build once that pin moves.
    - Words the lead drafted for someone take `draft=True` until that person
      approves them.
13. **No document states how many stages the runner has.** `--list` prints
    them. `--docs` refuses a count written close to that word, in digits or
    in the number words it lists; `build.STAGE_COUNT` is the rule. The ledger
    may state one, as a fact about its date.

14. **No published file holds an email address,** except the site's contact,
    `logan@loganw.dev`. The local-only stage refuses any other address, and
    it names only how many it found, since CI's logs are public. Key a
    commit's author by GitHub login, or by a hash of the address, never by
    the address itself.

15. **The site's own ledger is a source.** `facts.own_prose()` and
    `facts.own_entry()` read `docs/VALIDATION.md`, and MANIFEST hashes it.
    After appending an entry, rebuild before committing, or the `manifest`
    stage fails. Every heading there is dated at its start. Entries are only
    appended, because a page cites an entry by its heading's line. A commit
    of the site's own that a page cites goes through `facts.own_commit()`,
    which refuses one that main doesn't hold. A squashed parcel's commits
    are like that.

16. **The spec names Wally on Home and on About; decision 16 allows the name
    on one page only,** the Preservation thread's. The local-only stage
    refuses it in any other published file.

## The discipline that matters most here

A number that isn't read from its source doesn't appear on the site. If you
can't find where a figure comes from, don't print it. Either mark it
*stated*, with who said it and when, or leave it out.
