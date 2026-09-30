"""Verify: "Don't trust this - run one." (docs/SPEC.md, "Verify"; briefs/P1.md).

Four checks, cheapest first, each with what it costs and what a pass does
and does not prove. The first three are sourced at cft-fp256's pin (its
README, CLAUDE.md, docs/VERIFICATION.md and CONFORMANCE.md); the fourth is
this site's own, described the way its own documents already describe it -
loganw.dev is not itself a pin, so there is no file to quote through
facts.prose() for a claim about this site's own build.

The site's own limit, stated once at the end: every quotation above shows
that this page quotes cft-fp256 faithfully at its pin. It does not show that
cft-fp256's claims are true - cft-fp256's own gates decide that, and running
one of the four checks is how a reader checks it directly.
"""
import facts
from render import C, L, SOURCE_REPO, render

PAGE = {"file": "verify.html", "nav": "Verify",
        "title": "Verify - loganw.dev",
        "description": "Don't trust this page - run one of the checks below, cheapest first."}


def _lede():
    P = facts.prose
    return render([
        "cft-fp256's contract: an ",
        P("cft-fp256", "CONFORMANCE.md",
          r"(implementation can be built and proven without this repository's RTL\s+or library - a different "
          r"chip, a different process, a different\s+language - and still be interchangeable with them bit "
          r"for bit)"),
        ". The checks below are how a reader confirms that directly, without taking this site's word for it, "
        "cheapest first.",
    ])


def checks():
    P = facts.prose
    url = P("cft-fp256", "README.md", r"\*\*<(https://loganw234\.github\.io/cft-fp256/)>\*\*")
    items = []

    items.append([
        L(url.raw, "cft-fp256's own conformance replay"), ", in the browser. Cost: a browser tab, nothing "
        "installed. It ",
        P("cft-fp256", "README.md", r"It (replays\s+the published conformance vectors in front of you)"), ".",
    ])

    items.append([
        C("make golden"), " in a clone of cft-fp256. Cost: ",
        P("cft-fp256", "docs/VERIFICATION.md", r"(\d\.\d min at four workers)", num=True), ". ",
        P("cft-fp256", "README.md", r"^(The golden model's self-tests)"), ": ",
        P("cft-fp256", "docs/VERIFICATION.md",
          r"(Its pytest suite\s+checks the model against its own invariants and against mpmath and\s+"
          r"MPFR where they can arbitrate)"),
        ". ",
        P("cft-fp256", "docs/VERIFICATION.md", r"(Nothing below re-litigates a value it\s+has decided)"),
        ".",
    ])

    items.append([
        C("make verify-quick"), ". Cost: ",
        P("cft-fp256", "CLAUDE.md", r"^make verify-quick\s+# (~\d+ min, \d+ of \d+ stages)", num=True), ". ",
        "`quick` is ",
        P("cft-fp256", "docs/VERIFICATION.md",
          r"`quick` is (the\s+`docs`, `generated`, `buildargs` and `sweepjudge` checks, the\s+model-versus-C "
          r"stages, the GPU's photograph, the bindings, the language\s+legs, the soak spot check, the "
          r"workloads, the demos and the remote\s+backend)"),
        "; it does not run ",
        P("cft-fp256", "docs/VERIFICATION.md",
          r"`gate` adds (the golden\s+suite, the vectors, the library replay, the transcendentals, MPFR, the\s+"
          r"C\+\+ replay, lint and formal)"),
        " - those need ", C("make verify-gate"), ". And, ",
        P("cft-fp256", "README.md", r"\*\*(CI's green tick does not cover synthesis, timing or silicon)\.\*\*"),
        ".",
    ])

    items.append([
        C("python site/build.py --verify-facts"), " in a clone of ", L(SOURCE_REPO, "this site"), ". Cost: one "
        "read per figure this site prints, at its pin or from the committed GitHub snapshot; a private "
        "repository's read is skipped by name. It proves every figure this site prints - including every quote "
        "above - is still exactly what its source gives right now; it does not prove that source's own claim "
        "is true, and a stated word has no source to re-read at all.",
    ])
    return "<ol>%s</ol>" % "".join("<li>%s</li>" % render(i) for i in items)


LIMIT = ("Every quotation above is read from cft-fp256's own documents, at the commit this site pins - the "
         "same discipline this whole site holds itself to. That shows this page quotes cft-fp256 faithfully. "
         "It does not show that cft-fp256's claims are true: cft-fp256's own gates decide that, and the checks "
         "above are how a reader runs them directly, rather than taking this site's word for it.")


def render_page(ctx):
    return (
        '<h1>Verify</h1>'
        '<div class="measure"><p class="lede">%s</p></div>'
        '<h2><small>I</small>Ways to check this</h2>'
        '<div class="cta"><p>Don\'t trust this - run one.</p>%s</div>'
        '<h2><small>II</small>What checking here does not do</h2>'
        '<div class="measure"><p class="cap">%s</p></div>'
        % (_lede(), checks(), LIMIT)
    )


def controls():
    """The negative control named "an unsourced sentence on Verify" (P1.md):
    render.fig() already refuses a figure no fact produced, so the way past
    it is a numeral typed straight into this page's HTML, bypassing fig()
    altogether - a count written into a string by hand. That is caught not
    by this page but by the numbers stage reading the built page, so this
    proves it, on a copy of this page's own built HTML."""
    import pathlib
    import shutil
    import tempfile

    import build

    out = []
    page = build.PUBLIC / PAGE["file"]
    if not page.is_file():
        out.append(("unsourced-sentence", False,
                    "public/%s is not built yet; run python site/build.py first" % PAGE["file"]))
        return out
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        shutil.copytree(build.PUBLIC, root, dirs_exist_ok=True)
        copy = root / PAGE["file"]
        t = copy.read_text(encoding="utf-8")
        planted = t.replace("</footer>", "<p>reads 4 checks by hand</p></footer>", 1)
        if planted == t:
            out.append(("unsourced-sentence", False, "could not plant: </footer> is not in %s" % PAGE["file"]))
        else:
            copy.write_text(planted, encoding="utf-8", newline="\n")
            found = [f for f in build.check_numbers(root)[0] if PAGE["file"] in f and "'4'" in f]
            out.append(("unsourced-sentence", bool(found),
                        "a hand-typed count on %s, outside any fact's mark: %s"
                        % (PAGE["file"], found[0] if found else "passed")))
    return out
