"""About (docs/SPEC.md, "About"; decisions 14, 16). Logan's own register:
Home's already-approved biography, plus what it leaves out, each new
sentence carrying a draft label until Logan approves it (decision 14's
pattern). Co-authors are named, not restated: the statement itself stays on
Method alone (decision 9's scope). Decision 16 overrides the spec's own
"Wally note stated plainly" here: the name appears only on the Preservation
thread's page, so this page links there instead of naming it.
"""
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
    """Words drafted here from Logan's own spec, not yet his approved words
    (decision 14's pattern): the label says so until he approves them."""
    return S(text, draft=True)


# ---------------------------------------------------------------------------
# The register, in three paragraphs. The first is Home's own biography,
# home.WHO, already approved (decision 14): imported, not retyped, and it
# carries no draft label. The other two add what it leaves out, and are new
# words drafted here, not yet Logan's approved words: DRAFTED names them,
# so controls() can check each one carries its label without guessing which
# of the page's other, already-settled statements ("for now", the refused
# list) should be exempt.
# ---------------------------------------------------------------------------

DRAFTED = [
    "I have a GED, and one month of formal computer science.",
    "My own figure for the balance is still 1:24, not a measurement.",
]


def register_block():
    p1 = render([S(home.WHO)])
    p2 = render([D(DRAFTED[0])])
    p3 = render([D(DRAFTED[1])])
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
    items = S('skills grid, services, testimonials, hero photo, newsletter, and the word "passionate"')
    body = render(["Refused on this site, by name: ", items, "."])
    return '<p>%s</p>' % body


def game_work_block(ctx):
    body = render([
        "The game-community project has its own thread, crediting everyone who has worked on it directly: ",
        page_link(ctx, "Threads", "thread-preservation.html", "its own page"), "."
    ])
    return '<p>%s</p>' % body


def render_page(ctx):
    return (
        '<div class="measure"><p class="lede">Logan, in his own register.</p></div>'
        + register_block()
        + coauthors_block(ctx)
        + contact_block()
        + refused_block()
        + game_work_block(ctx)
    )


def controls():
    ctx = {"built": {"Method": "method.html"}, "pages": {"Threads": ["thread-preservation.html"], "Work": []}}
    facts.reset_log()
    render_page(ctx)
    real = list(facts.LOG)

    def undrafted(recs):
        # Checked against DRAFTED by name, not "every statement but
        # home.WHO": About also states home.WHO's approved words, "for
        # now" and the refused-on-this-site list without a draft label,
        # correctly, since none of the three is a new word drafted here.
        return [r["text"] for r in recs if r["kind"] == "stated" and r["text"] in DRAFTED
                and "drafted from" not in facts.label(r)]

    # 1. A drafted statement without its draft label: on a copy of the real
    # page's own logged figures, one of DRAFTED has its label rewritten to
    # what draft=False would have produced.
    target = next(r for r in real if r["text"] in DRAFTED)
    planted = list(real)
    planted[planted.index(target)] = dict(target, where="stated by Logan, 2026-09-29")
    real_bad, plant_bad = undrafted(real), undrafted(planted)
    caught = not real_bad and bool(plant_bad)
    return [("about-draft-label", caught,
            "the real page: %s; a copy with %r stripped of its draft label: %s"
            % (real_bad or "each of DRAFTED reads as a draft", target["text"][:60],
               plant_bad or "NOT CAUGHT"))]
