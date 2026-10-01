"""Thread: Film & photography (docs/SPEC.md, thread 2)."""
import facts
from facts import V, fact
import mapgen
from render import C, L, esc, render

PAGE = {"file": "thread-film.html", "nav": "Threads", "title": "Film & photography — loganw.dev",
        "description": "CanonBracketTool through the darkroom to a quantum-grown film stock, and what StoryDocs "
                       "took out of the middle of it: the thread's account, its part of the map, and its door."}


def account():
    P = facts.prose
    paras = []
    paras.append(render([
        "The earliest work here is bare, by Logan's own account: CanonBracketTool, ",
        facts.api_description("CanonBracketTool"), ", and Microscope-Stacker, ",
        facts.api_description("Microscope-Stacker"), "."]))
    paras.append(render([
        "atlas-darkroom grew out of the same cloud atlas as the Determinism thread's PrettyCloud: ",
        P("atlas-darkroom", "README.md",
          r"^(A print engine for the \[Atlas of Mathematical Forms\]\(https://github\.com/loganw234/PrettyCloud\))"),
        ". It is ", facts.api_visibility(["atlas-darkroom"]), " for now. Extracted from it with their history "
        "carried: atlas-optical, ",
        P("atlas-optical", "README.md", r"^(The glass of the Eidograph, on its own)"),
        " (", facts.api_visibility(["atlas-optical"]), " for now); and atlas-film, ",
        P("atlas-film", "README.md", r"^(The medium of the Eidograph)"), "."]))
    paras.append(render([
        "atlas-film underlies Quantum-Film, ",
        P("Quantum-Film", "README.md", r"^\*\*(Film stocks whose crystals are laid by quantum circuits)"),
        ", checked at ", facts.stage_count("Quantum-Film", "verify/run.sh"), " runner stages — the prints on "
        "Map & Ledger are its output."]))
    paras.append(render([
        "StoryDocs, ", P("StoryDocs", "README.md", r"^Books and papers compiled from (Markdown manifests)",
                         display="a book-and-paper pipeline built from Markdown manifests"),
        ", was ", P("StoryDocs", "README.md", r"(taken out of atlas-darkroom)"),
        " — the book side is the pipeline the Eidograph volumes were made with; the paper side, new, is a hybrid "
        "of a research paper and that book's own idiom. It is ", facts.api_visibility(["StoryDocs"]),
        " for now, born ", facts.born("StoryDocs"), ". It has since touched half of the map's other projects, "
        "which the arrows out of it show, derived from its projects/ directories rather than typed by hand."]))
    return "".join('<p>%s</p>' % p for p in paras)


def door():
    return facts.stated("bring a process — a development recipe, a claimed printing method, or a historical "
                        "process's parameters — and see it reproduced to the same bits, or shown where it "
                        "doesn't.", "Logan", "2026-09-29")


def render_page(ctx):
    door_html = render(door())
    if "Propose" in ctx["built"]:
        door_body = '<p class="cta">%s <a href="%s">Propose a thread</a>.</p>' % (door_html, ctx["built"]["Propose"])
    else:
        door_body = '<p class="cta">%s The Propose page isn’t built yet, so this isn’t a link.</p>' % door_html
    return ('<div class="measure"><p class="lede">Bare beginnings, a shared darkroom, and a pipeline that outgrew '
           'the room it was built in.</p></div>'
           '<h2><small>I</small>The account</h2>%s'
           '<h2><small>II</small>This thread’s part of the map</h2>%s'
           '<h2><small>III</small>Its door</h2>%s'
           % (account(), mapgen.lane_slice(1), door_body))
