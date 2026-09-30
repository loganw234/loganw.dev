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

## 2026-09-29 - P0.2: verifier-P0's first five findings on bc2ffbc, fixed while it finishes

verifier-P0's re-check logged five ways past the new gates at 17:15:17, each
passing all 10 stages. It also found CLAUDE.md trap 9 false. These fixes are
on branch `p0.2`, cut from `bc2ffbc`, so that `p0.1` stays still while it
works.

- **Duplicate attributes.** A browser keeps the first of two same-named
  attributes, and the checks' `dict()` kept the last. So a page ran under a
  policy the check never read. Both local-only and numbers now refuse a
  repeated attribute, and numbers reads every alt, title and aria-label
  value.
- **Stylesheet text.** Every string in a stylesheet is now held to the
  numbers rule, which covers `quotes`, `list-style-type` and generated
  content. `counter-reset`, `counter-set`, `counter-increment` and
  `@counter-style` are refused, since they print numbers without a string.
- **Number words in a paraphrase.** A display may not add a number word its
  source lacks, as it already could not add a digit.
- **Allowed names.** A page module can no longer allow names; one that
  defines `NUMERAL_NAMES` is refused. Allowed names live in
  `site/data/numeral_names.json`, which is the lead's. Each must appear in
  some fact's text, and the numbers stage prints each one it allowed.
- **Published types.** An asset must be a `.png`, `.jpg` or `.webp` under
  `assets/`, and must be that type by its bytes. local-only refuses any
  published file that is not a page, text, JSON, image or font of its
  claimed type, apart from BUILD and MANIFEST.
- **CLAUDE.md trap 9**, rewritten: no page reads the organisation's pins
  yet, so nothing needs the fetch.

Three more, found by the lead reading its own gates:

- A `<meta name="twitter:description">` would put a card's text before
  readers unchecked. Only the site's own four meta tags are allowed now.
- `fonts/SOURCES.txt` publishes typed sizes, hashes and a total. The
  manifest stage now checks each against the fonts' bytes.
- The privacy stage reads a name wrapped at one of its own hyphens as one
  word.

Each is planted in `--control` and caught, 87 of 87.
`bash verify/run.sh --require-all` on this tree passed 10 of 10, with
nothing skipped.

## 2026-09-29 - the biography approved

Logan, 2026-09-29: "Biography is good, once the verifier finishes you are
clear to begin".

- **The biography.** Home's biography is the lead's draft, built from the
  spec's own words. Its label no longer calls it a draft. It now reads
  "stated by Logan, 2026-09-29". SPEC decision 14 records the approval in
  Logan's words.
- **The round.** Once verifier-P0 reports READY, the lead may:
  - merge;
  - create the public repository;
  - push, which deploys (decision 7);
  - begin the round.

  Logan gave this clearance in the same message.

## 2026-09-29 - the workflow's actions, moved to their current majors before the first push

Read from each action's GitHub releases, 2026-09-29:

| action | was | now |
|---|---|---|
| actions/checkout | v4 | v7 |
| actions/setup-python | v5 | v7 |
| actions/upload-pages-artifact | v3 | v5 |
| actions/deploy-pages | v4 | v5 |

The old majors ran on Node 20; checkout v5 and setup-python v6 moved to
Node 24. The breaking changes in between don't touch this site:

- upload-pages-artifact v4 leaves dotfiles out, and `public/` has none;
- setup-python v7 removed the `pip-install` input, which this workflow never
  used, and Python versions past their end of life. 3.12 is not one of them.

The first push tests the deploy job itself; nothing here can run it locally.

## 2026-09-29 - verifier-P0 on bc2ffbc: NOT READY; the rest of its findings, fixed on p0.2

verifier-P0's re-check of `p0.1` at `bc2ffbc` came back **NOT READY**.

**Held by gates it watched fail:**

- open regressions;
- drift and manifest;
- the runner;
- CI.

**Beyond the five findings fixed in the P0.2 entry above, still open:**

- **The "newest" rule.** Making `last_verified` take the *oldest* pass
  changed four dates on Home, and every stage passed.
- **The ledger parser.** A fence left open, or 4 backticks closed by 3,
  dropped every later heading without a word.
- **MANIFEST.** Its header said the source lines hash what the build read
  besides the pins. They hashed only pins.json and the snapshot.
- **Pins.** The rule that GitHub has each pin was only the snapshot's word.
  A local-only pin plus a hand-edited snapshot passed everything, and SPEC
  section 4 stated the rule as absolute.
- **Assets.** An asset named with `../` wrote outside `public/`.
- **Docs.** The stage-count rule missed "Stages: 10.", "The stage count is
  10.", "a dozen stages", "ten separate, independent stages" and "10 (ten)
  stages". VALIDATION.md's links were never checked, and a raw `<img src>`
  to a missing file passed.
- **Privacy.** The search skipped any file with a NUL byte, so UTF-16 went
  unread. It never read earlier commits, which a push would publish.
- **False claims:**
  - CLAUDE.md trap 13 ("in any form");
  - "refuses any numeral", in the README, CLAUDE.md and facts.py;
  - the footer ("every figure ... names where it was read", while its own
    pins print without a label);
  - Home's fourth check, which said "a figure from a private repository is
    skipped by name", while private snapshot figures are re-read.

**Fixed on `p0.2`:**

- **The "newest" rule.**
  - A control plants a newer passing run for atlas-film.
  - For each ledger, a control finds the newest pass a second way, by
    walking the entries from the newest back, and compares it with the
    page.
- **The ledger parser.**
  - It refuses an unclosed fence, and a heading underlined with dashes.
  - It reads a heading indented up to three spaces, or with a tab after its
    marks, as CommonMark does.
  - At the pins, none of the three ledgers has any of these shapes.
- **MANIFEST** now hashes every file under `site/`, and `--manifest` checks
  each against the checkout. So in CI, a code change that was never rebuilt
  into `public/` fails too. The header now says exactly what the source
  lines hash.
- **A new `github` stage** asks GitHub itself about every pin, with Logan's
  login, on the desktop. In CI it is skipped by name, and `facts` fetches
  each public pin from GitHub. SPEC section 4 now names all three ways the
  rule is held.
- **Writing.** `write()` refuses any published path that climbs out of
  `public/`.
- **Docs.** The stage-count rule now matches a count close to "stages" on
  either side, and near "stage count" and "number of stages". "stage 2", an
  index, is not a count. Links are checked in every document, the ledger
  included, and raw `<img src>` links are read.
- **Privacy.** The search reads every file as bytes: UTF-16 by its
  byte-order mark or its NUL pattern, and the name as UTF-8 or UTF-16 in any
  other binary file. It also reads every blob reachable from any ref.
- **The claims.** Each is reworded.
  - The numerals limit is stated in the README, CLAUDE.md and facts.py:
    digits straight after a letter are read as a name, so "x3397" would
    pass.
  - Trap 13 names its rule.
  - The footer says what it labels, and what facts.json lists.
  - The fourth check says what is skipped and what is only listed.

**Correction to the P0.1 entry.** It credited cft-rebound's move to
2026-09-14 to "entries 36 and 37". Only entry 36 matches a declared pass
form: `hw/verify-image.sh` 8 of 8 PASS, and `device-test` 813 checks 0
failed. Entry 37's "60 rows, 0 failures" is a benchmark table, which no
declared form matches. The date is right, and so is its source.

**binary-sites, measured.** Its `build` workflow is classed as verifying.
Its Chromium smoke test exits 0 when the runner has no Chromium. The run at
the pinned commit, `35645956458`, ran the test: its log prints "ok" for all
four sites. So the pass Home shows included the browser check. The
skip-and-exit-0 is a weakness in binary-sites' own gate. It is reported to
Logan, and the site doesn't paper over it.

**The count.** `--control` caught 109 of 109. The runner now has one more
stage, `github`.

## 2026-09-29 - verifier-P0 on p0.2 at 3743c52: NOT READY on four small gaps; fixed

verifier-P0 re-checked `p0.2` at `3743c52`: 11 of 11 passed, and controls
caught 109. It held these by faults it chose:

- the newest rule, both ways;
- the manifest, including a stylesheet built into `public/` that existed
  only untracked;
- a local-only pin vouched for by a hand-edited snapshot, caught by the
  `github` stage;
- local-only;
- docs.

Four gaps passed every stage:

1. **Ancestry.** Removing the check that a run is on the pinned commit or an
   ancestor of it changed nothing at these pins, and no control planted a
   run outside the pin's history.
2. **A single dash.** A heading underlined with one dash was dropped without
   a word. The rule matched two dashes or more, and the docstring promised a
   refusal.
3. **Privacy.** The search missed a name that appeared only as a path, in an
   annotated tag's message, or in a compressed PNG text chunk.
4. **The footer.** It said every figure above it names where it was read.
   Four of the map's figures had no source anywhere on the page: the
   snapshot date, two "private" markers and "refesl.live".

**Fixed:**

1. A control plants a newer run on a commit outside atlas-film's history,
   once passing and once failing. Neither may change last verified or the
   open column.
2. The parser refuses:
   - an underline of one dash or more;
   - a heading inside a quote or a list item;
   - an HTML `<h2>`.

   A rule after a closed fence is still read as a rule. On the desktop, a
   control reads every ledger a second way, with markdown-it-py's CommonMark
   parser, and compares counts: 152, 37 and 19 entries match 152, 37 and 19
   level-2 headings. Where markdown-it-py is missing, the control is skipped
   by name.
3. The privacy search reads every path, now and in history, every annotated
   tag's message, and every PNG text chunk, compressed ones inflated. What it
   cannot read is stated: text drawn as pixels, and compressed data in other
   formats.
4. The list under the map now gives the source of everything the drawing
   marks. The numbers stage refuses a figure above the footer whose source
   is nowhere on the page, and the footer says where the map's sources are.

**The two side notes:**

- A name in `numeral_names.json` must now have the shape of one:
  capitalised words, then one number. So "28 of 41", which a fact holds,
  can't be allowed as a name.
- Headings in a quote or as HTML are refused, as above.

**Also recorded:** decision 24, Logan's word that the parcels, and their
verifiers, run on Sonnet.

`--control` now catches 123 of 123.

## 2026-09-29 - verifier-P0 on p0.2 at 00c847e: NOT READY on three overclaims; fixed

verifier-P0 re-checked `00c847e`: 11 of 11 passed and controls caught 123.
The four gaps from its previous report are closed; it removed each fix and
watched the matching control name it. Three sentences still claimed more
than their gates held:

1. **The footer.** It says every figure above it names its source "beside
   it, or ... in the list under the map". The gate only checked for a label
   somewhere on the page, so a second, unlabelled copy of a figure passed.
2. **The parser's docstring.** It said every other shape of level-2 heading
   is refused. Not refused:
   - a quote in a list item, and a list item in a quote: both dropped;
   - a heading inside a multi-line HTML comment: read, though it never
     renders;
   - an `<h2>` inside another HTML block: escaped both the parser and the
     cross-check.
3. **Privacy.** The search didn't read commit identities (author,
   committer, tagger), and didn't say so.

It also noted that CI pinned markdown-it-py by version only, not by hash.

**Fixed:**

1. **The numbers stage** now holds the footer's own words. A figure outside
   the map must have its label directly after it. A figure the map draws
   must have its label in the list under the map. Two controls plant the
   verifier's second copy and a missing line under the map.
2. **The parser now follows CommonMark's HTML-block rules.**
   - A comment runs from `<!--` to `-->`, and a block-level tag's block runs
     to the next blank line. Neither holds a heading.
   - It refuses an `<h2>` anywhere outside a code span, and a comment left
     open.
   - It refuses a heading under any nesting of quotes and list items.
   - The cross-check now compares every level-2 heading's line and title
     with CommonMark's, not just the count. All three ledgers are identical:
     152, 37 and 19.
   - The docstring now says which shapes are refused, and that the
     cross-check holds the rest.
3. **Privacy** now reads every author, committer and tagger, name and
   email, and the docstring lists them.
4. **CI** installs `markdown-it-py` and `mdurl` with `--require-hashes`
   from `verify/requirements.txt`. The hashes are PyPI's published sha256,
   matched against a hash-checked download.

`--control` now catches 131 of 131.

## 2026-09-29 - verifier-P0 on p0.2 at e6ce3d3: NOT READY on one gap, a stylesheet hiding the sources; fixed

verifier-P0 re-checked `e6ce3d3`: 11 of 11 passed, and controls caught 131.
It closed all three overclaims from its previous report, each by watching
the matching control fail on its own sabotage. Its line-and-title
cross-check caught a parser that put every heading one line off, while the
counts all still matched.

**The gap.** One file under `site/styles/` holding `.src{display:none}`
passed every stage. In the browser, 49 of the 124 labels vanished. The gates
read the HTML, and nothing read what a stylesheet hides.

**Fixed:**

- The numbers stage refuses any stylesheet rule that hides what it styles,
  unless `site/data/css_hides.json` (the lead's, empty today) names its
  selector. The hiding forms it refuses:
  - `display:none`;
  - `visibility:hidden` or `collapse`, and `content-visibility:hidden`;
  - zero opacity, zero font size, and a zero scale;
  - transparent text;
  - `clip` and `clip-path`;
  - `text-indent`;
  - an opacity filter.
- Three controls plant `.src{display:none}`, `.fig{visibility:hidden}` and
  `main .src{font-size:0}`.
- The README states what remains: the gates don't lay the page out, so
  text coloured like its background, or stacked under something else,
  would pass.
- The page contract, `_common.md` and P2's brief say how to ask for a
  hiding selector. P2's phone layout will need one, and its hidden view may
  hold no figure the shown one lacks.

**The side note.** The parser's docstring said a block-level HTML block runs
to the next blank line, and that isn't true of `<pre>`, `<script>`,
`<style>` or `<textarea>`. The parser now follows CommonMark's HTML block
types 1 to 5, each ending at its own marker:

- the closing tag;
- `-->`;
- `?>`;
- `>`;
- `]]>`.

It refuses any of them left open. Seven shapes agree with markdown-it-py,
including a `<pre>` spanning a blank line. The ledgers are unchanged at 152,
37 and 19 entries.

`--control` now catches 135 of 135.

## 2026-09-29 - verifier-P0 on p0.2 at 1c1779b: NOT READY on transparent text spelled another way; fixed

verifier-P0 re-checked `1c1779b`. It watched the hiding controls and the
`<pre>` control fail on its own sabotage. One claim still went further than
its check:

- **Transparent text.** The README listed it as refused, but the check
  matched only the word `transparent`. `.src{color:rgba(0,0,0,0)}` made all
  124 labels transparent in the browser, and every stage passed. So did
  `#0000`.
- **Two more spellings.** `font-size:calc(0px)` and the standalone `scale:0`
  also passed.

**Fixed.** The hiding check now reads each declaration's value, not its
words:

- **Colour.** It reads a colour's alpha in every notation: `#rgba`,
  `#rrggbbaa`, `rgb()`, `rgba()`, `hsl()`, `hsla()`, and the newer colour
  functions. It checks `color`, `fill` and `-webkit-text-fill-color`, and
  refuses `fill-opacity:0`.
- **Custom properties.** It follows them: `var(--x)` is read as every value
  `--x` is given anywhere in the stylesheet, fallbacks included.
- **Zero values.** It refuses a zero, and anything computed with `calc()`,
  `min()`, `max()` or `clamp()`, in each of these:
  - opacity;
  - font size;
  - the `font` shorthand;
  - `scale`;
  - `zoom`;
  - `transform`;
  - an `opacity()` filter.
- **Other properties.** It refuses `mask`, and `fill:none`.

The site's own stylesheet uses `fill:none` on the map's axis and arrows,
which are SVG paths drawn as strokes and hold no text. Those two selectors
are now named in `site/data/css_hides.json`, with that reason.

Six new controls plant the verifier's spellings and three more:

- `rgba(0,0,0,0)`;
- `#0000`;
- a transparent custom property;
- `calc(0px)`;
- `scale:0`;
- map text with `fill:none`.

The README lists exactly what the check refuses. Near-zero values, text
coloured like its background, and text off screen or stacked under
something else remain the stated limit.

**The side note.** An empty comment, `<!-->` or `<!--->`, is complete in
CommonMark, but the parser had held it open. CommonMark tests an HTML
block's end on its whole first line, and the parser now does the same.
A control plants the empty comment.

`--control` now catches 142 of 142.

## 2026-09-29 - verifier-P0 on p0.2 at 1b87925: NOT READY, the README's CSS list claimed more than the check read; fixed both ways

verifier-P0 re-checked `1b87925`. It watched the custom-property control
fail on its own sabotage. The empty comments now agree with CommonMark.

The README said a colour with zero alpha is refused "in any notation", and
zero opacity "in any property that sets one". Six spellings inside those
claims passed:

- a `var()` fallback containing parentheses, which stopped the property
  being read;
- a property registered with `@property` and an initial value of
  `transparent`;
- an alpha written with `calc()`;
- a negative alpha, and a negative opacity, both of which browsers clamp to
  zero;
- `-webkit-clip-path`.

Two of them hid all 124 labels, and every stage passed. The verifier said
why the rounds keep finding new spellings: the check reads CSS text, and the
browser renders it. It suggested the README name the spellings the check
reads, and let "anything else passes" cover the rest.

**Fixed, both ways.**

1. **The check.**
   - It reads `var()` with nested parentheses.
   - It takes an `@property`'s initial value as a definition.
   - It refuses a computed alpha, and values below zero.
   - It reads property names without a vendor prefix.

   Seven new controls plant each spelling, plus the side note below.
2. **The README.** It now lists exactly what the check refuses, as the
   check's own comment does, and says anything else passes. "In any
   notation" and "any property that sets one" are gone.

**The side note.** An entry in `css_hides.json` exempted its selector from
every hiding form, so `.map .edge{display:none}` passed. An entry now names
the declarations it may use, and allows only those. The map's two entries
allow `fill:none` alone. The page contract, `_common.md` and P2's brief
say so.

`--control` now catches 149 of 149.

## 2026-09-29 - verifier-P0 on p0.2 at 72f8525: NOT READY on nested and at-rule blocks; fixed

verifier-P0 re-checked `72f8525`.

**Closed.** All six spellings from its last round are refused, and so is
`display:var(--d)` with `--d:none`. The allowlist is scoped per
declaration: `.map .edge{display:none}` is refused. When it sabotaged the
check back to whole-selector exemptions, the control named it.

**Still open.** The check skipped every block whose prelude starts with
`@`. With CSS nesting, an at-rule inside a style rule holds declarations
that apply to the parent. These passed every stage:

- `.src{@media all{display:none}}`
- `@scope (.src){display:none}`
- `.src{@supports (display:block){display:none}}`

In Chrome, each of the first two hid 49 of the 124 labels.

**Found while fixing it.** The lead found a sibling: the old block reader
matched only innermost blocks, so in `.src{display:none; .x{...}}` the
declaration beside the nested rule was never read.

**Fixed.**

- A brace-depth scanner replaces the old regex. It reads the declarations
  directly inside every block, at any depth, at-rules included, and keeps
  quoted strings whole.
- A string left open ends at its line, as a browser ends it, so a stray
  quote can't swallow the rules after it.
- A nested block is named by its own prelude, so `css_hides.json`, which
  names flat selectors, never allows one.

**New controls, each caught:**

- the verifier's three blocks;
- a declaration beside a nested rule;
- a keyframe that fades to nothing;
- an allowed declaration nested under its parent;
- a hiding rule after a string left open;
- the scanner reading all 88 blocks of the real stylesheet, one per opening
  brace outside a string.

The README's "Styles" item says every block is read.

`--control` now catches 157 of 157.

## 2026-09-29 - verifier-P0 on p0.2 at d1b34d1: NOT READY on a quote inside an unquoted url(); fixed by one CSS tokenizer for every check

verifier-P0's run was cut short by a dropped connection, then resumed from
the same copy.

**Closed.** At `d1b34d1` its three at-rule forms are refused, and so is the
lead's sibling, a declaration beside a nested rule. It sabotaged the
reading of at-rule blocks, and the controls named the change. The
block-count control caught its first plant.

**The gap.** The two-line file

    .src{background:url(assets/pauli-print.png');display:none}
    }

passed every stage.

- A browser reads the quote as a malformed URL that ends at the `)`, so
  `display:none` applies. In Chrome it hid 49 labels.
- The scanner read the quote as the start of a string running to the end of
  the line, so it never saw `display:none`.
- The stray `}` on the next line kept the block count even, so the
  block-count control passed too.

**Fixed.** Stylesheets are now cut into tokens once, the way CSS Syntax 3
cuts them, by `build.css_tokens`:

- a comment runs to `*/`;
- a string runs to its closing quote or, if left open, to the end of its
  line;
- an unquoted `url(` runs to its first `)`, and is malformed if it holds a
  quote, a space, `(`, `{`, `}` or `;`.

Every stylesheet check reads through it:

- the hiding check's block scanner;
- the numbers stage's strings and counters;
- local-only's loads;
- the links check's `url()`s.

No check strips comments with a regex any more. While fixing this, the lead
found that such a regex spans from a `/*` inside one string to a `*/` inside
another, deleting the rule between them before the check sees it.

Local-only also refuses every shape in which a reading of the text and a
browser's could still part:

- a string or a comment left open;
- a comment marker inside a string;
- a malformed `url()`;
- a backslash escape, which it already refused.

**Controls.** Seven new ones: the verifier's plant, the comment-marker
trick, a semicolon inside an unquoted `url()`, and each refused shape. The
block count now reads the tokens. The README's "Styles" item says how
stylesheets are read.

`--control` now catches 164 of 164.

## 2026-09-29 - verifier-P0 on p0.2 at b40598b: NOT READY on a form feed in a string; fixed, with a tinycss2 cross-check

verifier-P0 re-checked `b40598b`.

**Closed.** Last round's `url()` plant is refused. The verifier stopped
`css_tokens` recognising `url(`, and three controls named the change.

**The gap.** CSS Syntax 3 turns carriage returns and form feeds into line
feeds before it reads anything, so a browser ends a string at a form feed.
The tokenizer ended a string only at a line feed. The plant was
`.src{content:'a<FF>;display:none;x:'` followed by a newline and `}`. It
passed every stage, and in Chrome it hid 49 labels. Carriage returns never
reached the tokenizer, since the build reads files as text, but form feeds
did.

The verifier also noted that each of the last five rounds found one more
place where a hand-written reading and a browser's part. A cross-check
against a real CSS parser would end that, and it needed Logan's approval
for the dependency.

**Logan, in chat:** "Installing something for a cross check is fine".

**Fixed:**

- `css_tokens` now does what CSS Syntax 3 does first: CR LF, CR and form
  feed become line feeds, and NUL becomes U+FFFD.
- Local-only refuses any control character in a stylesheet other than a line
  feed or a tab.
- **The cross-check.** A control reads the published stylesheet a second
  time with tinycss2, which follows CSS Syntax 3 and CSS nesting. It fails
  the gate if the two readings differ in the number of blocks, any block's
  prelude or properties, or the hiding check's verdicts.
  - On the real stylesheet the two readings agree: 88 blocks.
  - Every plant from the last five rounds reads the same in both.
  - A second control shows the comparison bites. A reader that sees only
    innermost blocks, as this build's first one did, is named: it reads 1
    block where tinycss2 reads 2.
- **The claim.** The docstring and the README now say local-only refuses
  "the shapes this build knows of", and that the cross-check holds the rest.
  "Any shape" is gone.
- **Pins.** `verify/requirements.txt` pins tinycss2 1.5.1 and webencodings
  0.5.1 by PyPI's published sha256, next to markdown-it-py and mdurl. All
  four were matched by a hash-checked download. They are the versions this
  desktop already had installed, so nothing was installed here. CI installs
  from the file.

`--control` now catches 168 of 168.

## 2026-09-29 - verifier-P0: READY on p0.2 at ed990fb

verifier-P0 re-checked `ed990fb` and reported **READY**. Every item on its
list is now either held by a gate it watched fail on a fault of its own
choosing, or stated as a limit where the claim is made. Every fault it
built that passes the gates lands inside a stated limit.

**What it ran:**

- **The desktop.** `bash verify/run.sh --require-all` passed 11 of 11 stages,
  with nothing skipped, and the controls caught 168.
- **Simulated CI.**
  - build, privacy and github were skipped by name;
  - facts read 153 figures again and skipped 19;
  - the controls caught 165 and skipped 3;
  - both cross-checks ran.

**The backstop, watched working.** In a copy, it undid both form-feed fixes
and published its plant. The hand-written checks let it through. The
tinycss2 cross-check failed the gate and named the block: `.src` read as
`['content']` in this build and as `['content', 'display', 'x']` in
tinycss2.

**Its one side note, a wording fix, is made.**

- Local-only refuses ASCII control characters, which is also the CSS
  specification's own set.
- The README's sentence and the check's sentence now say "an ASCII control
  character".
- It is the only change after `ed990fb`.
- `bash verify/run.sh --require-all` passed 11 of 11 again after it.

**For the push.** The verifier could not test the deploy job itself: its
four action versions, and Pages set to deploy from Actions, run only on the
first push to main. That run is watched.
