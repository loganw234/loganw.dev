"""Work: every project on Home's ledger (docs/SPEC.md, "Work"). The first five
(decision 15) get a full nine-section dossier; the rest are listed as Home
already lists them, so the two pages never carry two descriptions of one
project that could drift apart.
"""
import copy

from pages import _dossier
import facts
from facts import V, Src, Refusal, fact
import pages.home as home
from render import C, L, esc, render

PAGE = {"file": "work.html", "nav": "Work", "title": "Work — loganw.dev",
        "description": "Every project this site covers, with a full dossier for the projects the first version "
                        "goes deepest on.",
        "index": True}

# name -> (html file, txt file). Order is the spec's (decision 15).
DOSSIERS = [
    ("cft-fp256", "work-cft-fp256.html"),
    ("Quantum-Film", "work-quantum-film.html"),
    ("cft-rebound", "work-cft-rebound.html"),
    ("HonestFramework", "work-honestframework.html"),
    ("ParcelRound", "work-parcelround.html"),
]
DOSSIER_FILE = dict(DOSSIERS)


def _project_name(r):
    p = r["project"]
    return p.inner if hasattr(p, "inner") else p


def render_page(ctx):
    built = set(ctx.get("pages", {}).get("Work", []))
    out, thread = [], None
    for r in home.rows():
        if r["thread"] != thread:
            if thread is not None:
                out.append("</ul>")
            thread = r["thread"]
            out.append("<h2>%s</h2><ul class=\"plain\">" % esc(thread))
        name = _project_name(r)
        dest = DOSSIER_FILE.get(name)
        if dest and dest in built:
            out.append("<li><a href=\"%s\">%s</a> — a full dossier</li>" % (esc(dest), esc(name)))
        else:
            out.append("<li>%s</li>" % render(r["project"]))
    if thread is not None:
        out.append("</ul>")
    lede = ("<div class=\"measure\"><p class=\"lede\">Every project on Home's ledger is here. "
            "%s of them carry a full dossier: what each is, what it is not, its contract, what has "
            "verified it, the failures it kept, how to test it, how to try to prove it wrong, what it "
            "connects to and where every figure on its page was read.</p></div>"
            % render(_dossier_count()))
    return lede + "".join(out)


@fact
def _dossier_count():
    return V(str(len(DOSSIERS)), Src("file", "site/pages/work.py", "the dossier modules this page links, counted"),
             raw=str(len(DOSSIERS)), num=True)


def controls():
    out = []

    # 1. A kept-failure commit that doesn't exist: a hash mutated by one
    # character must be refused by the fact that checks the commit at the pin.
    good = "f192bf0"
    bad = "f192bf1"     # one character changed; not a commit in cft-fp256
    try:
        _dossier.kept_failure("cft-fp256", bad, "a control's mutated hash")
        out.append(("kept-failure-hash", False, "a mutated hash (%s for %s) was accepted" % (bad, good)))
    except Refusal as e:
        out.append(("kept-failure-hash", True, "a mutated hash was refused: %s" % e))

    # 2. A dossier missing one of the nine sections, or with section 2 left
    # empty, must be refused by name, naming the dossier and the section.
    sections = [_dossier.section(t, [_dossier.para(["x"])]) for t in _dossier.TITLES]
    dropped = [s for s in sections if s.title != "What it is not"]
    try:
        _dossier.check_sections("planted", dropped)
        out.append(("dossier-section", False, "a dossier missing 'What it is not' passed"))
    except Refusal as e:
        out.append(("dossier-section", "What it is not" in str(e) and "planted" in str(e),
                    "a dossier missing a section: %s" % e))
    emptied = copy.deepcopy(sections)
    emptied[1].blocks = []
    try:
        _dossier.check_sections("planted", emptied)
        out.append(("dossier-empty", False, "a dossier with an empty 'What it is not' passed"))
    except Refusal as e:
        out.append(("dossier-empty", "What it is not" in str(e), "an empty mandatory section: %s" % e))

    # 3. A twin that has lost a figure must be refused, by comparing the fact
    # ids the page carries against the ids its twin carries.
    v = facts.pin_commit("cft-fp256")
    html = "<p>%s</p>" % render(v)
    text_ok = "commit %s [fact %d]\n" % (v.text, v.id)
    try:
        _dossier.twin_ids("planted", html, text_ok)
        ok_result = True
    except Refusal:
        ok_result = False
    out.append(("twin-figure", ok_result, "a matching page and twin were %s" % ("accepted" if ok_result else "refused")))
    text_dropped = "commit, nothing else\n"
    try:
        _dossier.twin_ids("planted", html, text_dropped)
        out.append(("twin-figure", False, "a twin missing fact %d passed" % v.id))
    except Refusal as e:
        out.append(("twin-figure", str(v.id) in str(e), "a twin missing a figure: %s" % e))

    return out
