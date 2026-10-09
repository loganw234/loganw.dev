# Round 2 of loganw.dev: an update round on Sonnet parcels and Haiku verifiers, measured

Written after the round from its ledger, which is archived beside this file
in [round2-ledger/](round2-ledger/), and from the session's transcripts,
which are not published. It covers one round of one project: the site
brought up to the projects it describes, as they stood on 2026-10-08. The
owner asked for it this way: "since this is a lightweight round in terms of
'complexity', utilize Sonnet models for the parcels and Haiku as verifiers.
We have also started to track metrics a bit deeper, keeping totals on
parcels, agents, token use, time, etc."

So this file has two jobs: to say what happened, and to give the round's
totals, measured. It went past a verifier, on Haiku, before it was
committed; the last section says what that verifier found.

Times are local (UTC-7), from the ledger's own stamps, which every author
wrote with `date`, and from the transcript's timestamps for the owner's
words. Commits are named by their short SHAs on the branch `round2`.

## The setting

- **The project.** loganw.dev, Logan W.'s site. Every figure on it is read
  from a repository at a pinned commit, from a committed GitHub snapshot, or
  from the site's own ledger, or is marked as stated, with who said it and
  when; a gate refuses anything else. Round 1 built it, on
  2026-09-29 and 30 (ParcelRound's case study 5).
- **The job.** Between 2026-09-29 and 2026-10-08, seven of the site's pinned
  repositories moved on GitHub: cft-fp256 by 381 commits, ParcelRound by 37,
  Quantum-Film by 171, StoryDocs by 1, and three of the Mercenaries-Fan-Build
  organisation's by 5, 409 and 70. HonestHarness, new, was public. The pages
  still described the projects as round 1's pins had them.
- **The owner's decisions** (SPEC.md, decisions 31 to 36), each through the
  question tool: HonestHarness gets a row on Map & Ledger and a node on the
  map, and its dossier waits until its round 1 lands on main; this file and
  the ledger go in the site's own repository; push when verified; one IBM
  hardware print, on the Film thread's own page (asked twice, below); every
  verifier on Haiku, the lead's work included; and a stated line of his that
  a pin has overtaken may be replaced by a figure read from its source, with
  anything else coming to him.
- **The models,** read from each agent's own transcript: the lead on
  claude-opus-5-5; the four parcels on claude-sonnet-5-5; the eight
  verifiers on claude-haiku-5-5. (Round 1's "sonnet" was claude-sonnet-5:
  the same request resolved to a newer model.)
- **What was new against round 1:**
  - the round's totals kept as it ran: every dispatch and report in the
    lead's ledger file, with the runtime's figures, and a script,
    [round_metrics.py](round2-ledger/tools/round_metrics.py), that reads the
    transcripts;
  - every check on Haiku, the plan's and the lead's included;
  - every parcel designed first and built only on the lead's "go";
  - every parcel's verifier worked on a copy holding two planted faults, in
    a clone of its own that held no other branch;
  - escalation by the runtime's messages, each agent sending a test message
    at the start.

## Timeline

| when | what |
|---|---|
| 13:16 | Logan asks for the round. The lead surveys what moved (`gh api` compare, every pin) and moves the pins in a scratch worktree: three pages refuse, each at its first refusal. |
| 13:32 | Logan's four decisions, through the question tool. |
| 13:40 | The plan's first draft (`6ec5616`); verifier-plan dispatched. |
| 13:53 | P0 committed (`05413b2`): the pins, the snapshot, HonestHarness's row and node. The build had met two more refusals than the trial. The full gate passes on it at 13:58. |
| 14:17 | verifier-plan: NOT READY, eight defects. Two are the owner's to answer. |
| 14:18 | Logan answers them: Haiku for every verifier; his overtaken lines may be read from their sources. |
| 14:22-14:52 | Drafts 2, 3 and 4. verifier-plan's second pass finds 2 defects, its third 2 wrong answers: by the lead's three-pass rule, the third goes to Logan. |
| 14:54 | Logan approves draft 4 (`9f3c894`). |
| 14:55 | verifier-P0 and the four parcels dispatched; the parcels for their designs only. Each test message arrives by 14:56:41. |
| 15:22 | verifier-P0: NOT READY. SPEC.md quoted Logan's request without its last sentence; and "beside the existing prints" could mean Map & Ledger's section headed "The film thread". |
| 15:24 | Logan, asked again: "The Film thread's own page". |
| 15:32 | verifier-P0: READY. |
| 15:39-15:56 | The four designs. P4 needs no new path and gets "go" at 15:42. |
| 15:51 | P4 reports (`1e6b4ec`). Its planted copy passes the full gate; verifier-P4 dispatched at 15:57. |
| 15:59 | The seam commit (`427900e`): nine source paths the designs need. verifier-P0 READY on it at 16:13; "go" to P1, P2 and P3. |
| 16:22 | verifier-P4: NOT READY, both plants found. P4's own commit merged (`4d534df`), with the lead's restates. |
| 16:30-16:34 | P2 (`37d0609`) and P1 (`bef03b0`) report. |
| 17:17 | Their planted copies pass the full gate; verifier-P1 and verifier-P2 dispatched. |
| 17:22 | P3 reports (`583d3eb`); verifier-P3 dispatched at 17:29. |
| 17:43-17:55 | verifier-P1, verifier-P2 and verifier-P3: each NOT READY, each on its two plants. P1, P2 and P3 merged, with the lead's restates. |
| 18:00 | The full gate passes on every parcel merged (`a4a438c`); the keys go into the ledger. |
| 18:03 | The round's entry in the site's own ledger (`9b35773`); the full gate passes on it. |
| 18:08 | verifier-I dispatched on the lead's merges, restates and records. |
| 18:33 | verifier-I: NOT READY, four findings; every merge, made again with `git merge-tree`, is clean. Two of its findings go to Logan, who settles both: About's credits sentence narrowed, and Corrections' fourth gap shown. |
| 18:42 | The lead's fixes (`7f2d51b`); the full gate passes on them. verifier-I's second pass. |
| 18:52 | verifier-I: READY. |
| 18:56 | `main` fast-forwarded to `7f2d51b` and pushed. The deploy's gate and deploy jobs pass; every published file but BUILD is byte for byte the build, and BUILD names `7f2d51b`. |

## What happened

**1. Haiku verifiers caught every planted fault: 8 of 8, each on its first
pass.** Each parcel's copy held two faults of the kinds no stage of the gate
reads. The keys are in [round2-ledger/keys/](round2-ledger/keys/), each
file's SHA-256 recorded in the lead's ledger file before its verifier went
out.

| parcel | the plant | its kind |
|---|---|---|
| P4 | "says all further mods are now built around" the Modkit | a tense its source doesn't have |
| P4 | the organisation, "which austinkregel founded and leads with his collaborators" | a claim about a person, with a pronoun no one stated |
| P1 | cft-fp256's language as "the one atlas-engine's plates are now written in" | a relation no source states |
| P1 | "no step so far has moved a recorded bit" | a sentence its source contradicts |
| P2 | "Across its rounds, its planted faults: ten of ten" | one round's figure as every round's |
| P2 | "The fifth round's case study records" a sixth-round quote | a lead-in naming the wrong source |
| P3 | the results summary quoted without its sentence on the shortfall | a quote cut short |
| P3 | "the device whose run came closest to its noise model's prediction" | a selection reason no source gives |

- Each finding cites the source line its plant contradicts. verifier-P3
  went further than the plant: it showed from the results tables that
  ibm_marrakesh, not ibm_kingston, is nearer its prediction on two of the
  measures.
- **The limit.** All four reports also note that the parcel's design, in
  the ledger, reads otherwise at the planted sentences. verifier-P2 writes
  that it "did not use the design to find them"; the other three don't say
  in which order they read. So the clone closed the route by `git diff`, and
  left the route by the ledger open, which ParcelRound's case study 6 found
  of its own round too ("A verifier that read the design first could have
  found every plant by comparison alone").
- **Beside the plants, real findings:** in P4's work, a count that didn't
  say what it left out and a scope sentence no guard held; in P1's, two
  citations in its own commit message; in P2's, two wrong labels and a
  quote cut short; in P3's, a "half" that is 8 of 17, a README heading
  printed as prose, and a docstring. Each was restated by the lead at its
  merge.
- **Three claims of the verifiers' own were wrong,** and the lead carried
  one of them into the record. Logan's decision 35 has the lead check each
  Haiku finding against the records before acting on it.
  - verifier-plan said cft-fp256's quick budget "no longer" named the GPU's
    photograph; its line 382 still does, and verifier-plan withdrew it ("I
    had read only lines 377 to 380").
  - verifier-P1 said a quote left "a dangling colon" on the page; the page
    has none.
  - verifier-P1 also said P1's commit message cited CONFORMANCE.md lines
    312 and 316 where the quote sat at 317 to 319. P1 was right. The lead
    took the reading without opening the lines, and wrote it into the merge
    message as a correction; verifier-I found it, and the site's ledger now
    corrects it.

**2. The update's real work was text, and it found sentences that had never
been true.** Moving the pins made the build refuse four things: one stated
line of Logan's and three quotes on Verify. Of every fact on the site, 27
read different text by themselves, 5 were gone and 77 new (`public/facts.json`
before and after P0, matched by method and arguments). Every other sentence
still quoted words that stood at the new pins, so every gate passed on
pages that described the projects as they had been. The parcels' designs
then found, in pages round 1 had published and its verifiers had passed:

- ParcelRound's dossier sent a reader to `CASE-STUDY.md` for a timeline,
  timestamps, cited commits and a recount that the file doesn't hold (P2);
- cft-fp256's dossier said `make golden` "needs only Python and, optionally,
  mpmath", where it needs pytest too, and that it compares results against
  `vectors/SHA256SUMS`, which it doesn't, and no gate does (P1);
- the Preservation thread's credits caption set Logan's statement inside a
  sentence that misread it, and a paragraph opened with a full stop (P4).

The site's own ledger lists every correction the round made, in its entry
of 2026-10-08.

**3. The owner's words took more checking than any parcel.** The plan went
past its verifier three times, on 8, 2 and 2 defects, and P0 three times.
Two of the plan's defects were the owner's to settle, and verifier-P0 found
a third: SPEC.md had quoted Logan's request without its last sentence, and
read "beside the existing prints" one way where it could be read another.
Each went back to Logan through the question tool, rather than being
settled by the lead's reading. verifier-I found two more of his to settle:
About's sentence on the Preservation thread's credits, which claimed more
than the thread now does, and Corrections' fourth gap, which the spec names
and the page had left out since round 1. He was asked five times in the
round, and answered each within minutes.

**4. Designing first held the parcels to their files, and moved the seam
to one commit.** Each design listed the source paths its labels would name.
The lead added all nine in one commit, which verifier-P0 checked before any
parcel built on it. P4 needed none, and built 31 minutes before the others.
The designs also corrected their briefs: P4's "mostly by people other than
Logan" was all of them; P1's rows stopped at 2026-09-23, not 09-29; P2's
METHOD.md quotes were 13, 3 of them ParcelRound's; and the brief's
HonestHarness "runs" the methods, where its README says it is "a harness
for running" them, with no code yet.

**5. Escalation by the runtime's messages reached the lead every time.**
All eleven agents sent a test message at the start, and every one arrived.
No agent needed a real escalation: the questions came in designs and
reports, at the moments the briefs set. Two verifiers' runtimes refused
their writes to their own ledger files ("Subagents should return findings
as text"), so their reports are in the lead's file instead.

**6. The lead's slips,** each written in the ledger when it was caught:
- the plan's first draft, with its eight defects;
- Python sent through a Bash heredoc twice, once to write a planted copy's
  key and once to archive the planting scripts; each time its backslashes
  didn't survive (CLAUDE.md trap 8), and each failed before it wrote
  anything;
- the metrics script missed every notification that arrived while the lead
  was busy, which the transcript keeps as an "attachment" record, not a
  "user" one; found mid-round, when two parcels showed fewer runs than they
  had reported;
- three full gates run at once, which slowed the controls stage of each
  from about 3 minutes to between 15 and 25;
- P0's commit subject counts its refusals as two where there were four;
- a verifier's wrong reading of two line numbers, taken without opening the
  lines and written into a merge message as a correction (above);
- the ledger's README forbids any address but the site's contact, and the
  lead's own brief gave the parcels the co-author trailer, with its address,
  to sign their commits with.

## Cost of the round (measured from the transcripts)

**The method,** as case studies 6 and 7 of ParcelRound measured theirs:
- Each agent's tokens are summed from its own transcript, once per message.
  Fresh tokens are input, cache writes and output; cache reads are counted
  apart, and so is output on its own.
- Runs, minutes and tool uses are the runtime's own notifications, one a
  run. The "tokens" a notification gives is the agent's context at the
  run's end (case study 7), so it is shown under that name and summed
  nowhere.
- Each model is read from the agent's own transcript.
- The lead's session is counted from Logan's request, as case study 6 did
  (case study 7 left it out).
- The script is [round_metrics.py](round2-ledger/tools/round_metrics.py). It
  reads the session's transcripts, which are not published, so it shows the
  method and cannot remake the figures from this repository.

**The build phase:** from Logan's request at 13:16:10 to the push at
18:56:43, 341 minutes of wall clock.

| agent | class | model (from its transcript) | runs | minutes | tool uses | messages | output | fresh | cache reads | context at end |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| verifier-plan: plan of record | verifier | claude-haiku-5-5 | 3 | 62 | 259 | 228 | 591 k | 1.9 M | 101.9 M | 829,822 |
| verifier-P0: the lead's P0 | verifier | claude-haiku-5-5 | 3 | 48 | 207 | 203 | 429 k | 1.6 M | 79.1 M | 705,030 |
| P1: cft-fp256 and Determinism | parcel | claude-sonnet-5-5 | 2 | 85 | 382 | 291 | 362 k | 1.9 M | 150.6 M | 861,184 |
| P2: the two methods | parcel | claude-sonnet-5-5 | 2 | 77 | 254 | 204 | 335 k | 1.8 M | 99.9 M | 770,084 |
| P3: Quantum-Film and Film | parcel | claude-sonnet-5-5 | 2 | 117 | 316 | 255 | 383 k | 3.3 M | 125.1 M | 795,829 |
| P4: Preservation thread | parcel | claude-sonnet-5-5 | 2 | 54 | 275 | 210 | 271 k | 871 k | 87.8 M | 639,911 |
| verifier-P4: Preservation thread | verifier | claude-haiku-5-5 | 1 | 26 | 113 | 110 | 249 k | 669 k | 27.0 M | 431,329 |
| verifier-P1: cft-fp256 pages | verifier | claude-haiku-5-5 | 1 | 28 | 140 | 122 | 248 k | 705 k | 31.5 M | 464,341 |
| verifier-P2: the two methods | verifier | claude-haiku-5-5 | 1 | 29 | 121 | 102 | 287 k | 745 k | 28.8 M | 497,654 |
| verifier-P3: Quantum-Film and Film | verifier | claude-haiku-5-5 | 1 | 23 | 123 | 78 | 262 k | 697 k | 21.1 M | 474,208 |
| verifier-I: the lead's integration | verifier | claude-haiku-5-5 | 2 | 32 | 199 | 151 | 329 k | 1.4 M | 51.2 M | 582,995 |
| the lead | lead | claude-opus-5-5 | - | 341 (wall) | 407 | 368 | 391 k | 1.2 M | 174.3 M | - |

| class | agents | runs | agent-minutes | tool uses | output | fresh | cache reads |
|---|---:|---:|---:|---:|---:|---:|---:|
| parcels | 4 | 8 | 334 | 1227 | 1.4 M | 7.8 M | 463.4 M |
| verifiers | 7 | 12 | 249 | 1162 | 2.4 M | 7.7 M | 340.6 M |
| the lead | 1 | - | - | 407 | 391 k | 1.2 M | 174.3 M |
| **all** | **12** | **20** | **583** | **2796** | **4.1 M** | **16.7 M** | **978.3 M** |

- **The verifiers wrote most of the output:** 57.9% of it, against the
  parcels' 32.7% and the lead's 9.4%. In fresh tokens the two were about
  equal, 7.7 M against 7.8 M, as case study 7 found of its own run.
- **Haiku writes more than it reads, against the earlier verifiers.** Each
  parcel verifier's single run wrote 248 k to 287 k output tokens; round
  6's Opus verifiers wrote 45 k to 68 k each (case study 6). Its fresh
  tokens per first run, 0.67 M to 0.75 M, sit near the medians case study 7
  measured on Sonnet and Opus first runs (805 k and 751 k).
- **The checking of the lead's own work** (the plan's verifier, P0's and
  the integration verifier, eight runs in all) used 4.9 M fresh tokens, more
  than any parcel used, and more than the four parcels' verifiers together
  (2.8 M).

## What METHOD.md should say differently (proposed; the owner's to settle)

1. **A pin move needs a reading for currency, which no gate makes.** After a
   move, a quote that still matches can describe the past. This round's
   briefs and verifier lists named it, and it was most of the work. The
   change: the verifier template's list gains "a sentence true at the pin
   but no longer the current truth", for any round that moves a pin.
2. **A planted copy is reachable by comparison through the ledger, too.**
   The clone closed `git diff`; the parcel's design in the shared ledger
   stayed readable. The change: a planted-copy verifier reads the parcel's
   ledger file only after it reports, or the plants go into a copy of the
   design as well.
3. **A smaller model can verify a content round, with the lead's re-check.**
   Four Haiku verifiers caught 8 of 8 plants and found real defects; of the
   twelve reports the verifiers gave before the push, two held claims that
   were wrong, three in all, and the lead carried one into the record.
   The change: where the work is content, verifiers may run on a smaller
   model, and the lead checks each finding against the records before
   acting on it (decision 35's own words).
4. **Read the cost from every record the transcript keeps.** A
   notification's "tokens" is a context size (case study 7), and a
   notification that arrives while the lead works is kept in another kind
   of record. The change: the cost method says both.
5. **Run the gate alone.** Three at once cost each controls stage five to
   eight times its time.

## The round's end

(To be filled after the integration verifier, the push and the live check.)
