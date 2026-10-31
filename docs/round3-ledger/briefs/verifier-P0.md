# Brief: verifier-P0 (round 3's shared core)

Read `briefs/_verifier.md` first; it holds everything every verifier is
given. This is what is yours.

## What you verify

The lead's P0, two commits on `round3`:
- `0e87fc2`: `.python-version` from 3.12.9 to 3.12.15 (decision 54);
- `2f52525`: everything else P0 does: the pins, the snapshot, the three
  requotes, the moved line citations, the Muse rule and its control,
  About's list, the two Map & Ledger rows, the map's two nodes, six edges
  and its re-laid labels, and SPEC.md's decisions 47 to 54.

Read them against `docs/ROUND3.md`'s P0 section at the commit your dispatch
names, and against the tree. There are no planted faults in P0: pick your
own. Your worktree is a git worktree of loganw.dev at that commit.

## Specific things to attack

1. **The pins.** `pins.json`'s three changed entries against GitHub
   (`gh api`), and the two new pins' workflow classes against what each
   workflow runs at the pin. The new snapshot: was it taken with these pins
   (its `pins` block), does pins.json name it exactly, and are its private
   names only the ones the site reads?
2. **The three requotes.** Each quote against its source at `19de866`: the
   resume's replay line, Verify's `gate` budget, the dossier's profile and
   its minor step. Does any sentence around a quote now claim more, or less,
   than the source? The resume is Logan's document: does its line still say
   what it said, or something its source does not?
3. **The moved line citations.** Every ledger line the dossier and Verify
   cite: is it the heading P0 says, at `19de866`? Is any citation left that
   points at the old line, or at a line that is not an entry's heading?
4. **The Muse rule.** Every place the site states the rule's words, in its
   code, its pages and its documents. Does the count each page prints match
   the words beside it? Does `build.py`'s agent-rule control fail on the
   fault it names? Build a commit message the rule miscounts.
5. **About's list.** Did anything on About change but the list (decision
   53)?
6. **Map & Ledger's two rows.** Each cell against its source at its pin;
   softfloat-bootstrap's dash and its reason; `newest_subject`'s second
   form. Does any cell quote the kit's "stays private" line (decision 47)?
7. **The map.** Each new edge's words at its pin, and the sentence each edge
   makes, read tail to head with its kind's words ("underlies",
   "verifies"): is each one true of its source? The layout: P0's message
   says no two labels overlap on the wide map, and the phone map's overlaps
   are the ones the live map already has. Check that in a browser if you
   can (the preview server serves `public/`), or by reading the SVG.
8. **SPEC.md.** Decisions 47 to 54, word for word against `lead.md`, and
   section 4's definition.
9. **The Python move.** `0e87fc2`'s message says the full gate passed on
   main's tree under 3.12.15 before it. `lead.md` records the run. Is
   anything in the repository still naming 3.12.9 where that would mislead?
10. **Every claim in a comment, a document or a commit message P0 wrote**,
    `2f52525`'s long message above all.
11. **Anything else.** The list above is what the lead suspects. Tell it what
    it did not think to ask.

The lead's full gate on `2f52525` is recorded in `lead.md`. Run the gate
yourself only if your list needs a stage the quick commands don't cover, and
only when your dispatch says no other gate is running.
