"""Method: how the work gets made (docs/SPEC.md, "Method"; decisions 8, 9,
19, 23). The co-authorship statement is stated once for the whole site,
here (decision 9; SPEC section 3's row, "kept in one place: the Method
page"). About names the same two collaborators and links back rather than
restating it (decision 9's own scope).
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
        "description": "How the work gets made: the ratio Logan states, HonestFramework and ParcelRound, this "
                       "round's own numbers, and the co-authorship statement, kept in one place."}


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
        " The one measurement on record is ParcelRound's second round, where its own accounting puts the "
        "human-active time at ", quote, ". In Logan's words, that reported time ",
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
        " ", page_link(ctx, "Work", "work-honestframework.html", "Its dossier"), " has the rest."
    ])
    pr = render([
        prose("ParcelRound", "README.md",
              r"^(A method for splitting one body of work across several coding agents\s+at\s+once,\s+without "
              r"the pieces failing to meet)\."),
        " ", prose("ParcelRound", "METHOD.md",
                   r"\*\*(Exactly one file owns each shared fact; everyone else includes it)\.\*\*"),
        " ", page_link(ctx, "Work", "work-parcelround.html", "Its dossier"), " has the rest."
    ])
    return '<div class="measure"><p>%s</p><p>%s</p></div>' % (hf, pr)


# ---------------------------------------------------------------------------
# III. This round, in numbers: send-backs and planted faults, ParcelRound's
# and this site's own, each naming its round and its source.
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
        render(["This site's own round, P3's verifier: ",
                facts.own_prose("docs/VALIDATION.md",
                                r"(The lead's control on the verifier\s+caught 2 of 2)\."), "."]),
        render(["This site's own round, as a whole, in the newest entry that records the controls: ",
                newest_control_count("docs/VALIDATION.md"), "."]),
    ]
    note = ("Each figure is as of its source's repository at its pin, or of this site's own ledger as read in "
           "the commit being built — never live.")
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

GEMINI = re.compile(r"^Co-Authored-By:.*\bgemini\b", re.I | re.M)


def gemini_credited(message):
    """The same rule facts.agent_credited uses (CLAUDE.md trap 4: a commit
    counts once, never once per trailer line), narrowed to Gemini alone."""
    return GEMINI.search(message) is not None


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
    gcommit = named_commit("Mercenaries2", "d66f97a",
                           "of every pinned repository, the one commit whose trailer names Gemini")
    gcount = gemini_commits("Mercenaries2")
    acount = facts.agents("Mercenaries2")
    trailer = render([
        "Gemini's name sits in a Co-Authored-By trailer on ", gcount, " of Mercenaries2's commits: ", gcommit,
        ", which also credits Claude — a commit counted once, never once per trailer line. ", acount,
        " of its commits credit Claude or Gemini this way. Logan's word is that ", S(home.AI_USE), "."
    ])
    return ('<div class="measure">'
           '<p>%s This is the one place the site states it.</p>'
           '<p>%s</p>'
           '<p>%s</p>'
           '</div>' % (statement, names, trailer))


def render_page(ctx):
    return (
        '<div class="measure"><p class="lede">A ratio Logan states, the methods behind it, this round\'s own '
        'numbers, and the co-authorship statement, kept in one place.</p></div>'
        '<h2><small>I</small>The ratio</h2>%s'
        '<h2><small>II</small>HonestFramework and ParcelRound</h2>%s'
        '<h2><small>III</small>This round, in numbers</h2>%s'
        '<h2><small>IV</small>Co-authorship</h2>%s'
        % (ratio_block(), methods_block(ctx), stats_block(), coauthor_block())
    )


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

    return out
