# Round 3: two new projects, and cft-fp256 at its new pin

This is the plan of record for the round that adds softfloat-bootstrap and
muse-softfloat to the site, and brings its cft-fp256 pages to that
repository as it stands on 2026-10-31. The lead (one Claude session, on Opus
5.5) wrote it that day. Logan's request, verbatim:

> Go ahead with the cleanup, then we will update the site with a couple new
> projects, a bootstrap kit and a muse-softfloat hackathon project, as well
> as updating the cft information (it has a new nightly page which shows
> quite a bit about a nightly case sweep, as well as a separate project which
> found an issue in the golden model that can go to the corrections page)

The method is [ParcelRound](https://github.com/loganw234/ParcelRound)'s
METHOD.md as it stands at its pin, `f42242e`, with its checklists, as in
round 2. Verification follows
[HonestFramework](https://github.com/loganw234/HonestFramework). Round 2's
plan is [ROUND2.md](ROUND2.md), and this one keeps its shape and its rules.

Draft 1 went past verifier-plan, which found four defects, and draft 2 one
more; this draft answers them, and the side notes the lead took. The round's
ledger records each finding and how the lead checked it.

## What moved

Measured on 2026-10-31 by `gh api .../compare/<pin>...<default branch>` for
every pin in [pins.json](../pins.json), from 05:01:31 to 05:02:18. Every pin
not listed is identical to its default branch.

| repository | pin | GitHub's main | commits ahead | this round |
|---|---|---|---:|---|
| cft-fp256 | `ab51655` | `19de866` | 646 | moves |
| QRO-Crate | `8858978` | `8fe0268` | 10 | stays |
| Mercenaries-Fan-Build/mercs2-modkit | `9acb750` | `1d2c536` | 45 | stays |
| Mercenaries-Fan-Build/mercs2-wad-simulator | `d18af76` | `13d96ed` | 1109 | stays |
| Mercenaries-Fan-Build/notes-on-the-released-game | `dac773d` | `1fcc294` | 204 | stays |

**New on the account**, by `gh repo list loganw234` against the 2026-10-15
snapshot's list:
- **softfloat-bootstrap**, public since its creation on 2026-10-24, its main
  `a23a0ff`: three commits and no workflows. Its README calls it "the
  builder of the bootstrap kit for Logan's Meta AI hackathon, 2026-10-26 to
  2026-11-04". The same README says the repository "stays private"; GitHub
  has shown it public from its creation, and Logan's word is that public is
  right (below).
- **muse-softfloat**, public, created 2026-10-26, its main `a2241fc`: 185
  commits, every one with the trailer `Co-Authored-By: Muse Code
  (muse-wonder-full-1.0)`. Its workflows are "Library CI (Linux gate)",
  which runs its own gate, and "Deploy demo site to GitHub Pages".
- The account also holds two private repositories the site does not read.
  Neither is new: they were created on 2025-10-11 and 2026-04-18. The
  snapshot leaves them out, as it leaves out every private repository the
  site does not read, and nothing in this round names them.

**What cft-fp256's record holds now.** `git diff ab51655 19de866 --
docs/VALIDATION.md` adds 90 headings, dated 2026-10-12 to 2026-10-30. The
newest entry at the old pin was dated 2026-10-06. Three of the new ones are
this round's subject:
- 2026-10-22, "the nightly progress page (parcel NP ...)":
  `hw/card_stress_progress.py` reduces the card's long run to
  `site/nightly.json`, which `site/nightly.html` shows. It is published at
  <https://loganw234.github.io/cft-fp256/nightly.html>;
- 2026-10-29, "the nightly page redesigned";
- 2026-10-30, "issue 1, the first outside report": exp2m1(emax + 1) toward
  zero raised overflow, in the golden model, the C, the vectors and the
  WebAssembly module. The entry says the report came "from a clean-room
  audit of loganw234/muse-softfloat (binary16/32/64), cross-tested against
  this library and an exact arbiter". The fix merged as `48e2aa22`. GitHub's
  issue 1 was opened and closed from the owner's account.

**The trial.** In a scratch worktree of main at `797f588`, the lead moved
cft-fp256's pin, added the two new pins, took a snapshot there, and rendered
each page on its own. Each page stops at its first refusal, so the trial saw
one refusal a page:
- the resume, at cft-fp256's README.md, whose published set "is
  **1,072,415** now";
- Verify, at docs/VERIFICATION.md, whose sentence on the `gate` budget now
  goes on past the words it quoted;
- cft-fp256's dossier, at CONFORMANCE.md, which now opens "**Profile 3.1,
  2026-10-13**".

The other 16 pages rendered. Of the figures they read, 8 read a different
text than `public/facts.json` at `797f588`. One of the 8 is the newest
cft-fp256 entry that Map & Ledger names, which is now issue 1. So, as in
round 2, the round's real work is not the build's refusals but the text:
the pages describe cft-fp256 as it stood on 2026-10-08.

## Logan's decisions (2026-10-31)

Through the question tool, verbatim, question and then answer. Each answer
is the option Logan chose, in the words the lead wrote for that option; his
choice is his word. SPEC.md records them as decisions 47 to 55: 47 to 54 in
P0, and 55 in the resume's own commit. The lead's
reading of each, where one is needed, follows it, marked as the lead's.

1. "softfloat-bootstrap's README says the repository "stays private" (only
   the zip goes to the Meta directories), but GitHub has shown it public
   since it was made, 2026-10-24 23:55 UTC. Is public what you want?" -
   "Public is right": "Keep it public. The site carries it like any public
   pin and never quotes the README's 'stays private' line, which is now
   stale."
2. "How should the site carry softfloat-bootstrap and muse-softfloat in this
   round?" - "Rows and nodes now (Recommended)": "Pin both at GitHub's main.
   Each gets a Map & Ledger row and a map node in the Determinism lane, with
   edges quoting their own files. Dossiers wait until the hackathon closes
   on 2026-11-04."
3. "cft-fp256's ledger calls issue 1 "the first outside report". It was
   filed from your own account, by a clean-room audit of muse-softfloat. On
   Corrections, does it retire the signature row ("first outside correction
   — pending")?" - "Own row; signature stays (Recommended)": "A new row read
   from cft-fp256's ledger at the new pin: found by 'a clean-room audit of
   loganw234/muse-softfloat', fixed in 48e2aa22. The signature row stays
   pending until a stranger files one."
4. "All 185 of muse-softfloat's commits credit "Muse Code
   (muse-wonder-full-1.0)" in their Co-Authored-By line. The site's
   agent-credited rule counts only Claude or Gemini, so it would read 0 of
   185. How should Muse be counted?" - "Count Muse, name it on Method
   (Recommended)": "The rule counts Claude, Gemini or Muse (185 of 185).
   SPEC's definition says so, and Method's co-authorship section adds a
   sentence read from muse-softfloat's trailers. Your statement there is
   unchanged."
5. "Besides cft-fp256 and the two new pins, three more pins trail GitHub:
   QRO-Crate is 10 commits ahead, with a round of its own running today, and
   the organisation's three Preservation repositories are 45, 1,109 and 204
   ahead. Which move in this round?" - "cft-fp256 and the new two
   (Recommended)": "QRO-Crate, mid-round, and the three Preservation
   repositories stay at their pins for a later update. Their pages are
   unchanged."
6. "How should the work be split, and on which models?" - "Sonnet parcels,
   Haiku verifiers (Recommended)": "As in round 2. The lead does P0: pins,
   snapshot, rows, nodes and the Muse rule. Then Sonnet parcels take the
   cft-fp256 pages, Corrections and Method. Each parcel is verified on a
   planted copy on Haiku, and the lead's own work on Haiku too."
7. "About says "The AI collaborators are named here: Claude and Gemini."
   Once muse-softfloat is on the site, that list leaves out Muse. Should
   About name Muse too?" - "Name Muse too (Recommended)": ""The AI
   collaborators are named here: Claude, Gemini and Muse." Only that list
   changes; the rest of About stays as you approved it."
8. "The gate runs only under Python 3.12.9 (.python-version), and this
   machine no longer has it. `python` is now Miniconda's 3.12.15, and the
   3.12 install the py launcher lists is gone (perhaps in the 10-26
   toolchain reinstall). How should I get 3.12.9 for the round's gates?" -
   "Move the gate to 3.12.15": "Change .python-version to 3.12.15, so the
   desktop and CI both run 3.12.15, recorded in the ledger. Python's HTML
   parser reads edge cases differently between releases, so the gate itself
   would need checking first."
9. "Your resume quotes cft-fp256's binary256 soak: 541 passes in 70 minutes,
   0 failures. At the new pin the record also states the card's long stress
   run (61 hours, 4,086 legs, 0 failures, 2026-10-19) and the nightly sweep
   (10 nights, 20,759,013,456,650 cases, 0 disagreements). Should the resume
   cite them too?" - "Add both, quoted (Recommended)": "Two short lines
   beside the soak, each quoted from cft-fp256's record at the pin with its
   file and line, as the resume's other lines are. The PDF and the text twin
   follow."

*The lead's readings:*
- On 3: "found by" quotes cft-fp256's record of the report, since no
  repository of the audit was found to pin. Those words name
  loganw234/muse-softfloat, Logan's own project, so the row doesn't read as
  a stranger's. That the issue was opened from his account is GitHub's
  record, which no pin holds, so the row doesn't print it.
- On 5: QRO-Crate's "round of its own running today" rests on its push to
  main that morning and on its directories' times under `<repos>`. Neither
  was read for content. The question said "three more pins" and went on to
  list four, QRO-Crate and the organisation's three; his answer keeps all
  four at their pins.
- On 8: the gate's Python is a venv of Miniconda's 3.12.15 at
  `<repos>/loganw-dev-venv`, holding `verify/requirements.txt` installed by
  hash, so Miniconda's own packages are left as they are. Every gate this
  round runs with `PYTHON` set to it. CI can follow: actions/python-versions
  lists 3.12.15 as stable for ubuntu-24.04. Before the change landed, the
  full gate ran on main's tree with `.python-version` alone changed, and
  passed with nothing skipped. The question's "perhaps in the 10-26
  toolchain reinstall" was the lead's guess, from cft-fp256's entry of
  2026-10-26 (afternoon), not a measurement.
- On 9: the question's figures were the lead's reading of the record at the
  pin, which the ledger's entry for the answer says. The two are one item of
  the resume, of two printed lines, so that
  cft-fp256 still fits on the printout's first page: the run in the README's
  own sentence on it, the sweep in the ledger's newest totals, beside the
  ledger's sentence on what a case total adds. Commit `2cbb7e7`, after P0.
- **The push** waits on Logan's word: decision 33, "Push when verified", was
  round 2's.

## Rules carried into this round

Each is a standing rule, with where it was given.

- The full gate, `bash verify/run.sh --require-all` under the Python
  `.python-version` names, before every push, and run alone (CLAUDE.md:
  "Start here", and trap 19). A push to main deploys.
- Only main is ever pushed, never `git push --all` (trap 17).
- The shared core first, then a verifier on it, then the round (decision
  18). The lead's seam commits, merges and records go past a verifier
  before main moves (METHOD.md section 7).
- Agents test what they can quickly, and hand large runs back to the lead.
  Here the large run is the full gate, which is the lead's.
- Only a regression or a wrong answer sends work back. Anything else merges
  as a recorded known limit, and a sentence that claims more than is true is
  restated at the merge (METHOD.md section 6).
- **Logan's words.** About and the front page are his approved words
  (decisions 26 and 29), every `stated()` figure is his statement, or is
  drafted from his words and labelled so until he approves it
  (`build.SPEAKERS` names Logan alone),
  and the spec's choices are his. They change only at his word, except that
  a stated line a pin has overtaken may be replaced by a figure read from
  its source, recorded in the ledger (decision 36). Anything that needs new
  words of his, or drops one of the spec's choices, goes to him.
- Logan's pronouns are he and his (trap 18). Anyone else is written by name
  unless their pronouns are stated.
- No published file holds an email address but `logan@loganw.dev` (trap
  14), or the name Wally outside the Preservation thread's page (trap 16).
  No tracked file names a private repository the site does not read (the
  privacy stage).
- Other repositories are read only at commits, through `git show`, never
  from their working trees, and no agent switches a branch in them (trap 1).
  Other sessions are working in cft-fp256 and QRO-Crate, and the hackathon
  runs in `<repos>/Muse-Softfloat`, which holds its own clone of
  muse-softfloat. The site reads the two new repositories only from its own
  clones under `.cache/`, never from that one.

## The shape

1. **This plan goes past a verifier**, and the lead answers its findings in a
   new draft, which the verifier re-checks, before Logan approves it.
2. **P0, the lead's,** on the branch `round3`, then verifier-P0 on it.
3. **Wave 1: P1, P2 and P3 in parallel, each designing first.** Each parcel
   reads its pages against the new pin, writes a design, and stops. The lead
   reviews the three designs, then makes one seam commit adding every new
   source path and numeral name the designs need. That commit goes past
   verifier-P0, scoped to it, and then each parcel gets "go" with its SHA.
4. **Each parcel's verifier** works on a copy of the parcel's work that may
   hold planted faults (below).
5. **Merges onto `round3`**, one at a time. Before each, the lead reads every
   author's file in the ledger; after each, the full gate, whose numbers and
   links stages read every page together (links also holds each dossier's
   Connections to the map's edges) and are the round's seam test; then the
   lead's restates.
6. **The verifiers' side notes** get a step of their own after the last
   merge. The lead then appends the round's entry to the site's own ledger,
   `docs/VALIDATION.md`. That entry also records the push of `797f588`,
   which the entry of 2026-10-16 left waiting on Logan's word, and its
   deploy; and the cleanup of 2026-10-31.
7. **The integration verifier** on the lead's own work: its merges, made
   again from their parents with `git merge-tree`, its restates, its
   records.
8. **Main moves to `round3`'s tip** after the full gate and the integration
   verifier's READY, and is pushed at Logan's word. The lead checks the live
   deploy byte for byte.

## P0: the lead's

On `round3`, from `797f588`, in three commits: `0e87fc2`, the gate's Python;
`2f52525`, the rest, whose full gate passed with nothing skipped; and
`f57c22e`, the record link this section promised muse-softfloat's row. After
P0, the lead's `2cbb7e7` adds decision 55's item to the resume. What P0
does:

- **`.python-version`:** 3.12.15 (decision 54), once the full gate had passed
  under it on main's tree, as its own commit, so its effect on the gate is
  seen apart from the round's.
- **pins.json:** cft-fp256 to `19de866`. softfloat-bootstrap is pinned at
  `a23a0ff` and muse-softfloat at `a2241fc`, each with no `dir`, so each is
  read from the site's own clone under `.cache/repos/`, fetched with
  `LOGANW_FETCH=1` (trap 9). Their workflows are classed by what they run:
  muse-softfloat's "Library CI (Linux gate)" `verifies` and "Deploy demo
  site to GitHub Pages" `deploys`; softfloat-bootstrap has none.
- **The snapshot:** a new one taken with the new pins, and pins.json pointed
  at it by its exact name (trap 10).
- **The refusals**, fixed only as far as the build needs, each requoted to
  what cft-fp256 now writes: the resume's published set, Verify's `gate`
  budget, and the dossier's profile. P1 and P2 own what their pages should
  say. cft-fp256's ledger header grew by three lines at the new pin, so
  every entry the dossier and Verify cite by line moved down by three; P0
  moves each citation, checked against its heading.
- **The Muse rule** (decision 50). `facts.AGENT` counts a commit whose
  message has a Co-Authored-By line naming Claude, Gemini or Muse.
  `snapshot_github.py` shares that rule, so the snapshot uses it too. The
  label every count prints, Map & Ledger's caption, and SPEC.md section 4's
  definition say so. `build.py`'s agent-rule control holds it: a Muse
  trailer counts its commit once, and a word that only contains "muse"
  counts none.
- **About's list** (decision 53): "Claude, Gemini and Muse". Only that list
  changes.
- **Map & Ledger** (`site/pages/home.py`):
  - **New rows.** softfloat-bootstrap and muse-softfloat get one each, in
    the Determinism lane. Each row gives:
    - what it is, quoted from its README at its pin;
    - its state;
    - last verified, as SPEC.md section 4 defines it. muse-softfloat's comes
      from its classed CI runs. softfloat-bootstrap's is a dash with its
      reason, as QRO-Crate's is. Its ledger records its runner's passes in
      one entry, headed "2026-10-23 to 2026-10-24", which the parser dates
      at its start, while both runs were made on 2026-10-24: a declared pass
      form would print the newest pass a day early;
    - its agent-credited count;
    - its own front door as its check.

    Neither row quotes the kit's README line that the repository "stays
    private" (decision 47).
  - **cft-fp256's row** is re-read at the new pin.
- **The map** (`site/data/relations.json`): the two nodes in the Determinism
  lane, born on their first commits at their pins, and their edges. Each
  edge names the words at its pin that make it, as every edge does. The new
  snapshot runs the axis to 2026-11-02, and at that scale labels ran into
  their neighbours and past the wide map's edge, so `site/mapgen.py`
  re-lays them: the wide map is wider, three labels sit left of their
  markers, and on a phone a label is kept inside the viewBox and off the
  month ticks. No gate reads where text lands; that is a stated limit. On a
  phone a label still sits under its own marker and may cover a marker born
  days later in its column: seven labels do on the live map, and
  softfloat-bootstrap's now covers muse-softfloat's (verifier-P0's A).
- **Work** lists the two among the projects with no dossier.
- **The Record** reads every pinned repository's docs/VALIDATION.md, as it
  always has. So softfloat-bootstrap's ledger joins it, and the trial parsed
  it. muse-softfloat keeps its record in docs/RECORD.md, which the Record
  doesn't read, so its row names that file instead.
- **The resume**, which is the lead's, is re-read at the new pin for its
  cft-fp256 quotes. A requote that changes what the resume claims, beyond
  restoring its quote, goes to Logan, since its statements are his (decision
  46). Its replay line said the published set "is" 1,068,915 cases "and
  that exact set was replayed"; at the pin the set is 1,072,415 and the card
  replayed the earlier one, so the line now reads "the 1,068,915-case set
  was replayed", which keeps its claim about the replay and drops the
  published set's size; Logan's word is to leave the size out (decision
  55). Whether the resume should also cite what the record states after the
  soak it quotes, the card's long stress run and the nightly sweep, would
  change what it claims, so it went to Logan, whose word is to cite both,
  dated (decision 55, in `2cbb7e7` and `c5e5e79`). The printout keeps its
  two pages by one point.
- **`build.SOURCE_PATHS`:** P0's labels name no path it does not list
  (verifier-P0's C). Its follow-up adds `site/nightly.json`, for the
  resume's dated line, a path P1's brief expects to need too.
- **SPEC.md:** decisions 47 to 54, and section 4's definition.

**verifier-P0** reads P0 against this plan and the tree, and picks its own
faults.

## Wave 1

Every parcel works in a worktree cut from `round3` at P0's tip. Its first
phase is a design, written in its ledger file, and then it stops. Each design
lists, page by page:
- every sentence or figure that the new pin makes stale or wrong, with the
  source line at the new pin that shows it;
- every new thing at the new pin that the page should say, with its source;
- every repository path its new labels would name that `build.SOURCE_PATHS`
  does not list, and every name with a numeral that
  `site/data/numeral_names.json` would need;
- any line of Logan's it finds overtaken, for the lead to take under
  decision 36 or to Logan.

On "go", it builds, rebuilds `public/` on its branch, runs the checks and its
controls (below), commits, and reports.

**The checks every parcel runs,** each in seconds: `python site/build.py`,
then its `--numbers`, `--links`, `--local-only`, `--check` and
`--verify-facts` modes. The full gate is the lead's.

**The controls every parcel runs**, each built in a copy under its scratch
directory, never in its worktree, with its output reported:
- a figure on one of its pages typed by hand where a fact was: the numbers
  stage refuses it by name;
- a label on one of its pages naming a path `build.SOURCE_PATHS` does not
  list: the numbers stage refuses it;
- one of its new `prose()` patterns given its source's old words: the build
  refuses it by name.

**What no gate holds, stated as a limit:** whether a sentence is the current
truth at the pin, rather than only true at it. That is the round's subject,
and the gates cannot read it. Each parcel's verifier reads every sentence on
its pages against the newest entries at the pin, and that reading is how the
property is held.

### P1: cft-fp256's dossier, and cft-rebound's

- **Owns:** `site/pages/work_cft_fp256.py` and
  `site/pages/work_cft_rebound.py` (cft-rebound's pin did not move; P1
  checks only what that page reads from cft-fp256).
- **What moved:** the 90 entries from 2026-10-12 to 2026-10-30. Among
  them:
  - revision 8's hard workloads;
  - the math library's routines, golden-first;
  - the card's long stress run and the nightly campaign that followed it;
  - three outside test sources;
  - profile 3.1;
  - issue 1 and its fix.
- **The nightly sweep:** the dossier shows the nightly page, its figures
  read from `site/nightly.json` at the pin, with a link to the live page.
  The live page goes on past the pin, so the dossier says which night its
  figures stop at.
- **Logan's, and staying:** every `stated()` line the dossier prints.
- **The trap:** a section still true at the new pin but no longer the
  current truth. That means "Verified" rows that stop at 2026-10-06, "Kept
  failures" without issue 1, and a "Test it" step whose cost changed.
- **Its own control, besides the three:** a figure read from
  `site/nightly.json` at a key the file at the pin does not have is refused
  by name.
- **The regression it is most likely to cause:** a nightly figure printed
  as the current state when it is the pin's, or one night's total given as
  the campaign's.

### P2: Verify and the Determinism thread

- **Owns:** `site/pages/verify.py` and `site/pages/thread_determinism.py`.
- **What moved:**
  - docs/VERIFICATION.md's budgets;
  - `CLAUDE.md`'s two budget lines, which the thread quotes, read new counts
    at the pin;
  - cft-fp256's own conformance replay, in the browser, as Verify calls it:
    its WebAssembly module was rebuilt for profile 3.1 on 2026-10-16 and
    again for issue 1, whose entry says it was "stale since 2026-10-22";
  - the nightly page, a record a reader can look at rather than a check to
    run;
  - the two new projects in the thread's lane. The map slice draws them
    from `relations.json`, and the account's words about them are P2's.
- **Logan's, and staying:** the Determinism door, including its
  "workloads" and "bit-identical everywhere" (decision 27). `propose.py`,
  on no parcel's list, renders the door, and its own control reads the word
  "workloads".
- **The trap:** a check whose cost or reach changed at the new pin, and a
  check that names the browser replay as current for a week in which its
  record says it was stale.
- **Its own control, besides the three:** the browser replay's sentence,
  given the old pin's words, is refused by name.
- **The regression it is most likely to cause:** a quote cut short so that
  the sentence around it claims more than its source, as round 2's Verify
  `gate` budget did.

### P3: Corrections and Method

- **Owns:** `site/pages/corrections.py` and `site/pages/method.py`.
- **Corrections:**
  - Issue 1's row (decision 49), every cell read from cft-fp256's ledger at
    the pin: the entry's date; the claim; "found by", in the entry's own
    words, which name loganw234/muse-softfloat, Logan's own project; "fixed";
    and `48e2aa22`, a commit the pin descends from. That the issue was
    opened from his account is GitHub's record, which no pin holds, so the
    row does not print it.
  - The caption, restated: the ledger's other rows are the site's own
    corrections, and this one is cft-fp256's.
  - The signature row stays.
  - The "where I'd attack first" quotes re-read at the new pin. A gap the
    record now says was closed goes to Logan through the lead (decision
    36).
- **Method:** a sentence read from muse-softfloat's trailers (decision 50),
  beside the sentence on Gemini's. Logan's statement there is unchanged,
  and so is its ONLY_HERE. The count sentence that says "Claude or Gemini"
  is restated to the rule as it now reads.
- **Logan's, and staying:** the rules of engagement, the gaps' names, the
  signature row, decision 9's statement, and the ratio (decision 8).
- **The trap:** a "found by" that reads as an outside finder's, and a
  "fixed" that claims more than the entry does. The entry records known
  limits beside the fix.
- **Its own control, besides the three:** a fix commit the pin does not
  descend from is refused by name.
- **The regression it is most likely to cause:** a row whose cells read
  from two different entries.

### What no parcel touches

The seams and the shared pages are the lead's: `site/facts.py`,
`site/render.py`, `site/build.py`, `site/mapgen.py`, `site/printout.py`,
`site/snapshot_github.py`, `site/style.css`, `site/data/`, `pins.json`,
`sources/`, `verify/`,
`site/pages/home.py`, `site/pages/work.py`, `site/pages/threads.py`,
`site/pages/record.py`, `site/pages/resume.py`, `site/pages/_dossier.py`,
`site/pages/_settled.py`, `site/pages/_p5.py`, `site/pages/front.py`,
`site/pages/about.py`, and every document (README, CLAUDE.md, `docs/`). A
stylesheet a parcel needs is a new file of its own under `site/styles/`.
Every page module on no parcel's list keeps its code this round, and is the
lead's if it must change; its rendered page still changes by what it reads,
such as the map's new nodes and the numbering of figures. `public/` is generated: parcels rebuild it on their
branches, and at each merge the lead rebuilds it rather than merging its
text.

## Planted faults

Planted faults stay light (decision 20), and are kept from being found by
anything but reading, as in round 2:

- **The copy.** One commit, whose parent is the parcel's own commit's
  parent and whose tree is the parcel's plus two plants, with `public/`
  rebuilt from it. It carries the parcel's own message, author and dates,
  and sits on a branch of its own, named as a parcel's branch is, never on
  `round3` (`tools/make_plant.py` in the ledger, which refuses `round3`,
  `main` and any branch that already exists). The lead runs the full
  gate on it before dispatch, and every stage must pass, so no stage points
  at a plant.
- **The plants** are faults of the kind the gates cannot read: a sentence
  that claims more than its source at the pin, a quote that is true at the
  pin but overtaken by a newer entry, a caption that names the wrong source.
- **The clone.** The verifier works in a clone of its own, under its scratch
  directory, made with `git clone --no-local --single-branch` from that
  branch, which holds only `round3`'s history and the planted commit. The
  parcel's own commit is not in it, and its brief puts every other branch
  and worktree of loganw.dev out of bounds until it has reported.
- **The design.** A planted-copy verifier reads the parcel's ledger file
  only after it reports, since a design there names what the parcel meant
  to write (round 2's case study, proposal 2).
- **The key.** Its SHA-256 goes in the lead's ledger file before that
  verifier is dispatched, and the key itself after the last planted-copy
  verifier has reported. The plants never reach `round3`: the lead merges
  the parcel's own commit, by its SHA. The plant branches are local, are
  never pushed, and are deleted at the round's end, after a bundle of them
  is kept with the ledger.

## The metrics

As in round 2. Each dispatch and report goes in the lead's ledger file, with
the runtime's own figures, its "tokens" recorded as the context at the run's
end. `tools/round_metrics.py` in the ledger, round 2's script with this
round's prefix, reads the transcripts at the round's end, the lead's own
session from the request at 04:22:42. Its table goes in the round's entry in
`docs/VALIDATION.md`, beside the wall clock and the planted-fault yield. Two
limits of the script: it counts the agents described "R3 " in the lead's own
subagent folder, so a parcel's own subagents are not counted (each brief
asks a parcel to say in its file when it spawns one); and it labels times at
a fixed -0700, which is wrong from 02:00 PDT on 2026-11-01 (09:00 UTC), when
the desktop's clock goes to -0800.

## Time and cost (an estimate, not a measurement)

- The plan's verification and P0's, about an hour. Wave 1's designs, about
  half an hour; the builds, about an hour; their verifiers, about half an
  hour. The merges, the integration verifier and the push, about an hour.
  Several hours of wall clock in all.
- The cost is read from the transcripts afterwards, never estimated in the
  record.

## What READY means

READY is "a gate, or a stated limit": every property of the work is held by
a gate the verifier has watched fail on a fault it picked itself, or is
stated as a limit where the claim is made, and the verifier's own evading
fault lands inside that limit. "Found nothing" is an acceptable answer.

The lead's rule since round 2 holds: each verifier has up to three passes,
a re-check scoped to the diff since its previous pass. If a third pass still
finds a wrong answer, the lead records it and asks Logan before going on.
The lead checks every Haiku finding against the records before acting on
it (decision 35).

## The ledger

At `<repos>/loganw-dev-r3-ledger/`, outside every repository. Its README
holds the rules, round 2's with one addition: no name of a private
repository the site does not read. Everything in it may be published, so it
holds no absolute path, no secret, and no address but the contact. Whether
it is archived in this repository, as round 2's was, is Logan's to say at
the round's end.
