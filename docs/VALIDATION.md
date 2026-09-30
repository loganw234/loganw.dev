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

## 2026-09-29 - the first push: main at 7174f67, deployed; the custom domain set

**Before the push.**

- Logan cleared the step: "once the verifier finishes you are clear to
  begin".
- main was fast-forwarded to `p0.2`, at `7174f67`.
- `bash verify/run.sh --require-all` on main passed 11 of 11, with nothing
  skipped.
- The commits carry the author identity Logan's other public repositories
  already carry.
- Pages was enabled with Actions as its source, through
  `gh api -X POST repos/loganw234/loganw.dev/pages -f build_type=workflow`.

**The first run**, `36660606803`: every step passed.

- **The gate job**, 1 min 5 s.
  - It installed `verify/requirements.txt` with `--require-hashes`.
  - It ran `LOGANW_FETCH=1 bash verify/run.sh`.
  - build, privacy and github were skipped by name.
  - facts read 153 again and skipped 19.
  - The controls caught 165 and skipped 3.
  - The verdict was PASS, with those skips counted. That is the same result
    as the local CI simulation.
- **The deploy job**, 12 s. It ran checkout v7, upload-pages-artifact v5 and
  deploy-pages v5. This is the first time these ran; verifier-P0 could not
  test them.

**Live**, at `https://loganw234.github.io/loganw.dev/`:

- `BUILD` reads "Deployed from 7174f67cbcd0bc6a9d9e1fbadbd26cbdcce732a9".
- index.html, style.css, facts.json and the three prints are byte-identical
  to `public/`.
- In the browser pane the fonts loaded under the Content-Security-Policy,
  and the console showed no errors.
- The prints were not fetched there, because the pane was hidden and they
  load lazily. They load where the pane is drawn, as they did at 16:4x
  locally.

**The custom domain.** `gh api -X PUT repos/loganw234/loganw.dev/pages -f
cname=loganw.dev` succeeded. It was set before any DNS change, as GitHub
advises against a takeover.

- HTTPS is enforced once GitHub has a certificate, which needs Logan's DNS
  records first.
- loganw.dev still resolves to 15.197.148.33 and 3.33.130.190, not to
  GitHub.

## 2026-09-29 - live at https://loganw.dev

Logan updated the DNS and turned on HTTPS: "I enabled HTTPS already, site is
live and working at loganw.dev". Measured from the desktop:

- **DNS.** Cox's, Google's and Cloudflare's resolvers give loganw.dev
  GitHub Pages' four A records. `www` is a CNAME to loganw234.github.io.
  There are no AAAA records, so there is no IPv6, which is optional.
- **Pages settings.** cname `loganw.dev`, `https_enforced` true, and a
  certificate `approved` for loganw.dev and www.loganw.dev.
- **The site.**
  - `https://loganw.dev/` answers 200, and its index.html is byte-identical
    to `public/`.
  - `BUILD` reads "Deployed from 86d31be3df3d1e6bdb50c74c15c53f35b0932f60",
    from the second push's run, `36660975285`, which passed.
  - `http://loganw.dev/`, `https://www.loganw.dev/` and
    `https://loganw234.github.io/loganw.dev/` each answer 301 to
    `https://loganw.dev/`.
- **The desktop's cache.** This desktop's own DNS cache still held the
  domain's old address, 15.197.148.33, which fails the TLS handshake. So
  these checks pinned curl to 185.199.108.153 with `--resolve`. The public
  resolvers above all have the new records, and the stale entry is this
  machine's alone.

## 2026-09-29 - P1 and P3 merged and live; no email address may be published

**Merged and live:**

- **P1**, Record and Verify, merged as `2c5faa2`. verifier-P1 said READY at
  `1e21d8e`, after three rounds.
- **P3**, Work and the five dossiers, merged as `ff23593`. verifier-P3 said
  READY at `729461d`. The lead's control on that verifier caught 2 of 2
  planted faults.
- Both deploys passed. `BUILD` read each merge commit, and the new pages
  answer 200 at loganw.dev.

**Found in P2's work, before any merge.** P2's credits keyed an account by
its commit email. As a result, facts.json on P2's branch held Logan's own
address, in 4 facts' arguments. The pages themselves print no address.

**The new rule.** No published file may hold an email address except the
site's contact, `logan@loganw.dev` (decision 14).

- The local-only stage now refuses any other address in any text file it
  publishes: pages, text twins, facts.json, the stylesheet, BUILD and
  MANIFEST.
- It reports only how many addresses it found, because CI's logs for a
  public repository are public.
- Two controls plant an address, one in a page and one in facts.json, and
  both are caught.
- Main's published files hold none today. P2 must meet the rule before its
  merge.

## 2026-09-29 - P2 merged (squashed), live; the lead's seam fix: one list of edges for the map and the dossiers

**P2.** verifier-P2 said READY at `bdbac1f`.

- Its first NOT READY was on a gap in a control: `credits-grouping` never
  exercised case-folding. P2 added `credits-case-fold`, and the verifier
  watched it fail on its own fault.
- The lead's own finding was that P2's facts.json keyed an account by its
  email address. P2 now keys by a hash, and the verifier found no trace of
  the address in any tracked or published file.
- P2's earlier branch commits held that address. So P2 was squash-merged as
  `6c163dd`, and main's history never holds it in a file.
- `bash verify/run.sh --require-all` on the squash passed 11 of 11, with
  nothing skipped.

**The seam.** At the merge, all five dossiers' Connections read
relations.json alone. The map, since P2, also draws the edges derived at
StoryDocs' pin, so each dossier missed StoryDocs.

- `mapgen.all_edges()` is now the one list. It holds relations.json's own
  edges, then those derived at a pin, each with its evidence.
- `mapgen.build()` and `_dossier.edges_for()` both read it.
- cft-fp256, Quantum-Film, HonestFramework and ParcelRound now list
  StoryDocs. cft-rebound does not, since StoryDocs has no `projects/`
  directory for it.

**New controls:**

- Each of the 5 dossiers lists exactly the map's edges touching it.
- The old reading, relations.json alone, is shown to miss 4 edges.

`--control` caught 187 of 187.

## 2026-09-29 - edff2b0 live; the site's own ledger becomes a source

**Live.** The deploy of `edff2b0` passed (run 36670593449).

- `BUILD` names `edff2b0`.
- threads.html, thread-film.html, thread-preservation.html,
  work-cft-fp256.html and facts.json answer 200 at loganw.dev.
- The live facts.json holds no trace of Logan's own address.

**Why a new source.** Two of wave 2's pages state facts about this site's
own history: the failures its verifiers caught, and the rounds that built
it. That history is recorded here, in this file. This repository can't be
one of its own pins, so the file is read from the tree being built.

**What holds it:**

- `facts.own_prose()` and `facts.own_entry()` read this file under
  `prose()`'s rules.
  - A pattern must match once.
  - A paraphrase prints its source's words beside it.
  - Every heading must be dated at its start.
- MANIFEST hashes this file, as it hashes pins.json and the snapshot. An
  entry appended after the build fails the `manifest` stage until public/ is
  rebuilt.
- `--verify-facts` reads it again from the checkout, in CI too.
- A figure taken from it links to its line on main. Entries are only
  appended, so a line keeps its entry.

**New controls** (7): the ledger changed after the build; a file outside
the own record; a pattern that matches more than once, and one that matches
nothing; a paraphrase adding a date; an entry asked for at a line with no
heading; and a heading not dated at its start.

`--control` caught 194 of 194.

## 2026-09-29 - wave 1's verifier findings, folded from the round ledger; a cited commit must be on main

**Where this comes from.** Each verifier kept its own file in the round's
ledger, which sits outside this repository and is archived at the round's
end. What follows is what each found before its parcel merged, and where the
fix reached main. The verifiers measured it; the lead read their files.

**verifier-P1** (Record and Verify):

- On `d474080`, it found that the Record's link to each entry, the one a
  reader clicks, was checked by nothing. A link one line off passed every
  stage. Fixed at `5128ce6`: the link and its check now read one href, and
  the check compares it with a fresh read of the ledger.
- On `d474080`, verify.html stated details of cft-fp256's contract in its
  own words, outside any quote. Fixed at `5128ce6`, by quoting.
- On `5128ce6`, one more such sentence remained, in check 3. Fixed at
  `1e21d8e`, where verifier-P1 said READY.

**verifier-P2** (the map on phones, and the Threads):

- On `137157f`, it found that the `credits-grouping` control never exercised
  case-folding. A one-token change to `account_of` passed that control and
  broke the page. P2 added a `credits-case-fold` control, which the verifier
  watched fail on its own fault, and it said READY at `bdbac1f`.
- P2 was squash-merged, so `bdbac1f` is not on main. Its fix reached main
  in `6c163dd`.

**verifier-P3** (Work):

- On `9260b4f`, which carried the lead's two planted faults, it reported
  both, and nothing else in P3's work. The lead's control on the verifier
  caught 2 of 2.
- The lead then asked P3 to quote one sentence the verifier had judged
  borderline, and to look for others like it. P3 quoted five, at `729461d`,
  where verifier-P3 said READY.

**A cited commit must be on main.** A page that cites a commit of this
site's own, as the fix for a finding, goes through `facts.own_commit`. It
refuses a commit that the commit being built doesn't descend from, such as
`bdbac1f`, which GitHub doesn't have. CI's checkout now fetches the whole
history, since a shallow one can't show descent; a shallow checkout is
skipped by name.

- New controls (3): a commit only a side branch holds; a commit the history
  lacks; and a shallow checkout.
- The workflow's comment said the gate used one library. Its controls use
  two, markdown-it-py and tinycss2, each with one dependency, and the
  comment now says so.

`--control` caught 197 of 197.

## 2026-09-29 - Wally only on the game thread's page: decision 16 becomes a gate, before wave 2

**Why now.** Decision 16 says Wally appears only on the game thread's page.
The spec itself names Wally twice more: on Home, and in About's register. P5
writes About, and nothing yet refused the name there.

**What holds it.** The local-only stage refuses the name in every published
text file except `thread-preservation.html` and `facts.json` (`build.ONLY_IN`).
facts.json records the text of every figure and statement, so the
Preservation page's own statement of the name is there too.

- It reads each file with character references decoded, and a second time
  with its tags stripped as well, so an entity, an attribute or markup
  inside the word doesn't hide it.
- It matches the whole word, in any case.
- 5 new controls plant the name on Home: in a sentence, in lower case,
  split by markup, as a character reference, and in an attribute.

`--control` caught 202 of 202.

## 2026-09-29 - verifier-seam's early findings on the lead's seam, fixed; two corrections

verifier-seam is checking the lead's own commits since `ed990fb`. Before
its verdict, it wrote four findings on shared code into the round's ledger.
Each is fixed here, with a control, for its re-check.

**The email gate read raw bytes only.** A page carried a made-up address in
each of these shapes, and every stage passed:

- as `&#64;`;
- as `%40`, in a `mailto:` link and in a GitHub link;
- split by `<wbr>`;
- URL-quoted in facts.json's arguments.

A browser decodes each to the address. The gate now reads every published
text file in each of the ways `build.readings` gives: as it is, with
character references decoded, with inline tags removed and other tags read
as spaces, each of those percent-decoded, and a JSON file as its strings.
The Wally gate reads the same way. 7 new controls plant an address in these
shapes, on a page and in facts.json. An address spelled out for a person to
reassemble is not recognised, which CLAUDE.md states as a limit.

**The Connections control compared two functions, not the pages.** It held
`_dossier.edges_for()` to `mapgen.all_edges()`. An edge dropped where a
dossier renders it, or where the map draws it, passed every stage. The
`links` stage now reads the published pages: each dossier's Connections
must be exactly the edges the map on Home draws touching its project. 3 new
controls: a dossier missing an edge, a dossier listing an edge the map
doesn't draw, and the map no longer drawing an edge a dossier lists.

**The site's own ledger, cited by position.**

- `own_entry(path, line)` returned whatever entry was at that line, so an
  entry inserted above a cited one made it return another entry, silently.
  It now takes the heading's whole text, which must match exactly one
  entry.
- `own_prose(..., last=True)` moved its citation to a later entry that
  repeated the words. `own_prose` no longer takes `last=`: a second match
  refuses by name.
- `--verify-facts` compared a figure's text alone, so a citation that had
  moved to another line read again as the same. It now compares everything
  the record says about where the figure was read. On this tree, 1512
  figures read again as the same.
- 3 new controls: a heading two entries share; an entry inserted above a
  cited one; and a citation published at another line, with the same
  words. The control that asked for an entry at a line with no heading now
  asks for a heading the ledger lacks.

**Two corrections to the lead's records:**

- The entry "P2 merged (squashed), live…" says "each dossier missed
  StoryDocs". That is false for cft-rebound, for which StoryDocs has no
  `projects/` directory: it had no edge to miss. Four of the five missed
  StoryDocs' edges. `mapgen.all_edges`'s docstring said the same, and is
  corrected.
- The README said a figure comes "from one of two places" over three
  bullets. It now says "one of these places".

`--control` caught 215 of 215.

## 2026-09-29 - verifier-seam: NOT READY on main and on wave2-prep; each finding fixed, and seven records corrected

verifier-seam read `2b5c292` and `0176ce4` together, then re-checked
`wave2-prep` at `71c82fe`. It said NOT READY on both. It confirmed the
site itself everywhere it looked:

- the merges took exactly the verified commits;
- `6c163dd`'s tree is `bdbac1f`'s, byte for byte;
- no file in main's history holds the author address;
- the live site is `public/` at `2b5c292`, byte for byte, apart from
  `BUILD`.

What failed was gates and records. Each finding, and what changed:

**Text put together past the email and Wally checks.** A comment, a
zero-width space, a soft hyphen or an SVG `<tspan>` inside the word, CSS
`content` built from two strings, an IDN domain, a non-ASCII top-level
domain, and an address literal each passed every stage. Now:

- `build.readings` removes comments and inline tags, and drops characters a
  browser draws as nothing.
- `build.INLINE` and `build.BREAKING` place every allowed tag. The import
  refuses a tag in neither set.
- The address pattern takes any script, a quoted local part and an address
  literal. A PNG's text chunks are read.
- Local-only refuses an HTML comment, a processing instruction and a CDATA
  section, none of which the build writes.
- A stylesheet string that holds a letter or a digit is refused unless
  `build.CSS_STRINGS` lists it.
- The README states what is left: text put together by layout alone, a
  name in look-alike letters from another script, and an address spelled
  out for a person. A font's compressed tables aren't read.

**A map class on another element.** verifier-seam gave Verify's source
labels the narrow map's class, and at one width they vanished. Each entry
in `css_hides.json` now names the elements its class may be on. The
numbers stage refuses the class anywhere else: `div>svg` is a div holding
one svg and nothing else.

**A Connections item written another way.** An item with a parenthesis
before its colon was never parsed, so its false edge passed. A Connections
section must now be one list, and each item an edge as the dossiers write
it.

**`own_commit` took any name.** `HEAD~1`, a tag and `ff23593^2` were each
printed as the figure. `HEAD~1` then moved to another commit as history
grew. `own_commit` now takes 7 to 40 hex digits only, and ignores
replacement refs.

**A CRLF copy.** On the desktop a CRLF copy of a source passed the gate
with a clean `git status`, and a fresh checkout then failed. The build now
refuses a text source that holds a carriage return.

**Side notes, acted on:**

- A GitHub `#L` link into a Markdown file opens the rendered view at its
  top. Links to a line of a Markdown file now carry `?plain=1`
  (`facts.line_anchor`), and the links stage refuses one without it.
- A StoryDocs directory with fewer bends than nodes lost edges silently in
  `zip()`. The build now refuses it.
- The invariant in the controls that compared two functions and reported
  itself as a control is gone. Its one real plant stays: the dossiers
  rendered from relations.json alone, which the links stage refuses.
- The footer now names this site's own ledger among the places a figure
  is read again.
- The ten CSS load controls were each satisfied by any problem. After the
  string rule, two were caught by it rather than their own rule. Each now
  needs its own rule's words.

**Corrections to earlier entries, found by verifier-seam:**

1. "Live at https://loganw.dev" says the resolvers gave "GitHub Pages' four
   A records". Today the authoritative server, Google, Cloudflare and Quad9
   return three. Whether four were returned at 19:50 isn't known.
2. The wave 1 fold says verify.html's unquoted sentences were "Fixed at
   `5128ce6`, by quoting". Two of the three were cut, not quoted.
3. The same entry says verifier-P3 "reported both, and nothing else in P3's
   work". It also flagged sentences in P3's work as borderline. That is
   what the lead then asked P3 to quote.
4. "The site's own ledger becomes a source" says `own_prose` requires every
   heading to be dated at its start. Only `own_entry` did. `own_prose` does
   from this commit.
5. The P0.2 READY entry says local-only's control-character rule "is also
   the CSS specification's own set". It isn't: the rule also refuses the
   form feed and the carriage return, which CSS reads as line breaks.
6. `6c163dd`'s commit message credits only the lead's model. P2's commits,
   which it squashes, were made on Sonnet 5. It also had no CI run of its
   own: it was pushed with `edff2b0`, whose run deployed both.
7. CLAUDE.md said `own_commit` refuses a commit "that main doesn't hold".
   It refuses one the commit being built doesn't descend from, and CLAUDE.md
   now says so.

`--control` caught 245 of 245.

## 2026-09-30 - verifier-seam: NOT READY on 56a5b82; pages held to a subset of HTML that a browser reads the same way

verifier-seam re-checked `0176ce4..56a5b82`. Every earlier finding held on
its own faults. It then built new shapes that passed all 11 stages outside
the stated limits:

- a name or an address joined across a tag a browser drops or never draws:
  a stray end tag, a `<td>` outside a table, a `<title>` or `<meta>` in the
  body, and a second doctype;
- a `>` inside an attribute, which the tag-stripping pattern misread;
- the unassigned code points U+2065, U+FFF0 and U+E0000, which a browser
  draws as nothing;
- an at sign printed by CSS;
- a second edge appended to a Connections item;
- an annotated tag's hash, given to `own_commit`;
- a figure drawn only in a page's own wide map;
- every source label on Verify, wrapped in `<title>`: 0 px wide, while the
  numbers stage still counted each as beside its figure.

**One cause.** The gates read a page as Python's parser does, and a browser
repairs a broken page another way. Answering each shape wouldn't converge.
So pages are now held to a subset of HTML in which the two build the same
page, as the stylesheet check refuses the shapes where two readings part.

- **The subset** (`build.PARENTS`):
  - strict nesting;
  - each element only where HTML allows it (a `<title>` or `<meta>` only in
    the head, a cell only in a row);
  - text only where a browser draws it;
  - no self-closed HTML element, and one doctype, first;
  - no comment, processing instruction or CDATA section.

  The site's own 13 pages fit it unchanged.
- **Text is read by the parser** (`build._Text`), not a pattern. Inline
  tags join a word, and every other tag breaks it. Each attribute's value
  is read on its own. Then come Unicode's compatibility forms, so a
  fullwidth letter or at sign reads as itself.
- **A character a browser draws as nothing is refused.** That is Unicode's
  whole Default_Ignorable_Code_Point set and every format character,
  right-to-left overrides included, in any published text file,
  facts.json's strings included.
- **A stylesheet may hold only the strings `build.CSS_STRINGS` lists.**
- **A Connections item must be exactly** its edge, its evidence's figure,
  and that figure's source.
- **`own_commit` refuses a hash that names a tag.**
- **The two maps that swap by width come in pairs,** and each pair draws
  the same figures.
- **An image is a PNG,** whose text chunks are read. JPEG and WebP, whose
  metadata no check read, are no longer allowed. A PNG chunk that could
  hold text no check reads (`eXIf`, where verifier-seam put an address,
  `iCCP`, or a private chunk) is refused, and so are bytes after `IEND`.
  The site's prints hold only `IHDR`, `IDAT` and `IEND`.
- **Links to a range of lines** in a Markdown file need `?plain=1` too.
- **Masking.** Everything build.py prints has each address but the contact
  masked. A check that quotes what it refused can't print one, and CI's
  logs are public.
- **Controls.** The email controls "split by a comment" and "split by an
  SVG tspan" were caught by the raw text, which still held a whole
  address. They now split inside the domain. verifier-seam broke the
  comment removal and the tspan joining in a copy, and the old controls
  still reported the fault caught.
- **Speed.** Characters are matched with one pattern built from code
  points, not a loop, and each file's readings are kept by its bytes.
  Local-only takes about a second, as before.

**Corrections to the entry above:**

- It says an IDN domain, a non-ASCII top-level domain and an address
  literal "each passed every stage". verifier-seam measured those three
  at unit level only.
- CLAUDE.md trap 14 said local-only "names only how many it found". The
  rules that quote a stylesheet string or a comment printed what they held.
  The output of every stage is now masked instead, and trap 14 says so.

**A fault in the lead's own controls, found while writing these.** On the
desktop, 24 of the controls' `write_text` calls wrote CRLF: Python on
Windows turns each line feed into a carriage return and a line feed unless
told not to.

- A plant restored that way left carriage returns behind, in MANIFEST
  among other files.
- The five new controls that plant a character drawn as nothing, on a
  page, were then satisfied by MANIFEST's U+000D, not by their own plant.
- Every write now passes `newline="\n"`. Each of those controls names the
  file and the code point it planted, and no control output holds U+000D.
- CI runs on Linux, where the fault could not arise.

`--control` caught 275 of 275.

## 2026-09-30 - verifier-seam: NOT READY on c06a0ea; the subset's own gaps closed, one tag syntax, one Python

verifier-seam re-checked `0176ce4..c06a0ea`. Every fault from its previous
verdict was refused, by the rule meant for it. It then broke the subset
itself, and each break is closed here:

- **A `<title>` inside SVG `<text>`,** empty, split the name and an address.
  A browser draws the text whole, while the check read a break. An SVG
  title now stands only in `<svg>`, `<g>` or a shape.
- **A no-break space after the charset `<meta>`.** Python's `strip()` calls
  it whitespace; HTML doesn't. In a browser it closes the head, and the
  policy and title land in the body. The parsers now use HTML's own
  whitespace (`build.HTML_SPACE`), and `<html>` must hold a head and then
  a body.
- **An override written as a character reference** (`&#x202E;`) drew the
  name backwards. The check refused only the literal character. Characters
  drawn as nothing are now refused after references are decoded too.
- **An end tag holding an attribute** passed on the desktop's Python 3.12.9,
  and CI's floating 3.12 would have refused it. Two answers:
  - Every tag must now be written the one way the build writes them, and
    every `&` must start a reference ending in `;`. The site's 13 pages
    already are.
  - The gate runs only under the Python `.python-version` names (3.12.9),
    and CI's setup reads the same file. Measured: `python3`, which is
    3.13.14 here, is refused before any stage runs.
- **An address in `IEND`'s data** passed the chunk rule. Chunks the format
  sizes must be that size. A PNG may now hold no text chunk at all:
  verifier-seam also carried an address in a UTF-16 string inside one.
- **Encoded addresses in printed output.** A line that names an address in
  any reading (`&#64;`, `%40`, a fullwidth at sign) is withheld whole.
- **Side notes:**
  - CSS `direction` and `unicode-bidi` are refused, since they draw a word
    backwards.
  - The name is matched between letters, so "Wally2" and "Wally_" count.
- **The author address in the round's ledger.** It was in three files,
  never in this repository. The lead redacted it from two, and P4 from its
  own. The privacy stage now refuses an address in any file or commit
  message that pushing HEAD would publish, history included. Allowed are
  the contact, domains and address blocks reserved for examples, and the
  co-author trailer's address. A folding of the ledger into this file
  would be refused.
- **P4 found a control reading the wrong fact.** "A figure the map draws,
  with its line under the map removed" took the first `snapshot_date` fact
  in facts.json, which is Home's only while no page sorts before
  `home.py`. P4's `corrections.py` does. The control now takes the id from
  the line it removes. Two others that picked a fact the same way now take
  theirs from the page they plant in.

**Corrections to the entries above:**

- "24 of the controls' `write_text` calls": that is right at the fix. At
  `56a5b82` there were 22, as verifier-seam counted. The same round added
  two more, all in `controls()`.
- The entry dated 2026-09-30 lists U+FFF0 and U+E0000 among shapes that
  "passed all 11 stages". verifier-seam measured those two at unit level
  only.
- The README's "Pages" and CLAUDE.md trap 14 said the subset holds pages "in
  which this check's parser and a browser build the same page". The gaps
  above contradicted that until now, and on the desktop's Python only
  until the version was pinned.

`--control` caught 294 of 294.

## 2026-09-30 - P4 merged; a page may keep a text to itself (ONLY_HERE)

**P4 merged.** verifier-P4 said READY on P4's own `4d11e60`. The lead's
control on the verifier caught 2 of 2: a misquoted rule of engagement, and
an unsourced sentence on Propose. The merge takes `4d11e60`, never the
commit that carried the plants. Not pushed.

**Why ONLY_HERE.** verifier-P5 found that "the one place the site states
it", on Method, was held by no gate. P5's control rendered Method and
About only, and a copy of decision 9's statement on Home passed every
stage. No page module can read another page, so the gate is the lead's:

- A page may declare `ONLY_HERE = [text, ...]`: texts that only it may
  print.
- local-only refuses each such text on any other published page or text
  file. It reads a page's text as the parser gives it, with whitespace
  collapsed and in lower case, so markup or line breaks inside it don't
  hide it.
- facts.json, which records every statement's text, holds each by design.
- A restatement in other words passes. That limit is stated in the page
  contract.
- 1 new control, with a planted declaration: refused on another page,
  split by markup, and passed on its own.

`--control` caught 304 of 304.

## 2026-09-30 - wave 2 merged: P5 after one send-back; every page built; the seam's own push first

**The seam, pushed first.** verifier-seam said READY on `0176ce4..07b1526`
after five passes. main fast-forwarded to `07b1526`, and the gate passed on
the clean tree: 11 of 11, 294 controls. The push deployed.

- Run 36690194219 passed.
- Its log says "Resolved .python-version as 3.12.9", so CI now runs the
  desktop's Python.
- `BUILD` named `07b1526`, and the live facts.json held no trace of the
  author address's domain.

**P5, Method and About.** verifier-P5 said NOT READY on `d445b42`, with two
findings:

- **A stale "newest entry".** Method said the ledger's newest entry recorded
  "275 of 275". That was true when P5 wrote it, and false once this ledger
  grew. A fact now reads the newest entry that records the controls at
  build (`newest_control_count`). verifier-P5 grew a copy of the ledger
  twice, and the figure followed.
- **"The one place the site states it"** (decision 9) was held by no gate.
  Method now declares the statement `ONLY_HERE`. verifier-P5 planted it on
  Threads and in a dossier's text twin, and local-only refused both.

P5 fixed both at `4a883e4`, where verifier-P5 said READY. P5's first commit
had held two real mail domains in a control. P5 recommitted rather than
merge them into history, and it disclosed that.

**Every page is built.** Home, Threads (with its three threads), Work (with
its five dossiers), Method, Record, Verify, Corrections, Propose and About.
About's two new sentences are drafts, labelled so until Logan approves
them.

`--control` caught 307 of 307.

## 2026-09-30 - verifier-seam: NOT READY on 576b08a; ONLY_HERE now reads attributes and folded forms

verifier-seam checked the lead's commits since `07b1526`. Both merges took
exactly the verified tips (`4d11e60`, never the planted `bd44300`; and
`4a883e4`), each tree equal to its tip's, and nothing on main was lost.
Every figure in the two newest entries checked out against the bytes.

**The one defect: ONLY_HERE read a page's text, and nothing else.** An
exact copy of decision 9's statement passed every stage in any of these:

- another page's meta description, which a search result or a link
  preview shows;
- a tooltip;
- fullwidth letters.

`only_here_problems` now reads the same readings the name and address
checks use (`texts_of`): the text, each attribute's value, references and
percent-encoding decoded, and compatibility forms folded. 3 new controls
plant the statement in a meta description, in a tooltip and in fullwidth
letters on Home, and each is refused.

**Corrections.** The page contract and the entry "P4 merged; a page may
keep a text to itself" said local-only "refuses each on any other published
page". The merge message of `45a3165` said decision 9's statement is "held
once by ONLY_HERE". Neither held for an attribute's value or a fullwidth
copy until this entry's commit.

`--control` caught 310 of 310.

## 2026-09-30 - verifier-seam: NOT READY on 1142ab9; ONLY_HERE compares letters and digits, not characters

verifier-seam re-checked `1142ab9`. Its earlier copies of the statement in a
meta description, a tooltip and fullwidth letters were all refused. Then it
changed only punctuation:

- the statement without its final period, in Threads' meta description
  (full gate);
- the statement without its comma, on Verify (full gate);
- "wouldn't" for Logan's "wouldnt" (unit level).

Each passed. The check compared characters, punctuation included. Its
stated limit is a restatement in other words, and these are the same
words.

**The fix.** `ONLY_HERE` now compares letters and digits alone, in order,
folded to lower case and to Unicode's compatibility form (`build._folded`).
Spacing, punctuation and case don't count. A declared statement is long
enough that its letters don't turn up in that order by chance: the site's
38 published files hold no false match.

**The controls** use a stand-in text with a declaration of their own. They
don't plant decision 9's statement: that is `statement9-once`, P5's
control. 8 cases are each refused on Home:

- as it is, which also passes on its own page;
- split by markup;
- in the meta description;
- in a tooltip;
- in fullwidth letters;
- without its final period;
- without its comma;
- with an apostrophe its source doesn't have.

The page contract's "refuses each on any other published page" now holds
for the same words in any spacing, punctuation, case or compatibility
form.

**Corrections to the entry above:**

- It says the fullwidth copy "passed every stage". verifier-seam measured
  that one at unit level only.
- It says "3 new controls plant the statement". They plant the stand-in,
  not decision 9's statement.
- From here on, the lead's records name the level each shape was measured
  at: the full gate, or a unit-level call. verifier-seam asked for this
  after the third such overstatement.

`--control` caught 314 of 314.

## 2026-09-30 - every page live at 8260fa8; About had printed a pronoun for Logan that Logan never stated

**Live.** verifier-seam said READY on `8260fa8`. Its punctuation faults were
refused after a full rebuild, and the copies that still passed fell inside
stated limits. main was pushed.

- Deploy run 36701445776 passed.
- `BUILD` names `8260fa8`, and all nine pages and facts.json answer 200.
- The navigation links all nine pages.
- About carries its 2 draft labels, and no "Wally".
- The live facts.json holds no trace of the author address's domain.

**A correction, found by the lead on the live page.** About's lede read
"Logan, in his own register." Logan's pronouns have never been stated, and
every brief said to write "Logan". Neither P5 nor verifier-P5 caught it,
and no gate reads pronouns.

- The lede now reads "In Logan's own register."
- Two comments, in `about.py` and `method.py`, are corrected the same way.
- Measured on the rebuilt site: no he, his, him, she or her in any
  published page's text.
- CLAUDE.md trap 18 records it, and the verifier template now names it.

## 2026-09-30 - the round closes: About's sentences approved, the door kept, the labels made, the ledger archived

**Logan's decisions,** in chat on 2026-09-30:

1. "Both sentences are approved": About's two drafted sentences (SPEC
   decision 26).
   - They are now Logan's statements of that date, and About carries no
     draft label.
   - `render_page` refuses every `stated()` figure the page prints that
     carries no draft label and isn't settled. Settled means its words, who
     said them and when are exactly as `SETTLED` has them.
     - Its marks are read by the numbers stage's own reader, so a mark is
       found however its attribute is cased or its id encoded.
     - Where or when the figure was rendered doesn't matter.
   - A sentence printed as plain text, not through `stated()`, is outside
     it: the check reads figures, and plain text is none.
   - 17 controls check it:
     - in each of About's five blocks, a statement planted before the
       block's content and one planted after it, each refused by name,
       while the same statement with its draft label passes;
     - a statement rendered before the page starts, then printed inside
       it;
     - a settled sentence given another who, and one given another date;
     - a statement whose who reads like a draft label;
     - a statement returned through another fact;
     - a mark whose attribute name is upper case, and one whose id is
       written as character references.

     Each also needs the real page to pass.
   - Measured at unit level, on copies of `about.py`, each of these
     sabotages fails at least one control:
     - a window of the log in place of the printed marks;
     - marks read by a regular expression, not the numbers stage's reader;
     - the page's first printed figure skipped, or its last;
     - the date left uncompared, or who;
     - a draft label read as a substring;
     - a statement known by its method rather than its kind;
     - the refusal removed.
2. On the workloads door: "Keep it, at worst aspirational, at best already
   true" (SPEC decision 27). The door is unchanged.
3. "Go ahead and create them": the labels DISPROOF and proposal now exist
   on `loganw234/loganw.dev` (`gh label list`), so the issue forms' labels
   apply.
4. "Go ahead and cleanup".
   - The five parcel worktrees are removed.
   - The merged parcel branches are deleted, and so are P2's squash-merged
     branch, `p0.1`, `p0.2` and `wave2-prep`.
   - The control branches `verifier-P3-commit` and `verifier-P4-commit` are
     kept locally, as the controls' record.
   - GitHub has one branch, main (`git ls-remote`).
5. "Archive the notes into ParcelRound with a case study doc regarding this
   round". The round's ledger is `archive/round5-ledger.zip` in ParcelRound,
   beside `CASE-STUDY-5.md`. It is on a branch there, and not yet pushed.
6. On pronouns: "He/his is fine" (SPEC decision 28, CLAUDE.md trap 18).

**Wave 2's side notes, closed:**

- The page contract's `ONLY_HERE` paragraph now states what the check
  compares, and its look-alike limit. It also says that a short declaration
  could refuse by chance, loudly.
- README "Pages" says `run.sh` checks Python's version string, not the
  parser's bytes.
- `row-typed-cell`'s docstring no longer understates the numbers stage.
  Text typed over an existing mark is caught, digit or not.
- The Corrections ledger's second row cited `1e21d8e`, where verifier-P1
  said READY. But this ledger's wave 1 entry records its finding as fixed
  at `5128ce6`.
  - The row now cites `5128ce6`, as its source does, so one fix commit
    answers the finding, as the page's caption says.
  - The further sentence verifier-P1 found on `5128ce6` was fixed at
    `1e21d8e`.
- Method's "This is the one place the site states it" shows a reader no
  limit. It stays as it is until Logan words it.

**verifier-close** checked this entry's first three versions. None was
pushed. It said NOT READY on each, and every finding is accepted.

- **On the first,** three findings:
  1. That version said the Corrections row named both commits. It named
     one.
  2. About's control planted in one block only. The register, rendered
     before the refusal started reading, printed a changed sentence as
     Logan's, and every stage passed.
  3. The refusal's reach wasn't stated where the claim was made.
- **On the second,** four findings:
  1. A new block, rendered before the refusal started reading, still
     passed. The check read a window of the log, so a list of blocks to
     plant in couldn't cover it. It now reads the page's printed marks.
  2. That version counted two findings where there were three.
  3. The privacy stage's summary line claimed more than the stage checks.
     It now says what README says: any file or commit message that
     pushing HEAD publishes.
  4. Two sabotages passed every control: the date left uncompared, and
     the page's first figure skipped. Each now fails one.
- **On the third,** one finding. The check read mark ids with a regular
  expression. So an upper-case attribute name, or an id written as
  character references, passed it, while the numbers stage still read the
  mark as a figure. The check now reads marks with the numbers stage's own
  reader.

Each is answered above. Its side notes:

- A statement known by its method rather than its kind would have let one
  returned through another fact pass every control. A control plants one
  now.

- SPEC section 2's heading and the list at the top of SPEC now give both
  dates.
- README and CLAUDE.md trap 14 now name every address the privacy stage
  allows: the contact, the co-author trailer's, and those reserved for
  examples, domains or documentation address blocks.
- A who that reads like a draft label no longer passes: a draft is read
  from the label's start.
- The question to Logan quoted About's first sentence and described the
  second. Both were live on About, word for word, when Logan approved them.
- Method's sentence had not been put to Logan. The lead's report of this
  close puts it to him.

**A correction to the entry above.** It says "every brief said to write
"Logan"". Wave 2's briefs did. The rule was added at 22:20 on 2026-09-29,
after wave 1 was dispatched.

`--control` caught 330 of 330.
