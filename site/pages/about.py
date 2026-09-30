"""About (docs/SPEC.md, "About"; decisions 14, 16). Logan's own register:
Home's already-approved biography, plus what it leaves out, in sentences
Logan approved on 2026-09-30 (decision 26). A statement Logan hasn't
approved carries a draft label (decision 14's pattern), and the build
refuses one that doesn't. Co-authors are named, not restated: the
statement itself stays on Method alone (decision 9's scope). Decision 16
overrides the spec's own "Wally note stated plainly" here: the name appears
only on the Preservation thread's page, so this page links there instead of
naming it.
"""
import re

import facts
from facts import V, Src, Refusal, fact
from pages import home
from pages._p5 import page_link
from render import C, L, esc, render

PAGE = {"file": "about.html", "nav": "About", "title": "About — loganw.dev",
        "description": "Logan's own register: the path in, the AI collaborators, the contact, and what the site "
                       "refuses to be."}


def S(text, **kw):
    return facts.stated(text, "Logan", "2026-09-29", **kw)


def D(text):
    """Words drafted here from Logan's own spec, not yet approved by Logan
    (decision 14's pattern): the label says so until Logan approves them."""
    return S(text, draft=True)


def A(text):
    """Words drafted here and approved by Logan as written: "Both sentences
    are approved" (2026-09-30, decision 26)."""
    return facts.stated(text, "Logan", "2026-09-30")


# ---------------------------------------------------------------------------
# The register, in three paragraphs. The first is Home's own biography,
# home.WHO, already approved (decision 14): imported, not retyped, and it
# carries no draft label. The other two add what it leaves out: drafted here,
# and approved by Logan on 2026-09-30 (decision 26). SETTLED names every
# statement this page may print without a draft label, with the label it
# must carry: its words, who said them, and when. render_page refuses any
# other that lacks a draft label.
# ---------------------------------------------------------------------------

APPROVED = [
    "I have a GED, and one month of formal computer science.",
    "My own figure for the balance is still 1:24, not a measurement.",
]
REFUSED = 'skills grid, services, testimonials, hero photo, newsletter, and the word "passionate"'
SETTLED = {home.WHO: "stated by Logan, 2026-09-29",
           "for now": "stated by Logan, 2026-09-29",
           REFUSED: "stated by Logan, 2026-09-29",
           APPROVED[0]: "stated by Logan, 2026-09-30",
           APPROVED[1]: "stated by Logan, 2026-09-30"}


def register_block():
    p1 = render([S(home.WHO)])
    p2 = render([A(APPROVED[0])])
    p3 = render([A(APPROVED[1])])
    return '<div class="measure"><p>%s</p><p>%s</p><p>%s</p></div>' % (p1, p2, p3)


def coauthors_block(ctx):
    if "Method" in ctx.get("built", {}):
        method_link = L(ctx["built"]["Method"], "Method")
    else:
        method_link = "Method, not yet built"
    body = render([
        "The AI collaborators are named here: Claude and Gemini. What that credit means is stated once, on ",
        method_link, ", so it stays in one place."
    ])
    return '<p>%s</p>' % body


def contact_block():
    body = render([
        "Contact: ", L("mailto:logan@loganw.dev", "logan@loganw.dev"), ", ", S("for now"), "."
    ])
    return '<p>%s</p>' % body


def refused_block():
    items = S(REFUSED)
    body = render(["Refused on this site, by name: ", items, "."])
    return '<p>%s</p>' % body


def game_work_block(ctx):
    body = render([
        "The game-community project has its own thread, crediting everyone who has worked on it directly: ",
        page_link(ctx, "Threads", "thread-preservation.html", "its own page"), "."
    ])
    return '<p>%s</p>' % body


def printed(body):
    """The log's record for every figure body prints. Each mark is read by
    the numbers stage's own reader (build._Marks, Python's HTML parser), so
    it is found however its attribute is cased or its id encoded, exactly as
    that stage finds it. A mark whose id isn't plain digits, or that no
    logged fact has, is refused."""
    import build   # as corrections.py and method.py do: build imports the pages
    p = build._Marks()
    p.feed(body)
    p.close()
    recs = []
    for f in sorted({m["f"] for m in p.marks}):
        i = int(f) if re.fullmatch(r"[0-9]+", f) else 0
        rec = facts.LOG[i - 1] if 0 < i <= len(facts.LOG) else None
        if rec is None or rec["id"] != i:
            raise Refusal("about.html prints a mark for fact %r, which no logged fact has" % f)
        recs.append(rec)
    return recs


@fact
def relayed(text):
    """A statement returned through a fact of its own, so that its record's
    method isn't facts.stated. Only controls() calls it: the check must know
    a statement by its kind, whichever fact returned it."""
    return S(text)


def unsettled(recs):
    """The statements among recs that carry no draft label and aren't
    settled: their words, who said them and when, exactly as SETTLED has
    them."""
    return [r["text"] for r in recs if r["kind"] == "stated" and SETTLED.get(r["text"]) != r["where"]
            and not r["where"].startswith("drafted from ")]


BLOCKS = ("register_block", "coauthors_block", "contact_block", "refused_block", "game_work_block")


def render_page(ctx):
    """About's page. It refuses every stated() figure it prints, its marks
    read as the numbers stage reads them (printed()), that carries no draft
    label and isn't settled.
    Where or when the figure was rendered doesn't matter, only that the page
    prints it. A sentence printed as plain text, not through stated(), is
    outside it: the check reads figures, and plain text is none."""
    body = (
        '<div class="measure"><p class="lede">In Logan&#x27;s own register.</p></div>'
        + register_block()
        + coauthors_block(ctx)
        + contact_block()
        + refused_block()
        + game_work_block(ctx)
    )
    bad = unsettled(printed(body))
    if bad:
        raise Refusal("about.html states %r, which Logan hasn't approved as printed (its words, who and "
                      "when), with no draft label" % bad[0][:60])
    return body


def controls():
    """About's statements are Logan's settled words, or labelled drafts.
    - In each of BLOCKS, a statement planted before the block's content and
      one planted after it, with no draft label, must each be refused by
      render_page, by name. The same statement with its label must pass.
    - A statement rendered before the page starts, then printed inside it,
      must be refused.
    - So must a settled sentence given another who or another date, and a
      statement whose who reads like a draft label.
    - So must a statement returned through another fact, and marks written
      the other ways the numbers stage still reads as marks: an upper-case
      attribute name, and an id written as character references.
    Each control also needs the real page to pass."""
    ctx = {"built": {"Method": "method.html"}, "pages": {"Threads": ["thread-preservation.html"], "Work": []}}
    planted = "A sentence no one approved."
    g = globals()

    def attempt(name=None, statement=None, before=False, early=False, rewrite=None):
        saved = g[name] if name else None
        facts.reset_log()
        if name:
            pre = "<p>%s</p>" % render([statement()]) if early else None

            def planted_block(*a):
                p = pre or "<p>%s</p>" % render([statement()])
                p = rewrite(p) if rewrite else p
                return p + saved(*a) if before else saved(*a) + p
            g[name] = planted_block
        try:
            render_page(ctx)
            return None
        except Refusal as e:
            return str(e)
        finally:
            if name:
                g[name] = saved

    def refused(e):
        return bool(e) and "hasn't approved" in e

    real = attempt()
    fine = real or "passed, as it must"
    out = []
    for name in BLOCKS:
        for before in (True, False):
            where = "%s, %s its content" % (name, "before" if before else "after")
            bare = attempt(name, lambda: S(planted), before)
            labelled = attempt(name, lambda: D(planted), before)
            out.append(("about-draft-label", refused(bare) and labelled is None and real is None,
                        "in %s, an unapproved statement with no draft label: %s; the same with its label: %s; "
                        "the real page: %s" % (where, bare or "passed", labelled or "passed, as it must", fine)))
    early = attempt("register_block", lambda: S(planted), before=True, early=True)
    out.append(("about-rendered-before", refused(early) and real is None,
                "a statement rendered before the page starts, printed inside it: %s; the real page: %s"
                % (early or "passed", fine)))
    for cname, what, statement in (
            ("about-settled-who", "a settled sentence given to someone else",
             lambda: facts.stated(APPROVED[0], "Someone Else", "2026-09-30")),
            ("about-settled-when", "a settled sentence given another date",
             lambda: facts.stated(APPROVED[0], "Logan", "2026-09-29")),
            ("about-draft-who", "a statement whose who reads like a draft label",
             lambda: facts.stated(planted, "drafted from Logan", "2026-09-30")),
            ("about-relayed", "a statement returned through another fact", lambda: relayed(planted))):
        e = attempt("register_block", statement)
        out.append((cname, refused(e) and real is None, "%s: %s; the real page: %s" % (what, e or "passed", fine)))
    for cname, what, rewrite in (
            ("about-mark-case", "a mark whose attribute name is upper case",
             lambda h: h.replace('data-f="', 'DATA-F="')),
            ("about-mark-reference", "a mark whose id is written as character references",
             lambda h: re.sub(r'data-f="([0-9]+)"',
                              lambda m: 'data-f="%s"' % "".join("&#%d;" % ord(c) for c in m.group(1)), h))):
        e = attempt("register_block", lambda: S(planted), rewrite=rewrite)
        out.append((cname, refused(e) and real is None, "%s: %s; the real page: %s" % (what, e or "passed", fine)))
    facts.reset_log()
    return out
