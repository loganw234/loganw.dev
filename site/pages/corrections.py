"""Corrections: the site-wide rules of engagement for proving a claim on this
site wrong (docs/SPEC.md, "Corrections (global page)"; briefs/P4.md).

The rules of engagement and the "where I'd attack first" gaps are Logan's,
from the spec, printed through facts.stated() or quoted from cft-fp256 at its
pin. The corrections ledger is seeded from this site's own record,
docs/VALIDATION.md, read through facts.own_prose()/own_entry() and
facts.own_commit() - never typed from memory.
"""
import facts
from facts import V, Refusal, fact
from render import L, render

PAGE = {"file": "corrections.html", "nav": "Corrections",
        "title": "Corrections — loganw.dev",
        "description": "The rules for proving a claim on this site wrong, the gaps the record already names, "
                       "and every correction so far."}

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
# cft-fp256's pin. The spec also names "clause readings in COMPLIANCE"; that
# document's own conformance statement (docs/COMPLIANCE.md, "The conformance
# statement") states its coverage plainly and calls no clause reading of its
# own open to dispute anywhere in the file - checked, not found - so it is
# left out here rather than asserted without a source.
# ---------------------------------------------------------------------------

def attack_first():
    P = facts.prose
    items = [
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
# Every cell is read, never typed. The signature row is Logan's words,
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


LEDGER_CAP = ("A selection, not every finding this site's own ledger records: plain instances, early in this "
              "round, where a single fix commit answers a single finding, each read from "
              "docs/VALIDATION.md's own entry and checked against this site's own history. The rest of that "
              "entry, and everything since, is in the ledger itself.")


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
    one-character mutation of a real one (briefs/P4.md control 2)."""
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
    return out
