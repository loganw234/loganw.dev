# Round 1: the rest of the site

This is the plan for the parcel round that builds the pages after Home. The
lead (one Claude session) wrote it on 2026-09-29, working under Logan's
decisions in [SPEC.md](SPEC.md).

The method is [ParcelRound](https://github.com/loganw234/ParcelRound). Its
METHOD.md is used as it stood at round 2, with the proposals from case
studies 3 and 4 applied (decision 19; listed below). Verification follows
[HonestFramework](https://github.com/loganw234/HonestFramework).

## The shape

1. **P0**, the shared core. This is the lead's, and it lands and is pushed
   before any parcel starts.
2. **A verifier on P0** before anything is dispatched (decision 18). It
   works from a fresh clone of the committed P0 and picks its own faults.
3. **Wave 1:** P1, P2 and P3 in parallel, each followed by a verifier of its
   own.
4. **Wave 2:** P4 and P5, briefed from what wave 1's ledger taught.
5. **The lead** keeps the seam tests, every merge, `public/`, the documents
   that state the site's claims, and the ledger.

## P0: what every parcel builds on

- **`site/facts.py`** reads every figure.
  - Every figure is logged by `@fact`, so it can be read again.
  - It reads the pins and the snapshot, and refuses by name when it can't read
    a source.
  - It parses ledgers (three heading shapes; anything else is refused).
  - It computes "last verified" and open regressions (definitions in SPEC.md
    section 4).
- **`site/render.py`** holds the page shell (B's header, the navigation with
  unbuilt pages unlinked, the footer listing every pin) and E's inline
  sources. It refuses to print a figure that no fact produced.
- **`site/build.py`** has these modes:
  - build: finds pages by glob, writes `public/`, `facts.json`, `MANIFEST` and `BUILD`;
  - `--check`, `--verify-facts`, `--links`, `--local-only`, `--docs`: the checks;
  - `--control`: one planted fault per check, each of which must be caught.
- **`site/style.css`** plus `site/styles/*.css`, found by glob. The fonts are
  served from the site itself.
- **`site/mapgen.py`** draws the map from `site/data/relations.json`.
- **`site/pages/home.py`** is Home, with its ledger, map, checks, prints and
  "not here" box.
- **`verify/run.sh`**, **`.github/workflows/site.yml`**, README, CLAUDE.md,
  SPEC.md and VALIDATION.md.

**Parcels do not edit these seams:** `facts.py`, `render.py`, `build.py`,
`mapgen.py` (except P2), `style.css` and `pins.json`. If you need a change to
one, ask through `urgent/`. What a parcel adds:

- its page module or modules under `site/pages/`;
- its stylesheet under `site/styles/`;
- its facts, with `@fact`, in its own modules.

**`public/` is generated.** Parcels build and commit it on their branches, so
their gates pass. At each merge the lead resolves any conflict in `public/`
by rebuilding, never by merging the text.

## Wave 1

### P1: Record and Verify

- `record.html`: the dated timeline. It is every entry of every pinned ledger,
  merged, oldest first. Each row gives the date, the repository, the entry's
  title, and a link to the entry at its pin. The count check: the entries
  shown must equal the entries parsed, per repository, and any mismatch is
  refused by name. The page states its framing: the Record is weighted
  towards the three repositories that keep a ledger, which is how the method
  grew (decision 12).
- `verify.html`: "Don't trust this — run one." It gives the checks, cheapest
  first, each with what it costs and what a pass does and does not prove.
  The site's own check is among them (`--verify-facts`). It also states the
  site's limit: the site quotes its sources faithfully, and whether their
  claims are true is their own gates' job.
- **The trap:** `entries()` already refuses a heading it can't date. Don't
  write a second parser. Use it, and add a fact for each entry.

### P2: the map on a phone, and the three Threads

- The map gets a narrow layout: a vertical time axis, swapped in by CSS, with
  no script. On a phone, the map currently opens on its sparse 2025 stretch.
- New nodes: binary-sites (Determinism), and Microscope-Stacker (already on
  the map). nextpnr-xilinx is listed only; place it by its fork date, never
  its first commit, which is upstream's from 2018. Every new edge names the
  file that makes it.
- Three thread pages:
  - Determinism, Film & photography, and Preservation;
  - each has its slice of the map, an account drawn from the repositories,
    and its own door (the Propose page's doors);
  - the Preservation page is the only place Wally appears (decision 16), and
    it credits every other contributor directly, with a link (decision 10).
- **Open for Logan:** which thread StoryDocs belongs to.

### P3: Work, five dossiers

- cft-fp256, Quantum-Film, cft-rebound, HonestFramework and ParcelRound, each
  in the spec's nine sections:
  1. what it is;
  2. what it is not (mandatory);
  3. the contract, quoted;
  4. verified: dated rows linked to ledger entries;
  5. kept failures: two or three, with the commits that fixed them;
  6. test it: cheapest first;
  7. prove it wrong;
  8. connections, from relations.json;
  9. provenance.
- Each dossier gets a plain-text twin, generated, `work/<name>.txt`.
- **Light planted faults** (decision 20). After P3 reports, the lead plants
  two faults in one dossier and keeps the answer key outside the tree and the
  ledger. It is committed in three steps: the plants, then the verifier's
  audit, then the key. Then the plants are removed before the merge.

## Wave 2

- **P4: Corrections and Propose.**
  - The rules of engagement, stated once for the whole site.
  - "Where I'd attack first", drawn from the gaps the record names.
  - The corrections ledger, seeded with verifier-caught failures and marked
    by origin.
  - The signature row: "first outside correction — pending".
  - The Propose page, and its issue templates on this repository: DISPROOF,
    and the three-line proposal.
  - The contact address is `logan@loganw.dev` (decision 14).
- **P5: Method and About.**
  - The Method page states the co-authorship once, in Logan's words (equal
    attribution, decision 9).
  - It gives the round statistics, drawn from ParcelRound's case studies,
    each figure read and cited.
  - The ratio is Logan's statement until measurements exist (decision 8).
  - About: a draft for Logan to approve (decision 14).

## Rules in force for this round

These come from ParcelRound's case studies 3 and 4 (decision 19), and are
applied in every brief.

**The lead**

- The lead's P0 goes past a verifier before any parcel that reads it is
  dispatched.
- The lead arms its watch on the ledger in the same step as its first
  dispatch. It re-arms the watch whenever it expires, keeps its snapshot, and
  runs one watch at a time on files of its own.
- The lead's decisions go in the ledger first, then in the message.
- The lead's fixes to a verifier's findings go back to that verifier, which
  picks its own faults.
- The lead's seam commits and records (VALIDATION entries, commit messages)
  go past a verifier before main moves.
- The lead checks its own tree after every agent. An agent's "what I did not
  do" is a claim like any other.

**Briefs and the ledger**

- Every brief names the agent's own scratch directory. No secrets live in a
  directory an agent is given.
- Every brief states the READY standard before the first pass: a gate, or a
  stated limit.
- Timestamps are substituted from the clock, never typed.
- A parcel's question for the lead goes in `urgent/`.
- When a pause is announced, each agent records where it is.
- Name a control by the property that makes it bite, or run it before the
  brief goes out.
- A trap one round measured goes into the next round's seam as a refusal.

**Verifiers**

- A verifier's list includes the lead's grants and rulings made after
  dispatch, and "check every claim in a comment, doc or commit message".
- A gate that reads source text is a stated limit, not a guarantee. A limit
  is stated by the behaviour it concedes.
- A stated limit is tested: the verifier builds a fault that passes every
  gate, and READY requires that fault to land inside the limit.
- Units, domains and quantifiers are claims too. A figure that crosses into
  the documents from any report carries its definition, or is re-measured.
- Side notes get a step of their own at the end of each wave.
- What is audited is frozen: auditors read a committed SHA, never a tree the
  lead is editing.

**Merges**

- A seam that changes mid-round is checked against every open branch at once.
- The lead may prepare a merge while a verifier works, but the verdict still
  gates main.

## The ledger

The ledger is kept outside every repository, at
`C:\Users\logan\source\repos\loganw-dev-ledger\`:

- one file per author;
- `urgent/` for messages that mean "stop and read this";
- the ParcelRound template, with the timestamp rule added.

At the end of the round, the durable findings go into this repository's
records, and the ledger is archived with its timestamps.

## What READY means

A verifier returns READY when every property its list asks about is one of two
things:

- **held by a gate** that it has watched fail on a fault it picked itself;
- **stated as a limit** in the page or document that makes the claim, where
  the verifier's own evading fault lands inside that limit.

"Found nothing" is an acceptable answer.
