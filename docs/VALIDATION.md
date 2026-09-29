# Validation ledger

This file records every run that established something, in the order it
happened. A figure here is a fact about the run that produced it, on the date
given. It is never updated to match a later measurement; a later run gets a
later entry, and a correction is a new entry naming the old one. Failures stay
in, including the ones caused by whoever wrote this file. A ledger of
successes would be a brochure.

This file is not a description of how the site works; that's
[README.md](../README.md). It's not a list of what's true now either; that's
the site, generated from pins.json. It is the evidence those two cite.

---

## 2026-09-29 - the spec measured against the repositories it describes

Logan pasted a build spec for the site and asked for the site to adhere to
HonestFramework. Before any build, the spec's premises were checked against
the repositories. That applies ParcelRound's rule to read the requester's
code rather than its list of asks, to Logan's own spec. The results are in
[SPEC.md](SPEC.md) section 3. The runs:

- `git log --format=%ad --date=short | sort | head -1` in each local clone
  gives each repository's first commit. PrettyCloud 2026-07-15;
  atlas-darkroom 07-27; atlas-film 07-27; atlas-optical 07-30; atlas-engine
  08-22; cft-fp256 08-28; cft-rebound 09-09; ParcelRound 09-11;
  HonestFramework 09-12; Quantum-Film 09-25. For repositories not cloned,
  `gh api .../commits`: CanonBracketTool 2025-11-04, Microscope-Stacker
  2025-11-06. atlas-film's and atlas-optical's READMEs each state they were
  split out of atlas-darkroom with its history on 2026-08-28. Extraction
  rewrote their hashes, so their root commits don't match the darkroom's.
- `gh repo list loganw234` found 45 repositories: 35 public and 10 private.
  Among the private ones are atlas-darkroom, atlas-optical, StoryDocs and
  binary-sites.
- Across every local clone, the Co-Authored-By trailers name Gemini once, on
  Mercenaries2 `d66f97a`, alongside Claude.
- `git grep -E '1 ?: ?24'` across every repository found no source for "1:24".
  None of the matches is a ratio. ParcelRound's are clock times ("11:24"),
  cft-fp256's are register bit ranges (`[31:24]`) and libming's is a
  timestamp. Quantum-Film's and notes-on-the-released-game's are in JSON data:
  roll records and a debugger database. The one measurement of the ratio is in
  ParcelRound CASE-STUDY-2, lines 35 and 532: 1 h 38 min human-active against
  23 h 40 min API time.
- Of every repository, only three keep a `docs/VALIDATION.md`: cft-fp256
  (152 headings), cft-rebound (37: 24 dated, 13 numbered) and Quantum-Film
  (19).

### What the lead got wrong along the way

- `git rev-parse --short HEAD origin/main` failed with "Needed a single
  revision". The fault was the command (`--short` takes one revision), not
  the repository.
- A `grep -m4` for Quantum-Film's "14 of 14" stopped at four matches, and was
  nearly read as "not found". Run again without the cap, it still found no
  "14 of 14". The 14 comes from ParcelRound's case study and from the runner's
  own stage count.
- A "runner/Makefile" column in the method-signals table counted the
  mod-build Makefiles in the Mercenaries 2 repositories as gates. It was
  dropped before it was used.
- The figure "21 of 46" agent commits for Merc2Reborn, given to Logan
  earlier that day, counted trailer lines. The commit count is 20. See the
  next entry but one.

## 2026-09-29 - design experiments A to E, and the one chosen

`design/experiments/build.py` renders one Home page in four directions. Each
figure is read at 13 pinned commits and from a GitHub snapshot. A fifth
direction, E, is the combination Logan chose: "D looks good, but the color
scheme of A (the blue), and the font and header choice of B". Later: "E looks
good as it is".

- `python build.py --check`: 10 files exactly what the pins render.
- `python build.py --control`: both plants were caught. A stale ABI was found
  in page A, at line 122. With cft-fp256 re-pinned to `644ee2d`, the build
  refused, naming cft-fp256.
- A stale ABI planted by hand in a written page made `--check` exit 1, and 0
  again after a rebuild.
- A to D hash-identical (`sha256sum -c`) before and after the change that
  made E's source paths break only at `/`.
- At 375 px wide, run in iframes in the browser pane:
  - no page scrolls sideways, whether the width reads 375 or 360 (360 when
    the frame shows a scrollbar);
  - a planted 600 px element was caught, at scrollWidth 616.

  The first run of that control read `scrollWidth` after its frame had been
  removed, got 0, and could not fail. It was run again with the reading taken
  first, and caught the plant.

## 2026-09-29 - the shared core (P0): pins, facts, the Home page, the gate

The site's generator, built so that every figure it prints is read at a pin
and logged.

### Measured

- `python site/snapshot_github.py` took `sources/github-2026-09-29.json`:
  - 45 repositories captured, and 43 recorded (see "Found, and fixed");
  - 7 read only through the API;
  - CI runs for the four repositories that declare a test workflow:
    atlas-engine 24, atlas-film 2, cft-fp256 470, mercs2-lua-essentials 82.
- The fonts: 8 files, 512,869 bytes, fetched at Logan's word
  (`site/fonts/SOURCES.txt`, with each file's sha256). The browser pane's
  network log for the built page showed three font requests, all local: the
  three Latin files, 310,304 bytes. Nothing was fetched from another host.
- `python site/build.py`: 17 files, 15 pins, 144 figures in `facts.json`.
  - The first build took 76 s. Memoising git reads per pin, and one
    `rev-list` for ancestry, brought it to 4.0 s.
  - `facts.json` was byte-identical before and after that change: 144 figures
    each time.
- The ledger parser refused, by name, twice on its first builds:
  - cft-fp256 `docs/VALIDATION.md:678`, a heading dated in brackets at its
    end;
  - cft-rebound `docs/VALIDATION.md:2705`, a numbered entry with no date
    anywhere; entries 30 to 33 all lack one.

  Both are now rules (`site/facts.py`, `entries()`). A numbered entry is dated
  by the commit that wrote its heading.
- `bash verify/run.sh --require-all` (run `20260929-145924`, before the first
  commit): 7 passed, 0 failed, 0 skipped. `VERDICT: PASS, nothing skipped`.
  - `build`: 17 files exactly what the pins render.
  - `facts`: 139 figures read again and the same, 0 different, 0 skipped,
    5 stated.
  - `controls`: 7 planted faults, each caught by name.
  - `runner-control` failed, as it must.
- The runner's own control was watched failing. With `check_links` sabotaged
  in a copy of the tree, `runner-control` reported "NEGATIVE CONTROL DID NOT
  FAIL" and the run failed.
- With no clones reachable, `build` skipped by name, and `--require-all`
  turned that into a failure.

### Found, and fixed, on the way

- The first no-clones run printed "1 skipped" over 118 figures skipped inside
  the passing `facts` stage. The VERDICT line now counts figures skipped
  inside passing stages.
- **Correction to the entry two above:** Merc2Reborn has 20 commits carrying
  an agent trailer, of 46. `d66f97a` carries two trailers (Claude and Gemini),
  which is how a count of trailer lines reached 21.
- nextpnr-xilinx showed 45 of 3397 agent-written commits. That count is true,
  but it describes the fork's parent's history. A fork now gets a dash, and
  the reason.
- **Both snapshots named private repositories the site never reads,** with
  their descriptions, in files that were about to become public. This was
  found while reviewing the first commit's staged files. Both snapshots were
  filtered in place, and both scripts now filter when they capture. A
  snapshot records every public repository, and a private one only if it is
  read.
  - Two private repositories were dropped from the site's snapshot, and eight
    from the experiments'.
  - Afterwards, `grep` found neither unrelated name in any file.
  - The experiments' `--check` still passed, and so did
    `verify/run.sh --require-all` (run `20260929-150827`, 7 of 7).
- A control written for the documents check first invented its own finding,
  because the check it controlled could not see the planted file. It was
  rewritten to call the same function that `--docs` uses on README.md and
  CLAUDE.md, and caught its plant.

### Not done, and why

- **The map on a phone.** It opens on its sparse 2025 stretch. That is
  parcel P2's job ([ROUND1.md](ROUND1.md)).
- **The other eight pages and the plain-text twins.** They are the round's.
- **The site's own watched-fail gate against its sources.** The spec asks
  that a stale number planted in a source record turn the build red. The
  `stale-pin` control re-pins cft-fp256 to its first commit and requires a
  refusal. It does not edit a source repository, and never will: those
  repositories are read, never written.

## 2026-09-29 - a correction: the trailer count is a lower bound, not a measure of AI use; and where StoryDocs came from

**What the lead got wrong.** The first measurement of the day counted
Claude and Gemini Co-Authored-By trailers per repository:
CanonBracketTool 0 of 9, Microscope-Stacker 0 of 7, and 83% to 100% from
PrettyCloud on. The lead read those counts as a measure of how much of each
project an agent had done. On that reading it:

- scoped the biography to "From PrettyCloud on";
- called the spec's "agents write the lines" false for the two earliest
  projects;
- greyed those projects out on the map.

Logan's correction: "basically every project was entirely AI driven, the
commit co author line simply wasn't always there. So the counts are honest,
but the overall work is basically entirely AI." A trailer count measures
the trailers. Reading it as the work was a domain error, the same kind
ParcelRound's round 4 found in its verifiers' figures.

**Changed on branch `p0.1`:**

- The biography: "AI agents have written essentially all of the code in
  these projects", stated.
- The Home column is renamed "agent-credited". Its caption calls the count a
  lower bound and gives Logan's word, stated.
- The map no longer greys out any node by its trailer count, and its legend
  entry is gone.
- `docs/SPEC.md`: decision 23, the corrected row in section 3, and the
  definition in section 4.

**StoryDocs** (decision 22). Logan: it "came from the darkroom project, its
'art books' were the basis of the system", and it has touched most of the
projects. Its README at `673148c` agrees: the book side was "taken out of
atlas-darkroom", and the paper side is "a hybrid of a research paper and
that book's idiom". Its `projects/` directories at that pin are atlas-engine,
atlas-film, atlas-optical, cft-fp256, method, prettycloud and quantum-film.
Its first commit is 2026-09-20. Its place on the map, and edges derived from
those directories, are parcel P2's work.

### Measured

`python site/build.py` published 17 files, now holding 131 figures:

- 14 figures fewer, because the map no longer reads each node's trailer
  count;
- 1 more, Logan's stated sentence.

`bash verify/run.sh --require-all` passed, with nothing skipped.

## 2026-09-29 - P0.1: verifier-P0's report on the shared core, and what each finding changed

verifier-P0 checked `2c02ffe` and reported **NOT READY**. Only two properties
were held by a gate it had watched fail: the drift gate, and `--verify-facts`
for figures read at a pin. For every other claim it built a fault that passed
all 7 stages of that runner. Every finding is accepted.

**Fixed with a gate**, each watched failing in `--control`:

- **The figures.**
  - `fig()` now prints a figure only if it is exactly what its fact returned
    (`facts.logged`), and marks it with its fact's id.
  - A new `numbers` stage refuses:
    - a numeral on a page outside a mark;
    - a mark whose text or source label isn't its own fact's;
    - a figure span with no id;
    - the number words it lists.
  - The stamp's page count, the footer's pins and "private" markers, and the
    map's dates and markers are now facts.
- **Paraphrases.** The page prints the source's words beside the paraphrase.
  A display carrying a numeral its source lacks is refused, and so is a
  pattern that matches more than once.
- **"Last verified".** Every workflow of every pin is classed, and the build
  refuses an unclassed one. Ledger passes are declared as named forms.
  cft-fp256 now counts CI only: its ledger's last `VERDICT: PASS` was a
  2-stage `--only` run. CI times are converted to the pinned commit's
  author's calendar.
- **Open regressions.** A control plants a failure, a timed_out and a
  startup_failure, each shown as open, and a cancelled and an
  action_required run, each passed over.
- **Pins.** The snapshot records the SHA GitHub gives for each pin. The
  build refuses a pin the snapshot didn't look up, one GitHub doesn't have,
  or one a local directory resolves differently.
  - atlas-darkroom's pin `6a33735` existed only in Logan's clone: one commit
    on top of GitHub's `c1b9b6e`, "the fp256 overlap, brought current". It is
    re-pinned to `c1b9b6e`.
- **Manifest.** A `manifest` stage, which CI runs, holds `public/` to its
  MANIFEST file for file. It also holds pins.json and the snapshot to the
  hashes MANIFEST now records.
- **Local-only.** An allowlist of elements and attributes replaces the list
  of refused loads, and every page carries a Content-Security-Policy. CSS
  `url()` is read in any case, and CSS escapes and `@import` are refused.
- **Links.** A link must name a published file exactly, and its `#anchor`
  must exist.
- **Documents.** No document states the stage count. `--docs` refuses a
  count in any form, including inside fences. It also checks links with
  titles, reference links, raw anchors and heading anchors.
- **The runner.**
  - `--require-all` refuses `--only` and `--skip`, and `--resume` refuses a
    dirty tree.
  - The runner's control must print `CAUGHT:`.
  - A skip inside any stage fails under `--require-all`, and the count
    survives a resume.
  - With `--only`, the verdict names the selection.
- **Privacy.** A `privacy` stage runs on the desktop, with Logan's `gh`
  login. It looks for any private repository the site doesn't read in every
  tracked or new file, every commit message and every branch name, and
  prints places, never names.
- **Statements.** `stated()` takes who and when, with no default.
  - "A revision-7 round is under way off main" is tied to cft-fp256 at
    `77b8440`, and refuses the build once that pin moves.
  - The biography is labelled as drafted from Logan's words and not yet
    approved, until Logan approves it (decision 14).
- **The ledger parser.** A heading inside a code fence is not an entry.

**Stated as limits**, in `facts.py`, the README and CLAUDE.md:

- The numbers stage sees number words only from its list, not "one" or
  ordinals.
- A paraphrase's meaning is not checked.
- A snapshot figure is re-read from the committed snapshot, not from GitHub
  today.
- A numbered ledger heading that was retitled is dated at its retitling.
- A hand edit that also rewrites MANIFEST passes CI; only the desktop's
  `build` stage sees it.
- The privacy stage sees names, not descriptions.

**Corrected claims:**

- SPEC section 3's Preservation row: two people besides Logan, not three
  ("Rebase" is Headless Rebase's own account). The organisation has 12
  public repositories, of which the site pins 4.
- The ledger caption, the footer, the README, CLAUDE.md, and the runner's
  header and stage descriptions.
- The map's caption now names the UTC dates. Its family is "mercs2
  repositories": it includes a fork and a wiki, so "tools" was wrong. Its
  axis end is derived, and its two bare-name edges now quote a sentence.
- The prints' caption.

### The lead's own errors in this work

- **The snapshot pointer.** The lead pointed `pins.json` at a new snapshot
  with `ls | sort | tail -1`. `-1554.json` sorts before `.json`, so it
  picked the morning's file. Now CLAUDE.md trap 10.
- **The first `--control` run.** It reported one control not failing. That
  label plant had replaced nothing, because the label is wrapped in a link.
  All twelve docs controls reported caught, but on the real CLAUDE.md's
  `7 stages`, not on their plants. Every plant now counts as a failed
  control when it plants nothing, or when its base already fails. Each
  control must name its own plant.
- **The prints caption.** The first fix named `ec65c44`, the last commit to
  touch the prints *folder*. That commit wrote another file there. Reading
  the rendered page caught it. Each print's own last commit is read now, and
  the caption refuses if the three disagree. It shows `e7935ef`, which is
  what verifier-P0 measured.

### Measured

- **Build.** `python site/build.py` published 17 files, with 178 figures in
  facts.json. `--numbers` found 270 marks, each tied to its own fact.
- **Changes to published figures.**
  - atlas-darkroom, atlas-optical and binary-sites showed a dash for last
    verified; they now show a date, because their test workflows are now
    classed.
  - cft-rebound moved from 2026-09-13 to 2026-09-14 (entries 36 and 37).
  - mercs2-lua-essentials moved from 2026-08-05 to 2026-08-04: its run was
    created at 19:21 -0700, three seconds after its pinned commit.
  - The new agent-credit rule changed no count. atlas-darkroom went from
    1006/1157 to 1005/1156 because of its re-pin; the dropped local commit
    was agent-credited.
- **Ledger entries.** Still 152, 37 and 19 at the pins.
- **Gate.** `bash verify/run.sh --require-all` ran 10 stages, all passing,
  with nothing skipped, in 52 s. `--control` caught 65 of 65.
- **Build time.** The build takes 12 to 14 s against 4 s at P0. The code is
  not the cause: a bare `git rev-parse` took 0.68 s here this hour, and the
  build makes about 97 git calls.

## 2026-09-29 - P0.1, continued: text in CSS generated content

Before sending P0.1 back to verifier-P0, the lead looked for a way past the
numbers stage. It found one: a stylesheet's `content:` puts text in front of
a reader, and no check of the HTML reads it. A rule like
`.stamp::after{content:" 3397 tests"}` would have printed a typed figure
past every stage.

The numbers stage now reads generated content in every published
stylesheet, holding it to the same rule as a page's loose text. It refuses
`counter()` and `attr()` there, since the text they print comes from no fact.
Both are planted in `--control`, and both are caught. The count is now 67 of
67.

A new stated limit, in the README: an image is checked only as the bytes its
pin gives. What it shows is not read.

## 2026-09-29 - P0.1, continued: two more ways past the numbers stage, closed while the verifier re-checks

The lead found two more ways past its own numbers stage after sending P0.1
to verifier-P0:

- **A figure behind a sign.** A numeral counted only if its word started
  with a digit or one of six prefixes, so `$5` or `=5` passed. Now any run
  of digits counts unless a letter or an underscore comes before it, so a
  name such as cft-fp256 or Mercenaries2 is still not a figure. A name
  caught anyway, like "UTF-8", goes in a page's `NUMERAL_NAMES`.
- **The tick exemption.** A month label was allowed in any element classed
  `tick`, so `<span class="tick">Sep 2026</span>` could state a date in
  prose. Now only SVG text of that class, inside an `svg`, is exempt.

Both are planted in `--control` and caught, which makes 69 of 69. The page
itself still passes: 270 marks, and no numeral outside one.
