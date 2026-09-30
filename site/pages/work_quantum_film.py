"""Dossier: Quantum-Film (docs/SPEC.md, "Work"; decision 15)."""
from pages import _dossier
import facts
from facts import prose
from render import C, L

NAME = "Quantum-Film"
PAGE = {"file": "work-quantum-film.html", "nav": "Work",
        "title": "Quantum-Film — Work — loganw.dev",
        "description": "The dossier for Quantum-Film: what it is, its contract, what has verified it, "
                        "the failures it kept, and how to try to prove it wrong."}


def _sections(built):
    S = _dossier.section

    what_it_is = S("What it is", [_dossier.para([
        prose(NAME, "README.md",
              r"^\*\*(Film stocks whose crystals are laid by quantum circuits, and a fixer that\s+makes every "
              r"print of a roll the same, bit for bit, on every machine)\.\*\*"), "."])])

    what_it_is_not = S("What it is not", [_dossier.list_([
        [prose(NAME, "README.md",
               r"- (\*\*Not a quantum advantage\.\*\* At these sizes both quantum laws are classically\s+"
               r"simulable\. That is exactly what makes them checkable)\.")],
        [prose(NAME, "README.md",
               r"- (\*\*Not deterministic at the shot\.\*\* A roll from a device is unique)\.")],
        [prose(NAME, "README.md", r"- (\*\*Not on hardware yet\.\*\*)")],
        [prose(NAME, "README.md", r"- (\*\*Not a model of any real film's grain\.\*\*)")],
    ])])

    contract = S("The contract", [_dossier.para([
        "“", prose(NAME, "README.md",
              r"(\*\*The authority\*\* is `quantum_film/golden`: pure Python and mpmath at 256\s+bits, with "
              r"exact counter-based uniforms \(SHA-256\))\.", num=True), " ",
        prose(NAME, "README.md",
              r"(It imports nothing it\s+could share with what it judges)"), "; ",
        prose(NAME, "README.md", r"(a test holds that\s+mechanically)\."), ".” ",
        prose(NAME, "README.md",
              r"(The\s+circuits, the float paths and Atlas's results are all scored against it)\."), "."])])

    verified = S("Verified", [
        _dossier.para(["Last verified: ", facts.last_verified(NAME), "."]),
        _dossier.list_([
            [L(facts.pin(NAME).href("docs/VALIDATION.md", 342), _dossier.ledger_title(NAME, "docs/VALIDATION.md", 342))],
            [L(facts.pin(NAME).href("docs/VALIDATION.md", 870), _dossier.ledger_title(NAME, "docs/VALIDATION.md", 870))],
        ])])

    kept_failures = S("Kept failures", [_dossier.list_([
        [prose(NAME, "docs/VALIDATION.md",
               r"- (\*\*The claim\*\*, in the README, STOCKS\.md, ROUND1\.md, DETERMINISM\.md and the\s+not-yet-"
               r"dispatched P3 brief: `givens\.py`'s Pauli tile ran on Atlas and\s+matched the exact law)\."),
         ". ", prose(NAME, "docs/VALIDATION.md",
               r"(So the shelf's Pauli law has never run on Atlas)\."), " — ",
         L(facts.pin(NAME).href("docs/VALIDATION.md", 409), _dossier.ledger_title(NAME, "docs/VALIDATION.md", 409)),
         ". Fixed by commit ",
         _dossier.kept_failure(NAME, "b0e9ed1", "the Atlas run is credited to the law that actually ran, and "
                                "every gate the P0 verifier showed could not fail now fails its planted fault"),
         "."],
        [L(facts.pin(NAME).href("docs/VALIDATION.md", 1033), _dossier.ledger_title(NAME, "docs/VALIDATION.md", 1033)),
         ": ", prose(NAME, "docs/VALIDATION.md", r"(The entry\s+copied the label without its definition)\."),
         ". Fixed by commit ",
         _dossier.kept_failure(NAME, "283330c", "VALIDATION corrects the P1 entry's two labels: a unit mislabel "
                                "and an absolute-vs-relative mislabel"), "."],
    ])])

    test_it = S("Test it", [_dossier.list_([
        [C("make verify-quick"), ": ", prose(NAME, "README.md",
         r"make verify-quick\s+# (~65 s: lint, docs, vectors, golden, circuits, decode, client, fixer, pinned, "
         r"develop, the control and its twin)", num=True), "."],
        [C("make verify"), ": ", prose(NAME, "README.md",
         r"make verify\s+# (adds the cft and live-Atlas stages); pinned and cft skip BY NAME without "
         r"libcft, Atlas without a key"), "."],
    ], ordered=True)])

    prove_it_wrong = S("Prove it wrong", [
        _dossier.prove_it_wrong_opening(built),
        _dossier.list_([
            ["Look at the first prints yourself and compare the structure-factor claim against what the eye can "
             "actually see in the published images — free."],
            [C("make verify-quick"), " on a clean clone, and read whether ",
             prose(NAME, "README.md", r"(The negative control, and its twin)"), " still catches a moved crystal."],
            ["Feed the fixer a record with one crystal moved yourself, by hand, and confirm it is refused for "
             "its digest and for no other reason."],
            ["Repeat the same Atlas job and check whether the bytes really differ: “",
             prose(NAME, "README.md",
                   r"(Identical requests to Atlas returned different bytes wherever sampling\s+was involved)"),
             ",” which needs an Atlas account this dossier does not supply."],
        ], ordered=True)])

    connections = S("Connections", [_dossier.connections_block(NAME)])

    provenance = S("Provenance", _dossier.provenance_block([
        (NAME, ["README.md", "docs/VALIDATION.md"]),
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
    return {"work-quantum-film.txt": text}
