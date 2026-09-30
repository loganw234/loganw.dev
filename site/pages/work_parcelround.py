"""Dossier: ParcelRound (docs/SPEC.md, "Work"; decision 15). It keeps no
docs/VALIDATION.md ledger and no workflow (pins.json: "workflows": {}) - the
method's own tools are its case studies, so "Verified" reads what those
record rather than a build.
"""
from pages import _dossier
import facts
from facts import prose
from render import C, L

NAME = "ParcelRound"
PAGE = {"file": "work-parcelround.html", "nav": "Work",
        "title": "ParcelRound — Work — loganw.dev",
        "description": "The dossier for ParcelRound: what it is, its contract, what its case studies record, "
                        "the failures it kept, and how to try to prove it wrong."}


def _sections():
    S = _dossier.section

    what_it_is = S("What it is", [_dossier.para([
        prose(NAME, "README.md",
              r"^(A method for splitting one body of work across several coding agents at\s+once, without the "
              r"pieces failing to meet)\."), "."])])

    what_it_is_not = S("What it is not", [_dossier.para([
        "Under “", prose(NAME, "README.md", r"## (Is this for you\?)"), "”: ",
        "“Don't” ", prose(NAME, "README.md",
              r"\*\*Don't\*\* (for a single task, for exploratory work where the split isn't\s+obvious yet, or "
              r"where the pieces can't be tested separately)\."), ". ",
        prose(NAME, "README.md",
              r"(Two agents\s+on a two-way split is usually slower than doing it yourself, because\s+the brief "
              r"costs more than the work)\."), "."])])

    contract = S("The contract", [_dossier.para([
        "Under “", prose(NAME, "METHOD.md", r"## 1\. (The one failure mode)"), "”: ",
        prose(NAME, "METHOD.md",
              r"The failure is that (\*\*the work between the parcels belongs to\s+nobody\*\*, and it is "
              r"invisible because every parcel's own gate is green)\."), "."])])

    verified = S("Verified", [
        _dossier.para(["No ", C("docs/VALIDATION.md"), " ledger and no workflow: the method has no build of its "
                       "own to gate. What its case studies record instead is a measurement of the method: "]),
        _dossier.list_([
            ["The round ", C("CASE-STUDY.md"), " measures returned “",
             prose(NAME, "README.md",
                   r"\*\*(twelve corrections from five parcels — every single parcel\s+corrected its brief)"
                   r"\*\*", num=True),
             "”, on the strength of one line: “",
             prose(NAME, "README.md", r'\*"(Report anything you found that this brief got wrong)\."\*'), ".”"],
        ])])

    kept_failures = S("Kept failures", [_dossier.list_([
        [prose("ParcelRound", "CASE-STUDY-2.md",
               r"(every guess was AHEAD of the clock \(by 3 to 90 minutes\))", num=True), ", across every author "
         "of that round. ",
         prose(NAME, "CASE-STUDY-2.md",
               r"(The fix that finally held for the lead was mechanical: write the entry with a placeholder and "
               r"let the append command substitute `date`)\."), " The method's own rule now: “",
         prose(NAME, "CASE-STUDY-2.md", r"(stamps are substituted, not typed)\."), "” Recorded by commit ",
         _dossier.kept_failure(NAME, "f2a0483", "P3's first findings and self-corrected stamps: the clock, "
                                "again — the origin of this ledger's own timestamp rule"), "."],
        [prose(NAME, "CASE-STUDY-2.md",
               r"(which is how a wrong number propagates - it was in the ledger for fifteen minutes and got used "
               r"once)"), ". ",
         prose(NAME, "CASE-STUDY-2.md",
               r"(a correction should EDIT nothing but should be linked from the entry it corrects)"), " (",
         prose(NAME, "CASE-STUDY-2.md",
               r"(\"see 11:52\" appended below the old entry is an append, not an edit)"), "), and ",
         prose(NAME, "CASE-STUDY-2.md",
               r"(a number a sibling might reuse should be stated in the entry that supersedes it in the form the "
               r"sibling would search for)\."), ". Recorded by commit ",
         _dossier.kept_failure(NAME, "42e76cc", "V2 finds a regression and a propagated wrong number: the "
                                "correction that ships beneath a stale number can still lose to it"), "."],
    ])])

    test_it = S("Test it", [_dossier.list_([
        ["Read ", C("CASE-STUDY.md"), "'s worked example yourself and check its timeline is internally "
         "consistent — free, and the whole argument for the method rests on it."],
        ["Compare ", C("templates/brief.md"), " and ", C("templates/verifier.md"), " against what the case "
         "studies say a brief and a verifier actually did."],
        ["Try the method's own seam test on a codebase you already know: list every file each of several "
         "independent changes would touch, and see whether one file appears in several such lists at once."],
    ], ordered=True)])

    prove_it_wrong = S("Prove it wrong", [
        _dossier.para(["Cheapest first; the site-wide rules of engagement are stated once, on the Corrections "
                       "page — not yet built, so this dossier does not link it."]),
        _dossier.list_([
            ["Count ", C("CASE-STUDY.md"), "'s own corrections yourself; a count that disagrees with the figure "
             "this dossier's Verified section quotes is a disproof."],
            ["Read the worked example's timestamps against the commits it cites, and check each one exists."],
            ["Apply the method to a real, multi-agent piece of work of your own and see whether the one failure "
             "mode still finds something the briefs missed; a clean round is evidence against the method's reach, "
             "not proof it is wrong, since “found nothing” is a stated, acceptable result here too."],
        ], ordered=True)])

    connections = S("Connections", [_dossier.connections_block(NAME)])

    provenance = S("Provenance", _dossier.provenance_block([
        (NAME, ["README.md", "METHOD.md", "CASE-STUDY.md", "CASE-STUDY-2.md"]),
    ]))

    return [what_it_is, what_it_is_not, contract, verified, kept_failures, test_it, prove_it_wrong,
            connections, provenance]


def render_page(ctx):
    sections = _sections()
    ctx["_p3_sections"] = sections
    return _dossier.html(NAME, sections)


def extra_files(ctx):
    sections = ctx.get("_p3_sections") or _sections()
    text = _dossier.twin(NAME, "%s — dossier" % NAME, sections)
    html = _dossier.html(NAME, sections)
    _dossier.twin_ids(NAME, html, text)
    return {"work-parcelround.txt": text}
