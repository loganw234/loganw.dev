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
import facts
from facts import V, Src, Refusal, fact
from pages import _settled, front
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
# front.WHO, already approved (decision 14): imported, not retyped, and it
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
SETTLED = {front.WHO: "stated by Logan, 2026-09-29",
           "for now": "stated by Logan, 2026-09-29",
           REFUSED: "stated by Logan, 2026-09-29",
           APPROVED[0]: "stated by Logan, 2026-09-30",
           APPROVED[1]: "stated by Logan, 2026-09-30"}


def register_block():
    p1 = render([S(front.WHO)])
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


BLOCKS = ("register_block", "coauthors_block", "contact_block", "refused_block", "game_work_block")


def render_page(ctx):
    """About's page. It refuses every stated() figure it prints that carries
    no draft label and isn't settled (pages._settled, the rule the front page
    shares). A sentence printed as plain text, not through stated(), is
    outside it: the check reads figures, and plain text is none."""
    body = (
        '<div class="measure"><p class="lede">In Logan&#x27;s own register.</p></div>'
        + register_block()
        + coauthors_block(ctx)
        + contact_block()
        + refused_block()
        + game_work_block(ctx)
    )
    return _settled.refuse(body, PAGE["file"], SETTLED)


def controls():
    """About's statements are Logan's settled words, or labelled drafts:
    pages._settled.controls plants each fault its check was found to miss
    into each of BLOCKS."""
    ctx = {"built": {"Method": "method.html"}, "pages": {"Threads": ["thread-preservation.html"], "Work": []}}
    return _settled.controls(globals(), BLOCKS, render_page, ctx, "about", (APPROVED[0], "Logan", "2026-09-30"),
                             S, D)
