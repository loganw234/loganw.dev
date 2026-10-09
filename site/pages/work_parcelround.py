"""Dossier: ParcelRound (docs/SPEC.md, "Work"; decision 15). It keeps no
docs/VALIDATION.md ledger and no workflow (pins.json: "workflows": {}). Its
sixth round gave it a gate of its own, tools/check_method.py, and an adoption
record, ADOPTION.md. This page quotes the gate and never runs it: "Verified"
reads what the gate says it holds, what ADOPTION.md records and what the case
studies measured, rather than a build.
"""
import re

from pages import _dossier
import facts
from facts import V, Refusal, fact, pin, prose
from render import C

NAME = "ParcelRound"
PAGE = {"file": "work-parcelround.html", "nav": "Work",
        "title": "ParcelRound — Work — loganw.dev",
        "description": "The dossier for ParcelRound: what it is, its contract, what its gate and its case studies "
                        "record, the failures it kept, and how to try to prove it wrong."}

# ADOPTION.md's table: `| id | proposal | type | status | evidence | ...`. The ids are the
# four kinds the method's own gate reads (a case study's proposals, and the B, R and S rows).
_ROW = re.compile(r"^\| (?:CS\d+#\d+|B\d+|R\d+|S\d+) \| .*? \| .*? \| (.*?) \| ", re.M)
_STATUSES = ("adopted in part", "adopted", "pending", "not adopted")


@fact
def adoption_state(name):
    """ADOPTION.md's rows, counted by status at the pin. A status it does not
    know is refused by name, so a new kind of status cannot be left out of the
    count; so is a file with no rows."""
    p = pin(name)
    rows = _ROW.findall(p.show("ADOPTION.md"))
    if not rows:
        raise Refusal("%s %s: no rows in ADOPTION.md's table" % (name, p.short))
    count = dict.fromkeys(_STATUSES, 0)
    for status in rows:
        kind = next((s for s in _STATUSES if status.startswith(s)), None)
        if kind is None:
            raise Refusal("%s %s ADOPTION.md: a row's status is %r, which is not one of %s"
                          % (name, p.short, status[:40], ", ".join(_STATUSES)))
        count[kind] += 1
    text = "%d rows: %d adopted, %d adopted in part, %d pending, %d not adopted" % (
        len(rows), count["adopted"], count["adopted in part"], count["pending"], count["not adopted"])
    return V(text, p.src("file", "ADOPTION.md", "its %d rows, counted by the status column" % len(rows),
                         "ADOPTION.md"), raw=text, num=True)


def _sections(built):
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
              r"invisible because every parcel's own gate is green)\."), ". Of its own rules it says: “",
        prose(NAME, "METHOD.md",
              r"^(Every rule here is here because something broke without it, or because\s+its practice caught a "
              r"defect before it shipped, or, where the rule says\s+so, because it rests on practice that held, "
              r"on a cost, or on the owner's\s+word)\."), ".”"])])

    verified = S("Verified", [
        _dossier.para(["No ", C("docs/VALIDATION.md"), " ledger and no workflow. The sixth round's case study "
                       "records what that round added: “",
                       prose(NAME, "CASE-STUDY-6.md",
                             r"- the method gets (a gate of its own, `tools/check_method\.py`, and an\s+adoption "
                             r"record, ADOPTION\.md, one row per proposal);"), ".” Of what the gate reads, its own "
                       "docstring says: “",
                       prose(NAME, "tools/check_method.py",
                             r"^(It reads structure and citations, never what a rule says)\."), ".” It gives the "
                       "gate's threat model: “",
                       prose(NAME, "tools/check_method.py",
                             r"^(Threat model \(the owner's decision, 2026-10-02\)\. The gate guards against two\s+"
                             r"things)", num=True), "”, namely “",
                       prose(NAME, "tools/check_method.py", r"^  - (drift by honest, fallible authors):"),
                       "” and “",
                       prose(NAME, "tools/check_method.py", r"^  - (accidental publication):"),
                       "”; and it states what it does not guard against: “",
                       prose(NAME, "tools/check_method.py", r"^(It does not guard against deliberate evasion):"),
                       ".” This page quotes the gate and does not run it; Test it, below, says how you can."]),
        _dossier.para(["What the method's records hold, and what its case studies measured:"]),
        _dossier.list_([
            [C("ADOPTION.md"), ", which says what METHOD.md has taken in from each case study, holds ",
             adoption_state(NAME), ". For a pending row it says: “",
             prose(NAME, "ADOPTION.md", r"The reason is given\. (A\s+pending proposal is the owner's to settle)\."),
             ".”"],
            ["The round ", C("CASE-STUDY.md"), " measures returned “",
             prose(NAME, "README.md",
                   r"\*\*(twelve corrections from five parcels — every single parcel\s+corrected its brief)"
                   r"\*\*", num=True),
             "”, on the strength of one line: “",
             prose(NAME, "README.md", r'\*"(Report anything you found that this brief got wrong)\."\*'), ".”"],
            ["The sixth round records the same of its own parcels: “",
             prose(NAME, "CASE-STUDY-6.md", r"\d+\. \*\*(Every parcel corrected its brief)\.\*\*"),
             "”, and for its first wave “",
             prose(NAME, "CASE-STUDY-6.md",
                   r"\*\*Wave 1\.\*\* (Thirteen brief errors from four parcels, each confirmed by\s+the lead at "
                   r"its source)", num=True), ".”"],
            ["The sixth round also planted faults in the copies its verifiers worked on: “",
             prose(NAME, "CASE-STUDY-6.md", r"\*\*Planted faults: (ten of ten caught, from the sources)\.\*\*",
                   num=True), ".” Its own reading of that figure: “",
             prose(NAME, "CASE-STUDY-6.md",
                   r"(A verifier that\s+read the design first could have found every plant by comparison\s+alone)"
                   r"\."), ".”"],
        ])])

    kept_failures = S("Kept failures", [_dossier.list_([
        [prose("ParcelRound", "CASE-STUDY-2.md",
               r"(every guess was AHEAD of the clock \(by 3 to 90 minutes\))", num=True), ", across every author "
         "of that round. ",
         prose(NAME, "CASE-STUDY-2.md",
               r"(The fix that finally held for the lead was mechanical: write the entry with a placeholder and "
               r"let the append command substitute `date`)\."), " The method's own rule now: “",
         prose(NAME, "CASE-STUDY-2.md", r"(stamps are substituted, not typed)\."), ".” METHOD.md adds, from the "
         "third round, that “",
         prose(NAME, "METHOD.md",
               r"corrects what round 2 was taken to show: (a typed stamp errs in both\s+directions)\."),
         "”: “",
         prose(NAME, "METHOD.md",
               r"(Most guesses there ran ahead of the clock too, but two ran behind,\s+both by about four "
               r"minutes)\."), ".” Recorded by commit ",
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
        ["The method's own gate, in its sixth round: “",
         prose(NAME, "CASE-STUDY-6.md", r"\d+\. \*\*(A parcel found a gate control that could not fail)\.\*\*"),
         ".” “",
         prose(NAME, "CASE-STUDY-6.md",
               r"(Once a parcel cited a cft-fp256 line beside the pin,\s+as every parcel would, the pin was named "
               r"and the control could not fail)\."), ".” The method's own rule: “",
         prose(NAME, "METHOD.md", r"\*\*(A gate that cannot fail is not a gate)\*\*"), ".” Fixed by commit ",
         _dossier.kept_failure(NAME, "1dc5ed4", "the foreign-pin control stays live wherever a pin is cited"),
         "."],
    ])])

    test_it = S("Test it", [_dossier.list_([
        [C("python tools/check_method.py"), ": “",
         prose(NAME, "README.md",
               r"\| (The front door: `python tools/check_method\.py` says whether the method still holds together);"),
         ".” Its docstring adds: “",
         prose(NAME, "tools/check_method.py", r"(There\s+is no cache: each run reads everything again)\."), ".”"],
        [C("python tools/check_method.py --control"), ": “",
         prose(NAME, "README.md", r"; (`--control` shows each of its checks can fail)\."), "”; in its docstring's "
         "words, it will “",
         prose(NAME, "tools/check_method.py",
               r"--control\s+(plant faults, each in a copy of the\s+tree or in a scratch repository, at\s+least "
               r"one per check; each must be\s+caught)"), ".”"],
        ["Read ", C("CASE-STUDY.md"), "'s worked example yourself and check that its account holds together — "
         "free, and README.md calls it “", prose(NAME, "README.md", r"## (The clearest single argument for it)"),
         ".”"],
        ["Compare ", C("templates/brief.md"), " and ", C("templates/verifier.md"), " with ", C("METHOD.md"),
         ": ADOPTION.md says “",
         prose(NAME, "ADOPTION.md",
               r"(Each rule in a template is tagged, in\s+parentheses, with the METHOD\.md section it comes from, "
               r"or \"own\" for the\s+templates' own guidance, as each template's legend says)"),
         ",” so follow a tag, and read the section it names."],
        ["Try the method's own seam test on a codebase you already know: list every file each of several "
         "independent changes would touch, and see whether one file appears in several such lists at once."],
    ], ordered=True)])

    prove_it_wrong = S("Prove it wrong", [
        _dossier.prove_it_wrong_opening(built),
        _dossier.list_([
            ["Build a fault the gate's threat model covers, in a copy of the tree, and run ",
             C("python tools/check_method.py"), ". Its docstring claims: “",
             prose(NAME, "tools/check_method.py",
                   r"(Inside the threat model, the gate must catch it\s+or a limit below must state it)\."),
             ".” A fault inside the model that passes, with no stated limit covering it, is a disproof."],
            ["Pick a row of ", C("ADOPTION.md"), " marked adopted, or a line of a template tagged with a section, "
             "and read the METHOD.md section it names. The gate states what it cannot see there: “",
             prose(NAME, "tools/check_method.py",
                   r"- anchors: (it holds that an adopted row's headings exist, not that the rule\s+is under them)"
                   r"\."), ",” and “",
             prose(NAME, "tools/check_method.py",
                   r"(It holds that a section named exists, not that it holds the rule the\s+line beside it "
                   r"claims)\."), ".” A section that does not hold the rule is a disproof."],
            ["Check the sources of the timeline in ", facts.exists(NAME, "CASE-STUDY-6.md"), ". Its heading says “",
             prose(NAME, "CASE-STUDY-6.md",
                   r"(from the ledger's own timestamps, and from the commits' times where a row says so)\)"),
             ".” Compare a row that says so with the times of the commits it describes, and any other row with the "
             "stamp of the ledger entry it comes from. A row that disagrees with its source is a disproof."],
            ["Recount the sixth round against the ledger its case study archives: “",
             prose(NAME, "CASE-STUDY-6.md",
                   r"(The ledger is archived beside this file as\s+\[archive/round6-ledger\.zip\]"
                   r"\(archive/round6-ledger\.zip\))", num=True), ".” The figures Verified quotes from that case "
             "study are counts a recount can disagree with; a count the archived ledger does not bear out is a "
             "disproof."],
            ["Apply the method to a real, multi-agent piece of work of your own and see whether the one failure "
             "mode still finds something the briefs missed; a clean round is evidence against the method's reach, "
             "not proof it is wrong, since “found nothing” is a stated, acceptable result here too."],
        ], ordered=True)])

    connections = S("Connections", [_dossier.connections_block(NAME)])

    provenance = S("Provenance", _dossier.provenance_block([
        (NAME, ["README.md", "METHOD.md", "ADOPTION.md", "CASE-STUDY.md", "CASE-STUDY-2.md", "CASE-STUDY-6.md",
                "tools/check_method.py"]),
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
    return {"work-parcelround.txt": text}
