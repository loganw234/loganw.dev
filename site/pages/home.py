"""Home: the current truth, on one page (docs/SPEC.md, "Home").

Everything here is read at the pins through facts.py, or said to be stated.
The ledger's rows are the projects the site covers so far; the round adds the
threads and work pages that explain them.
"""
import facts
from facts import V, fact
import mapgen
from render import C, L, SOURCE_REPO, esc, render

PAGE = {"file": "index.html", "nav": "Home", "title": "Logan W. — loganw.dev",
        "description": "Logan W.'s projects, and the record behind every figure about them."}

PRINTS = [("pauli-print.png", "Pauli"), ("poisson-print.png", "Poisson"), ("trix-print.png", "TRI-X")]
ASSETS = [("assets/" + f, "Quantum-Film", "docs/prints/" + f) for f, _ in PRINTS]

LEDGER_CAP = ("Each row is read from the repository it names, at the commit in the footer. <i>Last verified</i>: the "
              "newest recorded pass of the repository's own gate at or before its pin &mdash; a CI workflow that "
              "passed on the pinned commit or an ancestor of it, or a ledger line that records a pass, as pins.json "
              "declares for each; a dash means none is recorded. <i>Agent-written</i>: commits carrying a Claude or "
              "Gemini Co-Authored-By trailer, of all its commits &mdash; a trailer, not a line count.")


@fact
def unread_gate(name):
    """A repository read only through the snapshot: its gate runs are not read."""
    return V("—", facts.api_src(name, "read only through the GitHub snapshot; no gate runs are read for it"),
             raw="", num=True)


@fact
def fork_agents(name):
    """A fork's history is mostly its parent's: nextpnr-xilinx showed 45/3397,
    a true count of the wrong commits. So a fork gets a dash, and the reason."""
    if not facts.repo_meta(name).get("isFork"):
        raise facts.Refusal("%s is not a fork" % name)
    return V("—", facts.api_src(name, "a fork: a count over its history would mostly count its parent's "
                                            "commits, so none is given"), raw="", num=True)


def row(thread, name, what, state, check):
    pinned = name in facts.PINS["repos"]
    meta = facts.repo_meta(name)
    project = L(meta["url"], name) if facts.is_public(name) else name
    if pinned:
        last, agent, red = facts.last_verified(name), facts.agents(name), facts.ci_red(name)
        if red.text:
            state = state + [" · open: ", red]
    else:
        last = unread_gate(name)
        agent = fork_agents(name) if meta.get("isFork") else facts.api_agents(name)
    return dict(thread=thread, project=project, what=what, state=state, last=last, agent=agent, check=check)


def rows():
    P, S = facts.prose, facts.stated
    out = []
    T = "Determinism"
    out.append(row(T, "PrettyCloud",
                   [P("PrettyCloud", "README.md", r"^(A WebGL2 point-cloud atlas)\.")],
                   ["served at ", P("PrettyCloud", "README.md", r"served at (prettycloud\.io)")],
                   [L("https://prettycloud.io/", "open it")]))
    out.append(row(T, "atlas-engine",
                   [P("atlas-engine", "README.md", r"^(A language for platonography),")],
                   [P("atlas-engine", "README.md", r"\*\*(Sixty-eight of sixty-eight, one hash)\.\*\*")],
                   ["cft-fp256's ", C("photograph"), " stage, ",
                    P("cft-fp256", "README.md", r"`photograph`\s+stage reruns it in (a minute and a half)")]))
    out.append(row(T, "cft-fp256",
                   [P("cft-fp256", "README.md", r"^\*\*(A math coprocessor that gets the same answer everywhere)\.\*\*")],
                   ["ABI ", facts.macros("cft-fp256", "host/include/cft.h",
                                         ["CFT_ABI_VERSION_MAJOR", "CFT_ABI_VERSION_MINOR"]),
                    " on main; ", S("a revision-7 round is under way off main")],
                   [C("make verify-quick"), ", ",
                    P("cft-fp256", "CLAUDE.md", r"^make verify-quick\s+# (~\d+ min, \d+ of \d+ stages)", num=True)]))
    out.append(row(T, "cft-rebound",
                   [P("cft-rebound", "README.md", r"^(REBOUND's IAS15 integrator with its arithmetic routed through libcft)")],
                   [P("cft-rebound", "README.md", r"(At binary64 it is\s+REBOUND's own IAS15 bit for bit)")],
                   [C("make check-quick"), ", ", P("cft-fp256", "CLAUDE.md", r"the (\d+-second warm)\s+`make check-quick`")]))
    out.append(row(T, "binary-sites",
                   [P("binary-sites", "README.md", r"^(Four sites, one per IEEE 754 binary interchange format)")],
                   [facts.api_visibility(["binary-sites"]), " for now; ",
                    P("binary-sites", "README.md", r"^\*\*(binary32\.com · binary64\.com · binary128\.com · binary256\.com)\*\*")],
                   ["—"]))
    out.append(row(T, "nextpnr-xilinx",
                   [P("cft-fp256", "docs/README.md",
                      r"(a fork of it \(loganw234/nextpnr-xilinx, `dense`\) starts at the pinned 0\.9\.6)",
                      display="a fork of openXC7's router for the tile's dense routing")],
                   ["listed, not covered here"],
                   [L(facts.repo_meta("nextpnr-xilinx")["url"], "repository")]))
    out.append(row(T, "ParcelRound",
                   [P("ParcelRound", "README.md",
                      r"^(A method for splitting one body of work across several coding agents\s+at\s+once)")],
                   [facts.count_paths("ParcelRound", r"CASE-STUDY(-\d+)?\.md", "CASE-STUDY*.md files at the pin"),
                    " rounds recorded; METHOD.md last changed ", facts.last_change("ParcelRound", "METHOD.md")],
                   [L("https://github.com/loganw234/ParcelRound/blob/%s/CASE-STUDY-4.md" % facts.pin("ParcelRound").full,
                      "case study 4")]))
    out.append(row(T, "HonestFramework",
                   [P("HonestFramework", "README.md",
                      r"^(A way to lay out a project so that an AI can write nearly all of it\s+and\s+"
                      r"\*\*no claim about it ever rests on the AI's judgement\*\*)")],
                   [P("HonestFramework", "README.md", r"The (\w+) mechanisms\. Start here"),
                    " mechanisms, and a gate of its own"],
                   [C("python " + facts.exists("HonestFramework", "tools/check_claims.py").text)]))
    T = "Film & photography"
    for name in ("CanonBracketTool", "Microscope-Stacker"):
        out.append(row(T, name, [facts.api_description(name)], [S("a beginning project, from before the method")],
                       [L(facts.repo_meta(name)["url"], "repository")]))
    out.append(row(T, "atlas-darkroom",
                   [P("atlas-darkroom", "README.md",
                      r"^(A print engine for the \[Atlas of Mathematical Forms\]\(https://github\.com/loganw234/PrettyCloud\))")],
                   [facts.api_visibility(["atlas-darkroom"]), " for now"], ["—"]))
    out.append(row(T, "atlas-optical",
                   [P("atlas-optical", "README.md", r"^(The glass of the Eidograph, on its own)")],
                   [facts.api_visibility(["atlas-optical"]), " for now; spun out of atlas-darkroom ",
                    P("atlas-optical", "README.md", r"Extracted whole from\s+atlas-darkroom on (\d{4}-\d{2}-\d{2})", num=True)],
                   ["—"]))
    out.append(row(T, "atlas-film",
                   [P("atlas-film", "README.md", r"^(The medium of the Eidograph)")],
                   ["branch ", C("pinned"), " at ",
                    P("ParcelRound", "CASE-STUDY-4.md", r"\*\*atlas-film's `pinned`\*\* at `([0-9a-f]{7})`", num=True),
                    ", ", P("ParcelRound", "CASE-STUDY-4.md", r"(Whether atlas-film's `pinned` merges into its main)",
                            display="its merge left open")],
                   [L(facts.pin("atlas-film").href("PROVENANCE.md"), facts.exists("atlas-film", "PROVENANCE.md"))]))
    demo = P("Quantum-Film", "README.md", r"(https://loganw234\.github\.io/Quantum-Film/)", display="the web demo")
    out.append(row(T, "Quantum-Film",
                   [P("Quantum-Film", "README.md", r"^\*\*(Film stocks whose crystals are laid by quantum circuits)")],
                   [facts.stage_count("Quantum-Film", "verify/run.sh"), " runner stages"],
                   [L(demo.raw, demo)]))
    T = "Preservation"
    out.append(row(T, "Mercenaries2",
                   [P("Mercenaries2", "README.md", r"^(A revival project for \*\*Mercenaries 2: World in Flames\*\*)")],
                   ["online play through ", P("Mercenaries2", "README.md", r"The public server at `(refesl\.live)`")],
                   [L("https://github.com/loganw234/Mercenaries2/blob/%s/README.md" % facts.pin("Mercenaries2").full,
                      "README")]))
    out.append(row(T, "mercs2-lua-essentials",
                   [C("Ess"), ", ", P("mercs2-lua-essentials", "README.md",
                                      r"^`Ess` — (the foundational Lua library for Mercenaries 2 modding)")],
                   ["one of ", facts.family("(mercs2-|merc2-|wad-simulator)", ["Merc2-Mods-Exp"]), " public mercs2 tools"],
                   [L(facts.repo_meta("mercs2-lua-essentials")["url"], "repository")]))
    return out


def ledger_table():
    head = ("<thead><tr><th>project</th><th>what it is</th><th>state</th><th>last verified</th>"
            "<th class=\"n\">agent-written</th><th>check it</th></tr></thead>")
    body, thread = [], None
    for r in rows():
        if r["thread"] != thread:
            thread = r["thread"]
            body.append('<tr class="th"><td colspan="6">%s</td></tr>' % esc(thread))
        body.append('<tr><td class="p">%s</td><td>%s</td><td>%s</td><td class="d">%s</td><td class="n">%s</td><td>%s</td></tr>'
                    % tuple(render(r[k]) for k in ("project", "what", "state", "last", "agent", "check")))
    return "<table>%s<tbody>%s</tbody></table>" % (head, "".join(body))


def checks():
    P = facts.prose
    url = P("cft-fp256", "README.md", r"\*\*<(https://loganw234\.github\.io/cft-fp256/)>\*\*",
            display="Replay the published conformance vectors")
    items = [
        [L(url.raw, url), " in your browser. Nothing to install."],
        [C("make golden"), " in a clone of cft-fp256: ",
         P("cft-fp256", "README.md", r"^(The golden model's self-tests)", display="the golden model's self-tests"), "."],
        [C("make verify-quick"), ": ",
         P("cft-fp256", "CLAUDE.md", r"^make verify-quick\s+# (~\d+ min, \d+ of \d+ stages)", num=True), "."],
        [C("python site/build.py --verify-facts"), " in a clone of ", L(SOURCE_REPO, "this site"),
         ": every figure on this page read again at its pin, or skipped by name where the repository is private."],
    ]
    return "<ol>%s</ol>" % "".join("<li>%s</li>" % render(i) for i in items)


def not_here():
    P = facts.prose
    P("HonestFramework", "CASE-STUDY.md", r"^\| `(atlas-darkroom)` \|")   # "cites both" must be true of both
    items = [
        [C("atlas-darkroom"), " and ", C("atlas-optical"), " are ", facts.api_visibility(["atlas-darkroom", "atlas-optical"]),
         " for now. HonestFramework's case study ",
         P("HonestFramework", "CASE-STUDY.md", r"^\| `(atlas-optical)` \|", display="cites both"),
         ", so those citations cannot be checked from here yet."],
        [facts.stated("Nothing here is for sale, and there is no newsletter.")],
    ]
    return '<ul class="plain">%s</ul>' % "".join("<li>%s</li>" % render(i) for i in items)


def prints():
    P = facts.prose
    q = facts.pin("Quantum-Film")
    figs = "".join('<figure><img src="assets/%s" alt="The %s print" width="512" height="512" loading="lazy">'
                   '<figcaption>%s</figcaption></figure>' % (f, esc(alt), esc(alt)) for f, alt in PRINTS)
    cap = render([P("Quantum-Film", "README.md", r"(Pauli, its Poisson twin and TRI-X) below"),
                  ", laid by Quantum-Film at ", L(q.href(), C(q.short)), ". ",
                  P("ParcelRound", "CASE-STUDY-4.md", r"(Every print re-developed to the same bits) \(`--check`\)"),
                  " when checked."])
    return '<div class="prints">%s</div><p class="cap">%s</p>' % (figs, cap)


def render_page(ctx):
    who = facts.stated("I'm Logan. I have worked as a carpenter since I was fifteen, and I have no formal training "
                       "in computing. From PrettyCloud on, AI agents have written essentially all of the code; gates "
                       "decide what is true, and the record keeps what they said.")
    return ('<div class="measure"><p class="lede">%s</p></div>'
            '<h2><small>I</small>Where each project came from</h2>%s'
            '<h2><small>II</small>Ledger</h2><div class="table-wrap">%s</div><p class="cap">%s</p>'
            '<div class="measure"><h2><small>III</small>Check it yourself</h2><div class="cta"><p>Don\'t trust this page.</p>%s</div>'
            '<h2><small>IV</small>The film thread</h2>%s'
            '<h2><small>V</small>Not here</h2>%s</div>'
            % (render(who), mapgen.block(), ledger_table(), LEDGER_CAP, checks(), prints(), not_here()))
