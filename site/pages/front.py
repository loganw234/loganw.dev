"""Home: the front page, a lighter landing space before Map & Ledger
(decision 29). It is for a general reader, in Logan's own words. Its one
link in its body is to Map & Ledger, one click on (decision 30); its
footer's note also links the page it retells.

Each of Logan's paragraphs here, and his note in the footer, is still a
stated() figure, held to his approved words by pages._settled, as About's
are. The difference is where the sources are given. At Logan's word ("The front page can be light on the "stated by"
and direct pins ... it can still clarify that in the footer", 2026-09-30),
this page prints each figure without its label, and gives every label once,
in a note in its footer. The numbers stage holds that: a figure here passes
without a label beside it only if the note gives a label of exactly its own
fact's, and no other page may carry such a note.
"""
import facts
from pages import _settled
from render import esc, fig, render, source

PAGE = {"file": "index.html", "nav": "Home", "title": "Logan W. — loganw.dev",
        "description": "What this site is, and why the rest of it is so thorough."}

# Drafted by the lead from the spec's own words (docs/SPEC.md, section 1: "carpenter
# since fifteen", "no formal training", "agents write essentially all the lines",
# "gates decide what's true"), and approved by Logan on 2026-09-29: "Biography is
# good" (decision 14). It opened Home until the front page took Home's place.
WHO = ("I'm Logan. I have worked as a carpenter since I was fifteen, and I have no formal training in computing. "
       "AI agents have written essentially all of the code in these projects; gates decide what is true, and the "
       "record keeps what they said.")

# Drafted by the lead from Logan's answers to two rounds of questions, and
# approved by Logan: "Approved, and yes, Map & Ledger right after Home", then
# "Approved, go ahead with those three changes" for three phrases the lead
# narrowed before it shipped, confirmed as printed with "Confirmed, add the
# carpenter credit, keep the link" (2026-09-30, decision 29, where his
# answers are recorded).
WHAT = ("I work alongside AI to build systems you can check for yourself, and some unusual experiments. The first "
        "major one, cft-fp256, is an experiment in its own right: how far can one untrained person take a serious "
        "engineering project, now that AI has lifted the barrier of expertise? It's a math coprocessor that gets the "
        "same answer everywhere. The goal is to take it from the silicon all the way to a written promise about its "
        "arithmetic, using only open tools.")
STARTED = ("It began with Mercenaries 2, a video game from 2008, and a set of names somebody deleted. I could make up "
           "strings the game would accept in their place, but a string that works isn't the name a developer "
           "actually typed. Something can work and not be true, and that idea runs through everything here.")
CARPENTER = ("I work the way a carpenter does: to a measurement. You check what you built against a number rather "
             "than your own opinion of it, and you're honest about how close you actually got.")
EXPERTISE = ("I don't need to be an expert in every subject. I need to understand the whole system well enough to say "
             "what it should do, see the consequences, and steer, while AI agents bring the specialist knowledge that "
             "makes each decision informed rather than arbitrary.")
ACCOUNTABLE = ("AI gives one person a huge workforce that can't be held accountable for its work. So nothing it makes "
               "is taken on its word: everything has to pass a test that could have failed.")
THOROUGH = ("The goal is to never let \"trust me\" be an acceptable answer. On the next page, every number names "
            "where it came from, and one that drifts stops the site from building.")
WHY = ("When something interests me, I'm drawn to it, like pulling a thread. When work doesn't pull me, I lose "
       "interest and focus, so it's both a strength and a weakness. Recreating film stock grain by grain, for "
       "instance, realistically benefits no one. It was part of the larger atlas-darkroom experiment.")
DOOR = "Where each project came from, and where each one stands."
NOTE = ("This page is in Logan's own words: Home's biography, and the rest approved on 2026-09-30. The lines on how "
        "it started, and on working like a carpenter, retell PrettyCloud's about page, where the whole story is. This "
        "is the one page here that gives its sources in one note instead of beside each figure. The record starts on "
        "Map & Ledger, and every figure there names where it came from.")
APPROVED = [WHAT, STARTED, CARPENTER, EXPERTISE, ACCOUNTABLE, THOROUGH, WHY, DOOR, NOTE]

# Every statement this page may print without a draft label, with the label
# it must carry: its words, who said them, and when (pages._settled).
SETTLED = {WHO: "stated by Logan, 2026-09-29"}
SETTLED.update({t: "stated by Logan, 2026-09-30" for t in APPROVED})

# The whole story, on the page this one retells: PrettyCloud's live about
# page, for a reader. The build doesn't read it.
STORY = "https://prettycloud.io/about.html"


def S(text, **kw):
    return facts.stated(text, "Logan", "2026-09-30", **kw)


def D(text):
    """Words drafted here, not yet approved by Logan: the label says so until
    Logan approves them."""
    return S(text, draft=True)


def bare(v):
    """A statement printed without its label, which the footer's note gives."""
    return fig(v, src=False)


def lede_block():
    return '<p class="lede">%s</p>' % bare(facts.stated(WHO, "Logan", "2026-09-29"))


def what_block():
    return '<h2>What this is</h2><p>%s</p>' % bare(S(WHAT))


def started_block():
    return '<h2>How it started</h2><p>%s</p>' % bare(S(STARTED))


def work_block():
    return ('<h2>How the work gets done</h2><p>%s</p><p>%s</p><p>%s</p>'
            % (bare(S(CARPENTER)), bare(S(EXPERTISE)), bare(S(ACCOUNTABLE))))


def thorough_block():
    return '<h2>Why the next page is so thorough</h2><p>%s</p>' % bare(S(THOROUGH))


def why_block():
    return '<h2>Why I do it</h2><p>%s</p>' % bare(S(WHY))


def door_block(ctx):
    target = ctx["built"]["Map & Ledger"]
    return '<h2><a href="%s">Map &amp; Ledger →</a></h2><p>%s</p>' % (esc(target), bare(S(DOOR)))


def note_block():
    """The footer's note: Logan's own note, with its label, then the one label
    it doesn't give, the biography's, and where the whole story is."""
    return ('<p class="sources">%s</p><p class="sources">Home&#x27;s biography%s. The whole story of how it started: '
            '<a href="%s">PrettyCloud&#x27;s about page</a>.</p>'
            % (render([S(NOTE)]), source(facts.stated(WHO, "Logan", "2026-09-29")), esc(STORY)))


BLOCKS = ("lede_block", "what_block", "started_block", "work_block", "thorough_block", "why_block", "door_block",
          "note_block")


def render_page(ctx):
    body = ('<div class="measure">' + lede_block() + what_block() + started_block() + work_block()
            + thorough_block() + why_block() + door_block(ctx) + '</div>')
    return _settled.refuse(body, PAGE["file"], SETTLED)


def footer_note(ctx):
    return _settled.refuse(note_block(), PAGE["file"], SETTLED)


def controls():
    """The front page's statements are Logan's settled words, or labelled
    drafts, in its body and in its footer's note alike: pages._settled plants
    each fault its check was found to miss into each of BLOCKS."""
    ctx = {"built": {"Map & Ledger": "map-ledger.html"}, "pages": {}}
    return _settled.controls(globals(), BLOCKS, lambda c: (render_page(c), footer_note(c)), ctx, "front",
                             (WHAT, "Logan", "2026-09-30"), S, D)
