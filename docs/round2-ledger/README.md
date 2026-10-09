# The round ledger (loganw.dev, round 2)

This is the round's record, while it runs and after it. The plan of record is
`docs/ROUND2.md` in loganw.dev, on the branch `round2`. At the round's end the
ledger is archived with its timestamps beside the round's case study, in
loganw.dev itself (Logan's word, 2026-10-08).

**Everything here will be published.** So no file here holds:
- a secret, or any part of an environment variable's value;
- an email address other than the site's contact, `logan@loganw.dev`;
- an absolute path. A path names the owner's machine. Name every place
  relative to `<repos>` (the directory that holds the owner's clones, and this
  ledger) or `<scratch>` (the scratch root). Your dispatch message defines
  both.

## The rules

**One file per author, append only.** Yours is named in your brief: `lead.md`,
`P1.md`, `verifier-P1.md`, and so on.
- Read every file here, and write only to your own.
- Never edit an entry. Correct one by appending a new entry that says which
  entry it corrects.

**Stamps come from the clock, never from memory.** Write every heading with
`date`:

    printf '\n## %s - <headline>\n\nMeasured: ...\nBelieved: ...\nFor: ...\n' "$(date '+%Y-%m-%d %H:%M:%S %z')" >> <your-file>.md

**Values come from the command that measured them**: SHAs, counts, times.
Never type one.

**Read the whole directory at three moments.** They are the floor, whatever
else brings news:
1. before you start;
2. before you design anything that touches a file your brief calls shared
   or forbidden;
3. before you write your report.

**Write an entry when it would change another agent's work, or the lead's.**
That means:
- environment facts;
- a brief that turned out wrong, the moment you find it;
- a finding about shared code.

Do not write progress or plans; a ledger full of status is one nobody reads.
Mark which claims you **measured** and which you only **believe**.

**Escalation.** Write the question in your own file first, then message the
lead and wait for its answer. If your runtime cannot message, stop, and make
the question your report: the lead resumes you with the answer. Never hold a
problem back for your final report.

**The test escalation.** When you start, send the lead one line, "<your
name>: test escalation", if your runtime can message. Say in your file
whether it could.

**The lead's messages.** Every message the lead sends you is in `lead.md`
first, and its decisions are there before they reach you.

**Verifiers** read only `lead.md` and this README until they have formed their
own view of the work. After that, they read the parcel's file to check its
claims.

**Planted faults.** A verifier may be given a copy of a parcel's work that
holds faults the lead planted. The key's SHA-256 goes in `lead.md` before that
verifier is dispatched. Keys, and any description of their plants, stay out of
this ledger until the last planted-copy verifier has reported.

**Your scratch directory** is named in your brief, under `<scratch>`. Put
everything you make outside your worktree there, and nowhere else.

**If a pause is announced**, write an entry saying exactly where you are
before you stop: what is committed, what is half done, what you were about to
do.

**Before you report**, stop every background process of your own: watches,
servers, long runs. Say in your report that you did.

## What the lead records for the round's metrics

Logan asked for the round's totals to be kept: parcels, agents, token use and
time. So the lead records, in `lead.md`:
- each dispatch: the agent's name, its model as requested, and the time;
- each report: the time, and the runtime's own figures for the run. The
  runtime's "tokens" figure is the agent's context size at the run's end, not
  the tokens it used (ParcelRound's case study 7), so it is recorded under
  that name, beside its tool uses and duration.

Token use is counted from the transcripts, by script, at each wave's end and
at the round's end, the lead's own session included. The script is
`tools/round_metrics.py`. Each model is named from the agent's own transcript.

## Entry format

    ## <date time zone> - <one-line headline>

    Measured: ...
    Believed: ...
    For: <who this is likely to matter to, or "anyone">
