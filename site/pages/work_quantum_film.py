"""Dossier: Quantum-Film (docs/SPEC.md, "Work"; decision 15)."""
from pages import _dossier
import facts
from facts import prose
from render import C, L

NAME = "Quantum-Film"
RESULTS = "docs/HARDWARE-RESULTS.md"
PAGE = {"file": "work-quantum-film.html", "nav": "Work",
        "title": "Quantum-Film — Work — loganw.dev",
        "description": "The dossier for Quantum-Film: what it is, its contract, what has verified it, "
                        "the failures it kept, and how to try to prove it wrong."}


def _sections(built):
    S = _dossier.section

    def entry(line):
        return [L(facts.pin(NAME).href("docs/VALIDATION.md", line), _dossier.ledger_title(NAME, "docs/VALIDATION.md", line))]

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
        [prose(NAME, RESULTS,
               r"^- \*\*(The comparison measures; it does not gate\.\*\* It says how far each device is from the law "
               r"and from the twin, not whether a device \"passed\")\.$")],
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
        _dossier.para(["Last verified: ", facts.last_verified(NAME), ". It counts only a full run of the runner with "
                       "nothing skipped; the newest full run the ledger records skipped one stage: “",
                       prose(NAME, "docs/VALIDATION.md",
                             r"^- (\*\*The front door at 83933cc:\*\* 17 stages passed and 0 failed\. atlas skipped "
                             r"by name, because no Atlas key was\s+used)\.", num=True), "”."]),
        _dossier.list_([entry(342), entry(870), entry(1479), entry(1571), entry(1612)]),
        _dossier.para(["The results document records its protocol: “",
                       prose(NAME, RESULTS, r"^(Nine jobs, each submitted once, in the pre-registered order\. Each "
                                            r"job's line was committed and pushed before any result was read\.)"),
                       "” Its one-paragraph summary: “",
                       prose(NAME, RESULTS,
                             r"^\*\*In one paragraph\.\*\* (All three devices carry the law's two quantum "
                             r"signatures, well clear of the classical twin: 4\.3% to 5\.4% of their five-crystal "
                             r"shots on forbidden layouts against the twin's 31\.1%, and coherences of \+0\.27 to "
                             r"\+0\.34 where a classical mixture gives 0\. And all three fall short of what their "
                             r"own noise models predicted\.)$"),
                       "” And it states a limit: “",
                       prose(NAME, RESULTS,
                             r"^- \*\*(One day\.\*\* Each device's jobs ran on one day; day-to-day variation is not "
                             r"measured\. Within the day, the sheets' runs measure run-to-run variation "
                             r"\(above\))\.$"), "”."])])

    kept_failures = S("Kept failures", [_dossier.list_([
        [prose(NAME, "docs/VALIDATION.md",
               r"- (\*\*The claim\*\*, in the README, STOCKS\.md, ROUND1\.md, DETERMINISM\.md and the\s+not-yet-"
               r"dispatched P3 brief: `givens\.py`'s Pauli tile ran on Atlas and\s+matched the exact law)\."),
         ". At that entry's date the ledger said: “", prose(NAME, "docs/VALIDATION.md",
               r"So (the shelf's Pauli law has never run on Atlas)\."), "” — ",
         L(facts.pin(NAME).href("docs/VALIDATION.md", 409), _dossier.ledger_title(NAME, "docs/VALIDATION.md", 409)),
         ". The law ran on Atlas later: see the second row under Verified. Fixed by commit ",
         _dossier.kept_failure(NAME, "b0e9ed1", "the Atlas run is credited to the law that actually ran, and "
                                "every gate the P0 verifier showed could not fail now fails its planted fault"),
         "."],
        [L(facts.pin(NAME).href("docs/VALIDATION.md", 1033), _dossier.ledger_title(NAME, "docs/VALIDATION.md", 1033)),
         ": ", prose(NAME, "docs/VALIDATION.md", r"(The entry\s+copied the label without its definition)\."),
         ". Fixed by commit ",
         _dossier.kept_failure(NAME, "283330c", "VALIDATION corrects the P1 entry's two labels: a unit mislabel "
                                "and an absolute-vs-relative mislabel"), "."],
        [prose(NAME, "docs/VALIDATION.md",
               r"^- (\*\*The READMEs frozen into the three IBM bundles say:\*\* \"To rehearse offline first, add "
               r"`--dry-run`\"\. For those\s+bundles that is wrong)\."),
         ". ", prose(NAME, "docs/VALIDATION.md",
                     r"^  - (The bundles stay as frozen, since their READMEs are in their manifests' hashes)\."),
         " — ", L(facts.pin(NAME).href("docs/VALIDATION.md", 1664), _dossier.ledger_title(NAME, "docs/VALIDATION.md", 1664)),
         ". The template was corrected by commit ",
         _dossier.kept_failure(NAME, "66d17c0", "the template tells a qpu bundle's runner to rehearse on a second "
                                "bundle frozen against a fake backend, and a test holds both routes"), "."],
    ])])

    test_it = S("Test it", [_dossier.list_([
        [C("make verify-quick"), ": ", prose(NAME, "CLAUDE.md",
         r"^make verify-quick\s+# (~\d+ min: lint, docs, vectors, golden, circuits, decode, client, fixer, hardware, "
         r"pinned, develop, compare, the control and its twin)$", num=True), "."],
        [C("make verify"), ": ", prose(NAME, "verify/run.sh", r"^#\s+bash verify/run\.sh\s+(every stage)$"), "; ",
         prose(NAME, "CLAUDE.md",
               r"^make verify\s+# adds cft and the live Atlas smoke; (any stage that cannot run skips BY NAME)$"), "."],
    ], ordered=True)])

    prove_it_wrong = S("Prove it wrong", [
        _dossier.prove_it_wrong_opening(built),
        _dossier.list_([
            ["Look at the first prints yourself and compare the structure-factor claim against what the eye can "
             "actually see in the published images — free."],
            ["Re-make a table of ", C(RESULTS), " from the committed records, and read whether any cell differs. “",
             prose(NAME, RESULTS,
                   r"(Every table below is quantum_film/compare\.py's own, made from the records committed under "
                   r"`docs/records/2026-10-05/ibm/`, and every number in the prose is computed from them)",
                   num=True), "”: ",
             prose(NAME, RESULTS,
                   r"To remake every table here: `(python -m quantum_film\.compare table --prediction <a prediction> "
                   r"docs/records/2026-10-05/ibm/<device>/run)`", num=True), "."],
            [C("make verify-quick"), " on a clean clone, and read whether the README's “",
             prose(NAME, "README.md", r"(The negative control, and its twin)"), "” still catch a moved crystal."],
            ["Feed the fixer a record with one crystal moved yourself, by hand, and confirm it is refused for "
             "its digest and for no other reason."],
            ["Repeat the same Atlas job and check whether the bytes really differ: “",
             prose(NAME, "README.md",
                   r"(Identical requests to Atlas returned different bytes wherever sampling\s+was involved)"),
             ",” which needs an Atlas account this dossier does not supply."],
        ], ordered=True)])

    connections = S("Connections", [_dossier.connections_block(NAME)])

    provenance = S("Provenance", _dossier.provenance_block([
        (NAME, ["README.md", "CLAUDE.md", RESULTS, "docs/VALIDATION.md", "verify/run.sh"]),
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
