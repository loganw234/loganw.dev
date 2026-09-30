"""Threads: the section's own page (docs/SPEC.md: "the organising spine -
three, not a project list"). Links to the three thread pages; P2's brief
also puts the map's own negative controls here, since this is the section
that owns the map's layout.
"""
import mapgen
from render import esc

PAGE = {"file": "threads.html", "nav": "Threads", "index": True, "title": "Threads — loganw.dev",
        "description": "The organising spine, not a project list: Determinism, Film & photography, Preservation. "
                       "Each has its own account, its own slice of the map, and its own door."}

THREADS = [
    ("Determinism", "thread-determinism.html",
     "Bit-identical arithmetic: a point-cloud atlas, a language for it, a coprocessor that will not drift."),
    ("Film & photography", "thread-film.html",
     "A print engine, split apart, and a quantum-grown film stock — and the paper pipeline the print engine "
     "grew into."),
    ("Preservation", "thread-preservation.html",
     "A Mercenaries2 revival, its modding tooling, and everyone who has committed to it, credited directly."),
]


def render_page(ctx):
    items = "".join(
        '<li><a href="%s">%s</a> — %s</li>' % (esc(file), esc(label), esc(desc))
        for label, file, desc in THREADS)
    return ('<div class="measure"><p class="lede">The organising spine, not a project list. Each thread is an '
           'account of where its projects came from, drawn from the repositories, with its own slice of the map '
           'and its own door.</p>'
           '<ul class="plain threads-index">%s</ul></div>' % items)


def controls():
    out = []

    # 1. A node missing from the narrow map: a copy of svg_narrow that drops
    # one node must fail the check that compares the node and edge sets of
    # the two layouts.
    M = mapgen.build()
    any_name = next(iter(M["nodes"]))
    wide = mapgen.svg_wide(M)[1:]
    sabotaged = mapgen.svg_narrow(M, omit=any_name)[1:]
    problems = mapgen.check_parity(wide, sabotaged)
    out.append(("map-parity", bool(problems), "a copy of the narrow renderer with %r dropped: %s"
               % (any_name, problems[0] if problems else "the parity check passed anyway")))

    # 3. A door links to Propose only once Propose is built.
    #
    # Rewritten (wave2-prep, granted to P4 in briefs/P4.md): the old version
    # above wrote a planted link into public/'s built thread pages and
    # expected build.check_links to refuse it, because propose.html was not
    # yet a published file. Once P4 publishes propose.html that target
    # resolves, the plant is no longer a fault, the control can never fail
    # again, and under --require-all the gate would then fail on a control
    # that cannot fail. It also wrote into the real public/, never a copy.
    #
    # The property survives without any of that: each thread page's own
    # render_page links Propose exactly when ctx["built"] names it, and not
    # before. Checked here by calling the three real modules' render_page
    # directly, in memory, under both states - never touching public/, and
    # never writing a file at all. To show the check itself bites, two fake
    # doors are run through the same test: one that links early, and one
    # that never catches up once Propose exists.
    import pages.thread_determinism as _det
    import pages.thread_film as _film
    import pages.thread_preservation as _pres

    def links_propose(render_page, built):
        html = render_page({"built": dict(built), "pages": {}})
        return 'href="propose.html"' in html

    def door_ok(render_page):
        early = links_propose(render_page, {})
        missing = not links_propose(render_page, {"Propose": "propose.html"})
        return not early and not missing

    for mod, label in ((_det, "thread-determinism"), (_film, "thread-film"), (_pres, "thread-preservation")):
        ok = door_ok(mod.render_page)
        out.append(("door-not-early", ok, "%s, rendered in memory with and without Propose in ctx['built']: %s"
                   % (label, "links it only once built, as it must" if ok
                      else "NOT CAUGHT: links early, or never catches up")))

    early_linked = links_propose(lambda ctx: '<p class="cta"><a href="propose.html">Propose a thread</a>.</p>', {})
    out.append(("door-not-early", early_linked,
               "a fake door linking Propose before it's built: %s" % ("caught" if early_linked else "NOT CAUGHT")))

    late_missing = not links_propose(lambda ctx: '<p class="cta">a door with no link</p>',
                                     {"Propose": "propose.html"})
    out.append(("door-not-early", late_missing,
               "a fake door that never links Propose once it's built: %s"
               % ("caught" if late_missing else "NOT CAUGHT")))
    return out
