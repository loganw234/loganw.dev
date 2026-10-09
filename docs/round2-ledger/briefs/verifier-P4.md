# Brief: verifier-P4 (the Preservation thread)

Read `briefs/_verifier.md` first; it holds everything every verifier is
given. This is what is yours.

## What you verify

Parcel **P4**'s work on the Preservation thread's page: the commit the
dispatch message names, in your own clone, `<scratch>/r2-verifier-P4/loganw.dev`.
**It may hold faults the lead planted.** Its parent is the tip of `round2`
P4 was given. Read `git show <the commit>` and `briefs/P4.md`, P4's brief,
and `docs/ROUND2.md`'s P4 section. Read `P4.md` in the ledger only once you
have formed your own view.

P4's job: make `site/pages/thread_preservation.py` the current truth at its
pins. Three of the page's seven repositories moved, all three the
Mercenaries-Fan-Build organisation's, read only from the site's own clones
under `.cache/repos/` (trap 9): mercs2-modkit `3a4d888` to `9acb750`,
mercs2-wad-simulator `fdf3597` to `d18af76`, notes-on-the-released-game
`b8c3958` to `dac773d`. Those clones are blob-less: read them with
`git -C .cache/repos/<org>--<name> show <sha>:<path>`, never `git grep`.

The lead's answers to P4's design are in `lead.md` (the entry after 15:42):
the organisation's four repositories in their own READMEs' words; the
Modkit pointer; the scope narrowed to the repositories listed; the gloss
"The modding side runs on" dropped; the caption's frame "In Logan's words:"
with his statement unchanged; a sentence saying what a commit count is not;
no agent figure.

## Specific things to attack

1. **Every sentence of the page's own words** (everything that isn't a
   quoted figure) against the sources the page cites, at their pins. Does
   any sentence claim more than its source says, in tense, scope or
   quantity?
2. **Every quotation** against its source at the pin: the words, the line
   its label names, and the sentence it is set in. Does the lead-in say the
   same as the quoted words?
3. **People.** Every sentence that names or describes a person or an
   account: is it shown by the commits at the pins, or said by a source the
   page cites? Is any pronoun written for anyone but Logan, whose pronouns
   are he and his (trap 18)? A count of commits is not a claim about who
   wrote the lines.
4. **The credits table** against `git log --format=%ae <pin>` at each of the
   seven pins, grouped as `account_of` groups them: every cell, every dash.
   And the links: each GitHub login's link, against `gh api user/<id>` for
   the noreply id.
5. **The scope sentence and its guard** (`org_items()` and the
   `credits-scope` control): does the guard refuse what the sentence would
   make false? Build a fault it should catch and one it might not.
6. **Logan's words**: his statement "@Wally is my discord username" and the
   door, unchanged in text, speaker and date; Wally nowhere else (trap 16;
   `facts.json` holds the statement too).
7. **P4's controls**: re-run at least two of its four, and its
   `credits-scope` control, from copies; each must fail for the reason it
   was written for.
8. **Scope**: `git diff --stat <parent> <commit>` against P4's brief: only
   its page module and `public/`.
9. **The commit message's claims**, one by one.
10. **Anything else.** Tell the lead what it did not think to ask.
