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
    result are drafted from his draft resume of 2026-10-15, and carry the
    draft label until he approves them as printed;
  - the background is Home's biography and About's first approved sentence,
    printed as Logan approved them, so they carry no draft label.
pages._settled holds every statement here to those two kinds, as it holds
About's and the front page's.
"""
import dataclasses

import facts
from facts import V, fact, prose
from pages import _settled, about, front
from render import L, esc, render

PAGE = {"file": "resume.html", "nav": None, "unlisted": True, "title": "Resume — loganw.dev",
        "description": "Logan's resume: each line quoted from its project at the commit this site pins, and his "
                       "own words marked as his."}

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

# Every statement this page may print without a draft label, with the label
# it must carry: its words, who said them, and when (pages._settled).
SETTLED = {front.WHO: "stated by Logan, 2026-09-29",
           about.APPROVED[0]: "stated by Logan, 2026-09-30"}

MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
HH_R1 = "Rounds/HonestHarness-R1/CASE-STUDY.md"


def S(text, **kw):
    return facts.stated(text, "Logan", DRAFTED, **kw)


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
    return ('<h1>Resume</h1><div class="measure"><p class="lede">%s</p>'
            '<p class="contact"><a href="mailto:logan@loganw.dev">logan@loganw.dev</a> · '
            '<a href="index.html">loganw.dev</a> · <a href="https://github.com/loganw234">github.com/loganw234</a></p>'
            '<p>%s</p>'
            '<p class="how">Each quotation below is its project&#x27;s own words at the commit this site pins, '
            'labelled with the file and line; every other figure names where it was read. What only Logan can say '
            'is marked as his statement, with its date; a statement he has not yet approved as printed says so.</p>'
            '</div>'
            % (render([D(ROLE)]), render([D(SUMMARY)])))


def oversight_block():
    P, CS = prose, lambda pat, **kw: prose("HonestHarness", HH_R1, pat, **kw)
    items = [
        ["ParcelRound: ", q(P("ParcelRound", "README.md", r"^(A method for splitting one body of work across several "
                                                           r"coding agents\s+at\s+once, without the pieces failing to "
                                                           r"meet)\.")),
         ". It exists because ",
         q(P("ParcelRound", "README.md", r"(Give four agents four well-scoped parcels of one feature and you\s+can "
                                          r"get four green gates and a feature that does not work)")),
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
         "; ", q(CS(r"\*\*(Plants that changed meaning or shape were caught \d+ of \d+):\*\*")), "."],
        ["Where a suite stops telling models apart, the record says so: ",
         CS(r"\*\*QS6:\*\* (\d+ of \d+ runs exact)", num=True), ", and ",
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
        [D(EXPERIMENT), " Its rule: ",
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
        ["In cft-rebound, ",
         q(prose("cft-rebound", "README.md", r"^(REBOUND's IAS15 integrator with its arithmetic routed through "
                                             r"libcft)")),
         ". ", q(prose("cft-rebound", "README.md", r"(At binary64 it is\s+REBOUND's own IAS15 bit for bit, which is "
                                                    r"a gate the port passes on\s+every build)\.")),
         "."],
    ]
    evidence = ["Where to look first: ",
                L(facts.pin("cft-fp256").href("docs/VALIDATION.md"), "the validation ledger"), ", ",
                L(facts.pin("cft-fp256").href("CONFORMANCE.md"), "the conformance contract"), ", and ",
                L(replay.raw, "the browser replay"), ", where ",
                q(P(r"(It replays\s+the published conformance vectors in front of you)")), "."]
    return project("cft-fp256", first_month("cft-fp256"), items, evidence)


def film_block():
    P = lambda pat, **kw: prose("Quantum-Film", "README.md", pat, **kw)
    H = lambda pat, **kw: prose("Quantum-Film", "docs/HARDWARE-RESULTS.md", pat, **kw)
    items = [
        [q(P(r"^\*\*(Film stocks whose crystals are laid by quantum circuits, and a fixer that\s+makes every print "
             r"of a roll the same, bit for bit, on every machine)\.\*\*")),
         "; ", q(P(r"(its tone curve and\s+grain scale are borrowed from a real stock in\s+\[atlas-film\]\([^)]*\), "
                   r"so only the placement\s+of the crystals is new)")), "."],
        ["On Moth's Atlas, its Pauli stock was ", q(P(r"(printed, with one print laid entirely by Atlas);")),
         "; then ",
         q(H(r"(On \d{4}-\d{2}-\d{2} the design docs/PREREGISTRATION\.md fixed beforehand ran on each of the three "
             r"IBM Quantum devices the owner's Open-plan instance reaches)\.")),
         ". The result is reported as it fell: ",
         q(H(r"(And all three fall short of what their own noise models predicted)\.")), "."],
        [D(WIN), " (", L(RESULTS, "the hackathon's results"), "). The entry: ",
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
        ["Built so far: ", q(P(r"^  - (the canonical writer and the strict reader);")), ", ",
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
        ["PrettyCloud: ", q(prose("PrettyCloud", "README.md", r"^# (Atlas of Mathematical Forms)$")), ", ",
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


def render_page(ctx):
    body = ('<div class="cv">' + head_block() + oversight_block() + cft_block() + film_block() + qro_block()
            + other_block() + background_block() + '</div>')
    return _settled.refuse(body, PAGE["file"], SETTLED)


def controls():
    """The resume's statements are Logan's settled words, or labelled
    drafts: pages._settled plants each fault its check was found to miss
    into each of BLOCKS, as on About and the front page."""
    return _settled.controls(globals(), BLOCKS, render_page, {"built": {}, "pages": {}}, "resume",
                             (about.APPROVED[0], "Logan", "2026-09-30"), S, D)
