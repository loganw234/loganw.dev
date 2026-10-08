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

## What moved

Measured on 2026-10-08 by `gh api .../compare/<pin>...<default branch>` for
every pin in [pins.json](../pins.json). Every pin not listed is identical to
its default branch.

| repository | pin | GitHub's main | commits ahead |
|---|---|---|---:|
| cft-fp256 | `77b8440` | `ab51655` | 381 |
| ParcelRound | `8767e23` | `f42242e` | 37 |
| Quantum-Film | `a7f02db` | `3a73823` | 171 |
| StoryDocs | `673148c` | `8548802` | 1 |
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
seven pins, took a snapshot there, and rendered each page on its own. The
workflow and pin checks passed. Three pages refused, each at its first
refusal:
- Map & Ledger and Work: Logan's word of 2026-09-29, "a revision-7 round is
  under way off main", is held to cft-fp256 at `77b8440`, and the pin moved;
- Verify: its CONFORMANCE.md pattern no longer matches, because the same
  words are rewrapped at `ab51655`.

Every other page rendered, and 17 figures read differently, all by reading
their sources again. So the round's real work is not the build's refusals:
it is the text. The pages describe the projects as they were on 2026-09-29.

## Logan's decisions (2026-10-08)

Through the question tool, verbatim, question and then answer. The lead's
reading of each, where one is needed, follows it, marked as the lead's.

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

And, from the request: **parcels on Sonnet, verifiers on Haiku.** The lead
reads "verifiers" as every verifier in the round: the plan's, P0's, each
parcel's, the integration verifier and the case study's.

## Rules carried into this round

Each is a standing rule, with the date it was given.

- The full gate, `bash verify/run.sh --require-all` under the Python
  `.python-version` names, before every push. A push to main deploys
  (Logan, 2026-09-29).
- Only main is ever pushed, never `git push --all` (CLAUDE.md, trap 17).
- The shared core first, then a verifier on it, then the round (decision
  18). And the lead's seam commits, merges and records go past a verifier
  before main moves (METHOD.md section 7).
- Agents test what they can quickly, and hand large runs back to the lead
  (cft-fp256's owner's rule of 2026-09-29, METHOD.md section 7). Here the
  large run is the full gate, which is the lead's.
- Only a regression or a wrong answer sends work back. Anything else merges
  as a recorded known limit, and a sentence that claims more than is true is
  restated at the merge (METHOD.md section 6, the send-back rule).
- Logan's pronouns are he and his (2026-09-30, trap 18). Anyone else the
  site names is written by name unless their pronouns are stated.
- No published file holds an email address but `logan@loganw.dev` (trap
  14). The name Wally appears only on the Preservation thread's page (trap
  16).
- Other repositories are read only at commits, through `git show`, never
  from their working trees, and no agent switches a branch in them (trap 1).
  Other sessions are working in cft-fp256 and HonestHarness.
- Logan's own words on the site (About, the front page, every `stated`
  figure) change only at his word.

## The shape

1. **This plan goes past a verifier**, and the lead answers its findings in a
   new draft, before Logan approves it.
2. **P0, the lead's,** on the branch `round2`, then a verifier on it.
3. **Wave 1: P1 to P4 in parallel, each designing first.** Each parcel reads
   its pages against the new pins, writes a design, and stops. The lead
   reviews the four designs, then makes one seam commit adding every new
   source path the designs need to `build.SOURCE_PATHS`. That commit goes
   past P0's verifier, scoped to it, and then each parcel gets "go".
4. **Each parcel's verifier** works on a copy of the parcel's work that may
   hold planted faults (below).
5. **Merges onto `round2`**, one at a time, the gate after each, and the
   lead's restates after each.
6. **The integration verifier** on the lead's own work: its merges, made
   again from their parents with `git merge-tree`, its restates, its
   records.
7. **Main moves to `round2`'s tip** after the full gate and the integration
   verifier's READY, and is pushed. The lead checks the live deploy byte for
   byte.
8. **The case study and the archived ledger**, past their own verifier, then
   pushed.

## P0: the lead's

On `round2`, from `43c36a2`. The full gate passes on both sides of it.

- **pins.json:** the seven pins above, moved to GitHub's main; HonestHarness
  added at `b310f82`, read from the owner's clone (`"dir": "HonestHarness"`,
  `"workflows": {}`).
- **The snapshot:** a new one, taken with the new pins, and pins.json pointed
  at it by its exact name.
- **The two refusals**, fixed only as far as the build needs:
  - the revision-7 statement on Map & Ledger is replaced by a figure read
    from cft-fp256's own ledger at its pin, so no word of Logan's is changed
    or needed;
  - Verify's CONFORMANCE.md pattern reads the same words, with any whitespace
    between them. P1 owns the rest of that page.
- **HonestHarness on Map & Ledger**, in the Determinism lane, with ParcelRound
  and HonestFramework: its row (what it is, its state, last verified, the
  agent-credited count, and a check), and its node and edges in
  `site/data/relations.json`, each edge naming the file at the pin that makes
  it. Work lists it with the other projects that have no dossier, since Work
  reads Map & Ledger's rows.
- **ParcelRound's row:** its "check it" link names the method's own gate at
  the pin, `tools/check_method.py`, where it named case study 4.
- **SPEC.md:** Logan's four decisions, and the models, as decisions 31 to 35.
- **The ledger**, at `<repos>/loganw-dev-r2-ledger/`, already exists, with its
  README, the lead's file and the metrics script.

**verifier-P0** reads P0's commits against this plan and the tree, and picks
its own faults.

## Wave 1

Every parcel works in a worktree cut from `round2` at P0's tip. Its first
phase is a design, written in its ledger file, and then it stops. Each design
lists, page by page:
- every sentence or figure that the new pin makes stale or wrong, with the
  source line at the new pin that shows it;
- every new thing at the new pin that the page should say, with its source;
- every repository path its new labels would name that `build.SOURCE_PATHS`
  does not list.

On "go", it builds, rebuilds `public/` on its branch, runs the checks below,
commits, and reports.

### P1: cft-fp256 and the Determinism thread

- **Owns:** `site/pages/work_cft_fp256.py`, `site/pages/thread_determinism.py`,
  `site/pages/verify.py`, `site/pages/corrections.py`, and
  `site/pages/work_cft_rebound.py` (cft-rebound's pin did not move; this
  parcel checks only what that page reads from cft-fp256).
- **What moved:** cft-fp256's ledger runs from revision 7 through the
  certificate plan's steps, the fixes round, the language round, and step 6
  to its close on 2026-10-06, with revision 8's first hardware images. Its ABI
  went from 0.15 to 0.18.
- **The trap:** a dossier row that is still true at the new pin but no longer
  the current truth, such as "Verified" rows that stop at 2026-09-29, or a
  "Where I'd attack first" gap the record now says was closed.

### P2: the two methods

- **Owns:** `site/pages/work_parcelround.py`, `site/pages/work_honestframework.py`,
  `site/pages/method.py` and `site/pages/propose.py`.
- **What moved:** ParcelRound's round 6 brought METHOD.md to the method as
  practised, added ADOPTION.md and a gate of its own
  (`tools/check_method.py`), recompiled the templates, and added case studies
  5 and 6. HonestFramework's pin did not move.
- **The trap:** the Method page's round statistics and the dossier's
  "Verified" section read case studies by line or pattern; a pattern that
  still matches can now describe the method's past rather than its present.

### P3: Quantum-Film and the Film thread

- **Owns:** `site/pages/work_quantum_film.py` and `site/pages/thread_film.py`,
  with the one IBM print as an asset of the Film thread's page.
- **What moved:** Quantum-Film's round 3 ran the shelf's Pauli law on three
  IBM Heron r2 devices, as pre-registered, laid each device's run as film, and
  revised the paper, the poster and the web demo. StoryDocs moved by one
  commit.
- **The trap:** a print is image content, which no gate reads. Its caption
  and source must say which device, which job, and which rule laid it, from
  the pin, not from the file's name.

### P4: the Preservation thread

- **Owns:** `site/pages/thread_preservation.py`.
- **What moved:** the organisation's three pinned repositories, by 5, 409 and
  70 commits. Its contributor counts already re-read.
- **The trap:** the page names people. Each is credited by name, as
  decision 10 says, and no pronoun is written for anyone whose pronouns are
  not stated. Wally stays on this page alone.

### What no parcel touches

The seams and the shared pages are the lead's: `site/facts.py`,
`site/render.py`, `site/build.py`, `site/mapgen.py`, `site/style.css`,
`site/data/`, `pins.json`, `sources/`, `site/pages/home.py`,
`site/pages/work.py`, `site/pages/threads.py`, `site/pages/record.py`,
`site/pages/_dossier.py`, `site/pages/_settled.py`, `site/pages/front.py`,
`site/pages/about.py`, and every document (README, CLAUDE.md, `docs/`). A
stylesheet a parcel needs is a new file of its own under `site/styles/`.
`public/` is generated: parcels rebuild it on their branches, and at each
merge the lead rebuilds it rather than merging its text.

## Planted faults

Planted faults stay light, as decision 20 has it: "can be light on this
project". Each parcel's verifier is given a copy of the parcel's commit that
may hold faults the lead planted: one commit, with the parcel's message,
whose tree is the parcel's plus two plants. The plants are faults no stage of the gate
reads, such as a sentence that claims more than its source, or a label's
words that differ from the source they cite. The key's SHA-256 goes in the
lead's ledger file before that verifier is dispatched, and the key itself
after the last planted-copy verifier has reported. The plants never reach
`round2`: the lead merges the parcel's own commit.

This measures what Haiku verifiers catch, beside round 6's Opus verifiers
(ten of ten) and ParcelRound's case study 7's Sonnet verifiers.

## The metrics

Logan asked for totals on parcels, agents, token use and time. They are kept
as ParcelRound's case studies 6 and 7 and HonestHarness's round 1 keep them.

- **In the ledger, as it happens:** every dispatch (the agent, its model as
  requested, the time), and every report (the time, and the runtime's own
  figures: its "tokens", recorded as the agent's context size at the run's
  end, which is what it is, beside its tool uses and duration).
- **By script, at each wave's end and at the round's end:**
  `tools/round_metrics.py` in the ledger reads the session's transcripts. Per
  agent: its model, read from its own transcript; runs; minutes; tool uses;
  messages; output tokens; fresh tokens (input, cache writes and output); and
  cache reads. The lead's own session is counted too, from the request at
  13:16:10. Totals by class: parcels, verifiers, the lead.
- **In the case study:** the per-agent table, the totals, the verifiers' share,
  the wall clock split between the build phase and what came after it, and
  the planted-fault yield by model.

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

Each verifier has up to three passes. A re-check is scoped to the diff since
its previous pass. If a third pass still finds a wrong answer, the lead
records it and asks Logan before going on.

## The ledger

At `<repos>/loganw-dev-r2-ledger/`, outside every repository. Its README
holds the rules: one file per author, append only; stamps from `date`; values
from the commands that measured them; three read moments; escalation by the
runtime's messages, the question written in the agent's own file first.
Everything in it will be published, so it holds no absolute path, no secret,
and no address but the contact. At the round's end it is archived in this
repository, beside the case study.
