"""Resume: Logan's resume, unlisted (docs/SPEC.md, decision 42). It is
reached by its address alone: it claims no navigation entry, carries
render.NOINDEX, and build.check_links refuses a link to it from any other
page. Unlisted is not private: the page is published, MANIFEST names it,
and facts.json holds its figures like any other page's.

It is held to the site's own rules, and at Logan's word ("Id also prefer
more come from cited sources than my claims where able", 2026-10-15) most of
it is the projects' own words, each quoted at its pin and labelled with the
file and line. What only Logan can say is a statement:
  - his role, his summary, cft-fp256 as his experiment, and the Moth Hack
    result were drafted from his draft resume of 2026-10-15, and Logan
    approved them as printed on 2026-10-16: "Also statements by me are
    approved" (decision 46);
  - the background is Home's biography and About's first approved sentence,
    printed as Logan approved them, so they carry no draft label.
pages._settled holds every statement here to those two kinds, as it holds
About's and the front page's.

At Logan's word of 2026-10-16 (decision 45), it reads without its sources
first: every figure carries its own label as a tooltip, and the stylesheet
hides the labels beside the figures until a reader opens "Show every source
beside its line" (site/data/css_hides.json names the rule). The page prints
as resume.pdf, which printout.py writes from the page's text twin,
resume.txt, and from nothing else.
"""
import dataclasses

import facts
import printout
from facts import V, fact, prose
from pages import _settled, about, front
from render import L, esc, render as _render

PAGE = {"file": "resume.html", "nav": None, "unlisted": True, "title": "Resume — loganw.dev",
        "description": "Logan's resume: every passage read from its project at the commit this site pins names "
                       "its source, and his own words are marked as his."}

DRAFTED = "2026-10-15"   # the day Logan gave his draft resume

# Logan's own words, from his draft resume, drafted here and not yet approved.
ROLE = "Independent project lead"
SUMMARY = ("I direct AI agents through engineering and research work beyond my own implementation expertise. I set "
           "the direction, review the evidence and decide what the record supports; the agents write essentially "
           "all of the code. What makes that workable is oversight that doesn't rest on the agents' word: checks "
           "that have been seen to fail, verifiers scored against planted faults, and dated records that keep the "
           "failed runs.")
EXPERIMENT = ("Used cft-fp256 to test how far one person without formal computing training can take a serious "
              "engineering effort with AI.")
WIN = "Winner, Quantum Native Repo category, Moth Hack 2026"
# The hackathon's results, for a reader, as Logan's draft links them. The
# build doesn't read it, so the result beside it stays his statement.
RESULTS = ("https://airtable.com/appfaqE6MpACGX3LN/shrKxNCu6BKEnDRVs?detail=eyJwYWdlSWQiOiJwYWdoWnN1YzFERmRxeVFweiIs"
           "InJvd0lkIjoicmVjN1ZzcmlDU2FaazVJNHgiLCJzaG93Q29tbWVudHMiOmZhbHNlLCJxdWVyeU9yaWdpbkhpbnQiOnsidHlwZSI6InBh"
           "Z2VFbGVtZW50IiwiZWxlbWVudElkIjoicGVsQ0pZYlE0ZGhBTmJqZ0wiLCJxdWVyeUNvbnRhaW5lcklkIjoicGVsNEVPbWVZZFhDYkVI"
           "VjIiLCJzYXZlZEZpbHRlclNldElkIjoic2ZzRjlpVGlzZWE2RWx5ZEsifX0")

# The day Logan approved the page's own statements as printed (decision 46).
APPROVED_ON = "2026-10-16"

# Every statement this page may print without a draft label, with the label
# it must carry: its words, who said them, and when (pages._settled).
SETTLED = {front.WHO: "stated by Logan, 2026-09-29",
           about.APPROVED[0]: "stated by Logan, 2026-09-30"}
SETTLED.update({s: "stated by Logan, %s" % APPROVED_ON for s in (ROLE, SUMMARY, EXPERIMENT, WIN)})

MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
HH_R1 = "Rounds/HonestHarness-R1/CASE-STUDY.md"


def render(segs):
    """Every figure here carries its label as a tooltip too (decision 45)."""
    return _render(segs, tip=True)


def S(text, **kw):
    return facts.stated(text, "Logan", DRAFTED, **kw)


def A(text):
    """Words Logan approved as printed: "Also statements by me are approved"
    (2026-10-16, decision 46)."""
    return facts.stated(text, "Logan", APPROVED_ON)


def D(text):
    """Words drafted from Logan's draft resume, not yet approved by him: the
    label says so until he approves them as printed."""
    return S(text, draft=True)


@fact
def first_month(name):
    """The month a repository began, as a resume gives a date ("Aug 2026"):
    facts.born's earliest author date at the pin, on its author's calendar.
    raw keeps the day."""
    b = facts.born(name)
    y, m, _ = b.raw.split("-")
    return V("%s %s" % (MONTHS[int(m) - 1], y), dataclasses.replace(b.src, detail=b.src.detail + "; its month"),
             raw=b.raw, num=True)


def q(v):
    """A quotation from a project: its words in curly quotes, then its source."""
    return ["“", v, "”"]


def flat(segs):
    out = []
    for s in segs:
        out.extend(flat(s) if isinstance(s, list) else [s])
    return out


def item(segs):
    return "<li>%s</li>" % render(flat(segs))


def project(name, since, items, evidence=None):
    """One project: its name, the month it began, its lines, and optionally
    where to look first."""
    out = ['<h3>%s <span class="when">since %s</span></h3><ul class="plain">' % (esc(name), render(since))]
    out += [item(i) for i in items]
    out.append("</ul>")
    if evidence:
        out.append('<p class="look">%s</p>' % render(flat(evidence)))
    return "".join(out)


def head_block():
    return ('<div class="measure"><p class="lede">%s</p>'
            '<p class="contact"><a href="mailto:logan@loganw.dev">logan@loganw.dev</a> · '
            '<a href="index.html">loganw.dev</a> · <a href="https://github.com/loganw234">github.com/loganw234</a></p>'
            '<p>%s</p>'
            '</div>'
            % (render([A(ROLE)]), render([A(SUMMARY)])))


def oversight_block():
    P, CS = prose, lambda pat, **kw: prose("HonestHarness", HH_R1, pat, **kw)
    items = [
        ["ParcelRound: ", q(P("ParcelRound", "README.md", r"^(A method for splitting one body of work across several "
                                                           r"coding agents\s+at\s+once, without the pieces failing to "
                                                           r"meet)\.")),
         ". It exists because ",
         q(P("ParcelRound", "README.md", r"It exists because (the obvious approach fails in a specific, repeatable\s+"
                                          r"way)\.")),
         ": ", q(P("ParcelRound", "README.md", r"(Give four agents four well-scoped parcels of one feature and you\s+"
                                                r"can get four green gates and a feature that does not work)")),
         ". ", facts.count_paths("ParcelRound", r"CASE-STUDY(-\d+)?\.md", "CASE-STUDY*.md files at the pin"),
         " rounds are recorded as case studies, and the sixth put ",
         q(P("ParcelRound", "README.md", r"(planted faults on every parcel's verifier)")), "."],
        ["HonestFramework: ",
         q(P("HonestFramework", "README.md", r"^(A way to lay out a project so that an AI can write nearly all of it"
                                              r"\s+and\s+\*\*no claim about it ever rests on the AI's judgement\*\*)")),
         ". Whether a claim is true ",
         q(P("HonestFramework", "README.md", r"(is answered by something\s+that cannot hold an opinion: a reference "
                                              r"implementation, a bit-identity\s+comparison, a hash, a gate that has "
                                              r"been watched to fail, an append-only\s+record with dates on it)\.")),
         "."],
        ["HonestHarness holds ",
         q(P("HonestHarness", "README.md", r"(the requirements, H1 to H17, derived from the record of cft-fp256's "
                                            r"rounds)")),
         ". Its first round asked: ",
         q(CS(r"(can a cheaper model, reached over an API, do\s+the skills a ParcelRound round measures)\?")),
         "? Replaying the planted faults of ParcelRound's sixth round, DeepSeek's flash model caught ",
         CS(r"\*\*The plants: (\d+ of \d+), by pass", num=True), ", where that round's own verifiers, on Opus, "
         "had caught ", CS(r"Round 6's Opus\s+verifiers caught (\d+ of \d+)\.", num=True), ". ",
         q(CS(r"\*\*(Every plant that changed a figure or a reference was caught in\s+every run, \d+ of \d+)\.\*\*")),
         ". ", q(CS(r"\*\*(Plants that changed meaning or shape were caught \d+ of \d+):\*\*")), "."],
        ["Where a suite stops telling strong models apart, the record says so: ",
         CS(r"\*\*QS6:\*\* (\d+ of \d+ runs exact)", num=True), ". ",
         q(CS(r"\*\*(So the QS6 slice cannot tell strong models apart)\.\*\*")), "."],
        ["This site is built the same way. In its second round each verifier, on Haiku, checked a copy of a "
         "parcel's work holding planted faults: ",
         q(facts.own_prose("docs/VALIDATION.md", r"(8 of 8 caught, each on its first pass)\.")), "."],
    ]
    evidence = ["Where to look first: ",
                L(facts.pin("ParcelRound").href("METHOD.md"), "ParcelRound's METHOD.md"), ", ",
                L(facts.pin("HonestHarness").href(HH_R1), "the case study of HonestHarness's first round"), "."]
    return ('<h2>Selected projects</h2>'
            + project("ParcelRound, HonestFramework and HonestHarness", first_month("ParcelRound"), items, evidence))


def cft_block():
    P = lambda pat, **kw: prose("cft-fp256", "README.md", pat, **kw)
    V_ = lambda pat, **kw: prose("cft-fp256", "docs/VALIDATION.md", pat, **kw)
    replay = P(r"^\*\*<(https://loganw234\.github\.io/cft-fp256/)>\*\*")
    items = [
        [q(P(r"^\*\*(A math coprocessor that gets the same answer everywhere)\.\*\*")), ": ",
         q(P(r"(It does IEEE 754 arithmetic at four precisions - 32, 64, 128 and 256\s+bits - and guarantees that "
             r"the same inputs give the same bits whether\s+the work runs on a laptop CPU, in a browser tab, on a "
             r"microcontroller,\s+or on the FPGA card it was designed for)\.")),
         ", the ", q(P(r"built for the\s+(AMD/Xilinx Alveo U50 through the open Vitis RTL kernel flow)")), "."],
        [A(EXPERIMENT), " ",
         q(P(r"(The rule is that a number in a document has a run behind it, and the\s+runs that failed stay in the "
             r"record)\.")), "."],
        ["Checked by ",
         q(P(r"\| (\d+ simulation targets checking every result and every flag against the golden model, and \d+ "
             r"machine-checked proofs, plus a negative control that must be refuted or the gate has stopped being "
             r"able to catch a bug)\. \|")),
         "; and ", q(P(r"\*\*(MPFR arbitrates all four formats)\*\*")), "."],
        [q(P(r"\*\*(The card replayed the conformance sets on silicon)\*\*")), ". ",
         q(P(r"(The published set is\s+\*\*[\d,]+\*\* cases)")), ", and that ",
         q(P(r"(exact set was replayed on the card, one tile, at each point of the\s+\d{4}-\d{2}-\d{2}/\d{2} clock "
             r"sweep from \d+ to \d+ MHz)\.")),
         ". A binary256 soak on the card ran ",
         q(V_(r"(\d+ passes in \d+ minutes, each a\s+resident run of a million elements at fma, add and mul)")),
         ", with ", q(V_(r"reference orbit to its checkpoint - (0 failures)")), "."],
        ["cft-rebound is ",
         q(prose("cft-rebound", "README.md", r"^(REBOUND's IAS15 integrator with its arithmetic routed through "
                                             r"libcft)")),
         ". ", q(prose("cft-rebound", "README.md", r"(At binary64 it is\s+REBOUND's own IAS15 bit for bit, which is "
                                                    r"a gate the port passes on\s+every build)\.")),
         "."],
    ]
    evidence = ["Where to look first: ",
                L(facts.pin("cft-fp256").href("docs/VALIDATION.md"), "the validation ledger"), ", ",
                L(facts.pin("cft-fp256").href("CONFORMANCE.md"), "the conformance contract"), ", and ",
                L(replay.raw, "the browser replay"), ", which ",
                q(P(r"It (replays\s+the published conformance vectors in front of you)")), "."]
    return project("cft-fp256", first_month("cft-fp256"), items, evidence)


def film_block():
    P = lambda pat, **kw: prose("Quantum-Film", "README.md", pat, **kw)
    H = lambda pat, **kw: prose("Quantum-Film", "docs/HARDWARE-RESULTS.md", pat, **kw)
    items = [
        [q(P(r"^\*\*(Film stocks whose crystals are laid by quantum circuits, and a fixer that\s+makes every print "
             r"of a roll the same, bit for bit, on every machine)\.\*\*")),
         "; ", q(P(r"(its tone curve and\s+grain scale are borrowed from a real stock in\s+\[atlas-film\]\([^)]*\), "
                   r"so only the placement\s+of the crystals is new)")), "."],
        ["Its Pauli stock's law ", q(P(r"\*\*The shelf's Pauli law (ran on Moth's Atlas emulator, and holds)\*\*")),
         ", and the stock was ", q(P(r"(printed, with one print laid entirely by Atlas);")), ". ",
         q(H(r"(On \d{4}-\d{2}-\d{2} the design docs/PREREGISTRATION\.md fixed beforehand ran on each of the three "
             r"IBM Quantum devices the owner's Open-plan instance reaches)\.")),
         ". The result is reported as it fell: ",
         q(H(r"\*\*In one paragraph\.\*\* (All three devices carry the law's two quantum signatures, well clear of "
             r"the classical twin):")),
         ". ", q(H(r"(And all three fall short of what their own noise models predicted)\.")), "."],
        [A(WIN), " (", L(RESULTS, "the hackathon's results"), "). ",
         q(P(r"(Entered for the Expert challenge #\d+: a repository of a quantum application that\s+runs a process "
             r"on media through the Atlas API)\.")), "."],
    ]
    return project("Quantum-Film", first_month("Quantum-Film"), items)


def qro_block():
    P = lambda pat, **kw: prose("QRO-Crate", "README.md", pat, **kw)
    items = [
        [q(P(r"^(An RO-Crate profile for quantum computing runs, built so that the difference\s+between two runs "
             r"can be attributed: to the question, the compile, what was\s+submitted, the sampling, readout, the "
             r"device's state and time, or drift\s+within a run)\.")),
         ". ", q(P(r"(Its first data are Quantum-Film's runs, on IBM's processors and\s+on Moth's Atlas "
                   r"emulator)\.")), "."],
        ["P0 is built, its parts including ", q(P(r"^  - (the canonical writer and the strict reader);")), ", ",
         q(P(r"^  - (the checker's steps [\d, ]+and \d+);")), " and ",
         q(P(r"^  - (the custody log and the audit record);")), ". ",
         q(P(r"(Nothing else is built: no adapter, no measures, no comparison, no profile\s+crate, no contributor "
             r"kit)\.")), "."],
    ]
    return project("QRO-Crate", first_month("QRO-Crate"), items)


def other_block():
    items = [
        ["Mercenaries2: ", q(prose("Mercenaries2", "README.md", r"^(A revival project for \*\*Mercenaries 2: World in "
                                                                 r"Flames\*\*)")),
         ". ", q(prose("Mercenaries2", "README.md", r"(Restores online services and exposes the\s+game's "
                                                     r"statically-linked Lua [\d.]+ runtime for modding)\.")), "."],
        ["PrettyCloud, the ", q(prose("PrettyCloud", "README.md", r"^# (Atlas of Mathematical Forms)$")), ": ",
         q(prose("PrettyCloud", "README.md", r"^(A WebGL2 point-cloud atlas)\.")), "."],
    ]
    return '<h2>Other public work</h2><ul class="plain">%s</ul>' % "".join(item(i) for i in items)


def background_block():
    """Home's biography and About's first approved sentence, as Logan
    approved them (decisions 14 and 26): settled, so no draft label."""
    return ('<h2>Background</h2><p>%s</p><p>%s</p>'
            % (render([facts.stated(front.WHO, "Logan", "2026-09-29")]),
               render([facts.stated(about.APPROVED[0], "Logan", "2026-09-30")])))


BLOCKS = ("head_block", "oversight_block", "cft_block", "film_block", "qro_block", "other_block", "background_block")


# Above the resume: its printout, the toggle that shows every source beside
# its line (resume.css; decision 45), and how to read the page. None of them
# is printed: printout.twin reads the <div class="cv"> alone.
TOOLS = ('<p class="tools"><a href="resume.pdf">A plain PDF of this page</a>, printed from it by the build</p>'
         '<details class="srcs"><summary>Show every source beside its line</summary></details>'
         '<div class="measure"><p class="how">Every underlined passage is read from its source, or is Logan&#x27;s '
         'own word. Hover over it to see where it was read, or who said it and when, or open &#x201c;Show every '
         'source beside its line&#x201d; above. Each quotation is its source&#x27;s own words: a project&#x27;s at '
         'the commit this site pins, or this site&#x27;s own ledger&#x27;s.</p></div>')

# The resume's markup as the last render_page made it, which the build then
# prints: render_all calls extra_files and print_files straight after it.
_CV = []


def render_page(ctx):
    cv = ('<div class="cv">' + head_block() + oversight_block() + cft_block() + film_block() + qro_block()
          + other_block() + background_block() + '</div>')
    body = _settled.refuse('<h1>Resume</h1>' + TOOLS + cv, PAGE["file"], SETTLED)
    _CV[:] = [cv]
    return body


def extra_files(ctx):
    """The page's text twin: the resume, a block a line, each figure with its
    id, as the dossiers' twins write them (printout.twin)."""
    return {"resume.txt": printout.twin(_CV[0])}


def print_files(ctx):
    """The page's printout, written from its twin alone (printout.pdf)."""
    return {"resume.pdf": printout.pdf(printout.twin(_CV[0]))}


def _printed(cv_inner):
    """A small resume's twin, its lines after the name, role and contact."""
    head = '<p class="lede">Role.</p><p class="contact">Contact.</p>'
    return printout.twin('<div class="cv">%s%s</div>' % (head, cv_inner)).split("\n")[3:-3]


def controls():
    """The resume's statements are Logan's settled words, or labelled
    drafts: pages._settled plants each fault its check was found to miss
    into each of BLOCKS, as on About and the front page. And the printout
    leaves out exactly the quotation marks the page sets straight around a
    figure, and no other (verifier-print's W1): each shape below keeps its
    marks, and the page's own shape loses them."""
    out = _settled.controls(globals(), BLOCKS, render_page, {"built": {}, "pages": {}}, "resume",
                            (about.APPROVED[0], "Logan", "2026-09-30"), S, D)
    o, c = chr(0x201C), chr(0x201D)
    fig = '<span class="q" data-f="7">quoted</span>'
    label = '<span class="src" data-f="7"> (a label)</span>'
    for what, inner, want in (
            ("the page's own shape loses both marks", "<p>A %s%s%s.</p>" % (o, fig + label, c), "A quoted [fact 7]."),
            ("a closing mark opening the next block is kept",
             "<p>Ends %s</p><p>%sstarts here.</p>" % (fig + label, c), c + "starts here."),
            ("a closing mark after a figure with no label is kept", "<p>A %s%s.</p>" % (fig, c),
             "A quoted [fact 7]%s." % c),
            ("an opening mark before a label, then a figure, is kept",
             "<p>A %s%s%s.</p>" % (o, label, fig), "A %squoted [fact 7]." % o),
            ("an opening mark with a space before its figure is kept, and the closing mark after its label is not",
             "<p>A %s %s%s%s.</p>" % (o, fig, label, c), "A %s quoted [fact 7]." % o),
            ("a closing mark after a label that follows no figure is kept",
             "<p>Prose%s%s here.</p>" % (label, c), "Prose%s here." % c)):
        try:
            got = _printed(inner)
            ok = want in got
        except Exception as e:  # noqa: BLE001 - a refusal is a result here, and is reported
            got, ok = [repr(e)], False
        # caught means the rule held: a wrong reader fails here by name
        out.append(("resume-printout-quotes", ok, "the rule holds: %s, reading %s" % (what, ascii(got))))
    # the page's reader refuses a block with nothing to print, as the twin
    # does (printout.blank; verifier-record2's R-2)
    for what, ch in (("a soft hyphen", chr(0xAD)), ("a no-break space", chr(0xA0))):
        try:
            _printed("<p>%s</p>" % ch)
            out.append(("resume-printout-blank", False, "a paragraph holding only %s passed" % what))
        except printout.Refused as e:
            out.append(("resume-printout-blank", "an empty <p>" in str(e), "a paragraph holding only %s: %s" % (what, e)))
    return out
