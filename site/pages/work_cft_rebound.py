"""Dossier: cft-rebound (docs/SPEC.md, "Work"; decision 15)."""
from pages import _dossier
import facts
from facts import prose
from render import C, L

NAME = "cft-rebound"
PAGE = {"file": "work-cft-rebound.html", "nav": "Work",
        "title": "cft-rebound — Work — loganw.dev",
        "description": "The dossier for cft-rebound: what it is, its contract, what has verified it, "
                        "the failures it kept, and how to try to prove it wrong."}


def _sections(built):
    S = _dossier.section

    what_it_is = S("What it is", [_dossier.para([
        prose(NAME, "README.md",
              r"^(REBOUND's IAS15 integrator with its arithmetic routed through libcft,\s+the IEEE 754-2019 "
              r"binary32/64/128/256 library of the cft-fp256\s+project, so that the same integrator runs at "
              r"binary64, binary128 and\s+binary256 - and, given an artifact, on the FP256 tile - with the same"
              r"\s+bits everywhere)\."), "."])])

    what_it_is_not = S("What it is not", [
        _dossier.para(["The README carries no “what it is not” heading. Its nearest equivalent is “",
                       prose(NAME, "README.md", r"## (Scope: what it integrates, and what it refuses)"),
                       "”, a refusal list rather than a limits statement. In the README's own words: “",
                       prose(NAME, "README.md",
                             r"(Everything below is refused, \*\*by name, with a message\*\* - never\s+silently "
                             r"ignored, never approximated)\."), ". ",
                       prose(NAME, "README.md",
                             r"(The list is one table in code\s+\(`cft_support_rows`, src/cft_supported\.c\) that "
                             r"both entry points walk,\s+and the gate walks it too and fails on any row no case "
                             r"exercises)\."), "”"]),
        _dossier.list_([
            [prose(NAME, "README.md", r"\| the tree code \(`REB_GRAVITY_TREE`\) \| "
                                       r"(this is direct summation\. `REB_GRAVITY_COMPENSATED` is refused too: a "
                                       r"different summation from the one ported) \|")],
            [prose(NAME, "README.md", r"\| every integrator except IAS15 \| "
                                       r"(WHFast is ranked first to follow \(docs/INTEGRATORS\.md\) and has not "
                                       r"been done) \|")],
            [prose(NAME, "README.md", r"\| `N_active > N` \| "
                                       r"(a heap overread in REBOUND's own gravity loop\. There is no bit-identity "
                                       r"to claim against undefined behaviour) \|")],
        ])])

    contract = S("The contract", [_dossier.para([
        prose(NAME, "README.md",
              r"(At binary64 it is\s+REBOUND's own IAS15 bit for bit, which is a gate the port passes on\s+every "
              r"build)\."), "."])])

    verified = S("Verified", [
        _dossier.para(["Last verified: ", facts.last_verified(NAME), "."]),
        _dossier.list_([
            [L(facts.pin(NAME).href("docs/VALIDATION.md", 123), _dossier.ledger_title(NAME, "docs/VALIDATION.md", 123))],
            [_dossier.ledger_date(NAME, "docs/VALIDATION.md", 3638), " — ",
             L(facts.pin(NAME).href("docs/VALIDATION.md", 3638), _dossier.ledger_title(NAME, "docs/VALIDATION.md", 3638))],
        ])])

    kept_failures = S("Kept failures", [_dossier.list_([
        [prose(NAME, "docs/VALIDATION.md",
               r"(REBOUND's IAS15 was thought to leave a \*stale polynomial\* behind when a\s+particle is "
               r"removed):"), ". ",
         prose(NAME, "docs/VALIDATION.md",
               r"(So the polynomial is not stale\. It is aliased, and the survivors do not\s+inherit each other's "
               r"coefficients - they inherit fragments of the level\s+above)\."),
         " — ", _dossier.ledger_date(NAME, "docs/VALIDATION.md", 2705), ", ",
         L(facts.pin(NAME).href("docs/VALIDATION.md", 2705), _dossier.ledger_title(NAME, "docs/VALIDATION.md", 2705)),
         ". Fixed by commit ",
         _dossier.kept_failure(NAME, "1561d35", "ias15_engine_alias_resize gathers the seven coefficient levels "
                                "into a shadow at the old stride and reads them back at the new one"), "."],
        [prose(NAME, "docs/VALIDATION.md",
               r"(A banner is the only place in this suite that states a step count\s+without executing it, so "
               r"under `--light` it was the only place that\s+could overstate the work done)\."),
         " — ", _dossier.ledger_date(NAME, "docs/VALIDATION.md", 3070), ", ",
         L(facts.pin(NAME).href("docs/VALIDATION.md", 3070), _dossier.ledger_title(NAME, "docs/VALIDATION.md", 3070)),
         ". Fixed by commit ",
         _dossier.kept_failure(NAME, "e12aed9", "every banner prints light_ran(steps), the count that actually ran"),
         "."],
    ])])

    test_it = S("Test it", [_dossier.list_([
        [C("make check-quick"), ": ", prose(NAME, "CLAUDE.md", r"\| `make check-quick` \| (cheaper arguments \+ "
           r"the gate cache) \|"), ", ", prose(NAME, "CLAUDE.md", r"\| `make check-quick` \|[^|]+\| (5 s warm) \|"),
         "."],
        [C("make check-light"), ": ", prose(NAME, "CLAUDE.md", r"\| `make check-light` \| (cheaper arguments \+ "
           r"cache \+ \*\*scaled step counts\*\*) \|", display="cheaper arguments, the cache, and step counts "
           "scaled down"), ", ", prose(NAME, "CLAUDE.md", r"\| `make check-light` \|[^|]+\| (~9 min) \|"), "."],
        [C("make check"), ": ", prose(NAME, "CLAUDE.md", r"\| `make check` \| (every gate at every format, "
           r"\*\*never skips\*\*) \|", display="every gate at every format, never skipping one"), ", ",
         prose(NAME, "CLAUDE.md", r"\| `make check` \|[^|]+\| (~55–70 min) \|"), "."],
    ], ordered=True)])

    prove_it_wrong = S("Prove it wrong", [
        _dossier.prove_it_wrong_opening(built),
        _dossier.list_([
            [C("make check-quick"), " on a clean clone, and see whether the cache lets anything silently pass: ",
             prose(NAME, "CLAUDE.md", r"(Every skip prints itself by name)"), "."],
            [C("make check-light"), " end to end, and compare it against ", C("make check"), " on the same "
             "commit: a scaled leg that disagrees with the full one is a disproof."],
            ["Point ", C("CFT_REBOUND_ARTIFACT"), " at the software backend and at a card image on the same "
             "problem and diff every coordinate: the contract is bit identity at binary64, not agreement within "
             "a tolerance."],
            ["Run ", C("make check"), " itself, which ", prose(NAME, "CLAUDE.md", r"`make check` is the one whose "
             r"meaning must not change, so it always\s+(executes)"), ", and read the log rather than the exit "
             "code."],
        ], ordered=True)])

    connections = S("Connections", [_dossier.connections_block(NAME)])

    provenance = S("Provenance", _dossier.provenance_block([
        (NAME, ["README.md", "CLAUDE.md", "docs/VALIDATION.md"]),
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
    return {"work-cft-rebound.txt": text}
