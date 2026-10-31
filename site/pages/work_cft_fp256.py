"""Dossier: cft-fp256 (docs/SPEC.md, "Work"; decision 15)."""
import json
import re

from pages import _dossier
import facts
from facts import V, Refusal, fact, pin, prose
from render import C, L

NAME = "cft-fp256"
LEDGER = "docs/VALIDATION.md"
NIGHTLY = "site/nightly.json"
PAGE = {"file": "work-cft-fp256.html", "nav": "Work",
        "title": "cft-fp256 — Work — loganw.dev",
        "description": "The dossier for cft-fp256: what it is, its contract, what has verified it, "
                        "the failures it kept, and how to try to prove it wrong."}


def ws(text):
    """A literal as a pattern in which every run of spaces may be any whitespace, so that a rewrap of the
    document it quotes does not break the quote; every other character is matched exactly."""
    return r"\s+".join(re.escape(w) for w in text.split())


# ---------------------------------------------------------------------------
# The nightly sweep (round 3): figures read from site/nightly.json at the pin.
# The file is cft-fp256's reduction of one run of the card's, resumed each
# night (its source names card-stress-1019; the long stress run that Verified's
# row of 2026-10-19 closes is another), one night added to it each morning, and
# the live page it feeds goes on past any commit this site reads. So a figure
# here is the pin's, through the file's newest night: a reader is told which
# night, and the page never says "now" in its own voice, though a quote of the
# record's does (verifier-P1's first pass, round 3).
# ---------------------------------------------------------------------------

@fact
def nightly(name, keys, first=None, part=None):
    """One value of site/nightly.json at the pin, found by its key path: nightly(NAME, ["totals", "cases"]).

    A key the file does not have is refused by name, with the path walked and the keys the file does have. The
    value is cited at the line where its last key is written, found by searching the text for each key after the
    line of the key before it; that line must hold `"key": value` as the file writes it, or the fact is refused,
    so a layout change in the reducer is loud. The search takes the first key of that name after its parent's, so
    a same-named key with the same value written earlier, inside a sibling object, would be cited in its place:
    a stated limit, and at the pin each figure the page prints is cited at its own key's line (verifier-P1's
    first pass, round 3). An integer is
    printed with thousands separators and a string as it is. `first` keeps the first characters of a string (a
    date from 'YYYY-MM-DD hh:mm:ss'); `part` is a pattern with one group that must match the string once (a
    sentence of one of the file's rules). Only integers and strings are figures here: a float, a boolean, a
    list or an object is refused, so the page cannot print an hours figure the file does not hold."""
    p = pin(name)
    text = p.show(NIGHTLY)
    try:
        node = json.loads(text)
    except ValueError as e:
        raise Refusal("%s %s %s: not JSON: %s" % (name, p.short, NIGHTLY, e))
    walked, pos = [], 0
    for k in keys:
        walked.append(str(k))
        if not isinstance(node, dict) or k not in node:
            raise Refusal("%s %s %s: no key %s (the file has %s there)"
                          % (name, p.short, NIGHTLY, ".".join(walked),
                             ", ".join(sorted(node)) if isinstance(node, dict) else "no object"))
        node = node[k]
        m = re.compile(r'"%s"\s*:' % re.escape(k)).search(text, pos)
        if m is None:
            raise Refusal("%s %s %s: the key %s is in the data but not written in the text after offset %d"
                          % (name, p.short, NIGHTLY, ".".join(walked), pos))
        pos = m.start()
    where = ".".join(walked)
    if isinstance(node, bool) or not isinstance(node, (int, str)):
        raise Refusal("%s %s %s: %s is %s, and this fact prints integers and strings only"
                      % (name, p.short, NIGHTLY, where, type(node).__name__))
    line = text.count("\n", 0, pos) + 1
    value = json.dumps(node, ensure_ascii=False)
    if not re.search(r'"%s"\s*:\s*%s' % (re.escape(walked[-1]), re.escape(value)), text.splitlines()[line - 1]):
        raise Refusal("%s %s %s:%d: the line for %s does not hold %s as the file writes it"
                      % (name, p.short, NIGHTLY, line, where, value))
    if first is not None and part is not None:
        raise Refusal("%s: a value is cut by first or by part, not both" % where)
    shown = node
    if first is not None or part is not None:
        if not isinstance(node, str):
            raise Refusal("%s %s %s: %s is a number, and only a string can be cut" % (name, p.short, NIGHTLY, where))
        if first is not None:
            shown = node[:first]
        else:
            ms = list(re.finditer(part, node))
            if len(ms) != 1:
                raise Refusal("%s %s %s:%d: the pattern %r matches %d times in %s; it must match once"
                              % (name, p.short, NIGHTLY, line, part, len(ms), where))
            shown = ms[0].group(1)
    out = "{:,}".format(shown) if isinstance(shown, int) else shown
    return V(out, p.src("file", "%s:%d" % (NIGHTLY, line), "%s, read as the JSON key path %s" % (NIGHTLY, where),
                        NIGHTLY, line),
             raw=value, num=bool(re.fullmatch(r"[0-9][0-9,.: -]*", out)))


@fact
def entry_title(name, path, line):
    """A ledger entry's heading by its line, as _dossier.ledger_title gives it, with its markdown marks taken out
    (facts.md_plain): the heading of 2026-10-20's entry ends in **...**, which would print its asterisks."""
    t, ents = facts.entries(name, path)
    e = next((e for e in ents if e["line"] == line), None)
    if e is None:
        raise Refusal("%s %s: no ledger entry heading at line %d" % (name, path, line))
    return V(facts.md_plain(e["title"]),
             pin(name).src("file", "%s:%d" % (path, line), "the entry's heading, without its markdown marks", path, line),
             raw=e["title"])


def _sections(built):
    S = _dossier.section

    what_it_is = S("What it is", [_dossier.para([
        prose(NAME, "README.md", r"^\*\*(A math coprocessor that gets the same answer everywhere)\.\*\*"), ". ",
        prose(NAME, "README.md",
              r"(It does IEEE 754 arithmetic at four precisions - 32, 64, 128 and 256\s+bits - and guarantees that "
              r"the same inputs give the same bits whether\s+the work runs on a laptop CPU, in a browser tab, on a "
              r"microcontroller,\s+or on the FPGA card it was designed for)\."), "."])])

    what_it_is_not = S("What it is not", [_dossier.para([
        prose(NAME, "README.md", r"^(Raw fp32 and fp64 throughput)\."), ". ",
        prose(NAME, "README.md",
              r"(Every CPU and GPU on the market serves\s+those formats at clocks and lane counts an FPGA fabric "
              r"will not match,\s+and nothing here pretends otherwise)\."), ". ",
        prose(NAME, "README.md",
              r"(The tile earns its place at the precisions commodity hardware does not\s+offer, and on the "
              r"guarantee that the answer does not move)\."), "."])])

    contract = S("The contract", [
        _dossier.para(["Named levels, quoted from ", C("CONFORMANCE.md"), ": “",
                       prose(NAME, "CONFORMANCE.md", r"\*\*(Level A - IEEE 754-2019 in radix 2)\.", num=True),
                       "” is the standard itself; “",
                       prose(NAME, "CONFORMANCE.md", r"\*\*(Level B - the cft-fp256 profile)\."), "” is “",
                       prose(NAME, "CONFORMANCE.md",
                             r"(Level A, plus every choice the\s+standard leaves to the implementation fixed to "
                             r"one answer, plus\s+operations the standard does not define)\."),
                       ".” The relationship runs one way, in the document's own words: “",
                       prose(NAME, "CONFORMANCE.md",
                             r"(An implementation conforming to the cft-fp256 profile conforms to)\s*$"), " ",
                       prose(NAME, "CONFORMANCE.md",
                             r"^> (IEEE 754-2019 in radix 2 for the operations the profile covers)\.", num=True),
                       ".”"]),
        _dossier.para(["The README states the promise directly: “",
                       prose(NAME, "README.md", r"(That guarantee is the product)\."), ".” ",
                       prose(NAME, "README.md", r"(The hardware only makes it faster)\."), "."]),
        _dossier.para(["The contract is versioned. CONFORMANCE.md opens with its profile, “",
                       prose(NAME, "CONFORMANCE.md", r"^\*\*(Profile 3\.1, 2026-10-13)\*\*", num=True), "” (",
                       prose(NAME, "CONFORMANCE.md",
                             r"\((profile 3 was 2026-10-05, profile 2\s+2026-10-02 and profile 1 2026-09-16); "
                             r"\"Versioning\" says why each\s+stepped\)", num=True),
                       "), and says of the tree: “",
                       prose(NAME, "CONFORMANCE.md",
                             r"\*\*The tree is at profile 3\.1\*\* \(2026-10-13\), (a minor step: cases\s+added, none "
                             r"moved)\."),
                       ".” A minor step is “",
                       prose(NAME, "CONFORMANCE.md",
                             r"\*\*A minor step\*\* is (an addition that changes no recorded case and no\s+accepted "
                             r"image):"), ".”"]),
        # Round 3, decision D2: the pin's own record disagrees with itself here, and the site quotes both lines
        # without settling it. It says neither that the profile stepped for issue 1's fix nor that it should have:
        # no file at the pin records a step for that fix (profile.py still reads (3, 1); the step to 3.1 that
        # docs/COMPATIBILITY.md:1002 and docs/ROADMAP.md:6446 record is of 2026-10-13), and a site that said it
        # would be the one deciding (verifier-P1's first pass, round 3).
        _dossier.para(["What CONFORMANCE.md says of the tree, “",
                       prose(NAME, "CONFORMANCE.md",
                             r"\*\*The tree is at profile 3\.1\*\* \(2026-10-13\), (a minor step: cases\s+added, none "
                             r"moved)\."),
                       ",” is that document's own word as of its last change, ",
                       facts.last_change(NAME, "CONFORMANCE.md"),
                       ". The ledger's newest entry, of ", _dossier.ledger_date(NAME, LEDGER, 26149),
                       ", reports a fix that changed published records: “",
                       prose(NAME, LEDGER,
                             r"(The 8 that change are the rtz and rdn transcendental sets of each format, each by "
                             r"exactly one record, exp2m1\(emax \+ 1\): the same value, flags 20 to 16\. The unfixed "
                             r"model's 72 rtz and rdn sets equal the committed record, so those 8 records are the "
                             r"published ones moving)\."),
                       ".” The same document calls a change to any recorded bit or flag a major step: “",
                       prose(NAME, "CONFORMANCE.md",
                             r"\*\*A major step\*\* is (a change to any recorded bit or flag, or to an\s+accepted "
                             r"image's result, flags, STATUS or acceptance)"),
                       ".” The pin holds both."])])

    def N(*keys, **cut):
        """One figure of the nightly page's data file, by its key path (nightly(), above)."""
        return nightly(NAME, list(keys), **cut)

    def row(line):
        """A dated row, linked to its ledger entry, as the first four are; the heading's markdown marks out."""
        return [L(facts.pin(NAME).href(LEDGER, line), entry_title(NAME, LEDGER, line))]

    nightly_url = prose(NAME, "README.md",
                        r"\[nightly\.html\]\((https://loganw234\.github\.io/cft-fp256/nightly\.html)\)").raw

    verified = S("Verified", [
        _dossier.para(["Last verified: ", facts.last_verified(NAME), "."]),
        _dossier.list_([
            [L(facts.pin(NAME).href("docs/VALIDATION.md", 7164),
               _dossier.ledger_title(NAME, "docs/VALIDATION.md", 7164))],
            [L(facts.pin(NAME).href("docs/VALIDATION.md", 13916),
               _dossier.ledger_title(NAME, "docs/VALIDATION.md", 13916))],
            [L(facts.pin(NAME).href("docs/VALIDATION.md", 18248),
               _dossier.ledger_title(NAME, "docs/VALIDATION.md", 18248))],
            [L(facts.pin(NAME).href("docs/VALIDATION.md", 18547),
               _dossier.ledger_title(NAME, "docs/VALIDATION.md", 18547))],
            # Round 3: four of the verification events the record holds after 2026-10-06, newest last, the ones
            # P1's brief named. The selection is editorial (P1's design): the record holds later ones, of
            # 2026-10-26, 10-27 and 10-29, which no row here gives (verifier-P1's first pass, round 3). Each row is
            # its entry's heading whole, so the row says what the entry says: the last of them says in its own
            # heading that none of it has touched the card or amd-arc-box.
            row(18943),
            row(21042),
            row(21275),
            row(22253),
        ], ordered=False),
        # The nightly sweep, as the data file at the pin gives it. Every figure is the file's `totals` (the
        # campaign summed to its newest night), never one night's own; the stop night is printed twice; and the
        # live page, which goes on past the pin, is linked beside the sentence that says so.
        _dossier.para(["The card's nightly sweep. The README says its ", L(nightly_url, "nightly page"), " “",
                       prose(NAME, "README.md",
                             r"(shows\s+how far the card's nightly stress run has come: the items fully covered,\s+"
                             r"night by night, and the hours on the card)\."),
                       ".” At the pin its data file, ", C(NIGHTLY), ", holds ", N("totals", "nights"),
                       " nights, the first starting ", N("totals", "first", first=10),
                       " and the newest, night ", N("newest", "night"), ", starting ", N("newest", "date"),
                       ". In them: ", N("totals", "slices"), " slices, ", N("totals", "cases"), " cases and ",
                       N("totals", "disagreements"), " disagreements, and ", N("totals", "legs", "total"),
                       " legs, of which ", N("totals", "legs", "by_status", "pass"), " passed, ",
                       N("totals", "legs", "by_status", "fail"), " failed and ",
                       N("totals", "legs", "by_status", "skipped"),
                       " were skipped. The file says what a night is: “", N("rules", "night"), "”"]),
        _dossier.para(["Reading those figures. The sweep has items no tile computes: the file counts “",
                       N("rules", "classes", part=r"(a host item per host tree and compiler, because no tile "
                                                  r"computes it)"),
                       ",” and the record says “",
                       prose(NAME, LEDGER, r"(The sweep's case totals add items whose tools count different things)"),
                       ".” These are the pin's figures, through night ", N("newest", "night"), ". The ",
                       L(nightly_url, "live page"), " goes on past them: the entry of ",
                       _dossier.ledger_date(NAME, LEDGER, 26082), " records “",
                       prose(NAME, LEDGER, r"; (the weekend window launched);"),
                       ",” and says of that run “",
                       prose(NAME, LEDGER, r"(It waits for 18:00 and runs until Monday 2026-11-02 07:45)\."),
                       ".” The entry that built the page is ",
                       L(facts.pin(NAME).href(LEDGER, 23603), "in the same ledger"), "."])])

    kept_failures = S("Kept failures", [_dossier.list_([
        [prose(NAME, "CLAUDE.md",
               r"(cocotb's inability to set an exit code — stated in its own\s+makefile at "
               r"`Makefile\.inc:88`, which checks only that the file \*exists\* —\s+meant three real RTL "
               r"failures were reported as a pass)\."),
         ". Fixed by the entry ",
         L(facts.pin(NAME).href("docs/VALIDATION.md", 10955), _dossier.ledger_title(NAME, "docs/VALIDATION.md", 10955)),
         ", commit ",
         _dossier.kept_failure(NAME, "f192bf0", "make sim reads its results instead of trusting cocotb's exit code"),
         "."],
        [prose(NAME, "CONFORMANCE.md", r"\*\*(exp2 at x = emin - p)\.\*\*"), ": ",
         prose(NAME, "CONFORMANCE.md",
               "(" + ws("Its exact value 2^(emin - p) is half the smallest subnormal, the tie between +0 and it, "
                        "which IEEE 754's roundTiesToAway (rmm) rounds to the subnormal. The model rounded it as a "
                        "quarter of the subnormal and gave +0") + ")"),
         ". ", prose(NAME, "CONFORMANCE.md",
                     "(" + ws("Step 6's design study M1 found it (its question 5), verifier-VM1 confirmed it") + ")"),
         " — in the entry ",
         L(facts.pin(NAME).href("docs/VALIDATION.md", 18206), _dossier.ledger_title(NAME, "docs/VALIDATION.md", 18206)),
         ". Fixed by commit ",
         _dossier.kept_failure(NAME, "ca43695", "exp2's tie goes to round_pack, as pow's and pown's exact branches "
                                                "always did; the profile's major step to 3"), "."],
        # Round 3, decision D1: issue 1 is the third, in the place of the reserved-MODE-bit bullet, since the spec
        # gives this section "2-3". The words are the entry's own (docs/VALIDATION.md:26149 on); the fix is the
        # merge the entry names ("merged as 48e2aa22") and Corrections prints. One of the entry's four known
        # limits, the oracle's pools, is quoted in "Prove it wrong"; the other three are in the entry, which the
        # date's label links (verifier-P1's first pass, round 3). Nothing here says who opened the issue: that is
        # GitHub's record. The entry is cited by its date, whose label links its heading, and not by its heading:
        # the heading calls the report "the first outside report", and the lead's ruling of 07:39:53 on the
        # Determinism thread keeps that word, in that sense, off a page other than Map & Ledger's row, while
        # Corrections' signature row says no outside correction has come. The word is printed on this page in
        # another sense, in 2026-10-20's heading ("three outside test sources").
        [prose(NAME, LEDGER,
               r"- (At x = emax \+ 1, under roundTowardZero and roundTowardNegative, exp2m1 returned the largest "
               r"finite, which is right, with overflow \| inexact \(0x14\), which is wrong)\."),
         ". Reported, in the entry's words, “",
         prose(NAME, LEDGER,
               r"(from a clean-room audit of loganw234/muse-softfloat \(binary16/32/64\), cross-tested against this "
               r"library and an exact arbiter)"),
         "” — in the entry of ", _dossier.ledger_date(NAME, LEDGER, 26149),
         ". No gate had caught it: “", prose(NAME, LEDGER, r"\*\*(The MPFR oracle never asked)\.\*\*"),
         ".” Fixed by commit ",
         _dossier.kept_failure(NAME, "48e2aa22", "the merge of fix-exp2m1 (issue 1's fix): exp2m1's overflow shortcut "
                                                 "starts at emax + 2, the MPFR check runs the ten functions on both "
                                                 "pools, and the WebAssembly module is rebuilt"), "."],
    ])])

    test_it = S("Test it", [_dossier.list_([
        [L(prose(NAME, "README.md", r"\*\*<(https://loganw234\.github\.io/cft-fp256/)>\*\*").raw,
           prose(NAME, "README.md", r"It (replays\s+the published conformance vectors in front of you)")),
         " — ", prose(NAME, "README.md", r"## (Try it without installing anything)"), "."],
        [C("make golden"), ": ",
         prose(NAME, "README.md",
               r"^(The golden model's self-tests \(any Python 3\.10\+, mpmath optional but\s+recommended\)):"),
         ", after “", prose(NAME, "README.md", r"^(pip install pytest mpmath)$"), "”. The record's newest timing of "
         "the golden stage is one run on one machine: the runner's stage, which runs “",
         prose(NAME, "verify/run.sh", r'^  (PY -m pytest "\$ROOT/python/tests" -q -rs --color=no)$'),
         "” and names no worker option, took “",
         prose(NAME, LEDGER, r"(golden ok 3,385 s, 5,951 passed and 3 skipped)"), "” on ",
         prose(NAME, LEDGER, r"runs behind it were MEASURED on (amd-arc-box) \(box_m2f2\.sh"),
         ", in the entry of ", _dossier.ledger_date(NAME, LEDGER, 26082), ". What ", C("make golden"),
         " takes elsewhere depends on the machine and on whether pytest is given workers."],
        ["the card: ", prose(NAME, "CONFORMANCE.md",
                              r"\*\*A device\.\*\* `host/tests/device_test\.c` (compares a device against\s+the "
                              r"software backend bit for bit across the elementwise operations)"), ", which needs "
         "the FPGA and its toolchain."],
    ], ordered=True)])

    prove_it_wrong = S("Prove it wrong", [
        _dossier.prove_it_wrong_opening(built),
        _dossier.list_([
            ["Open the web page above and hand it your own vector file: “",
             prose(NAME, "README.md", r"(Drop a vector file on it and it scores itself)\."), ".” Anything less "
             "than a perfect score is a disproof."],
            [C("make vectors"), " locally, then compare the digests it writes with the ones the repository "
             "publishes in ", L(facts.pin(NAME).href("vectors/SHA256SUMS"), facts.exists(NAME, "vectors/SHA256SUMS")),
             ", by the recipe CONFORMANCE.md gives; a differing line is a disproof. The record says this is a check "
             "no gate makes: “",
             prose(NAME, "CONFORMANCE.md",
                   r"\*\*A known limit: (no gate compares a set's digest with\s+`vectors/SHA256SUMS`)\.\*\*"),
             ".”"],
            ["Replay the identity protocol yourself in another language and compare its checksum line against the "
             "ones ", facts.exists(NAME, "docs/COMPATIBILITY.md"), " records; a differing hex value is a disproof."],
            ["Rebuild ", C("host/tools/mpfr_check.c"), " and widen its sweep past the campaign's own cases: the "
             "independent oracle is only as good as the cases put to it. The record names one it lacks: “",
             prose(NAME, "docs/VALIDATION.md",
                   r"(\*\*The MPFR campaign's pool\*\* \(host/tools/mpfr_check\.c, `build_tpool`\) lacks the tie's "
                   r"argument, so the gate's `mpfr` stage does not test the fix; XT-1's probe does)\."), ".”",
             # Round 3: the record's newest entry is the same kind of gap, found by a report; its own known limit
             # is a ranked attack target, so it is quoted here and not left in the entry.
             " The record's newest entry adds a limit of the same kind, after a case the oracle had never been "
             "asked (", L(facts.pin(NAME).href(LEDGER, 26149), "the entry"), "): “",
             prose(NAME, LEDGER,
                   r"(the oracle is only as wide as its pools: the ten now see both, and nothing but this case moved, "
                   r"but no sweep has asked which families any pool lacks)"), ".”"],
        ], ordered=True)])

    connections = S("Connections", [_dossier.connections_block(NAME)])

    provenance = S("Provenance", _dossier.provenance_block([
        # Every file of cft-fp256's that this page reads, quoted or only shown to exist (verifier-P1's first
        # pass, round 3).
        (NAME, ["README.md", "CONFORMANCE.md", "CLAUDE.md", "docs/COMPATIBILITY.md", "docs/VALIDATION.md",
                "vectors/SHA256SUMS", "verify/run.sh", NIGHTLY]),
    ]))

    return [what_it_is, what_it_is_not, contract, verified, kept_failures, test_it, prove_it_wrong,
            connections, provenance]


def render_page(ctx):
    sections = _sections(ctx["built"])
    ctx["_p3_sections"] = sections
    return _dossier.html(NAME, sections)


def extra_files(ctx):
    sections = ctx.get("_p3_sections") or _sections(ctx["built"])
    text = _dossier.twin(NAME, "%s — dossier" % NAME, sections)
    html = _dossier.html(NAME, sections)
    _dossier.twin_ids(NAME, html, text)
    return {"work-cft-fp256.txt": text}


def controls():
    """1. A stale kept-failure hash is refused by the fact that checks the
    commit at the pin; watched failing on a planted one-character mutation.
    2. The granted edit (briefs/P4.md, "the two granted edits"): every
    dossier's "Prove it wrong" opening links Corrections once ctx["built"]
    has it, and plainly does not before then - the same property
    threads.py's door-not-early control holds the thread doors to. Tested
    here, once, against _dossier.prove_it_wrong_opening() directly (every
    dossier calls the same function, so this covers all five), and against
    two fake openings that get one direction wrong each, to show the check
    bites.
    3. Round 3 (P1): the nightly fact refuses, by name, a key the file at the
    pin does not have, and a `part` that does not match the string once. A
    refusal that is only the machine lacking the clone (facts.Unavailable) is
    not a caught fault: it is passed up, and the page's controls are skipped
    by name there."""
    out = []
    try:
        _dossier.kept_failure(NAME, "48e2aa23", "a planted mutation of a real commit")
        out.append(("kept-failure", False, "a mutated hash (48e2aa23 for 48e2aa22) was accepted"))
    except facts.Unavailable:
        raise
    except facts.Refusal as e:
        out.append(("kept-failure", True, "a mutated hash was refused: %s" % e))

    for name, what, call, must in (
            ("nightly-key", "a key the file at the pin lacks (totals.nope)",
             lambda: nightly(NAME, ["totals", "nope"]), "no key totals.nope"),
            ("nightly-key", "a first key the file at the pin lacks (totaly.cases)",
             lambda: nightly(NAME, ["totaly", "cases"]), "no key totaly"),
            ("nightly-part", "a part of rules.classes that matches twice",
             lambda: nightly(NAME, ["rules", "classes"], part=r"(tile)"), "matches 2 times"),
            ("nightly-part", "a part of rules.night that matches nowhere",
             lambda: nightly(NAME, ["rules", "night"], part=r"(words it does not hold)"), "matches 0 times")):
        try:
            call()
            out.append((name, False, "%s was read" % what))
        except facts.Unavailable:
            raise
        except facts.Refusal as e:
            named = NIGHTLY in str(e) and must in str(e)
            out.append((name, named, "%s was refused%s: %s" % (what, " by name" if named else ", but not by name", e)))

    def links_corrections(block):
        return 'href="corrections.html"' in block["html"]

    unbuilt = _dossier.prove_it_wrong_opening({})
    built = _dossier.prove_it_wrong_opening({"Corrections": "corrections.html"})
    early = links_corrections(unbuilt)
    missing = not links_corrections(built)
    out.append(("dossier-corrections-link", not early and not missing,
               "prove_it_wrong_opening(), with and without Corrections in built: links it only once built (%s), "
               "and not before (%s)" % (not missing, not early)))

    fake_early = {"html": '<p><a href="corrections.html">Corrections</a></p>', "text": "x"}
    out.append(("dossier-corrections-link", links_corrections(fake_early),
               "a fake opening linking Corrections before it's built: %s"
               % ("caught" if links_corrections(fake_early) else "NOT CAUGHT")))
    fake_missing = {"html": "<p>no link here</p>", "text": "x"}
    out.append(("dossier-corrections-link", not links_corrections(fake_missing),
               "a fake opening that never links Corrections once it's built: %s"
               % ("caught" if not links_corrections(fake_missing) else "NOT CAUGHT")))
    return out
