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

    # 3. A door linked too early: propose.html is not a file this round
    # publishes (Propose is P4's, not built yet), so a link to it from any
    # thread page must be refused by build.py's own links check. Deferred
    # import: build.py imports pages, which imports this module, so the
    # import has to happen after this module already exists, not at the top
    # of it.
    import build as _build
    root = _build.PUBLIC
    for file in ("thread-determinism.html", "thread-film.html", "thread-preservation.html"):
        f = root / file
        if not f.is_file():
            out.append(("door-not-early", False, "could not plant: %s is not published" % file))
            continue
        t = f.read_text(encoding="utf-8")
        planted = t.replace("</main>", '<a href="propose.html">propose</a></main>', 1)
        if planted == t:
            out.append(("door-not-early", False, "could not plant a link into %s" % file))
            continue
        f.write_text(planted, encoding="utf-8", newline="\n")
        try:
            found = [p for p in _build.check_links(root) if "propose.html" in p]
        finally:
            f.write_text(t, encoding="utf-8", newline="\n")
        out.append(("door-not-early", bool(found), "a planted link to propose.html in %s: %s"
                   % (file, found[0] if found else "the links check passed it anyway")))
    return out
