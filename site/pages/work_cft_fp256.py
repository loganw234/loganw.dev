"""Dossier: cft-fp256 (docs/SPEC.md, "Work"; decision 15)."""
from pages import _dossier
import facts
from facts import prose
from render import C, L

NAME = "cft-fp256"
PAGE = {"file": "work-cft-fp256.html", "nav": "Work",
        "title": "cft-fp256 — Work — loganw.dev",
        "description": "The dossier for cft-fp256: what it is, its contract, what has verified it, "
                        "the failures it kept, and how to try to prove it wrong."}


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
                       prose(NAME, "README.md", r"(The hardware only makes it faster)\."), "."])])

    verified = S("Verified", [
        _dossier.para(["Last verified: ", facts.last_verified(NAME), "."]),
        _dossier.list_([
            [L(facts.pin(NAME).href("docs/VALIDATION.md", 7161),
               _dossier.ledger_title(NAME, "docs/VALIDATION.md", 7161))],
            [L(facts.pin(NAME).href("docs/VALIDATION.md", 13913),
               _dossier.ledger_title(NAME, "docs/VALIDATION.md", 13913))],
        ], ordered=False)])

    kept_failures = S("Kept failures", [_dossier.list_([
        [prose(NAME, "CLAUDE.md",
               r"(cocotb's inability to set an exit code — stated in its own\s+makefile at "
               r"`Makefile\.inc:88`, which checks only that the file \*exists\* —\s+meant three real RTL "
               r"failures were reported as a pass)\."),
         ". Fixed by the entry ",
         L(facts.pin(NAME).href("docs/VALIDATION.md", 10952), _dossier.ledger_title(NAME, "docs/VALIDATION.md", 10952)),
         ", commit ",
         _dossier.kept_failure(NAME, "f192bf0", "make sim reads its results instead of trusting cocotb's exit code"),
         "."],
        [prose("HonestFramework", "CASE-STUDY.md",
               r"(Nothing validated the reserved bits of a control word, so a device predating a\nnew flag "
               r"\*\*ignored\*\* it and read a thousand elements from a one-element\nbuffer)\.",
               display="a device predating a new capability flag ignored an unchecked reserved bit and read far "
                       "past a one-element buffer"),
         " — measured as a host-side segfault in the entry ",
         L(facts.pin(NAME).href("docs/VALIDATION.md", 10803), _dossier.ledger_title(NAME, "docs/VALIDATION.md", 10803)),
         ". Fixed by commit ",
         _dossier.kept_failure(NAME, "8b7dea1", "run_ok refuses any reserved MODE bit a build does not carry"), "."],
    ])])

    test_it = S("Test it", [_dossier.list_([
        [L(prose(NAME, "README.md", r"\*\*<(https://loganw234\.github\.io/cft-fp256/)>\*\*").raw,
           prose(NAME, "README.md", r"It (replays\s+the published conformance vectors in front of you)")),
         " — ", prose(NAME, "README.md", r"## (Try it without installing anything)"), "."],
        [C("make golden"), ": ", prose(NAME, "README.md", r"^(The golden model's self-tests)"), " (needs only "
         "Python and, optionally, mpmath)."],
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
            [C("make golden"), " locally, against the same vector sets published in the repository's ",
             L(facts.pin(NAME).href("vectors/SHA256SUMS"), facts.exists(NAME, "vectors/SHA256SUMS")), "."],
            ["Replay the identity protocol yourself in another language and compare its checksum line against the "
             "ones ", facts.exists(NAME, "docs/COMPATIBILITY.md"), " records; a differing hex value is a disproof."],
            ["Rebuild ", C("host/tools/mpfr_check.c"), " and widen its sweep past the campaign's own cases: the "
             "independent oracle is only as good as the cases put to it."],
        ], ordered=True)])

    connections = S("Connections", [_dossier.connections_block(NAME)])

    provenance = S("Provenance", _dossier.provenance_block([
        (NAME, ["README.md", "CONFORMANCE.md", "CLAUDE.md", "docs/VALIDATION.md"]),
        ("HonestFramework", ["CASE-STUDY.md"]),
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
    bites."""
    out = []
    try:
        _dossier.kept_failure(NAME, "8b7dea2", "a planted mutation of a real commit")
        out.append(("kept-failure", False, "a mutated hash (8b7dea2 for 8b7dea1) was accepted"))
    except facts.Refusal as e:
        out.append(("kept-failure", True, "a mutated hash was refused: %s" % e))

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
