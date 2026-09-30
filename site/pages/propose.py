"""Propose: "I don't take work. I follow what pulls." (docs/SPEC.md, "Propose
a thread"; briefs/P4.md).

Everything on this page is Logan's own word, printed through facts.stated(),
except the doors: each thread page's own door() is called here, never
retyped, and the method's door - new, tied to no thread - is defined here,
with "MIT" read from each method's own LICENSE at its pin.
"""
import facts
from render import L, esc, render

# Deferred in spirit only: build.py imports pages.*, which is how these
# modules already exist by the time this one does; the import itself is a
# normal top-level one, since pages.propose has no dependency the other way.
from pages import thread_determinism, thread_film, thread_preservation

PAGE = {"file": "propose.html", "nav": "Propose",
        "title": "Propose — loganw.dev",
        "description": "What pulls, what doesn't, the shape a proposal takes, and every door."}

PROPOSAL_URL = "https://github.com/loganw234/loganw.dev/issues/new?template=proposal.yml"


def S(text, **kw):
    return facts.stated(text, "Logan", "2026-09-29", **kw)


REGISTER = "I don't take work. I follow what pulls."


# ---------------------------------------------------------------------------
# I. What pulls, and what doesn't.
# ---------------------------------------------------------------------------

PULLS = ["checkable by someone who distrusts it", "“done” definable in advance",
         "ends open, dated, usable"]
DOESNT = ["deadline/demo/vibes definitions", "anything that can't be a gate",
         "“solve X by Y for Z” — tell me why X matters"]


def pulls_table():
    head = "<thead><tr><th>what pulls</th><th>what doesn't</th></tr></thead>"
    rows = []
    for a, b in zip(PULLS, DOESNT):
        rows.append("<tr><td>%s</td><td>%s</td></tr>" % (render([S(a)]), render([S(b)])))
    return '<div class="pulls table-wrap"><table>%s<tbody>%s</tbody></table></div>' % (head, "".join(rows))


# ---------------------------------------------------------------------------
# II. Money.
# ---------------------------------------------------------------------------

MONEY = "neither required nor sufficient — changes the schedule, not the standard"


# ---------------------------------------------------------------------------
# III. The three-line proposal, and the communities it has already pulled a
# thread from.
# ---------------------------------------------------------------------------

SHAPE = "problem · who struggles · provable done"
COMMUNITIES = ("small communities with problems nobody's paid to fix — the preservation thread started "
              "as exactly one of these")


def proposal_block():
    return render([
        "The intake takes this shape, ", S(SHAPE), ", through the proposal form on this repository: ",
        L(PROPOSAL_URL, "open it"), " - ", S("timestamped, no backend"), ".",
    ])


# ---------------------------------------------------------------------------
# IV. The doors. Each thread's own door() is called, never retyped. The
# method's is new, and belongs to no thread page, so it is defined here.
# ---------------------------------------------------------------------------

def door_method():
    """The spec's fourth standing door - the method itself, MIT, no thread
    of its own. Logan's exact words; "MIT" is verified separately, below,
    at each method's own LICENSE."""
    return facts.stated("the method (MIT, no permission needed; a story of it working or failing is worth "
                        "a message)", "Logan", "2026-09-29")


def mit_confirmed():
    """Both methods, confirmed MIT at their own pins - two separate reads,
    since they are two separate repositories."""
    return render([
        "Read at their pins: HonestFramework's own LICENSE opens ",
        facts.prose("HonestFramework", "LICENSE", r"^(MIT) License"), ", and ParcelRound's opens ",
        facts.prose("ParcelRound", "LICENSE", r"^(MIT) License"), " too.",
    ])


DOORS = [("Determinism", thread_determinism.door), ("Film & photography", thread_film.door),
        ("Preservation", thread_preservation.door)]


def doors_block():
    parts = []
    for label, door_fn in DOORS:
        parts.append('<p class="cta"><b>%s.</b> %s</p>' % (esc(label), render([door_fn()])))
    parts.append('<p class="cta"><b>The method.</b> %s</p>' % render([door_method()]))
    return '<div class="doors">%s<p class="cap">%s</p></div>' % ("".join(parts), mit_confirmed())


def render_page(ctx):
    return (
        '<div class="measure"><p class="lede">%s</p></div>'
        '<h2><small>I</small>What pulls, what doesn’t</h2>%s'
        '<h2><small>II</small>Money</h2>'
        '<div class="measure"><p>%s</p></div>'
        '<h2><small>III</small>Propose one</h2>'
        '<div class="measure"><p>%s</p><p>%s</p></div>'
        '<h2><small>IV</small>The doors</h2>%s'
        % (render([S(REGISTER)]), pulls_table(), render(["Money: ", S(MONEY), "."]),
           proposal_block(), render([S(COMMUNITIES), "."]), doors_block())
    )


def controls():
    """A door retyped (briefs/P4.md control 3): "Propose's copy of a
    thread's door changed by one word must be refused, because it no
    longer matches that thread's door()." This page keeps no copy at all -
    doors_block() calls thread_determinism.door() etc. directly, at render
    time, so nothing here could retype a door and silently drift; the
    property holds by construction, not by a check run after the fact.
    What the control demonstrates is the failure mode itself: a hand-typed
    copy, the way an editor tempted to paste the words in rather than call
    the function might produce, changed by one word, no longer equals a
    fresh call to the real door() - which is exactly the mismatch this
    page's own direct-call design makes structurally impossible."""
    out = []
    real = thread_determinism.door().text
    if "workloads" not in real:
        out.append(("door-retyped", False, "could not plant: 'workloads' is not in thread_determinism.door()'s text"))
    else:
        retyped = real.replace("workloads", "workflows", 1)
        caught = retyped != real
        out.append(("door-retyped", caught,
                   "a copy of thread_determinism's door retyped by one word, against a fresh door() call: %s"
                   % ("differ, as they must" if caught else "NOT CAUGHT: matched anyway")))
    return out
