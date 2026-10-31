"""Thread: Determinism (docs/SPEC.md, thread 1). One of three thread pages;
the section's own page is threads.py. Every sentence that states a fact
about a project is sourced or stated, as the common rules require.
"""
import facts
from facts import V, fact
import mapgen
from pages import _dossier
from render import C, L, esc, render

PAGE = {"file": "thread-determinism.html", "nav": "Threads",
        "title": "Determinism — loganw.dev",
        "description": "Bit-identical arithmetic, from a point cloud to an integrator: the thread's account, "
                       "its part of the map, and its door."}

# The heading's line, at cft-fp256's pin, of the ledger entry that records the audit of muse-softfloat
# (_dossier.ledger_date refuses a line that is no heading, so a pin that moves it refuses the build).
ISSUE_1 = 26149


def account():
    P = facts.prose
    paras = []
    paras.append(render([
        "It starts with a picture, and ends with a promise that the picture's numbers hold wherever they run. ",
        P("PrettyCloud", "README.md", r"^(A WebGL2 point-cloud atlas)\."), ". Its shapes wanted a language of "
        "their own: ", P("atlas-engine", "README.md", r"^(A language for platonography),"),
        " re-running ", P("atlas-engine", "README.md", r"\*\*(Sixty-eight of sixty-eight, one hash)\.\*\*"),
        " against the plates it draws."]))
    paras.append(render([
        "The language needed arithmetic that could not drift between machines, which is what cft-fp256 is: ",
        P("cft-fp256", "README.md", r"^\*\*(A math coprocessor that gets the same answer everywhere)\.\*\*"),
        ". Its ABI is ", facts.macros("cft-fp256", "host/include/cft.h",
                                      ["CFT_ABI_VERSION_MAJOR", "CFT_ABI_VERSION_MINOR"]),
        " on main, checked by ", C("make verify-quick"), " (",
        P("cft-fp256", "CLAUDE.md", r"^make verify-quick\s+# (~\d+ min, \d+ of \d+ stages)", num=True), ") and ",
        C("make verify-gate"), " (",
        P("cft-fp256", "CLAUDE.md", r"^make verify-gate\s+# (~\d+ h quiet, \d+ of \d+ - what a change should pass)",
          num=True), ")."]))
    paras.append(render([
        "The same repository also holds a language: ",
        P("cft-fp256", "docs/LANGUAGE.md",
          r"^(A small text language for dynamical systems - ordinary differential\s+equations and maps - whose "
          r"every rounding is fixed by the text)\."),
        "; and certificates: ",
        P("cft-fp256", "docs/CERTIFICATES.md",
          r"^(A certificate is a text file that says what a deterministic run was and\s+how accurate it is)"),
        "."]))
    paras.append(render([
        "Built on it: ",
        P("cft-rebound", "README.md", r"^(REBOUND's IAS15 integrator with its arithmetic routed through libcft)"),
        ": ", P("cft-rebound", "README.md", r"(At binary64 it is\s+REBOUND's own IAS15 bit for bit)"),
        ". The method itself was distilled out of this work: cft-rebound's own round history says it was ",
        P("cft-rebound", "docs/PARCEL-ROUNDS.md", r"(lifted into a standalone repository)",
          display="lifted into a standalone repository"), ", ParcelRound, ",
        P("ParcelRound", "README.md",
          r"^(A method for splitting one body of work across several coding agents\s+at\s+once)"),
        "; and cft-fp256's case study in HonestFramework, ",
        P("HonestFramework", "README.md",
          r"^(A way to lay out a project so that an AI can write nearly all of it\s+and\s+"
          r"\*\*no claim about it ever rests on the AI's judgement\*\*)"), "."]))
    # The lane's newer nodes (docs/SPEC.md decision 48), each said in its own README's words at its pin, and the
    # audit cft-fp256's ledger records of one of them. The kit's README also says the repository "stays private":
    # no pattern here reaches those lines (decision 47). The ledger entry's subject is quoted from the words that
    # follow its heading's own subject, which the pattern skips without naming (decision 49 and Corrections'
    # signature row: no word of the heading's subject is printed on this page).
    paras.append(render([
        "Newer in this lane, and carrying HonestFramework and ParcelRound to other models: softfloat-bootstrap is “",
        P("softfloat-bootstrap", "README.md",
          r"^(The builder of the bootstrap kit for Logan's Meta AI hackathon, 2026-10-26 to 2026-11-04):"),
        ".” Its README says of the agents the kit is for: “",
        P("softfloat-bootstrap", "README.md",
          r"(The agents work in a clean room: they may not read cft-fp256, which already implements this "
          r"arithmetic)\."),
        ".” muse-softfloat is “",
        P("muse-softfloat", "README.md",
          r"^(An IEEE 754 softfloat library for the RP2040 — binary16, binary32 and binary64 —\s+built with Meta's "
          r"Muse models under two working methods,\s+\[HonestFramework\]\([^)]*\) and ParcelRound)"),
        ",” and its README adds “",
        P("muse-softfloat", "README.md",
          r"\((the owner's methods, carried in the hackathon bootstrap kit, not in this\s+repository)\)"),
        ".” Its README names the workload that proves it in public: “",
        P("muse-softfloat", "README.md",
          r"The workload that proves it in public: \*\*(REBOUND's IAS15 integrator running on a\s+Raspberry Pi Pico "
          r"through this library, bit-identical to the unmodified desktop\s+run)\*\*"),
        ".”"]))
    paras.append(render([
        "cft-fp256's ledger records a report that came, in its words, from “",
        P("cft-fp256", "docs/VALIDATION.md",
          r"from (a clean-room audit of loganw234/muse-softfloat \(binary16/32/64\), cross-tested against this "
          r"library and an exact arbiter)\."),
        ".” Of what the audit found, the entry of ", _dossier.ledger_date("cft-fp256", "docs/VALIDATION.md", ISSUE_1),
        " says “",
        P("cft-fp256", "docs/VALIDATION.md",
          r"(The four cases it found at binary32 and binary64 were the one disagreement between the two libraries "
          r"that was a defect)\."),
        ",” and names it: “",
        P("cft-fp256", "docs/VALIDATION.md",
          r"^## 2026-10-30 - [^:]+: (exp2m1\(emax \+ 1\) toward zero raised overflow, in the golden model, the C, the "
          r"vectors and the WebAssembly module); "),
        ".”"]))
    paras.append(render([
        "HonestFramework and ParcelRound also run on open-weight models: HonestHarness is “",
        P("HonestHarness", "README.md",
          r"^(A harness for running \[ParcelRound\]\([^)]*\)\s+and \[HonestFramework\]\([^)]*\) on\s+"
          r"open-weight models)\."),
        ".”"]))
    paras.append(render([
        "binary-sites is ", facts.api_visibility(["binary-sites"]), " for now: ",
        P("binary-sites", "README.md", r"^(Four sites, one per IEEE 754 binary interchange format)"), ", ",
        P("binary-sites", "README.md", r"^\*\*(binary32\.com · binary64\.com · binary128\.com · binary256\.com)\*\*"),
        "."]))
    created = mapgen.api_created("nextpnr-xilinx")
    paras.append(render([
        "nextpnr-xilinx is a fork, kept for one FPGA target ",
        P("cft-fp256", "docs/README.md",
          r"(openXC7's router does not converge on the tile, what to change in it and in what order, and "
          r"why a fork of it \(loganw234/nextpnr-xilinx, `dense`\) starts at the pinned 0\.9\.6)",
          display="a fork of openXC7's router, which does not converge on the tile"),
        ". The map places it on ", created,
        " — read as when GitHub made the fork itself, never a commit: a fork's own commits are mostly its "
        "parent's, and this one's earliest, ", facts.api_born("nextpnr-xilinx"), ", is upstream's, from before "
        "this project existed."]))
    return "".join('<p>%s</p>' % p for p in paras)


def door():
    return facts.stated("workloads (bring one — if it fits libcft it runs bit-identical everywhere; the "
                        "record is the deliverable)", "Logan", "2026-09-29")


def render_page(ctx):
    door_html = render(door())
    if "Propose" in ctx["built"]:
        door_body = '<p class="cta">%s <a href="%s">Propose a thread</a>.</p>' % (door_html, ctx["built"]["Propose"])
    else:
        door_body = '<p class="cta">%s The Propose page isn’t built yet, so this isn’t a link.</p>' % door_html
    return ('<div class="measure"><p class="lede">Bit-identical arithmetic: a picture, a language for it, a '
           'coprocessor that will not drift, and what got built once it existed.</p></div>'
           '<h2><small>I</small>The account</h2>%s'
           '<h2><small>II</small>This thread’s part of the map</h2>%s'
           '<h2><small>III</small>Its door</h2>%s'
           % (account(), mapgen.lane_slice(0), door_body))
