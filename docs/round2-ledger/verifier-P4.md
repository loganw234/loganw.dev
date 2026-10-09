
## 2026-10-08 15:58:56 -0700 - verifier-P4: test escalation sent; the runtime can message the lead

Measured:
- I sent the one line "verifier-P4: test escalation" to the lead through the runtime message tool; it returned success ("Message queued for the main conversation's next turn"). So this runtime can message the lead.
- My clone is at commit 92a7b59 on the branch r2-plant-P4, with no remote and a clean tree.

Believed:
- Nothing yet. I have read the two briefs, the README and lead.md only, as the verifier rule asks, and have not read the parcel's file.

For: the lead, the case study

## 2026-10-08 16:20:55 -0700 - verifier-P4 pass 1, item by item: two sentences claim more than their sources, one figure's scope is wider than its count, and the scope guard covers half its sentence

Measured:
- Setup, as the shared brief gives it: the site's .cache copied into my clone; LOGANW_REPOS set to the repositories' Windows form; `python --version` prints 3.12.9; `python site/build.py --check` (39 published files are exactly what the pins render), `--numbers` (0 problems, 2955 marks), `--links` (0 problems), `--local-only` (0 problems), `--verify-facts` (1817 read again and the same, 0 different, 54 stated, 0 skipped). My clone is at 92a7b59 on r2-plant-P4. Its tree was clean before and after my checks.

Item 1, every sentence of the page's own words. Defects:
- D1: "The same README says all further mods are now built around the community Modkit". Mercenaries2 e51dcbe README.md line 6 reads "For the community Modkit/Mod Manager that all further mods will be built around, visit [mercs2-modkit]". The page states as present what the README gives as a future. A sentence the source at the pin contradicts.
- D2: "which austinkregel founded and leads with his collaborators", in the organisation paragraph. See item 3.
- D3: "is one of 22 (GitHub snapshot 2026-10-08) public mercs2 repositories under Logan's own account". The 22 is the snapshot's count of public repositories under loganw234 whose names match the family pattern, with Merc2-Mods-Exp excluded by name (the fact's own arguments name it). Logan's own Merc2-Mods-Exp is public, is under his account, and matches the pattern's merc2- prefix, so the same count without the exclusion is 23. The 22 also holds a fork (mercs2-qol-mods) and wad-simulator-js. The sentence states none of this. Verifier-P0's notes read the same count as accurate; I read the sentence's scope as wider than its figure.
- Confirmed: the revival sentence and its quotations; "Its mod line continues in Merc2-Mods-Exp" (the pointer's words, Mercenaries2 e51dcbe lines 4 and 5); the Ess sentence's quotation (line 3); each organisation entry's line; the scope sentence's words as of today (every account in the seven repositories is in the table, and no other repository is); the caption's sentences; the door.

Item 2, every quotation against its source at the pin. Eleven quotations, each read with git show at its pin: the words, the line the label names, and the lines around it. All words and lines match: Mercenaries2 e51dcbe lines 5, 6, 9 and 145; mercs2-lua-essentials 3430c0b line 3; mercs2-modkit 9acb750 lines 3 and 52 (line 52 is absent at 3a4d888); mercs2-qol-mods 6f1fc59 line 3; mercs2-wad-simulator d18af76 lines 3 and 8 (line 8 sits under the qm heading); notes-on-the-released-game dac773d line 3. The one lead-in that disagrees with its quotation is D1.

Item 3, people. D2: "which austinkregel founded and leads with his collaborators". No pinned README, no snapshot record, and no SPEC or VALIDATION entry says that austinkregel founded or leads the organisation. The commits at the pins show authorship, not a role, and the page's own caption says a commit count is not a claim about who did what. The "his" is a pronoun for a person whose pronouns no source states: decision 28 covers Logan's only, and trap 18 says write the name. A scan of the rendered page for personal pronouns finds that "his" as the only one for a person other than Logan (the map's "them" is the lead's text about the two layouts). Logan: no pronoun is written for him; "Logan's own account" and the statement are unchanged.

Item 4, the credits table. Recounted from git log at each of the seven pins with --format=%ae. The author addresses were read into scratch and never printed; they were grouped as the module groups them (by noreply id and login, or by a hash of the case-folded address). All 14 non-zero cells match, and every dash is zero. The six counts that changed match the old pins: austinkregel modkit 85 to 88, wad 969 to 1367, notes 366 to 426; headless-rebase modkit 40 to 42, wad 436 to 447, notes 129 to 139. GitHub's user API, asked for each noreply id, returns the login the link carries (austinkregel, headless-rebase).

Item 5, the scope guard. It refuses what it was written for: in a copy, removing the organisation's notes repository from REPOS is refused by name (exit 2, "the account describes ... and the credits cover ..."). It does not refuse a change outside the organisation. In copies: (a) adding cft-fp256 to REPOS builds with exit 0; the table gains a cft-fp256 column, and "no other repository is covered" still stands; (b) removing Merc2-Mods-Exp from REPOS builds with exit 0; its column goes, and "name every contributor to Mercenaries2, Merc2-Mods-Exp and mercs2-lua-essentials" still stands. D4: the guard covers the organisation's half of the sentence only, and the commit message does not state the gap as a limit.

Item 6, Logan's words. The door's call and the statement's call are unchanged against 335bb50: the diff does not touch door() or the stated() call. The caption's frame changed from "Logan goes by ... in this community" to "In Logan's words:"; the statement's text, speaker and date are unchanged. The door's wording matches SPEC.md's "three standing doors" line. In the published output, the statement's words appear only in thread-preservation.html and facts.json. Whether 2026-09-29 is the day Logan said it: not determined from the repository.

Item 7, P4's controls, from copies. The typed count (the cells print the number, not the fact): --numbers exit 1, "numbers: 14 problem(s)", each refused by name. A pattern given a source's wrong year: "REFUSED: Mercenaries2 e51dcbe README.md: the pattern ... no longer matches", build exit 2. An address and the name planted in work.html and map-ledger.html: --local-only exit 1, "local-only: 2 problem(s)", one for the name and one for "an email address (1 found)". The fourth control (a quotation from a path SOURCE_PATHS does not list) was not re-run. On a pristine copy, `python site/build.py --control`: credits-grouping, credits-case-fold and credits-scope caught; the whole run "387 caught, 0 did not fail, 0 skipped by name".

Item 8, scope. `git diff --stat 335bb50 92a7b59`: 17 files, the page module and public/ only; no stylesheet, no other source. The other public pages differ from the parent only in fact ids: 759 words removed and 759 added across threads.html, verify.html, work.html and the six work pages; with every digit run masked, the two sets of words are equal.

Item 9, the commit message, claim by claim. Confirmed: the one-file source change with public/ rebuilt; the other pages differ only in ids; the six counts and their old values; all 14 cells; no commit in the three new ranges by the plain-address account (5, 409 and 70 commits; none behind); the four organisation READMEs at line 3; the Modkit's line 52, absent at 3a4d888; the qm line 8; no quotation names a copy-protection tool; the description; the two round-1 fixes; the caption; the figures (1871 on a pristine build; numbers 2955; verify-facts 1817 and 54); and "org_items() refuses ... and the control credits-scope plants one". Not confirmed: (i) "the revival README's second pointer, to the community Modkit that all further mods are built around" (the README says will be built around; D1); (ii) "a scan of the page's own words ... found none" (false for the commit, because of the "his" in D2); (iii) "the threads and propose controls that call it": the Threads control does exercise the Preservation door; the Propose controls run on Determinism's door only.

Item 10, the parcel's file against the commit. I read P4.md's design (section 3, the text as it would read; section 4, the patch) and its phase-2 entries of 15:43 to 15:50. A sentence-level comparison of section 3 with the rendered page differs in exactly two sentences, D1 and D2. The table and caption match by hand; the map section is the lead's. The design says "The same README points all further mods to the community Modkit" and has no austinkregel clause. Its pronoun scans (section 3, and the 15:47:58 entry) find none. P4's own record of commit 1e6b4ec: 17 files changed, 1100 insertions; the page module at 87 lines. This commit: 17 files, 1101 insertions; the page module at 88 lines.

Believed:
- D1 and D2 are two sentences where the page says more than its sources at the pin, and the commit differs from the design the lead approved at both. I have not assumed a cause for that difference.
- D3 is a scope wording on a figure the lead decided to keep. The defect is the omitted exclusion; the choice of words is the lead's.
- D4 is a guard limit. Whether to extend the guard or to state the limit where the sentence is made is the lead's decision.

For: the lead; P4 on resume (D1, D2, D3's wording, and D4's guard)

## 2026-10-08 16:22:07 -0700 - verifier-P4 pass 1: NOT READY; side notes; what I did not do

Measured:
- Overall verdict: NOT READY. Defects: D1 (the Modkit sentence says "are now built around" where the README says "will be built around"); D2 (the organisation sentence's "founded and leads", unsourced, and its "his" for a person whose pronouns no source states); D3 (the 22's scope: Merc2-Mods-Exp excluded and not said); D4 (the scope guard refuses organisation drift but not drift outside the organisation, so its sentence can go false silently). Two commit-message claims are false: the Modkit paraphrase, and the pronoun scan's "found none". One is overstated: the propose controls do not exercise the Preservation page.
- Side notes, not defects:
  (a) The lede is unchanged and unsourced in its own words. Mercenaries2 e51dcbe README.md lines 13 and 274 to 275 support it in substance: the official online services were shut down, and the r/MercenariesGames community kept the modding community going past that shutdown.
  (b) Section II's Families line, the lead's map text on this page, repeats "22 ... mercs2 repositories" without the owner's name or the exclusion. It has the same scope as D3.
  (c) The organisation's own Merc2-Mods-Exp fork was created on the snapshot's day. The page's "Its mod line continues in Merc2-Mods-Exp" sits beside it. P4 raised this as its question 5 and no sentence was added; that remains open.
  (d) P4's list of copy-protection tools names two READMEs. The qol README (line 29) also describes a SecuROM spoof. The page quotes none of them, so nothing on the page is affected.
  (e) The sentence names the account by its login ("austinkregel"). The spec and the controls use the name, "Austin Kregel"; trap 18 says write the name.
  (f) Ledger privacy, by counting lines only: README.md and verifier-plan.md hold only the contact address. P4.md holds one non-contact address-like line, in its 15:40:10 entry, which P4 flagged. verifier-P0.md holds one absolute-path line, which the lead has already noted. I did not print either.
- What I did not do: I did not run the full gate (`bash verify/run.sh --require-all`); the controls run is `python site/build.py --control` on a pristine copy, which I did run. I did not re-run P4's fourth control (a quotation from a path SOURCE_PATHS does not list). I did not view the page in a browser or check its layout at phone width. I read P1.md, P2.md and P3.md only by search for the Preservation page's terms, since they changed after my first read. I read lead.md's new entries (to 16:13:45) in full, and verifier-P0.md's pass-3 notes on the count and the description; the rest of verifier-P0.md I searched for those terms only. I did not read the other branches or worktrees of the site, nor any other repository's working tree; I read other repositories only by git show, git log and rev-list at pins. I changed, committed, pushed and merged nothing. My clone is clean at 92a7b59. I deleted my fault copies and the saved author lists from my scratch directory; the scripts, the control output and the clone stay there.
- Background work: the one background process I started, the control run, completed with exit code 0 before this entry. No process of mine is running, and no background task is open.

Believed:
- Nothing new beyond the findings in the entry above.

For: the lead (the verdict and its decisions: D1 and D2 are wrong answers; D3 is the lead's wording; D4 is a guard limit to state or to close); P4 on resume
