"""Dossier: HonestFramework (docs/SPEC.md, "Work"; decision 15). It keeps no
docs/VALIDATION.md ledger, so "Verified" re-derives the two figures its own
tools/check_claims.py holds equal, straight from the pin - never by running
that script against a live checkout (briefs/_common.md: read other
repositories only at their pins).
"""
import re

from pages import _dossier
import facts
from facts import V, Src, Refusal, fact, pin, prose
from render import C, L

NAME = "HonestFramework"
PAGE = {"file": "work-honestframework.html", "nav": "Work",
        "title": "HonestFramework — Work — loganw.dev",
        "description": "The dossier for HonestFramework: what it is, its contract, what it records, "
                        "the failures it kept, and how to try to prove it wrong."}

_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
          "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15}


@fact
def mechanism_count_agrees(name):
    """METHOD.md's own numbered sections, counted at the pin, matching the
    word README.md states for them - the same equality tools/check_claims.py
    holds, re-derived here rather than run against a working tree."""
    p = pin(name)
    method, readme = p.show("METHOD.md"), p.show("README.md")
    sections = re.findall(r"^## (\d+)\. ", method, re.M)
    if sorted(int(s) for s in sections) != list(range(1, len(sections) + 1)):
        raise Refusal("%s: METHOD.md's sections are not numbered 1..%d" % (name, len(sections)))
    m = re.search(r"The (\w+) mechanisms", readme)
    if not m or _WORDS.get(m.group(1).lower()) != len(sections):
        raise Refusal("%s: README.md's word for the mechanism count does not match METHOD.md's %d sections"
                      % (name, len(sections)))
    return V(str(len(sections)), p.src("git", "METHOD.md and README.md",
                                       "METHOD.md's numbered sections, counted, against README.md's own word for them"),
             raw=str(len(sections)), num=True)


@fact
def case_study_total_agrees(name):
    """CASE-STUDY.md's per-repository table, summed at the pin, against the
    headline figure the same document and the README both quote - the other
    equality tools/check_claims.py holds."""
    p = pin(name)
    cs, readme = p.show("CASE-STUDY.md"), p.show("README.md")
    rows = re.findall(r"^\| `([a-z0-9-]+)` \| ([\d,]+) \| ([\d,]+) \|", cs, re.M)
    if len(rows) < 2:
        raise Refusal("%s: CASE-STUDY.md's repository table could not be found" % name)
    total = sum(int(r[1].replace(",", "")) for r in rows)
    claimed = {int(x.replace(",", "")) for x in re.findall(r"\*\*([\d,]{7,}) tracked lines\*\*", cs)}
    if claimed != {total}:
        raise Refusal("%s: CASE-STUDY.md's headline total does not match its own table's sum" % name)
    if not any(int(x.replace(",", "")) == total for x in re.findall(r"([\d]{3},\d{3}) lines", readme)):
        raise Refusal("%s: README.md's lines figure does not match CASE-STUDY.md's table" % name)
    return V("{:,}".format(total), p.src("git", "CASE-STUDY.md and README.md",
                                          "the %d-repository table, summed, against both documents' headline figure"
                                          % len(rows)),
             raw=str(total), num=True)


def _sections():
    S = _dossier.section
    mechanisms = mechanism_count_agrees(NAME)
    case_total = case_study_total_agrees(NAME)

    what_it_is = S("What it is", [_dossier.para([
        prose(NAME, "README.md",
              r"^(A way to lay out a project so that an AI can write nearly all of it and\s+\*\*no claim about it "
              r"ever rests on the AI's judgement\*\*)\."), "."])])

    what_it_is_not = S("What it is not", [_dossier.list_([
        [prose(NAME, "README.md",
               r"(\*\*Not a prompting guide\.\*\*\s+Nothing here depends on phrasing, model, or\s+version\. The "
               r"mechanisms are files and exit codes)\.")],
        [prose(NAME, "README.md",
               r"(\*\*Not a substitute for tests\.\*\*\s+It is a set of properties your tests and\s+build must "
               r"have before their green means anything)\.")],
        [prose(NAME, "README.md",
               r"(\*\*Not free\.\*\*\s+A project built this way carries a reference implementation it\s+could "
               r"have done without, a second copy of some checks, and a ledger that only\s+grows)\.")],
        [prose(NAME, "README.md",
               r"(\*\*Not about distrusting the agent\.\*\*\s+The agent in the case study wrote\s+essentially all "
               r"of 743,605 lines across six repositories, including every\s+mechanism described here, and found "
               r"most of the defects listed in it)\.", num=True)],
    ])])

    contract = S("The contract", [_dossier.para([
        prose(NAME, "README.md", r"(That is the whole thesis in one example)\."), ". ",
        prose(NAME, "README.md", r"(The agent wrote every line of the\s+fix)\."), ". ",
        prose(NAME, "README.md", r"(It decided nothing about whether the fix worked)\."), "."])])

    verified = S("Verified", [
        _dossier.para(["No ", C("docs/VALIDATION.md"), " ledger: HonestFramework is a document, not a build. What "
                       "it records instead is its own ", L(pin(NAME).href("tools/check_claims.py"),
                       facts.exists(NAME, "tools/check_claims.py")), ", which holds facts about itself equal "
                       "on every run. Re-read here from the pin, not by running that script against a checkout:"]),
        _dossier.list_([
            ["METHOD.md's numbered mechanisms: ", mechanisms, ", agreeing with the word README.md states for "
             "them."],
            ["CASE-STUDY.md's per-repository table sums to ", case_total, " tracked lines, agreeing with the "
             "headline both documents quote."],
        ])])

    kept_failures = S("Kept failures", [_dossier.list_([
        [prose(NAME, "METHOD.md",
               r"### (The trap has a second floor, and I fell through it)"), ". atlas-optical's own gate: “",
         prose(NAME, "METHOD.md", r"(The gate and the test use the \*\*computed\*\* one)\."), ".” ",
         prose(NAME, "METHOD.md", r"\*\*(So the rule needs its sharper form:)\*\*"), " ",
         prose(NAME, "METHOD.md",
               r"\*(a committed source figure is an\s+external authority only if the source derived it from "
               r"something other than the\s+input you are feeding it)\.\*"),
         ". Corrected by commit ",
         _dossier.kept_failure(NAME, "65447fd", "§1's external-authority case: two parsers agreeing is not "
                                "an authority"), " — this dossier's own pin."],
        [prose(NAME, "METHOD.md",
               r"(This is the part I got wrong, and it is worth more than the part I got right)\."), ". “",
         prose(NAME, "METHOD.md",
               r"(its controls, its key and both audit reports all\s+landed in \*\*one commit\*\*)\.", num=True),
         ".” “",
         prose(NAME, "METHOD.md",
               r"(There is no state of the repository in which the\s+controls exist without the key)"), " — so "
         "the blinding was never verifiable from the record. ",
         prose(NAME, "METHOD.md",
               r"### (Make the blinding a property of the record, not of your working tree)"),
         " is the fix. Corrected by commit ",
         _dossier.kept_failure(NAME, "759bb68", "§9's own citation: the blinding was never verifiable from the "
                                "record"), "."],
    ])])

    test_it = S("Test it", [_dossier.list_([
        [C("python tools/check_claims.py"), ": ", prose(NAME, "README.md",
         r"\[tools/check_claims\.py\]\(tools/check_claims\.py\)[^|]*\|\s*(This repo's own gate)\."), " — links, "
         "the mechanism count and the case-study total, all re-checked in under a second."],
        ["Recompute ", C("CASE-STUDY.md"), "'s per-repository table by hand: the same arithmetic ",
         case_total, " already shows, done again with nothing but the table."],
    ], ordered=True)])

    prove_it_wrong = S("Prove it wrong", [
        _dossier.para(["Cheapest first; the site-wide rules of engagement are stated once, on the Corrections "
                       "page — not yet built, so this dossier does not link it."]),
        _dossier.list_([
            [C("python tools/check_claims.py"), " on a clone, and see whether it still finds nothing."],
            ["Add up ", C("CASE-STUDY.md"), "'s per-repository table yourself; a sum that disagrees with the "
             "quoted headline is a disproof the script would also catch."],
            ["Pick one of the load-bearing quotations the audit re-verified and fetch its named source yourself: "
             "the method's own rule is that a citation is checked by fetching, not by plausibility."],
            ["Re-audit the claim-source controls in ", C("atlas-darkroom"), "'s external-sources programme "
             "against their named sources; that repository is private for now, so this is the one item here this "
             "dossier cannot hand you a path to."],
        ], ordered=True)])

    connections = S("Connections", [_dossier.connections_block(NAME)])

    provenance = S("Provenance", _dossier.provenance_block([
        (NAME, ["README.md", "METHOD.md", "CASE-STUDY.md", "tools/check_claims.py"]),
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
    return {"work-honestframework.txt": text}
