"""Corrections: the site-wide rules of engagement for proving a claim on this
site wrong (docs/SPEC.md, "Corrections (global page)"; briefs/P4.md).

The rules of engagement are Logan's, from the spec, printed through
facts.stated(). The "where I'd attack first" gaps are the spec's too, so their
names are Logan's (plain text here); the sentence beneath each is cft-fp256's,
quoted at its pin. The corrections ledger is seeded from this site's own
record, docs/VALIDATION.md, read through facts.own_prose()/own_entry() and
facts.own_commit() - never typed from memory. Its newest row is the first read
from another repository's ledger: cft-fp256's issue 1 (docs/SPEC.md, decision
49), every quote and figure in it read from that one entry at the pin, and a
few typed words joining them (III, below).
"""
import copy
import re

import facts
from facts import V, Refusal, fact, pin
from pages import _dossier
from render import L, plain, render

PAGE = {"file": "corrections.html", "nav": "Corrections",
        "title": "Corrections — loganw.dev",
        "description": "The rules for proving a claim on this site wrong, the gaps the record already names, "
                       "and a selection of the corrections so far, with where the rest are recorded."}

DISPROOF_URL = "https://github.com/loganw234/loganw.dev/issues/new?template=disproof.yml"
LEDGER_PATH = "docs/VALIDATION.md"


def S(text, **kw):
    return facts.stated(text, "Logan", "2026-09-29", **kw)


# ---------------------------------------------------------------------------
# I. The rules of engagement, stated once for the whole site.
# ---------------------------------------------------------------------------

def engagement():
    items = [
        [S("A disproof is a command, an input and the bit that differs, or a clause citation.")],
        [S("Documentation claims count: a misquotation is a disproof.")],
        [S("The venue is an issue on this repository, through the DISPROOF form, or an email to "
           "logan@loganw.dev."),
         " ", L(DISPROOF_URL, "Open the DISPROOF form"), "."],
        [S("Every filing gets a dated disposition: fixed, with the finder named, or refused by name.")],
        [S("It is acknowledged in days, and given its disposition when it's true.")],
        [S("There is no bounty: the entry is the reward.")],
    ]
    return "<ul class=\"plain\">%s</ul>" % "".join("<li>%s</li>" % render(i) for i in items)


# ---------------------------------------------------------------------------
# II. "Where I'd attack first" - the gaps the record already names, quoted at
# cft-fp256's pin. The names are the spec's (Logan's); the quoted sentences
# are cft-fp256's, re-read at its pin 19de866 in round 3: none is closed.
# (Round 2 read them at ab51655. docs/COMPLIANCE.md has no commit between the
# two pins; the other three sentences are unchanged and moved only by lines;
# and nothing in the ledger's new entries gives a second card, a different
# refusal cap or a different tree shape.) The
# spec's first, "clause readings in COMPLIANCE", was left out in round 1,
# since docs/COMPLIANCE.md calls none of its readings open to dispute. Round 2
# found that its own rows say how some clauses are met by a mechanism of its
# choosing, and Logan chose to show it, with that evidence: "Show it, with
# its evidence" (docs/SPEC.md, decision 38). Its quotes are rows 9.3 and 9.4.
# ---------------------------------------------------------------------------

def attack_first():
    P = facts.prose
    items = [
        ["Clause readings in COMPLIANCE: clause ",
         P("cft-fp256", "docs/COMPLIANCE.md", r"^\| (9\.3) \| getBinaryRoundingDirection,", num=True), ", “",
         P("cft-fp256", "docs/COMPLIANCE.md",
           r"^\| 9\.3 \| [^|]* \| (yes \(contexts\), with the mechanism being a context object that CARRIES the "
           r"rounding attribute rather than five separately named calls):"),
         "”; and clause ",
         P("cft-fp256", "docs/COMPLIANCE.md", r"^\| (9\.4) \| sum, dot,", num=True), ", “",
         P("cft-fp256", "docs/COMPLIANCE.md",
           r"^\| 9\.4 \| [^|]* \| (yes - over a contractual tree, where the clause leaves the order to the "
           r"implementation) \|$"),
         "”."],
        ["Cross-device determinism: ",
         P("cft-fp256", "docs/DETERMINISM.md",
           r"(What no second card carrying this\s+tile has yet shown is the cross-DEVICE half of the promise)"),
         "."],
        ["The transcendental refusal cap: ",
         P("cft-fp256", "docs/TRANSCENDENTALS.md", r"^\*\*(Reaching the cap is loud)\.\*\*"),
         "."],
        ["The reduction tree's shape: ",
         P("cft-fp256", "docs/HOSTAPI.md",
           r"(The tree shape is part of the contract, not an implementation detail)"),
         "."],
    ]
    return "<ul class=\"plain\">%s</ul>" % "".join("<li>%s</li>" % render(i) for i in items)


# ---------------------------------------------------------------------------
# III. The corrections ledger: date | claim | found by | disposition | fix.
# Every figure and quote in a cell is read, never typed; a few typed words, such
# as "fixed", join them. Three rows are this site's own corrections,
# read from its own ledger; the fourth is cft-fp256's issue 1, read from
# cft-fp256's ledger at its pin (below). The signature row is Logan's words,
# appended last.
# ---------------------------------------------------------------------------

def _own_entry_at(path, heading):
    t, ents = facts.own_entries(path)
    e = next((e for e in ents if e["title"] == heading), None)
    if e is None:
        raise Refusal("this site's %s has no entry headed %r" % (path, heading))
    return e


@fact
def own_ledger_date(path, heading):
    """A site-ledger entry's own date: the same re-derivation _dossier.py's
    ledger_date() does for a pinned ledger, through facts.own_entries()
    rather than a second parser."""
    e = _own_entry_at(path, heading)
    return V(e["date"], facts.own_src(path, e["line"], "the entry's own date"), raw=e["date"], num=True)


WAVE1_HEADING = ("2026-09-29 - wave 1's verifier findings, folded from the round ledger; "
                 "a cited commit must be on main")


def _row(claim_pattern, found_pattern, fix_sha, fix_what):
    OP = facts.own_prose
    date = own_ledger_date(LEDGER_PATH, WAVE1_HEADING)
    claim = [OP(LEDGER_PATH, claim_pattern), "."]
    found = [OP(LEDGER_PATH, found_pattern)]
    disp = ["fixed"]
    fix = [facts.own_commit(fix_sha, fix_what)]
    return [date], claim, found, disp, fix


# The fourth row (docs/SPEC.md, decision 49) is the first read from another
# repository's ledger: cft-fp256's issue 1, found by "a clean-room audit of
# loganw234/muse-softfloat". Every quote and figure is read from the one entry
# that records it, found by its heading's whole text and never by line, and
# entry_prose looks only between that entry's heading and the next, so a quote
# cannot come from a second entry: a pattern that matches only elsewhere is
# refused, saying where. The date is the entry's own, read from the same
# heading, ISSUE1, as every other cell; nothing else ties it to them
# (verifier-P3's first pass, round 3).
#
# The row says what the entry says and no more.
#   - "found by" is the entry's own words. The row never calls the report an
#     outside one (the entry's heading does, and so does the signature row,
#     which stays pending), and never says who filed it: that is GitHub's
#     record, which no pin holds.
#   - "fixed" rests on the fix cell, whose commit is read from the entry's
#     "merged as" line and shown to be a merge the pin descends from. Beside it
#     are the entry's own line on what the fix moved (8 published records) and
#     two of its known limits. cft-fp256's CONFORMANCE.md calls the tree "a
#     minor step: cases added, none moved", and no file at the pin records a
#     profile step for issue 1's fix (the step to 3.1 it records was on
#     2026-10-13); so the row never says the published record stood
#     unchanged, and never says the profile moved (P1's finding, in round 3's
#     ledger). check_row_words holds the words, and only the words.

CFT = "cft-fp256"
CFT_LEDGER = "docs/VALIDATION.md"
ISSUE1 = ("2026-10-30 - issue 1, the first outside report: exp2m1(emax + 1) toward zero raised overflow, in "
          "the golden model, the C, the vectors and the WebAssembly module; the MPFR oracle's table-9.1 pool; "
          "the module stale since 2026-10-22 (the lead; verifier VX1)")
ISSUE1_CLAIM = (r"^- (At x = emax \+ 1, under roundTowardZero and roundTowardNegative, exp2m1 returned the "
                r"largest finite, which is right, with overflow \| inexact \(0x14\), which is wrong)\.")
ISSUE1_FOUND = (r"from (a clean-room audit of loganw234/muse-softfloat \(binary16/32/64\), cross-tested "
                r"against this library and an exact arbiter)\.")
ISSUE1_FIX = r"^\*\*The fix\*\*, branch [\w.-]+ from [0-9a-f]{7,40}, merged as ([0-9a-f]{7,40}):"
ISSUE1_MOVED = (r"(The 8 that change are the rtz and rdn transcendental sets of each format, each by exactly "
                r"one record, exp2m1\(emax \+ 1\): the same value, flags 20 to 16\. The unfixed model's 72 rtz "
                r"and rdn sets equal the committed record, so those 8 records are the published ones moving)\.")
ISSUE1_ORACLE = r"^- (the oracle is only as wide as its pools):"
ISSUE1_COUNTER = r"^- (no test pins the neighbour counter at the new branch)\."
ISSUE1_FIX_WHAT = ("the merge of fix-exp2m1, which the entry says brought issue 1's fix in; the pin descends "
                   "from it, and it has two parents")
# Words the row never prints (check_row_words): the lexical edge of "says no more
# than the entry". A reader's inference in other words is not seen.
ROW_REFUSES = ("outside", "profile", "none moved")

_ENTRIES = {}


def _pinned_entry(name, path, heading):
    """One entry of a pinned ledger, found by its heading's whole text (what
    follows "## "): (the ledger's text, the entry). By line, a pin that moves
    a ledger's header returns another entry, silently - cft-fp256's header
    grew by three lines at this round's pin move, and CLAUDE.md's trap 15 is
    the same fault in this site's own ledger. By heading, the same entry is
    found, or the build refuses by name."""
    key = (name, path, pin(name).full)
    if key not in _ENTRIES:
        _ENTRIES[key] = facts.entries(name, path)
    text, ents = _ENTRIES[key]
    hits = [e for e in ents if e["title"] == heading]
    if len(hits) != 1:
        raise Refusal("%s %s: %d entries are headed %r; a cited entry needs exactly one"
                      % (name, path, len(hits), heading[:70]))
    return text, hits[0]


@fact
def pinned_entry_date(name, path, heading):
    """A pinned ledger entry's own date, cited at its heading: what
    _dossier.ledger_date() reads, found by the heading instead of a line."""
    p = pin(name)
    _, e = _pinned_entry(name, path, heading)
    return V(e["date"], p.src("file", "%s:%d" % (path, e["line"]), "the entry's own date (%s)" % e["how"],
                              path, e["line"]), raw=e["date"], num=True)


def _in_entry(name, path, heading, pattern):
    """The one match of pattern between an entry's heading and the next:
    (match, line, entry). A pattern that matches only in another entry is
    refused, saying where it did match."""
    text, e = _pinned_entry(name, path, heading)
    rx = re.compile(pattern, re.M)

    def line_of(m):
        return text.count("\n", 0, m.start(1)) + 1
    ms = list(rx.finditer(text, e["start"], e["end"]))
    if not ms:
        elsewhere = [line_of(m) for m in rx.finditer(text)]
        raise Refusal("%s %s %s: the pattern %r does not match within the entry dated %s (line %d)%s"
                      % (name, pin(name).short, path, pattern, e["date"], e["line"],
                         "; it matches only outside it, at line %s" % ", ".join(map(str, elsewhere))
                         if elsewhere else ""))
    if len(ms) > 1:
        raise Refusal("%s %s %s: the pattern %r matches %d times within the entry dated %s, at lines %s; make it "
                      "match once" % (name, pin(name).short, path, pattern, len(ms), e["date"],
                                      ", ".join(str(line_of(m)) for m in ms)))
    return ms[0], line_of(ms[0]), e


@fact
def entry_prose(name, path, heading, pattern, num=False):
    """facts.prose(), inside one entry of a pinned ledger: the file, the line
    and the words, with the pattern matching exactly once between that
    entry's heading and the next."""
    p = pin(name)
    m, line, e = _in_entry(name, path, heading, pattern)
    quoted = facts.md_plain(m.group(1))
    return V(quoted, p.src("file", "%s:%d" % (path, line), "in the entry dated %s" % e["date"], path, line),
             raw=quoted, num=num)


def _fix_commit(name, sha, what):
    """The commit an entry says merged its fix: it exists in the repository
    and the pin descends from it (_dossier.kept_failure), and it is a merge,
    as the entry says."""
    v = _dossier.kept_failure(name, sha, what)
    if len(pin(name).git("rev-list", "--parents", "-n", "1", sha).split()) < 3:
        raise Refusal("%s: %s is not a merge commit, and the entry says the fix merged as it" % (name, sha))
    return v


@fact
def entry_fix(name, path, heading, pattern, what):
    """The commit an entry names as the one its fix merged as, read from the
    entry ("merged as <sha>") and never typed, then shown by _fix_commit."""
    m, line, e = _in_entry(name, path, heading, pattern)
    sha = m.group(1)
    v = _fix_commit(name, sha, what)
    return V(sha, v.src, raw=sha, num=True)


def check_row_words(texts):
    """Refuse the row if a cell's text holds one of ROW_REFUSES as written, in
    any case. They keep to the trap docs/ROUND3.md names for this row: a "found
    by" that reads as an outside finder's, and a "fixed" that claims more than
    the entry does, such as a profile step. The third is CONFORMANCE.md's own
    quote, which belongs to the dossier. Lexical, so a stated limit: the same
    words with another space between them, or other words, pass."""
    text = " ".join(texts).lower()
    for w in ROW_REFUSES:
        if w in text:
            raise Refusal("the corrections row for cft-fp256's issue 1 prints %r: it says what its entry says and "
                          "no more, and so neither reads as an outside finder's nor says the profile moved "
                          "(docs/SPEC.md, decision 49)" % w)


def issue1_row():
    H = ISSUE1
    date = pinned_entry_date(CFT, CFT_LEDGER, H)
    claim = [entry_prose(CFT, CFT_LEDGER, H, ISSUE1_CLAIM), "."]
    found = [entry_prose(CFT, CFT_LEDGER, H, ISSUE1_FOUND)]
    disp = ["fixed; the entry also records “", entry_prose(CFT, CFT_LEDGER, H, ISSUE1_MOVED),
            "”, and, among its known limits, “", entry_prose(CFT, CFT_LEDGER, H, ISSUE1_ORACLE), "” and “",
            entry_prose(CFT, CFT_LEDGER, H, ISSUE1_COUNTER), "”."]
    fix = [entry_fix(CFT, CFT_LEDGER, H, ISSUE1_FIX, ISSUE1_FIX_WHAT)]
    row = ([date], claim, found, disp, fix)
    check_row_words([plain(cell) for cell in row])
    return row


def ledger_rows():
    return [
        _row(r"it found that (the Record's link to each entry, the one a\s+reader clicks, was checked by "
             r"nothing\. A link one line off passed every\s+stage)",
             r"\*\*(verifier-P1)\*\* \(Record and Verify\):",
             "5128ce6", "verifier-P1's finding on d474080: the Record's own per-row entry link was checked "
                        "by nothing; fixed so the link and its check read one href"),
        _row(r"(verify\.html stated details of cft-fp256's contract in its\s+own words, outside any quote)",
             r"\*\*(verifier-P1)\*\* \(Record and Verify\):",
             "5128ce6", "verifier-P1's finding on d474080: unquoted contract prose on verify.html; fixed at "
                        "5128ce6, two of its three sentences cut and one quoted (the wave 1 entry, and its "
                        "correction by verifier-seam). The one more such sentence verifier-P1 found on "
                        "5128ce6 is a further finding, fixed at 1e21d8e"),
        _row(r"it found that (the `credits-grouping` control never exercised\s+case-folding\. A one-token "
             r"change to `account_of` passed that control and\s+broke the page)",
             r"\*\*(verifier-P2)\*\* \(the map on phones, and the Threads\):",
             "6c163dd", "verifier-P2's finding on 137157f: credits-grouping's only fixture never exercised "
                        "case-folding; P2's fix, squash-merged to main as 6c163dd (not bdbac1f, which main "
                        "does not hold)"),
        issue1_row(),
    ]


SIGNATURE = ("first outside correction — pending — this row is here so you can watch me remove it")


def ledger_table():
    head = ("<thead><tr><th>date</th><th>claim</th><th>found by</th><th>disposition</th><th>fix</th></tr>"
            "</thead>")
    body = []
    for date, claim, found, disp, fix in ledger_rows():
        body.append('<tr><td class="d">%s</td><td>%s</td><td>%s</td><td>%s</td><td class="p">%s</td></tr>'
                    % (render(date), render(claim), render(found), render(disp), render(fix)))
    body.append('<tr class="signature"><td colspan="5">%s</td></tr>' % render([S(SIGNATURE)]))
    return '<div class="table-wrap"><table>%s<tbody>%s</tbody></table></div>' % (head, "".join(body))


LEDGER_CAP = ("A selection, not every finding. The older rows are this site's own corrections: plain instances, "
              "early in the site's first round, where a single fix commit answers a single finding, each read "
              "from docs/VALIDATION.md's own entry and checked against this site's own history; the rest of "
              "that entry, and everything since, is in that ledger itself. The newest row is cft-fp256's: each "
              "quote and figure in it is read from one entry of cft-fp256's own ledger at its pin, joined by a "
              "few typed words, and its fix commit is checked against cft-fp256's history at that pin. The rest "
              "of that record is in cft-fp256's ledger.")


def render_page(ctx):
    return (
        '<div class="measure"><p class="lede">Every rule below is site-wide, stated once, and holds for a '
        'sentence, a figure or a document alike.</p></div>'
        '<h2><small>I</small>Rules of engagement</h2>%s'
        '<h2><small>II</small>Where I’d attack first</h2>'
        '<div class="measure"><p>The gaps the record already names, at cft-fp256’s own pin:</p></div>%s'
        '<h2><small>III</small>The corrections ledger</h2>%s<p class="cap">%s</p>'
        % (engagement(), attack_first(), ledger_table(), LEDGER_CAP)
    )


# cft-fp256's pin of round 2: a commit its history holds that the pin of round 3
# descends from, and that the entry's fix (merged after it) is not part of.
OLD_PIN = "ab51655"


def _issue1_controls():
    """The controls for issue 1's row (docs/ROUND3.md, P3). Each plants a
    fault where the check must see it, in a copy of the built page or in
    memory, never in the worktree; render.render() passes a plain string
    through unchanged, so a typed figure is only the numbers stage's to refuse."""
    import json
    import pathlib
    import shutil
    import tempfile

    import build

    out = []

    def refused(name, what, fn, must):
        try:
            fn()
            out.append((name, False, "%s passed" % what))
        except facts.Unavailable:
            raise
        except Refusal as e:
            out.append((name, must in str(e), "%s: %s" % (what, e)))

    # 1 and 2: in a copy of public/, a figure typed by hand where the row's date
    # was, and a label naming a path build.SOURCE_PATHS does not list.
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        shutil.copytree(build.PUBLIC, root, dirs_exist_ok=True)
        data = json.loads((root / "facts.json").read_text(encoding="utf-8"))
        page = root / PAGE["file"]
        t = page.read_text(encoding="utf-8")
        date_rec = next((r for r in data["facts"] if r["method"] == "pages.corrections.pinned_entry_date"), None)
        claim_rec = next((r for r in data["facts"] if r["method"] == "pages.corrections.entry_prose"
                          and r["args"]["pattern"] == ISSUE1_CLAIM), None)
        if date_rec is None or claim_rec is None:
            out.append(("issue1-typed-date", False, "public/facts.json has no issue 1 row; run python site/build.py first"))
        else:
            planted = re.sub(r'<span class="fig" data-f="%d">[^<]*</span><span class="src" data-f="%d">.*?</span>'
                             % (date_rec["id"], date_rec["id"]), "2026-10-29", t, count=1)
            if planted == t:
                out.append(("issue1-typed-date", False,
                            "could not plant: the page has no mark for fact %d" % date_rec["id"]))
            else:
                page.write_text(planted, encoding="utf-8", newline="\n")
                found = [f for f in build.check_numbers(root)[0] if PAGE["file"] in f and "2026-10-29" in f]
                out.append(("issue1-typed-date", bool(found),
                            "the row's date typed by hand where its fact was: %s" % (found[0] if found else "passed")))
                page.write_text(t, encoding="utf-8", newline="\n")
            claim_rec["where"] = claim_rec["where"].replace(CFT_LEDGER, "docs/NOTES.md")
            (root / "facts.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8",
                                             newline="\n")
            found = [f for f in build.check_numbers(root)[0] if "docs/NOTES.md" in f]
            out.append(("issue1-label-path", bool(found),
                        "the claim's label naming a path SOURCE_PATHS does not list: %s"
                        % (found[0] if found else "passed")))

    # 3: a pattern given words its source does not have (the claim, with "wrong" changed to "right").
    refused("issue1-old-words", "the claim pattern given other words",
            lambda: entry_prose(CFT, CFT_LEDGER, ISSUE1, ISSUE1_CLAIM.replace("which is wrong", "which is right")),
            "does not match within the entry")

    # 4: the fix commit read against a pin that does not descend from it. The
    # real code path (_fix_commit, which runs _dossier.kept_failure), with
    # cft-fp256's Pin swapped in memory for a copy at the pin of round 2.
    sha = _in_entry(CFT, CFT_LEDGER, ISSUE1, ISSUE1_FIX)[0].group(1)
    _fix_commit(CFT, sha, ISSUE1_FIX_WHAT)          # at the pin of this round it passes
    real = pin(CFT)
    try:
        old = copy.copy(real)
        old.full = real.git("rev-parse", "--verify", "--quiet", OLD_PIN + "^{commit}").strip()
    except Refusal:
        raise facts.Unavailable("%s has no commit %s in %s" % (CFT, OLD_PIN, real.dir))
    old.short, old._anc, old._memo = OLD_PIN, None, {}
    facts._PIN[CFT] = old
    try:
        refused("issue1-fix-not-in-pin", "the entry's fix commit %s read against cft-fp256's pin %s" % (sha, OLD_PIN),
                lambda: _fix_commit(CFT, sha, ISSUE1_FIX_WHAT), "is not part of the history the pin")
    finally:
        facts._PIN[CFT] = real
    # ...and a commit the pin descends from that is no merge: 25d5b8d2, the fix
    # branch's own first commit, which the entry names (verifier-P3: no control
    # had exercised the merge check).
    refused("issue1-fix-not-a-merge", "the fix branch's own commit 25d5b8d2, which is no merge",
            lambda: _fix_commit(CFT, "25d5b8d2", ISSUE1_FIX_WHAT), "is not a merge commit")

    # 5: a cell whose words are in another entry (the one before, on verifier VM2F1's note).
    refused("issue1-two-entries", "a pattern whose words are in the entry before",
            lambda: entry_prose(CFT, CFT_LEDGER, ISSUE1,
                                r"(verifier VM2F1 noted that the golden stage's time was not shown)"),
            "it matches only outside it")

    # 6: the row's words. The entry's own heading reads "the first outside
    # report"; a cell that quotes it, or says the profile moved, is refused.
    m = _in_entry(CFT, CFT_LEDGER, ISSUE1, r"^## \d{4}-\d{2}-\d{2} - issue 1, (the first outside report):")[0]
    refused("issue1-row-words", "a cell quoting the entry's own heading words",
            lambda: check_row_words([facts.md_plain(m.group(1))]), "prints 'outside'")
    refused("issue1-row-words", "a cell saying the profile moved",
            lambda: check_row_words(["fixed; the profile moved to the next minor step"]), "prints 'profile'")
    return out


def controls():
    """1. A row with a typed cell (briefs/P4.md control 1): a hand-typed date
    beside a row's real, read one must be refused by the numbers stage, by
    name, on a copy of the built page - the same shape verify.py's own
    "unsourced-sentence" control demonstrates. A typed cell that carries no
    numeral the numbers stage reads (a name such as "verifier-P1", whose
    digit follows a letter), outside any mark, is not something any gate
    here can see; that is the site-wide limit CLAUDE.md and the
    README state (the numbers stage sees numerals and the number words it
    lists, not prose), and it is exactly the class of defect wave 1's
    verifiers caught only by reading every sentence - the reason this
    ledger's own rows exist. Text typed over a cell's existing mark is
    caught, digit or not: the numbers stage refuses a mark whose text isn't
    its own fact's (verifier-P4's side note, 2026-09-30).
    2. A fix commit main doesn't hold must be refused, and so must a
    one-character mutation of a real one (briefs/P4.md control 2).
    3. Issue 1's row, read from cft-fp256's ledger (docs/SPEC.md, decision
    49): _issue1_controls() below."""
    import pathlib
    import shutil
    import tempfile

    import build

    out = []
    page = build.PUBLIC / PAGE["file"]
    if not page.is_file():
        out.append(("row-typed-cell", False,
                    "public/%s is not built yet; run python site/build.py first" % PAGE["file"]))
    else:
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            shutil.copytree(build.PUBLIC, root, dirs_exist_ok=True)
            copy = root / PAGE["file"]
            t = copy.read_text(encoding="utf-8")
            planted = t.replace("</footer>", "<p>the fix for this landed on 2026-01-01</p></footer>", 1)
            if planted == t:
                out.append(("row-typed-cell", False, "could not plant: %s has no </footer>" % PAGE["file"]))
            else:
                copy.write_text(planted, encoding="utf-8", newline="\n")
                found = [f for f in build.check_numbers(root)[0] if PAGE["file"] in f and "2026-01-01" in f]
                out.append(("row-typed-cell", bool(found),
                            "a hand-typed date, not read through any fact: %s" % (found[0] if found else "passed")))

    try:
        facts.own_commit("5128ce7", "a one-character mutation of a real fix commit")
        out.append(("fix-not-on-main", False, "a mutated fix commit (5128ce7 for 5128ce6) was accepted"))
    except Refusal as e:
        out.append(("fix-not-on-main", True, "a mutated fix commit was refused: %s" % e))

    try:
        facts.own_commit("bdbac1f", "P2's verified tip, squashed away before it reached main")
        out.append(("fix-not-on-main", False, "bdbac1f, which main does not hold, was accepted as a fix"))
    except Refusal as e:
        out.append(("fix-not-on-main", True, "bdbac1f, which main does not hold (it was squashed into "
                    "6c163dd), was refused: %s" % e))

    out += _issue1_controls()
    return out
