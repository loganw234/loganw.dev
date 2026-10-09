# Brief: verifier-P0 (the lead's P0 of round 2)

Read `briefs/_verifier.md` first; it holds everything every verifier is
given. This is what is yours.

## What to verify

P0, the lead's own work, on the branch `round2`, against `docs/ROUND2.md`'s
"P0" section (the draft Logan approved, at the tip the dispatch message
names) and against the tree. P0 is commit `05413b2`, which wrote SPEC.md's
decisions 31 to 35. The plan's later drafts (`b6c7560`, `10b6b17` and the
tip) restate decision 35 and add decision 36, from Logan's answers of
14:18; they are the lead's records too. Read `git show 05413b2` and
`git diff 05413b2 <the tip> -- docs/SPEC.md`, and the commits' messages:
every sentence in a message is a claim too.

It is the lead's work, so it goes past you like a parcel's (decision 18;
METHOD.md section 7). The lead's fixes to your findings come back to you,
and you pick your own faults, not the fix's author's.

## Specific things to attack

1. **The pins and the snapshot.** Each pin in `pins.json` is the commit the
   plan names, and GitHub's main today (`gh api
   repos/<owner>/<name>/commits/<branch> --jq .sha`). The snapshot
   `sources/github-2026-10-08-1345.json` recorded each pin's full SHA, every
   workflow of every pinned repository, and no private repository the site
   does not read. HonestHarness's entry reads from the owner's clone, with no
   workflows.
2. **The replaced statement.** Map & Ledger's cft-fp256 cell now reads the
   ledger's newest entry (`home.newest_date`, `home.newest_subject`). Is the
   last heading of cft-fp256's `docs/VALIDATION.md` at `ab51655` really its
   newest entry? What does the cell print, and is it true? Build a ledger
   copy where it would be wrong (an older heading appended last, a heading
   with no colon) and see whether the facts refuse it or print something
   false. Was any word of Logan's changed rather than removed?
3. **Verify's three patterns** (`site/pages/verify.py`). Each quotes words
   that stand at `ab51655`. Is any quote now cut so that the sentence around
   it says something the source does not? (The `gate` budget is quoted only
   to "lint, formal".)
4. **HonestHarness's row, node and edges.** Every word of the row against
   the README at `b310f82`; each edge's kind (`site/data/relations.json`'s
   `kinds`) against what the README's words say. Is "was distilled into"
   true of cft-fp256 and HonestHarness, as the README puts it?
5. **ParcelRound's check**, `python tools/check_method.py`: does that file
   exist at `f42242e`, and is it a check a reader can run, as the
   HonestFramework row's is?
6. **`build.SOURCE_PATHS`.** The two paths added are the only ones P0's new
   labels name, and each names a file at its pin.
7. **SPEC.md's decisions 31 to 36** against Logan's words in `lead.md`'s
   entries of 13:3x and 14:18, word for word; and whether anything the lead
   reads into them is set apart from his words.
8. **The gate.** Run `bash verify/run.sh --require-all` yourself, from
   clean, and read its log.
9. **The commit message's claims**, one by one.
10. **Anything else.** Tell the lead what it did not think to ask.
