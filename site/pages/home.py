"""Home: the current truth, on one page (docs/SPEC.md, "Home").

Everything here is read at the pins through facts.py, or said to be stated.
The ledger's rows are the projects the site covers so far; the round adds the
threads and work pages that explain them.
"""
import datetime

import facts
from facts import V, fact
import mapgen
from render import C, L, SOURCE_REPO, esc, render

PAGE = {"file": "index.html", "nav": "Home", "title": "Logan W. — loganw.dev",
        "description": "Logan W.'s projects, and the record behind every figure about them."}

PRINTS = [("pauli-print.png", "Pauli"), ("poisson-print.png", "Poisson"), ("trix-print.png", "TRI-X")]
ASSETS = [("assets/" + f, "Quantum-Film", "docs/prints/" + f) for f, _ in PRINTS]

LEDGER_CAP = ("Each figure names where it was read: a repository at the commit in the footer, or the GitHub snapshot. "
              "<i>Last verified</i>: the newest recorded pass of the repository's own gate at or before its pin, on "
              "its author's calendar &mdash; a run of a workflow pins.json classes as verifying, on the pinned commit "
              "or an ancestor of it, or a ledger line in a form pins.json declares as a pass; a dash means neither "
              "records one. <i>Agent-credited</i>: commits with a Co-Authored-By line naming Claude or Gemini, of all "
              "its commits &mdash; a trailer, not a line count, and a lower bound: ")

# Logan, 2026-09-29, correcting the lead's reading of that column: the counts
# are honest, and they are not a measure of how much of a project an agent did.
# His words are recorded in docs/SPEC.md (decision 23); this is their meaning.
AI_USE = "every project here was AI-driven, and the co-author line was not always added to its commits"

# Drafted by the lead from the spec's own words (docs/SPEC.md, section 1: "carpenter
# since fifteen", "no formal training", "agents write essentially all the lines",
# "gates decide what's true"), and approved by Logan on 2026-09-29: "Biography is
# good" (decision 14). Until then the page labelled it a draft.
WHO = ("I'm Logan. I have worked as a carpenter since I was fifteen, and I have no formal training in computing. "
       "AI agents have written essentially all of the code in these projects; gates decide what is true, and the "
       "record keeps what they said.")


def S(text, **kw):
    return facts.stated(text, "Logan", "2026-09-29", **kw)


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
    P = facts.prose
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
                    " on main; ", S("a revision-7 round is under way off main", holds_at={"cft-fp256": "77b8440"})],
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
                      r"(openXC7's router does not converge on the tile, what to change in it and in what order, and "
                      r"why a fork of it \(loganw234/nextpnr-xilinx, `dense`\) starts at the pinned 0\.9\.6)",
                      display="a fork of openXC7's router, which does not converge on the tile")],
                   ["listed, not covered here"],
                   [L(facts.repo_meta("nextpnr-xilinx")["url"], "repository")]))
    out.append(row(T, "ParcelRound",
                   [P("ParcelRound", "README.md",
                      r"^(A method for splitting one body of work across several coding agents\s+at\s+once)")],
                   [facts.count_paths("ParcelRound", r"CASE-STUDY(-\d+)?\.md", "CASE-STUDY*.md files at the pin"),
                    " rounds recorded; METHOD.md last changed ", facts.last_change("ParcelRound", "METHOD.md")],
                   [L(facts.pin("ParcelRound").href("CASE-STUDY-4.md"), facts.exists("ParcelRound", "CASE-STUDY-4.md"))]))
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
    url = P("Quantum-Film", "README.md", r"\]\((https://loganw234\.github\.io/Quantum-Film/)\)")
    out.append(row(T, "Quantum-Film",
                   [P("Quantum-Film", "README.md", r"^\*\*(Film stocks whose crystals are laid by quantum circuits)")],
                   [facts.stage_count("Quantum-Film", "verify/run.sh"), " runner stages"],
                   [L(url.raw, P("Quantum-Film", "README.md", r"^- \*\*(The web demo)\*\*, live at"))]))
    T = "Preservation"
    out.append(row(T, "Mercenaries2",
                   [P("Mercenaries2", "README.md", r"^(A revival project for \*\*Mercenaries 2: World in Flames\*\*)")],
                   ["online play through ", P("Mercenaries2", "README.md", r"The public server at `(refesl\.live)`")],
                   [L(facts.pin("Mercenaries2").href("README.md"), facts.exists("Mercenaries2", "README.md"))]))
    out.append(row(T, "mercs2-lua-essentials",
                   [C("Ess"), ", ", P("mercs2-lua-essentials", "README.md",
                                      r"^`Ess` — (the foundational Lua library for Mercenaries 2 modding)")],
                   ["one of ", facts.family("(mercs2-|merc2-|wad-simulator)", ["Merc2-Mods-Exp"]),
                    " public mercs2 repositories"],
                   [L(facts.repo_meta("mercs2-lua-essentials")["url"], "repository")]))
    return out


def ledger_table():
    head = ("<thead><tr><th>project</th><th>what it is</th><th>state</th><th>last verified</th>"
            "<th class=\"n\">agent-credited</th><th>check it</th></tr></thead>")
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
    url = P("cft-fp256", "README.md", r"\*\*<(https://loganw234\.github\.io/cft-fp256/)>\*\*")
    items = [
        ["cft-fp256's web page ", L(url.raw, P("cft-fp256", "README.md",
                                               r"It (replays\s+the published conformance vectors in front of you)")),
         ". Nothing to install."],
        [C("make golden"), " in a clone of cft-fp256: ", P("cft-fp256", "README.md", r"^(The golden model's self-tests)"), "."],
        [C("make verify-quick"), ": ",
         P("cft-fp256", "CLAUDE.md", r"^make verify-quick\s+# (~\d+ min, \d+ of \d+ stages)", num=True), "."],
        [C("python site/build.py --verify-facts"), " in a clone of ", L(SOURCE_REPO, "this site"),
         ": every figure on this page read again, from its repository at its pin or from the committed GitHub "
         "snapshot. A figure from a private repository is skipped by name."],
    ]
    return "<ol>%s</ol>" % "".join("<li>%s</li>" % render(i) for i in items)


def not_here():
    P = facts.prose
    items = [
        [C("atlas-darkroom"), " and ", C("atlas-optical"), " are ", facts.api_visibility(["atlas-darkroom", "atlas-optical"]),
         " for now. HonestFramework's case study has a row for each, ",
         P("HonestFramework", "CASE-STUDY.md", r"^\| `(atlas-darkroom)` \|"), " and ",
         P("HonestFramework", "CASE-STUDY.md", r"^\| `(atlas-optical)` \|"),
         ", and those rows cannot be checked from here yet."],
        [S("Nothing here is for sale, and there is no newsletter.")],
    ]
    return '<ul class="plain">%s</ul>' % "".join("<li>%s</li>" % render(i) for i in items)


def prints():
    P = facts.prose
    figs = "".join('<figure><img src="assets/%s" alt="The %s print" width="512" height="512" loading="lazy">'
                   '<figcaption>%s</figcaption></figure>' % (f, esc(alt), esc(alt)) for f, alt in PRINTS)
    # Each print's own last commit: the folder's is a later commit that wrote
    # another file there (ec65c44), and the verifier found the first caption
    # naming the pin instead (a7f02db). One caption holds only if they agree.
    laid = [facts.last_commit("Quantum-Film", "docs/prints/" + f) for f, _ in PRINTS]
    if len({v.text for v in laid}) != 1:
        raise facts.Refusal("the prints were last written by different commits (%s); caption each one"
                            % ", ".join(v.text for v in laid))
    cap = render([P("Quantum-Film", "README.md", r"(Pauli, its Poisson twin and TRI-X) below"),
                  ", as Quantum-Film's commit ", laid[0], " laid them. ",
                  P("ParcelRound", "CASE-STUDY-4.md", r"(Every print re-developed to the same bits) \(`--check`\)"),
                  " when checked."])
    return '<div class="prints">%s</div><p class="cap">%s</p>' % (figs, cap)


def render_page(ctx):
    who = facts.stated(WHO, "Logan", "2026-09-29")
    cap = LEDGER_CAP + render(["Logan's word is that ", S(AI_USE), "."])
    return ('<div class="measure"><p class="lede">%s</p></div>'
            '<h2><small>I</small>Where each project came from</h2>%s'
            '<h2><small>II</small>Ledger</h2><div class="table-wrap">%s</div><p class="cap">%s</p>'
            '<div class="measure"><h2><small>III</small>Check it yourself</h2><div class="cta"><p>Don\'t trust this page.</p>%s</div>'
            '<h2><small>IV</small>The film thread</h2>%s'
            '<h2><small>V</small>Not here</h2>%s</div>'
            % (render(who), mapgen.block(), ledger_table(), cap, checks(), prints(), not_here()))


def controls():
    """A red run, planted in the snapshot: Home shows it as an open regression,
    and a run with no verdict is passed over. atlas-film is public, so this runs
    wherever its pin can be fetched."""
    out = []
    name, wf = "atlas-film", facts.verifying("atlas-film")[0]
    p = facts.pin(name)
    runs = facts.snap()["runs"].setdefault(name, [])
    newest = max(r["created"] for r in runs) if runs else "2026-01-01T00:00:00Z"
    later = (datetime.datetime.fromisoformat(newest.replace("Z", "+00:00")) + datetime.timedelta(hours=1)
             ).strftime("%Y-%m-%dT%H:%M:%SZ")
    for conclusion, red in (("failure", True), ("timed_out", True), ("startup_failure", True),
                            ("cancelled", False), ("action_required", False)):
        plant = dict(workflow=wf, sha=p.full, branch="main", status="completed", conclusion=conclusion,
                     created=later, url="https://example.invalid/planted")
        runs.append(plant)
        try:
            html = render(row("planted", name, ["x"], ["x"], ["x"])["state"])
        finally:
            runs.remove(plant)
        shown = "open: " in html and "red on" in html
        out.append(("red-run", shown == red, "a %s run on %s's pin was %s" % (
            conclusion, name, "shown as open" if shown else "passed over, as a run with no verdict must be"
            if not red else "NOT SHOWN")))
    return out
