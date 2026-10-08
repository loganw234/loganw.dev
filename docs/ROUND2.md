# Round 2: the update round

This is the plan of record for the round that brings the site up to the
projects as they stand on 2026-10-08. The lead (one Claude session, on Opus
5.5) wrote it that day. Logan's request, verbatim:

> Some projects have gotten updated a bit, I'd like to do an update round
> against the new information, but since this is a lightweight round in terms
> of 'complexity', utilize Sonnet models for the parcels and Haiku as
> verifiers. We have also started to track metrics a bit deeper, keeping
> totals on parcels, agents, token use, time, etc. See the new case studies
> for examples, particularly in HonestHarness as thats the most 'tracked'
> examples currently.

The method is [ParcelRound](https://github.com/loganw234/ParcelRound)'s
METHOD.md as it stands at `f42242e`, the method as practised after its round
6, with its checklists. Verification follows
[HonestFramework](https://github.com/loganw234/HonestFramework). Round 1's
plan is [ROUND1.md](ROUND1.md).

Draft 1 went past verifier-plan, which found eight defects; this draft
answers them. The ledger records each finding and how the lead checked it.

## What moved

Measured on 2026-10-08 by `gh api .../compare/<pin>...<default branch>` for
every pin in [pins.json](../pins.json); the same command re-run gives the
same counts while the projects stand still. Every pin not listed is
identical to its default branch.

| repository | pin | GitHub's main | commits ahead |
|---|---|---|---:|
| cft-fp256 | `77b8440` | `ab51655` | 381 |
| ParcelRound | `8767e23` | `f42242e` | 37 |
| Quantum-Film | `a7f02db` | `3a73823` | 171 |
| StoryDocs (private) | `673148c` | `8548802` | 1 |
| Mercenaries-Fan-Build/mercs2-modkit | `3a4d888` | `9acb750` | 5 |
| Mercenaries-Fan-Build/mercs2-wad-simulator | `fdf3597` | `d18af76` | 409 |
| Mercenaries-Fan-Build/notes-on-the-released-game | `b8c3958` | `dac773d` | 70 |

- **New on the account:** HonestHarness, public, created 2026-10-03. Its
  GitHub main is `b310f82`, whose README says "Status: research. There is no
  code yet." It has no workflows. Its round 1 runs on local branches that
  GitHub does not have, so the site cannot pin them.
- **ParcelRound's case study 7** is on its branch `case-study-7` at
  `894d125`, not on main. The pin is main, so this round reads case studies
  5 and 6, not 7.

**The trial.** In a scratch worktree of main at `43c36a2`, the lead moved the
seven pins, took a snapshot there, and rendered each page on its own. Each
page stops at its first refusal, so the trial saw one a page: Map & Ledger
and Work, at Logan's word of 2026-09-29, "a revision-7 round is under way
off main", held to cft-fp256 at `77b8440`; and Verify, at its CONFORMANCE.md
pattern. P0 then met two more on Verify (below).

**What the move changes, in all.** Every fact call in `public/facts.json`,
before the round (`43c36a2`) and after P0 (`05413b2`), matched by its method
and arguments: 27 read different text, all by reading their sources again;
5 are gone; 77 are new. So the round's real work is not the build's
refusals. It is the text: the pages describe the projects as round 1's pins
had them, and every quote on them still stands, so every gate passes.

## Logan's decisions (2026-10-08)

Through the question tool, verbatim, question and then answer. The lead's
reading of each, where one is needed, follows it, marked as the lead's.
SPEC.md keeps them as decisions 31 to 36.

1. "HonestHarness is public, but its GitHub main is still the research stage
   ... How should the site carry it in this round?" - "Row and map node now
   (Recommended)": "Pin GitHub's main; add it to Map & Ledger and the map
   beside ParcelRound and HonestFramework. A full dossier waits until round 1
   lands on main."
2. "Where should this round's case study, with its metrics and archived
   ledger, go?" - "In loganw.dev itself": "In this repo's docs/, with the
   ledger and cost scripts archived beside it, as HonestHarness keeps its
   own."
3. "A push to main deploys the site. Once the round passes the full gate and
   its integration verifier, should I push?" - "Push when verified
   (Recommended)": "Push, check the live deploy byte for byte, then report."
   - *The lead's reading:* this covers the round's push, and the push of the
     case study and its archive at the round's end, each after its own
     verifier's READY and the full gate.
4. "Quantum-Film's round 3 ran the law on three IBM devices and laid the
   results as prints (docs/prints/ibm-*). Should the Film thread show one?"
   - "Yes, one hardware print (Recommended)": "One IBM print beside the
   existing prints, read from the pin like the others, with its source beside
   it."
   - *The lead's reading:* the existing prints are on Map & Ledger, and the
     question was about the Film thread, so the IBM print goes on the Film
     thread's page, and Map & Ledger's three prints stay as they are.
5. "Decision 24 (round 1) kept the verifier of the shared core on the lead's
   model, because it checks code. You asked for Haiku as verifiers. Which
   model verifies the lead's own work this round ...?" - "Haiku for every
   verifier (Recommended)": "Every verifier on Haiku, the lead's work
   included; decision 24 stays as round 1's rule. The lead re-checks each
   Haiku finding against the records before acting."
6. "Your 2026-09-29 line on Map & Ledger, "a revision-7 round is under way
   off main", is no longer true ... How should stale lines of yours be
   handled?" - "Sourced reading; ask me otherwise (Recommended)": "Where a
   stated line of yours is overtaken, it may be replaced by a figure read
   from the source, recorded in the ledger; anything that needs new words of
   yours, or drops one of your spec's choices (such as a Corrections gap),
   comes to you."

So: **parcels on Sonnet; every verifier on Haiku**, the plan's, P0's, each
parcel's, the integration verifier and the case study's.

## Rules carried into this round

Each is a standing rule, with where it was given.

- The full gate, `bash verify/run.sh --require-all` under the Python
  `.python-version` names, before every push. A push to main deploys
  (Logan, 2026-09-29; CLAUDE.md).
- Only main is ever pushed, never `git push --all` (CLAUDE.md, trap 17).
- The shared core first, then a verifier on it, then the round (decision
  18). And the lead's seam commits, merges and records go past a verifier
  before main moves (METHOD.md section 7).
- Agents test what they can quickly, and hand large runs back to the lead
  (cft-fp256's owner's rule of 2026-09-29, METHOD.md section 7). Here the
  large run is the full gate, which is the lead's.
- Only a regression or a wrong answer sends work back. Anything else merges
  as a recorded known limit, and a sentence that claims more than is true is
  restated at the merge (METHOD.md section 6).
- **Logan's words.** About and the front page are his approved words
  (decisions 26 and 29), every `stated()` figure is his statement (CLAUDE.md
  trap 12), and the spec's choices are his (section 1 of SPEC.md). They
  change only at his word, except that a stated line a pin has overtaken may
  be replaced by a figure read from its source, recorded in the ledger
  (decision 36). Anything that needs new words of his, or drops one of the
  spec's choices, goes to him.
- Logan's pronouns are he and his (2026-09-30, trap 18). Anyone else the
  site names is written by name unless their pronouns are stated.
- No published file holds an email address but `logan@loganw.dev` (trap
  14). The name Wally appears only on the Preservation thread's page and in
  `facts.json`'s record of Logan's statement there (trap 16).
- Other repositories are read only at commits, through `git show`, never
  from their working trees, and no agent switches a branch in them (trap 1).
  Other sessions are working in cft-fp256 and HonestHarness.

## The shape

1. **This plan goes past a verifier**, and the lead answers its findings in a
   new draft, which the verifier re-checks, before Logan approves it.
2. **P0, the lead's,** on the branch `round2`, then verifier-P0 on it.
3. **Wave 1: P1 to P4 in parallel, each designing first.** Each parcel reads
   its pages against the new pins, writes a design, and stops. The lead
   reviews the four designs, then makes one seam commit adding every new
   source path and numeral name the designs need. That commit goes past
   verifier-P0, scoped to it, and then each parcel gets "go" with its SHA.
   No parcel has built anything when it lands, so each takes it by a
   fast-forward before building.
4. **Each parcel's verifier** works on a copy of the parcel's work that may
   hold planted faults (below).
5. **Merges onto `round2`**, one at a time. Before each, the lead reads every
   author's file in the ledger; after each, the full gate, whose links,
   numbers and connections stages read every page together and are the
   round's seam test; then the lead's restates.
6. **The verifiers' side notes** get a step of their own after the last
   merge, and the lead appends the round's entry to the site's own ledger,
   `docs/VALIDATION.md`.
7. **The integration verifier** on the lead's own work: its merges, made
   again from their parents with `git merge-tree`, its restates, its
   records.
8. **Main moves to `round2`'s tip** after the full gate and the integration
   verifier's READY, and is pushed. The lead checks the live deploy byte for
   byte.
9. **The case study and the archived ledger**, past their own verifier, then
   pushed.

## P0: the lead's

On `round2`, from `43c36a2`, at `05413b2`. The full gate passes on both sides
of it. What it does:

- **pins.json:** the seven pins above, moved to GitHub's main; HonestHarness
  added at `b310f82`, read from the owner's clone (`"dir": "HonestHarness"`,
  `"workflows": {}`).
- **The snapshot:** `sources/github-2026-10-08-1345.json`, taken with the new
  pins, and pins.json pointed at it by its exact name.
- **The refusals**, fixed only as far as the build needs:
  - Logan's revision-7 line is replaced, under decision 36, by cft-fp256's
    newest ledger entry at the pin, its date and its subject
    (`home.newest_date`, `home.newest_subject`). Work reads Map & Ledger's
    rows, so the one change clears both pages.
  - Verify had three: its CONFORMANCE.md pattern reads the same words with
    any whitespace between them; its `quick` budget is quoted as cft-fp256
    now writes it, which names `innerskips`, `ensurevectors` and the
    language's compiler; and its `gate` budget is quoted only as far as
    "lint, formal", where cft-fp256's sentence goes on to newer legs. P1 owns
    what the page should say.
- **HonestHarness on Map & Ledger**, in the Determinism lane: its row (what
  it is, its state, last verified, the agent-credited count, and a check),
  and its node and three edges in `site/data/relations.json`, each naming the
  words in its README at the pin that make it. It has no workflow and no
  ledger, so "last verified" is a dash with its reason, as SPEC.md section 4
  defines it. Work lists it with the projects that have no dossier.
- **ParcelRound's row:** its check is the method's own gate,
  `python tools/check_method.py`, where it linked to case study 4.
- **`build.SOURCE_PATHS`:** the two paths P0's new labels name.
- **SPEC.md:** Logan's decisions of 2026-10-08, 31 to 36.

**verifier-P0** reads P0 against this plan and the tree, and picks its own
faults.

## Wave 1

Every parcel works in a worktree cut from `round2` at P0's tip. Its first
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
  stage, or `fig()`, refuses it by name;
- a label on one of its pages naming a path `build.SOURCE_PATHS` does not
  list: the numbers stage refuses it;
- one of its new `prose()` patterns given its source's old words: the build
  refuses it by name.

**What no gate holds, stated as a limit:** whether a sentence is the current
truth at the pin, rather than only true at it. That is the round's subject,
and the gates cannot read it. Each parcel's verifier reads every sentence on
its pages against the newest entries at the pin, and that reading is how the
property is held.

### P1: cft-fp256 and the Determinism thread

- **Owns:** `site/pages/work_cft_fp256.py`, `site/pages/thread_determinism.py`,
  `site/pages/verify.py`, `site/pages/corrections.py`, and
  `site/pages/work_cft_rebound.py` (cft-rebound's pin did not move; this
  parcel checks only what that page reads from cft-fp256).
- **What moved:** cft-fp256's ledger runs from revision 7 through the
  certificate plan's steps, the fixes round, the language round, and step 6
  to its close on 2026-10-06, with revision 8's first hardware images. Its ABI
  went from 0.15 to 0.18. The Determinism thread also quotes ParcelRound's
  README, whose quoted sentence is unchanged.
- **Logan's, and staying:** the Determinism door; the rules of engagement on
  Corrections; and the "where I'd attack first" gaps' names, which are the
  spec's. The quotes under each gap are cft-fp256's, and are P1's to re-read.
  A gap the record now says was closed goes to Logan through the lead
  (decision 36).
- **The trap:** a section still true at the new pin but no longer the
  current truth: "Verified" rows that stop at 2026-09-29, a gap the record
  now says was closed, a "Test it" step whose cost changed.
- **Its own control, besides the three:** a dossier row citing a ledger line
  that is not an entry's heading is refused by name (`_dossier._entry_at`).

### P2: the two methods

- **Owns:** `site/pages/work_parcelround.py`, `site/pages/work_honestframework.py`,
  `site/pages/method.py` and `site/pages/propose.py`.
- **What moved:** ParcelRound's round 6 brought METHOD.md to the method as
  practised, added ADOPTION.md and a gate of its own
  (`tools/check_method.py`), recompiled the templates, and added case studies
  5 and 6. HonestFramework's pin did not move. The Method page also quotes
  Quantum-Film's README, whose pin moved; its quotes still match.
- **Logan's, and staying:** the ratio, the co-authorship statement, and every
  `stated()` line; and the three thread doors that propose.py renders, which
  are P1's, P3's and P4's pages' and Logan's words (propose.py's own control
  needs "workloads" in the Determinism door).
- **The trap:** a statistic still true of case studies 1 to 4 presented as
  the method's record, now that 5 and 6 exist; a dossier that calls the
  method gateless.
- **Its own control, besides the three:** a citation of `CASE-STUDY-7.md`,
  which is not at the pin, is refused by name.

### P3: Quantum-Film and the Film thread

- **Owns:** `site/pages/work_quantum_film.py` and `site/pages/thread_film.py`,
  with the one IBM print as an asset of the Film thread's page.
- **What moved:** Quantum-Film's round 3 ran the shelf's Pauli law on three
  IBM Heron r2 devices, as pre-registered, laid each device's run as film, and
  revised the paper, the poster and the web demo. StoryDocs, which is
  private, moved by one commit.
- **Logan's, and staying:** the Film thread's door.
- **The trap:** a print is image content, which no gate reads. Its caption
  must say which device, which job, and which rule laid it, from the pin, not
  from the file's name. And `docs/HARDWARE-RESULTS.md` says both that the
  devices carry the law's signatures and that all three fall short of their
  noise models' predictions; a page that says the first without the second
  claims more than its source.
- **Its own control, besides the three:** a copy of the print with a text
  chunk added is refused by the build's asset check.

### P4: the Preservation thread

- **Owns:** `site/pages/thread_preservation.py`.
- **What moved:** the organisation's three pinned repositories, by 5, 409 and
  70 commits. Its contributor counts already re-read.
- **Logan's, and staying:** its door, and "@Wally is my discord username".
- **The trap:** the page names people. Each is credited by name, as
  decision 10 says, and no pronoun is written for anyone whose pronouns are
  not stated.
- **Its own control, besides the three:** an email address, and the name
  Wally, each planted in a copy of another page: local-only refuses both.

### What no parcel touches

The seams and the shared pages are the lead's: `site/facts.py`,
`site/render.py`, `site/build.py`, `site/mapgen.py`, `site/style.css`,
`site/data/`, `pins.json`, `sources/`, `site/pages/home.py`,
`site/pages/work.py`, `site/pages/threads.py`, `site/pages/record.py`,
`site/pages/_dossier.py`, `site/pages/_settled.py`, `site/pages/_p5.py`,
`site/pages/front.py`, `site/pages/about.py`, and every document (README,
CLAUDE.md, `docs/`). A stylesheet a parcel needs is a new file of its own
under `site/styles/`. `public/` is generated: parcels rebuild it on their
branches, and at each merge the lead rebuilds it rather than merging its
text.

## Planted faults

Planted faults stay light, as decision 20 has it: "can be light on this
project". This is how they are kept from being found by anything but
reading:

- **The copy.** One commit, with the parcel's own message and parent, whose
  tree is the parcel's plus two plants, with `public/` rebuilt from it. The
  lead runs the full gate on it before dispatch: every stage must pass, so no
  stage points at a plant.
- **The plants** are faults of the kind the gates cannot read: a sentence
  that claims more than its source at the pin, a quote that is true at the pin
  but overtaken by a newer entry, a caption that names the wrong source.
- **The clone.** The verifier works in a clone of its own, under its scratch
  directory, made with `git clone --no-local --single-branch` from a branch
  that holds only `round2`'s history and the planted commit. The parcel's own
  commit is not in it. Its brief puts every other branch and worktree of
  loganw.dev out of bounds until it has reported.
- **The key.** Its SHA-256 goes in the lead's ledger file before that
  verifier is dispatched, and the key itself after the last planted-copy
  verifier has reported. The plants never reach `round2`: the lead merges the
  parcel's own commit, by its SHA.
- **The limit.** A verifier that left its clone for the parcel's own branch
  could find the plants by a diff. Its brief forbids that, and the yield is
  read with that limit: it measures what a verifier finds by reading, as far
  as it keeps to its brief.

This measures what Haiku verifiers catch, beside round 6's Opus verifiers
(ten of ten) and ParcelRound's case study 7's Sonnet verifiers.

## The metrics

Logan asked for totals on parcels, agents, token use and time. They are kept
as ParcelRound's case studies 6 and 7 and HonestHarness's round 1 keep them,
and like case study 6, they count the lead's own session (case study 7 left
it out).

- **In the ledger, as it happens:** every dispatch (the agent, its model as
  requested, the time), and every report (the time, and the runtime's own
  figures: its "tokens", recorded as the agent's context size at the run's
  end, which is what it is, beside its tool uses and duration).
- **By script, at each wave's end and at the round's end:**
  `tools/round_metrics.py` in the ledger reads the session's transcripts. Per
  agent: its model, read from its own transcript; runs; minutes; tool uses;
  messages; output tokens; fresh tokens (input, cache writes and output); and
  cache reads. The lead's own session is counted from the request at
  13:16:10. Totals by class: parcels, verifiers, the lead.
- **By hand, from the ledger:** the wall clock, split between the build phase
  and what came after it, and the planted-fault yield by model. The script
  doesn't make these.
- **In the case study:** the per-agent table, the totals, the verifiers'
  share, the wall-clock split, and the yield by model.

## Time and cost (an estimate, not a measurement)

- P0 and its verifier, about an hour. Wave 1's designs, about half an hour;
  the builds, about an hour; their verifiers, about half an hour. The merges,
  the integration verifier and the push, about an hour. The case study, about
  an hour. Several hours of wall clock in all.
- The cost is read from the transcripts afterwards, never estimated in the
  record.

## What READY means

READY is "a gate, or a stated limit": every property of the work is held by
a gate the verifier has watched fail on a fault it picked itself, or is
stated as a limit where the claim is made, and the verifier's own evading
fault lands inside that limit. "Found nothing" is an acceptable answer.

**The lead's own rule for this round,** not the method's: each verifier has
up to three passes, a re-check scoped to the diff since its previous pass. If
a third pass still finds a wrong answer, the lead records it and asks Logan
before going on. The reason: round 1's front page took eight versions to
READY, and a light round should put a long loop in front of its owner rather
than run it on. The lead re-checks every Haiku finding against the records
before acting on it (decision 35).

## The ledger

At `<repos>/loganw-dev-r2-ledger/`, outside every repository. Its README
holds the rules: one file per author, append only; stamps from `date`; values
from the commands that measured them; three read moments; escalation by the
runtime's messages, the question written in the agent's own file first.
Everything in it will be published, so it holds no absolute path, no secret,
and no address but the contact. At the round's end it is archived in this
repository, beside the case study.
