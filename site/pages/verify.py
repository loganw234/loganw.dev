"""Verify: "Don't trust this - run one." (docs/SPEC.md, "Verify"; briefs/P1.md).

Four checks, in the spec's order, each with what it costs, where and when that
was measured where a source says, and what a pass does and does not prove.
The page ranks them by no cost (decision 56): no current figure ranks them on
one machine, since the replay has no time, make golden's newest timing is the
runner's golden stage on the build box, of 2026-10-30, and CLAUDE.md's two
budget lines name no machine and no date. Their time figures were written on
2026-09-12 and have not changed since; their stage counts have, last on
2026-10-22 (git log -L at the pin; verifier-P2's second pass, round 3).
docs/VERIFICATION.md dates its own figure for the gate, quiet on
the Windows desktop in the census of 2026-09-04 and loaded on 2026-09-07
(item 3 quotes where and when). The first three checks
are sourced at cft-fp256's pin (its README, CLAUDE.md, docs/VERIFICATION.md,
CONFORMANCE.md, bindings/wasm/README.md, verify/run.sh, the Makefile and its
ledger); the fourth is this
site's own, described the way its own documents already describe it -
loganw.dev is not itself a pin, so there is no file to quote through
facts.prose() for a claim about this site's own build.

The site's own limit, stated once at the end: every quotation above shows
that this page quotes cft-fp256 faithfully at its pin. It does not show that
cft-fp256's claims are true - cft-fp256's own gates decide that, and running
one of the four checks is how a reader checks it directly. Beside it, in
cft-fp256's own words and not ours, what its documents say those gates do not
reach (limits()): the defects its record shows the gates passing and the
digests limit. After that list, in this site's words, the card's nightly run,
which is none of the checks.

A long quotation (the lede, the two budgets, the limits) is written with ws(),
so that a rewrap of the document it quotes does not break it. A ledger entry
is cited by its heading's line at the pin, which _dossier.ledger_date and
ledger_title refuse unless it is a heading; the lines below are checked
against the headings they name, and a pin that moves them refuses the build.
"""
import re

import facts
from pages import _dossier
from render import C, L, SOURCE_REPO, render

PAGE = {"file": "verify.html", "nav": "Verify",
        "title": "Verify - loganw.dev",
        "description": "Don't trust this page - run one of the checks below."}

VALIDATION = "docs/VALIDATION.md"
WASM = "bindings/wasm/README.md"

# cft-fp256's ledger entries this page reads, by the line of their heading at the pin.
EXP2_TIE = 18206       # 2026-10-05: the golden model's exp2 tie fixed, the profile's major step to 3
DIGESTS_OPEN = 23474   # 2026-10-22: gates that could pass a damaged input; it keeps the digests limit open
GOLDEN_RUN = 26082     # 2026-10-30: the lead's entry whose gate runs hold the golden stage's newest timing
ISSUE_1 = 26149        # 2026-10-30: the report, its fix, and the committed module's rebuild


def ws(text):
    """A literal as a pattern in which every run of spaces may be any whitespace, so that a rewrap of the
    document it quotes does not break the quote; every other character is matched exactly."""
    return r"\s+".join(re.escape(w) for w in text.split())


# The browser replay's full claim, as bindings/wasm/README.md writes it at the pin; controls() gives the same
# sentence the count the old pin's README had.
FULL_CLAIM = ws("For the full 1,072,415-case claim, generate the sets in a checkout (`make vectors`) and drag the "
                "`vectors/out/*.jsonl` files onto the page - same code path, whole files")


def _lede():
    P = facts.prose
    return render([
        "cft-fp256's contract, in its own words: “",
        P("cft-fp256", "CONFORMANCE.md",
          "(" + ws("It is written so that an implementation can be built and proven without this repository's RTL "
                   "or library - a different chip, a different process, a different language - and still be "
                   "interchangeable with them bit for bit") + ")"),
        ".” The checks below are how a reader confirms that directly, without taking this site's word for it.",
    ])


def checks():
    P = facts.prose
    url = P("cft-fp256", "README.md", r"\*\*<(https://loganw234\.github\.io/cft-fp256/)>\*\*")
    items = []

    # The replay is a committed build product, and its record says so (decision 56 asks no cost of it: it has a
    # browser tab and no time). What it holds is the page's own README's sample. The module it runs was stale from
    # 2026-10-22 until b9d60ebc, as the entry quoted below says; the record tells of an earlier stale module too, in
    # its section on ABI 0.12, so this gives no count (verifier-P2's first pass, round 3).
    items.append([
        L(url.raw, "cft-fp256's own conformance replay"), ", in the browser. Cost: a browser tab, nothing "
        "installed. It ",
        P("cft-fp256", "README.md", r"It (replays\s+the published conformance vectors in front of you)"),
        ". What it holds, in the page's own README: “",
        P("cft-fp256", WASM,
          "(" + ws("The embedded sample (4,015 cases; deterministic rule below) spans all four formats, all five "
                   "rounding attributes and every opcode class") + ")"),
        ".” And for the full claim: “",
        P("cft-fp256", WASM, "(" + FULL_CLAIM + ")"),
        ".” What a green verdict proves, in the same README: “",
        P("cft-fp256", WASM,
          r"\*\*(" + ws("compiling this library to wasm cannot have changed a single result bit, and the replay shows "
                        "it did not") + r")\.\*\*"),
        ".” Its module is a committed build product, and cft-fp256's record says of it, in the entry of ",
        _dossier.ledger_date("cft-fp256", VALIDATION, ISSUE_1), ": “",
        P("cft-fp256", VALIDATION, "(" + ws("the committed module was stale from 2026-10-22") + ")"),
        ",” and “",
        P("cft-fp256", VALIDATION,
          r"- \*\*(" + ws("b9d60ebc, the module.** The node module, the conformance page and the demos page were "
                          "rebuilt in the pinned emsdk 6.0.9 image") + ")"),
        ".”",
    ])

    # Decision 56 and the lead's ruling: the record's newest timing of the golden stage, with its entry's date and
    # host, and no old cell. docs/VERIFICATION.md's table (its golden row, line 354 at the pin) gives other figures
    # for it, which this line overtakes; P1's dossier quotes the same line. The runner's own line for the stage is
    # quoted beside it, and the Makefile's for `make golden`, so that the timing's basis is on the page: the runner's
    # names no worker option, and `make golden` adds pytest-xdist's workers where it imports (Makefile:20, :22, :26
    # and :112 at the pin). The timing is the runner's, not make golden's (verifier-P2's first pass, round 3).
    items.append([
        C("make golden"), " in a clone of cft-fp256. Cost: the record's newest timing of the golden stage, in the "
        "entry of ", _dossier.ledger_date("cft-fp256", VALIDATION, GOLDEN_RUN), ", on ",
        P("cft-fp256", VALIDATION, r"MEASURED on (amd-arc-box) \(box_m2f2\.sh at 922c2ade"), ": “",
        P("cft-fp256", VALIDATION, r"  - (golden ok 3,385 s, 5,951 passed and 3 skipped)\. Against M2F1's gate"),
        ".” The stage the runner runs for it is “",
        P("cft-fp256", "verify/run.sh", r'^  (PY -m pytest "\$ROOT/python/tests" -q -rs --color=no)$'),
        ",” which names no worker option. ", C("make golden"), " itself runs “",
        P("cft-fp256", "Makefile",
          r"^\s+(\$\(PYTHON\) -m pytest python/tests -q \$\(if \$\(XDIST_N\),-n \$\(XDIST_N\),\))$"),
        ",” which adds pytest-xdist's workers “",
        P("cft-fp256", "Makefile", r"^# pytest-xdist (only if this interpreter has it):"),
        ".” So what ", C("make golden"), " takes depends on the machine and on whether pytest-xdist is "
        "installed. ",
        P("cft-fp256", "README.md", r"^(The golden model's self-tests)"), ": ",
        P("cft-fp256", "docs/VERIFICATION.md",
          r"(Its pytest suite\s+checks the model against its own invariants and against mpmath and\s+"
          r"MPFR where they can arbitrate)"),
        ". ",
        P("cft-fp256", "docs/VERIFICATION.md", r"(Nothing below re-litigates a value it\s+has decided)"),
        ".",
    ])

    items.append([
        C("make verify-quick"), ". Cost: ",
        P("cft-fp256", "CLAUDE.md", r"^make verify-quick\s+# (~\d+ min, \d+ of \d+ stages)", num=True), ". ",
        C("quick"), " is ",
        P("cft-fp256", "docs/VERIFICATION.md",
          "`quick` is (" + ws("the `docs`, `generated`, `buildargs`, `sweepjudge`, `innerskips` and `ensurevectors` "
                              "checks, the model-versus-C stages, the language's compiler (`lang`, about two and a "
                              "half minutes run directly on a quiet desktop since its routines' legs left it on "
                              "2026-10-02), the GPU's photograph, the bindings, the language legs, the soak spot "
                              "check, the workloads, the demos and the remote backend - about twenty minutes after "
                              "a host build") + ")"),
        "; it does not run what ", C("make verify-gate"), " adds: ",
        P("cft-fp256", "docs/VERIFICATION.md",
          "`gate` adds (" + ws("the golden suite, the vectors, the library replay, the transcendentals, MPFR, the "
                               "C++ replay, lint, formal, the C auditor's gate (`audit`, about four minutes since "
                               "2026-09-29), two cases of the estimates study (`estimates`, under a minute since "
                               "2026-09-30), the compiler's routines (`lang-routines`, about two and a half "
                               "minutes run directly on a quiet desktop since 2026-10-02, and about two fifths "
                               "more on the desktop with M1's build, item 5's legs for the six - 42 and 46 per "
                               "cent of the old legs' time in two runs - and two thirds more on amd-arc-box, 252 s "
                               "against 150 s, 245 s in its gate), the language's variational equations "
                               "(`tangent`, three to six minutes since 2026-10-01, far longer on a busy desktop, "
                               "and 9 to 19 per cent more with item 5's leg N on the desktop, a tenth more on "
                               "amd-arc-box, 382 s against 346 s, 371 s in its gate) and the acceptance set "
                               "(`acceptance`, about six minutes since 2026-10-02) and the stress driver's own "
                               "suite (`cardstress`, about ten minutes in WSL since 2026-10-22; skipped by name "
                               "while another process uses the card)") + ")"),
        ". The gate: ",
        P("cft-fp256", "CLAUDE.md", r"^make verify-gate\s+# (~\d+ h quiet, \d+ of \d+ - what a change should pass)",
          num=True), "; the document's own figure is “",
        P("cft-fp256", "docs/VERIFICATION.md", r"\*\*(about two hours quiet\s+and four loaded on this host)\*\*"),
        "”. By quiet it means “",
        P("cft-fp256", "docs/VERIFICATION.md",
          r"\"Quiet\" is (" + ws("the Windows desktop (12 cores, 64 GB) with nothing else running, from the runner's "
                                 "own per-stage log of the 2026-09-04 census") + ")"),
        ",” and by loaded “",
        P("cft-fp256", "docs/VERIFICATION.md",
          r"\"loaded\" is (" + ws("the same host on 2026-09-07 carrying two other simulation suites, a formal run and "
                                  "a Vivado implementation at once") + r")\."),
        ".” And, ",
        P("cft-fp256", "README.md", r"\*\*(CI's green tick does not cover synthesis, timing or silicon)\.\*\*"),
        ".",
    ])

    items.append([
        C("python site/build.py --verify-facts"), " in a clone of ", L(SOURCE_REPO, "this site"), ". Cost: one "
        "read per figure this site prints, at its pin or from the committed GitHub snapshot; a private "
        "repository's read is skipped by name. It proves every figure this site prints - including every quote "
        "above - is still exactly what its source gives right now; it does not prove that source's own claim "
        "is true, and a stated word has no source to re-read at all.",
    ])
    return "<ol>%s</ol>" % "".join("<li>%s</li>" % render(i) for i in items)


LIMIT = ("Every quotation above is read from cft-fp256's own documents, at the commit this site pins - the "
         "same discipline this whole site holds itself to. That shows this page quotes cft-fp256 faithfully. "
         "It does not show that cft-fp256's claims are true: cft-fp256's own gates decide that, and the checks "
         "above are how a reader runs them directly, rather than taking this site's word for it. A link to one of "
         "cft-fp256's hosted pages opens whatever its host serves now, which may be a later commit than the one "
         "this site reads.")


def limits():
    """What cft-fp256's own documents say their checks do not reach, in their words and at the pin: the defects the
    record shows its gates passing (the exp2 tie, and a later one) and the digests limit. The card's nightly run
    follows the list, in this site's words, since no document of cft-fp256's says of it what the list's heading
    does (verifier-P2's first pass, round 3)."""
    P = facts.prose
    entry = EXP2_TIE   # the ledger entry of the exp2 tie and the profile's major step (a heading line, checked below)
    shared = [
        "“", P("cft-fp256", "docs/VERIFICATION.md",
               "(" + ws("One stage in this layer holds the library to something this project did not compute "
                        "(`photograph`): atlas-engine's deterministic camera around a plate as a sequencer "
                        "program, each pass's deposit buffer held to the SHA-256 an NVIDIA GPU wrote while "
                        "rendering the same frame from pinned GLSL. Every other stage here compares the C with "
                        "the golden model, and a defect the two shared would pass them all; this one would not")
               + ")"),
        ".” The record shows a defect of that kind: “",
        P("cft-fp256", "docs/VALIDATION.md",
          "(" + ws("Under rmm IEEE 754's roundTiesToAway gives sigma; `transcend.exp2` gave +0") + ")"),
        ",” and “",
        P("cft-fp256", "docs/VALIDATION.md",
          "(" + ws("golden, libcft and the oracle agree at ba03b1d, and at 3a2b2d0 exactly the four rmm ties are "
                   "wrong") + ")"),
        ".” ",
        P("cft-fp256", "CONFORMANCE.md",
          "(" + ws("Step 6's design study M1 found it (its question 5), verifier-VM1 confirmed it") + ")"),
        ", in the entry ",
        L(facts.pin("cft-fp256").href("docs/VALIDATION.md", entry),
          _dossier.ledger_title("cft-fp256", "docs/VALIDATION.md", entry)),
        ".",
        # A later defect of the same kind, in the entry of issue 1. The subject is the heading's words after its
        # own subject, which the pattern skips without naming (the heading calls the report by a word this page
        # does not print: Corrections' signature row says no such correction has come, decision 49).
        " A later one is in the entry of ", _dossier.ledger_date("cft-fp256", VALIDATION, ISSUE_1), ": “",
        P("cft-fp256", VALIDATION,
          r"^## 2026-10-30 - [^:]+: (" + ws("exp2m1(emax + 1) toward zero raised overflow, in the golden model, the C, "
                                            "the vectors and the WebAssembly module") + r"); "),
        ".” It came, in the entry's words, from “",
        P("cft-fp256", VALIDATION,
          r"from (a clean-room audit of loganw234/muse-softfloat \(binary16/32/64\), cross-tested against this "
          r"library and an exact arbiter)\."),
        ".” Why no gate caught it, in the entry's words: “",
        P("cft-fp256", VALIDATION, r"^- (The vectors are the golden model's)\.$"),
        ",” “",
        P("cft-fp256", VALIDATION,
          r"^- (`transcend_check\.py` compares the C with the golden model, and the two shared the shortcut)\.$"),
        ",” and “",
        P("cft-fp256", VALIDATION, r"^- \*\*(The MPFR oracle never asked)\.\*\*"),
        ".” Its own known limit: “",
        P("cft-fp256", VALIDATION,
          r"^- (the oracle is only as wide as its pools: the ten now see both, and nothing but this case moved, but no "
          r"sweep has asked which families any pool lacks)"),
        ".”",
    ]
    digests = [
        "“", P("cft-fp256", "CONFORMANCE.md",
               r"\*\*A known limit: (" + ws("no gate compares a set's digest with `vectors/SHA256SUMS`") + r")\.\*\*"),
        ".” The same passage goes on: “",
        P("cft-fp256", "CONFORMANCE.md",
          "(" + ws("A change that moves a recorded bit or case - to the model and libcft together, or to the "
                   "generator alone - therefore passes the gate budget at the vector sets") + ")"),
        ".” “",
        # the rest of the passage: which stages hold the committed module (the full census's, not the gate's), and
        # that the limit is not closed
        P("cft-fp256", "CONFORMANCE.md",
          "(" + ws("The full census's `node` and `wasm` stages replay the sets through the committed WebAssembly "
                   "module too, so a change to the model and libcft fails there until the module is rebuilt with it, "
                   "and then passes. From then on, and for a change to the generator alone throughout, only the "
                   "comparison above shows it. It is not closed now: closing it changes `verify/run.sh`, which "
                   "would need a gate run of its own (2026-10-05)") + r")\."),
        ".” The entry of ", _dossier.ledger_date("cft-fp256", VALIDATION, DIGESTS_OPEN), " agrees: “",
        P("cft-fp256", VALIDATION,
          r"KL-198 and KL-242 stay open:\*\* [^\n]*?(no gate compares a regenerated set's digest with the tracked "
          r"record)\."),
        ".”",
    ]
    # The card's nightly run is none of the checks above: its page is cft-fp256's own, it goes on past the pin, and
    # its figures at the pin are P1's, on the dossier, so none is printed here.
    nightly = [
        "The card's nightly stress run is none of the checks above. The README says its ",
        L(P("cft-fp256", "README.md",
            r"\[nightly\.html\]\((https://loganw234\.github\.io/cft-fp256/nightly\.html)\)").raw, "nightly page"),
        " “",
        P("cft-fp256", "README.md",
          r"(shows\s+how far the card's nightly stress run has come: the items fully covered,\s+night by night, and the "
          r"hours on the card)\."),
        ".” That page goes on past the commit this site reads.",
    ]
    return ("<ul class=\"plain\">%s</ul><p class=\"cap\">%s</p>"
            % ("".join("<li>%s</li>" % render(i) for i in (shared, digests)), render(nightly)))


def render_page(ctx):
    return (
        '<h1>Verify</h1>'
        '<div class="measure"><p class="lede">%s</p></div>'
        '<h2><small>I</small>Ways to check this</h2>'
        '<div class="cta"><p>Don\'t trust this - run one.</p>%s</div>'
        '<h2><small>II</small>What checking here does not do</h2>'
        '<div class="measure"><p class="cap">%s</p>'
        '<p class="cap">What cft-fp256\'s own documents say their checks do not reach:</p>%s</div>'
        % (_lede(), checks(), LIMIT, limits())
    )


def _replay_old_words():
    """The browser replay's sentence given the old pin's words: ab51655's bindings/wasm/README.md counted the full
    claim at 1,068,915 cases, and profile 3.1 made it 1,072,415. The reader this page uses must refuse the old
    words by name, saying the pattern no longer matches in that file at the pin. (A source this machine cannot read
    raises facts.Unavailable, which the runner skips by name.)"""
    old = FULL_CLAIM.replace("1,072,415", "1,068,915")
    if old == FULL_CLAIM:
        return ("replay-old-words", False, "could not plant: the full claim has no 1,072,415 to give the old count")
    try:
        facts.prose("cft-fp256", WASM, "(" + old + ")")
    except facts.Unavailable:
        raise
    except facts.Refusal as e:
        msg = str(e)
        return ("replay-old-words", WASM in msg and "no longer matches" in msg,
                "the full claim with the old pin's count, read at the new pin: %s ... %s" % (msg[:70], msg[-18:]))
    return ("replay-old-words", False, "the old pin's words for the full claim were read at the new pin")


def controls():
    """1. The negative control named "an unsourced sentence on Verify" (P1.md):
    render.fig() already refuses a figure no fact produced, so the way past
    it is a numeral typed straight into this page's HTML, bypassing fig()
    altogether - a count written into a string by hand. That is caught not
    by this page but by the numbers stage reading the built page, so this
    proves it, on a copy of this page's own built HTML.
    2. The browser replay's sentence given the old pin's words is refused by
    name (_replay_old_words)."""
    import pathlib
    import shutil
    import tempfile

    import build

    out = [_replay_old_words()]
    page = build.PUBLIC / PAGE["file"]
    if not page.is_file():
        out.append(("unsourced-sentence", False,
                    "public/%s is not built yet; run python site/build.py first" % PAGE["file"]))
        return out
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        shutil.copytree(build.PUBLIC, root, dirs_exist_ok=True)
        copy = root / PAGE["file"]
        t = copy.read_text(encoding="utf-8")
        planted = t.replace("</footer>", "<p>reads 4 checks by hand</p></footer>", 1)
        if planted == t:
            out.append(("unsourced-sentence", False, "could not plant: </footer> is not in %s" % PAGE["file"]))
        else:
            copy.write_text(planted, encoding="utf-8", newline="\n")
            found = [f for f in build.check_numbers(root)[0] if PAGE["file"] in f and "'4'" in f]
            out.append(("unsourced-sentence", bool(found),
                        "a hand-typed count on %s, outside any fact's mark: %s"
                        % (PAGE["file"], found[0] if found else "passed")))
    return out
