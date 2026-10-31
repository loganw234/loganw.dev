"""Method: how the work gets made (docs/SPEC.md, "Method"; decisions 8, 9,
19, 23). The co-authorship statement is stated once for the whole site,
here (decision 9; SPEC section 3's row, "kept in one place: the Method
page"). About names the same collaborators and links back rather than
restating it (decision 9's own scope). Section IV also reads muse-softfloat's
Co-Authored-By trailers (decision 50), beside Mercenaries2's Gemini one.
"""
import pathlib
import re
import subprocess
import tempfile

import facts
from facts import V, Src, Refusal, fact, pin, prose
from pages import home
from pages._p5 import page_link
from render import C, L, esc, render

PAGE = {"file": "method.html", "nav": "Method", "title": "Method — loganw.dev",
        "description": "How the work gets made: the ratio Logan states, HonestFramework and ParcelRound, the "
                       "rounds' own numbers, and the co-authorship statement, kept in one place."}


def S(text, **kw):
    return facts.stated(text, "Logan", "2026-09-29", **kw)


# ---------------------------------------------------------------------------
# I. The ratio (decision 8): Logan's own figure, not a measurement, beside
# the one measurement on record and Logan's word that it runs high.
# ---------------------------------------------------------------------------

def ratio_block():
    quote = prose("ParcelRound", "CASE-STUDY-2.md",
                  r"puts the human-active time at (1 h 38 min against\s+23 h 40 min of API time across every agent)")
    body = render([
        "Logan's own figure for the balance of human to machine time is ", S("1:24"), " — not yet a measurement. ",
        S("It will be measured from now on."),
        " The one measurement on record is ParcelRound's second round, where the desktop app's own accounting "
        "puts the human-active time at ", quote, ". In Logan's words, that reported time ",
        S("was a bit inflated, lining up more with the 1:24 figure"), "."
    ])
    return '<div class="measure"><p>%s</p></div>' % body


# ---------------------------------------------------------------------------
# II. HonestFramework and ParcelRound, one paragraph each, from their own
# README and METHOD.md at their pins.
# ---------------------------------------------------------------------------

def methods_block(ctx):
    hf = render([
        prose("HonestFramework", "README.md",
              r"^(A way to lay out a project so that an AI can write nearly all of it and\s+\*\*no claim about it "
              r"ever rests on the AI's judgement\*\*)\."),
        ". ", prose("HonestFramework", "METHOD.md",
                    r"because (a safeguard nobody has tested is just another claim)\."),
        " Its README lists its gate: “",
        prose("HonestFramework", "README.md",
              r"\| (This repo's own gate\. It refuses a broken link or a stated line count that has drifted)\. \|"),
        ".” ", page_link(ctx, "Work", "work-honestframework.html", "Its dossier"), " has the rest."
    ])
    pr = render([
        prose("ParcelRound", "README.md",
              r"^(A method for splitting one body of work across several coding agents\s+at\s+once,\s+without "
              r"the pieces failing to meet)\."),
        " ", prose("ParcelRound", "METHOD.md",
                   r"\*\*(Exactly one file owns each shared fact; everyone else includes it)\.\*\*"),
        " Its README lists its gate: “",
        prose("ParcelRound", "README.md",
              r"\| (The front door: `python tools/check_method\.py` says whether the method still holds together);"),
        ".” ", page_link(ctx, "Work", "work-parcelround.html", "Its dossier"), " has the rest."
    ])
    return '<div class="measure"><p>%s</p><p>%s</p></div>' % (hf, pr)


# ---------------------------------------------------------------------------
# III. The rounds, in numbers: send-backs and planted faults, ParcelRound's
# and this site's own, each naming its round and its source. Each figure is one
# round's own count: none is a total across rounds, and none is taken from
# a set of case studies other than the one its sentence names.
# ---------------------------------------------------------------------------

CONTROL_COUNT = re.compile(r"`--control` caught (\d+ of \d+)\.")


@fact
def newest_control_count(path):
    """The first "`--control` caught N of N" this site's own ledger
    records, searched from its newest entry back - never a fixed line: the
    ledger is append-only and grows at every merge, so a quote of "the
    newest entry" goes stale the moment a later entry lands that doesn't
    happen to repeat this line (verifier-P5, d445b42: quoted "275 of 275"
    at the then-newest entry; 07b1526 appended one with "294 of 294" before
    the page was even merged). Reading newest-back keeps the figure true as
    the ledger keeps growing, since a rebuild re-reads it from the tree
    being built."""
    text, entries = facts.own_entries(path)
    for e in reversed(entries):
        m = CONTROL_COUNT.search(text, e["start"], e["end"])
        if m:
            line = text.count("\n", 0, m.start(1)) + 1
            return V(m.group(1), facts.own_src(path, line, "the newest entry that records the controls"),
                     raw=m.group(1), num=True)
    raise Refusal("this site's %s: no entry records \"`--control` caught N of N\"" % path)


def stats_block():
    items = [
        render(["ParcelRound's second round: ",
                prose("ParcelRound", "CASE-STUDY-2.md", r"produced (four send-backs, none for a wrong bit)"),
                "."]),
        render(["Its third round: ",
                prose("ParcelRound", "CASE-STUDY-3.md", r"^(Six send-backs and eleven defects)\."), "."]),
        render(["That third round's own gate: ",
                prose("ParcelRound", "CASE-STUDY-3.md",
                      r"the gate: (32 planted controls, 29 of 29 mutations killed)"), "."]),
        render(["Its fourth round found a miss, too: ",
                prose("ParcelRound", "CASE-STUDY-4.md",
                      r"\*\*(equality with the authority passed 10 of 11 planted certificate faults)\*\*"), "."]),
        render(["Its fifth round was this site's own first. This site's ledger, on P3's verifier: ",
                facts.own_prose("docs/VALIDATION.md",
                                r"(The lead's control on the verifier\s+caught 2 of 2)\."), "."]),
        render(["ParcelRound's case study of that round: ",
                prose("ParcelRound", "CASE-STUDY-5.md",
                      r"\d+\. \*\*(Planted controls caught 2 of 2, twice\. The second could have been\s+passed by "
                      r"a diff\.)\*\*", num=True), " Its models: “",
                prose("ParcelRound", "CASE-STUDY-5.md", r"\*\*(The parcels and their verifiers ran on Sonnet 5)\*\*",
                      num=True), ".”"]),
        render(["Its sixth round, run on ParcelRound itself: ",
                prose("ParcelRound", "CASE-STUDY-6.md",
                      r"so (no parcel went\s+back; the round's one wrong answer was the lead's \(obs 4\))\.",
                      num=True), "."]),
        render(["Its sixth round's planted faults: ",
                prose("ParcelRound", "CASE-STUDY-6.md", r"\*\*Planted faults: (ten of ten caught, from the sources)\.\*\*",
                      num=True), ". Its own reading of that figure: ",
                prose("ParcelRound", "CASE-STUDY-6.md",
                      r"(A verifier that\s+read the design first could have found every plant by comparison\s+alone)"
                      r"\."), ". Its models, read from its transcripts: “",
                prose("ParcelRound", "CASE-STUDY-6.md",
                      r"read from the transcripts: (the lead and every verifier on\s+Opus 5\.5, the five parcels on "
                      r"Sonnet 5\.5)\.", num=True), ".”"]),
        render(["Its sixth round's gate, against the faults its verifier built on the first pass: ",
                prose("ParcelRound", "CASE-STUDY-6.md",
                      r"(Of its 84 faults, 47 caught; of the 37 that passed, 25 lay outside every limit the gate "
                      r"stated)\.", num=True), "."]),
        render(["This site's own build, in the newest ledger entry that records its controls: ",
                newest_control_count("docs/VALIDATION.md"), "."]),
    ]
    note = ("Each figure is as of its source's repository at its pin, or of this site's own ledger as read in "
           "the commit being built — never live. Each is the count its own source makes, of one round or one "
           "gate; none is a total across rounds.")
    return ('<div class="measure"><ul class="plain">%s</ul><p class="cap">%s</p></div>'
           % ("".join("<li>%s</li>" % i for i in items), esc(note)))


# ---------------------------------------------------------------------------
# IV. Co-authorship, stated once for the whole site.
# ---------------------------------------------------------------------------

STATEMENT_9 = ("AI Collaborators are attributed equal to the human one, the projects wouldnt exist if either "
              "were removed.")

# Kept in one place (decision 9; SPEC section 3's row): local-only refuses
# this text on any other published page or text file (build.only_here_problems).
ONLY_HERE = [STATEMENT_9]

# The agent-credit rule is facts.AGENT's (docs/SPEC.md, section 4: a
# Co-Authored-By line naming Claude, Gemini or Muse, Muse since decision 50).
# This page narrows it to Gemini alone and to Muse alone, and its count
# sentence says the rule's names. Both are read from the rule's own pattern,
# so neither can drift from it: a pattern of another shape, or a sentence with
# other names, refuses the build by name.
_ALTERNATION = re.compile(r"\\b\(\?:([a-z]+(?:\|[a-z]+)*)\)\\b")


def agent_names():
    """The names facts.AGENT counts, in the rule's order, read from its own
    pattern (a Co-Authored-By line naming one of a word-bounded alternation of
    agents)."""
    m = _ALTERNATION.search(facts.AGENT.pattern)
    if m is None:
        raise Refusal("facts.AGENT, %r, is not a Co-Authored-By line naming one of a word-bounded alternation of "
                      "agents, which Method's count words and its Gemini and Muse counts are read from"
                      % facts.AGENT.pattern)
    return tuple(m.group(1).split("|"))


def narrowed(name):
    """facts.AGENT's own rule narrowed to one of the names it counts: a
    Co-Authored-By line naming that agent alone."""
    names = agent_names()
    if name not in names:
        raise Refusal("facts.AGENT counts %s, not %r" % (", ".join(names), name))
    return re.compile(facts.AGENT.pattern.replace("(?:%s)" % "|".join(names), name), facts.AGENT.flags)


def gemini_credited(message):
    """The same rule facts.agent_credited uses (CLAUDE.md trap 4: a commit
    counts once, never once per trailer line), narrowed to Gemini alone."""
    return narrowed("gemini").search(message) is not None


def muse_credited(message):
    """The same rule, narrowed to Muse alone (docs/SPEC.md, decision 50)."""
    return narrowed("muse").search(message) is not None


# The count sentence names the agents the rule counts. It is typed here, in the
# rule's order and words, and held to the rule.
COUNT_WORDS = "Claude, Gemini or Muse"


def rule_words():
    names = [n.capitalize() for n in agent_names()]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " or " + names[-1]


def check_count_words(words):
    want = rule_words()
    if words != want:
        raise Refusal("Method's count sentence says its commits credit %s, and facts.AGENT counts %s; restate the "
                      "sentence to the rule" % (words, want))


def coauthor_statement():
    return S(STATEMENT_9)


@fact
def gemini_commits(name):
    """Commits whose message credits Gemini, of all commits at the pin -
    facts.agent_credited's own rule, narrowed to Gemini alone, so that
    Mercenaries2's d66f97a (which credits both Claude and Gemini) counts
    once here too."""
    p = pin(name)
    recs = p.git("log", p.full, "--format=%x1e%B").split("\x1e")[1:]
    n = sum(1 for r in recs if gemini_credited(r))
    return V("%d/%d" % (n, len(recs)),
             p.src("git", "git log", "commits with a Co-Authored-By line naming Gemini, of all commits"),
             raw="%d/%d" % (n, len(recs)), num=True)


def _messages(p):
    return p.git("log", p.full, "--format=%x1e%B").split("\x1e")[1:]


@fact
def muse_commits(name):
    """Commits whose message credits Muse, of all commits at the pin - the
    same rule as gemini_commits, narrowed to Muse alone, so that a commit
    counts once however many Muse lines it has (every one of muse-softfloat's
    commits has one: decision 50)."""
    p = pin(name)
    recs = _messages(p)
    n = sum(1 for r in recs if muse_credited(r))
    return V("%d/%d" % (n, len(recs)),
             p.src("git", "git log", "commits with a Co-Authored-By line naming Muse, of all commits"),
             raw="%d/%d" % (n, len(recs)), num=True)


# Every Co-Authored-By line naming Muse in muse-softfloat also carries an
# email address. No page prints one (CLAUDE.md, trap 14): the name is read up to
# the address, and a name that holds an ASCII "@" is refused here. An address
# in a spelling the local-only stage's readings decode, a fullwidth at sign
# say, is that stage's to refuse on a published page. One spelled out in words,
# for a person to reassemble, passes it, a limit CLAUDE.md states (trap 14;
# verifier-P3's first and second passes, round 3).
_NAME_BEFORE_ADDRESS = re.compile(r"^Co-Authored-By:[ \t]*(.*?)[ \t\r]*(?:<[^<>\n]*>)?[ \t\r]*$", re.I)


def muse_trailer_names(messages):
    """{name: commits}: the name in each Co-Authored-By line naming Muse, up
    to the address, counting a commit once per name."""
    rule = narrowed("muse")
    names = {}
    for msg in messages:
        here = set()
        for line in msg.splitlines():
            if rule.search(line):
                m = _NAME_BEFORE_ADDRESS.match(line)
                here.add(m.group(1) if m else line.split(":", 1)[-1].strip())
        for nm in here:
            names[nm] = names.get(nm, 0) + 1
    return names


def one_muse_name(names, where):
    """The one (name, commits) of a muse_trailer_names() result. The sentence
    says every Muse trailer is that name, so two names, or none, refuse; and
    a name with an ASCII "@" in it is refused without being printed."""
    if any("@" in nm for nm in names):
        raise Refusal("%s: a Co-Authored-By line naming Muse holds an address inside its name; no page prints "
                      "one" % where)
    if len(names) != 1:
        raise Refusal("%s: the Co-Authored-By lines naming Muse carry %s; Method's sentence says every one is "
                      "the same name" % (where, "no name" if not names else
                                         "%d different names (%s)" % (len(names), "; ".join(sorted(names)))))
    return next(iter(names.items()))


@fact
def muse_trailer_name(name):
    """The name in the Co-Authored-By line naming Muse, up to the address,
    which is the same in every commit that has one."""
    p = pin(name)
    nm, n = one_muse_name(muse_trailer_names(_messages(p)), "%s %s" % (name, p.short))
    return V(nm, p.src("git", "git log", "the name, before the address, in the Co-Authored-By line naming Muse of "
                                         "each of %d commits (the address is not printed)" % n), raw=nm)


@fact
def named_commit(name, sha, what):
    """A commit in a pinned repository's history, cited by its hash and
    shown to exist there and to be part of what the pin reads - the same
    check _dossier.kept_failure makes, under a label of its own rather
    than "the commit that fixed it", since this one fixed nothing."""
    p = pin(name)
    p.git("cat-file", "-e", sha + "^{commit}")
    full = p.git("rev-parse", sha).strip()
    if not p.is_ancestor(full):
        raise Refusal("%s: %s exists but is not part of the history the pin %s reads" % (name, sha, p.short))
    href = "" if p.private else "https://github.com/%s/%s/commit/%s" % (p.owner, p.ghname, sha)
    return V(sha, Src("git", "%s %s" % (name, sha), what, href, p.private), raw=sha, num=True)


def coauthor_block():
    statement = render([coauthor_statement()])
    names = render([
        "Quantum-Film's README credits ",
        prose("Quantum-Film", "README.md",
              r"together\s+with (AI collaborators \(Claude Opus 5\.5 and the agents it directed\))"),
        " as ", prose("Quantum-Film", "README.md", r"credited here as (contributors equal to the human one)"),
        ". Mercenaries2's README credits ",
        prose("Mercenaries2", "README.md",
              r"\*\*Gemini\*\* \(Google\)\s+—\s+(substantial AI\s+assistance)\s+throughout the project"),
        "."
    ])
    check_count_words(COUNT_WORDS)
    gcommit = named_commit("Mercenaries2", "d66f97a",
                           "of every pinned repository, the one commit whose trailer names Gemini")
    gcount = gemini_commits("Mercenaries2")
    acount = facts.agents("Mercenaries2")
    mcount = muse_commits("muse-softfloat")
    mname = muse_trailer_name("muse-softfloat")
    trailer = render([
        "Gemini's name sits in a Co-Authored-By trailer on ", gcount, " of Mercenaries2's commits: ", gcommit,
        ", which also credits Claude — a commit counted once, never once per trailer line. ", acount,
        " of its commits credit %s this way. " % COUNT_WORDS,
        "Logan's word is that ", S(home.AI_USE), ". ",
        # After Logan's word, so that his line on trailers left off is read as
        # about the projects it names, not about muse-softfloat, whose every
        # commit carries one (verifier-P3's first pass, round 3).
        "Muse's name sits in a Co-Authored-By trailer on ", mcount, " of muse-softfloat's commits, always as “",
        mname, "”."
    ])
    return ('<div class="measure">'
           '<p>%s This is the one place the site states it.</p>'
           '<p>%s</p>'
           '<p>%s</p>'
           '</div>' % (statement, names, trailer))


def render_page(ctx):
    return (
        '<div class="measure"><p class="lede">A ratio Logan states, the methods behind it, the rounds\' own '
        'numbers, and the co-authorship statement, kept in one place.</p></div>'
        '<h2><small>I</small>The ratio</h2>%s'
        '<h2><small>II</small>HonestFramework and ParcelRound</h2>%s'
        '<h2><small>III</small>The rounds, in numbers</h2>%s'
        '<h2><small>IV</small>Co-authorship</h2>%s'
        % (ratio_block(), methods_block(ctx), stats_block(), coauthor_block())
    )


def _planted_log(messages):
    """A repository built in a temporary directory with one commit per
    message: those messages, as git log gives them (newest first)."""
    with tempfile.TemporaryDirectory() as d:
        def g(*a):
            subprocess.run(["git", "-C", d, "-c", "user.name=planted", "-c", "user.email=planted@invalid", *a],
                           capture_output=True)
        g("init", "-q")
        f = pathlib.Path(d) / "a.txt"
        for i, msg in enumerate(messages):
            f.write_text("%d\n" % i, encoding="utf-8", newline="\n")
            g("add", "-A")
            g("commit", "-qm", msg)
        log = subprocess.run(["git", "-C", d, "log", "--format=%x1e%B"], capture_output=True).stdout
    return log.decode("utf-8", "replace").split("\x1e")[1:]


def _muse_controls():
    """Decision 50's sentence, and the count sentence's words held to the
    rule (docs/ROUND3.md, P3). Each plants a fault where the check must see it."""
    import json
    import shutil
    import build as _build
    out = []

    def refused(name, what, fn, must):
        try:
            fn()
            out.append((name, False, "%s passed" % what))
        except facts.Unavailable:
            raise
        except Refusal as e:
            out.append((name, must in str(e), "%s: %s" % (what, e)))

    # A figure typed by hand where its fact was, and a label naming a path
    # build.SOURCE_PATHS does not list, each planted in a copy of the built
    # page (render.render() passes a plain string through; only the numbers
    # stage refuses it).
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        shutil.copytree(_build.PUBLIC, root, dirs_exist_ok=True)
        data = json.loads((root / "facts.json").read_text(encoding="utf-8"))
        page = root / PAGE["file"]
        t = page.read_text(encoding="utf-8")
        count_rec = next((r for r in data["facts"] if r["method"] == "pages.method.muse_commits"), None)
        name_rec = next((r for r in data["facts"] if r["method"] == "pages.method.muse_trailer_name"), None)
        if count_rec is None or name_rec is None:
            out.append(("muse-typed-count", False, "public/facts.json has no Muse fact; run python site/build.py first"))
        else:
            planted = re.sub(r'<span class="fig" data-f="%d">[^<]*</span><span class="src" data-f="%d">.*?</span>'
                             % (count_rec["id"], count_rec["id"]), "184/185", t, count=1)
            if planted == t:
                out.append(("muse-typed-count", False,
                            "could not plant: the page has no mark for fact %d" % count_rec["id"]))
            else:
                page.write_text(planted, encoding="utf-8", newline="\n")
                found = [f for f in _build.check_numbers(root)[0] if PAGE["file"] in f and "184/185" in f]
                out.append(("muse-typed-count", bool(found),
                            "the Muse count typed by hand where its fact was: %s" % (found[0] if found else "passed")))
                page.write_text(t, encoding="utf-8", newline="\n")
            name_rec["where"] = name_rec["where"].replace(" git log", " docs/NOTES.md:3")
            (root / "facts.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8",
                                             newline="\n")
            found = [f for f in _build.check_numbers(root)[0] if "docs/NOTES.md" in f]
            out.append(("muse-label-path", bool(found),
                        "the Muse name's label naming a path SOURCE_PATHS does not list: %s"
                        % (found[0] if found else "passed")))

    # The count sentence's words, held to the rule that makes its figure: the
    # old rule's words are refused, and so is a rule that no longer counts Muse.
    refused("count-words", "the count sentence given the old rule's words", lambda: check_count_words("Claude or Gemini"),
            "restate the sentence to the rule")
    saved = facts.AGENT
    facts.AGENT = re.compile(saved.pattern.replace("|muse", ""), saved.flags)
    try:
        refused("count-words", "Method's own words under a rule that counts Claude and Gemini only",
                lambda: check_count_words(COUNT_WORDS), "restate the sentence to the rule")
        refused("count-words", "the Muse narrowing under a rule that no longer counts Muse",
                lambda: narrowed("muse"), "not 'muse'")
    finally:
        facts.AGENT = saved

    # Muse's count, by the commit rule: one commit crediting Muse twice over (as
    # "Muse Code", then as "MUSE") and Claude, one crediting Claude alone, one
    # naming a museum, one naming Muse outside a trailer.
    recs = _planted_log([
        "Bridge fixes\n\nCo-Authored-By: Muse Code <noreply@example.com>\nCo-Authored-By: MUSE <noreply@example.com>\n"
        "Co-Authored-By: Claude <noreply@example.com>",
        "Docs only\n\nCo-Authored-By: Claude <noreply@example.com>",
        "A visit\n\nCo-Authored-By: The Museum <noreply@example.com>",
        "Built with Muse.\n\nSigned-off-by: a person"])
    n = sum(1 for r in recs if muse_credited(r))
    naive = sum(len(re.findall(r"^Co-Authored-By:.*\bmuse\b", r, re.I | re.M)) for r in recs)
    out.append(("muse-commit-count", n == 1 and naive == 2,
                "a planted repository, one commit crediting Muse twice over and Claude, one crediting Claude alone, "
                "one naming a museum, one naming Muse outside a trailer: the commit rule counts %d commit(s) "
                "naming Muse, not the %d trailer lines a naive count would give" % (n, naive)))

    # Muse's name, up to the address (no page prints one), and one name only.
    same = ["x\n\nCo-Authored-By: Muse Code (muse-wonder-full-1.0) <noreply@example.com>",
            "y\n\nCo-Authored-By: Muse Code (muse-wonder-full-1.0) <noreply@example.com>"]
    nm, k = one_muse_name(muse_trailer_names(_planted_log(same)), "a planted repository")
    out.append(("muse-name-no-address", nm == "Muse Code (muse-wonder-full-1.0)" and k == 2 and "@" not in nm,
                "a planted repository, two commits with the same trailer and an address: the name read is %r, "
                "in %d commit(s), with no address in it" % (nm, k)))
    refused("muse-name-no-address", "a name with an address inside it, as a line without angle brackets gives",
            lambda: one_muse_name(muse_trailer_names(_planted_log(
                ["z\n\nCo-Authored-By: Muse Code noreply@example.com"])), "a planted repository"),
            "holds an address inside its name")
    refused("muse-name-one", "two different names",
            lambda: one_muse_name(muse_trailer_names(_planted_log(
                same + ["w\n\nCo-Authored-By: Muse Code (muse-wonder-full-1.1) <noreply@example.com>"])),
                "a planted repository"), "different names")
    return out


def controls():
    out = []

    # 2. The co-authorship statement appears once, on Method alone: held by
    # ONLY_HERE (verifier-P5, d445b42: the earlier version of this control
    # only re-rendered Method and About, so a copy on Home - or any other
    # already-built page - passed every stage). Plant it on a copy of
    # public/'s Home, and watch build.check_local_only refuse it by name;
    # About's "stated once, on Method" is held the same way, by the same
    # gate, since only_here_problems reads every published page but the
    # one ONLY_HERE names.
    import shutil
    import build as _build
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        shutil.copytree(_build.PUBLIC, root, dirs_exist_ok=True)
        home_page = root / "index.html"
        t = home_page.read_text(encoding="utf-8")
        planted = t.replace("</main>", "<p>%s</p></main>" % STATEMENT_9, 1)
        if planted == t:
            out.append(("statement9-once", False, "could not plant: </main> is not in index.html"))
        else:
            home_page.write_text(planted, encoding="utf-8", newline="\n")
            try:
                problems = _build.check_local_only(root)
            finally:
                home_page.write_text(t, encoding="utf-8", newline="\n")
            want = "states pages.method's ONLY_HERE text"
            found = [p for p in problems if want in p]
            out.append(("statement9-once", bool(found),
                       "decision 9's statement planted on index.html, in a copy of public/: %s"
                       % (found[0] if found else "passed")))

    # 3. Gemini's count, by the commit rule: a repository built in a
    # temporary directory, one commit crediting Gemini twice over (once as
    # "Gemini", once as "GEMINI") and Claude, one crediting Claude alone.
    # The rule must count 1 commit, not the 2 trailer lines a naive count
    # would find, and must not miss the case-varied line.
    with tempfile.TemporaryDirectory() as d:
        def g(*a):
            subprocess.run(["git", "-C", d, "-c", "user.name=planted", "-c", "user.email=planted@invalid", *a],
                           capture_output=True)
        g("init", "-q")
        f = pathlib.Path(d) / "a.txt"
        f.write_text("a\n", encoding="utf-8", newline="\n")
        g("add", "-A")
        g("commit", "-qm", "Bridge fixes\n\nCo-Authored-By: Gemini <noreply@example.com>\n"
                          "Co-Authored-By: GEMINI <noreply@example.com>")
        f.write_text("b\n", encoding="utf-8", newline="\n")
        g("commit", "-qam", "Docs only\n\nCo-Authored-By: Claude <noreply@example.com>")
        log = subprocess.run(["git", "-C", d, "log", "--format=%x1e%B"], capture_output=True).stdout
        recs = log.decode("utf-8", "replace").split("\x1e")[1:]
        n = sum(1 for r in recs if gemini_credited(r))
        naive = sum(len(re.findall(r"^Co-Authored-By:.*\bgemini\b", r, re.I | re.M)) for r in recs)
        out.append(("gemini-commit-count", n == 1 and naive == 2,
                   "a planted repository, one commit crediting Gemini twice over (as Gemini, then as GEMINI) and "
                   "Claude, one crediting Claude alone: the commit rule counts %d commit(s) naming Gemini, not "
                   "the %d trailer lines a naive count would give" % (n, naive)))

    out += _muse_controls()
    return out
