"""Thread: Preservation (docs/SPEC.md, thread 3). The only page Wally
appears on (decision 16): it is Logan's own word, stated below, not a
figure read from a repository - no source names a Discord handle.

Credits (decision 10, "Direct credit and links back"): every contributor to
the Preservation repositories, at their pins, grouped by account rather
than by the name on their commits - one GitHub account can commit under
several names (a discord-style handle, a full name, a typo of it), and a
count kept by name would double one person and never notice.
"""
import hashlib
import re

import facts
from facts import V, Src, Refusal, Unavailable, fact
import mapgen
from render import C, L, esc, render

PAGE = {"file": "thread-preservation.html", "nav": "Threads", "title": "Preservation — loganw.dev",
        "description": "A Mercenaries2 revival, its modding tooling, and everyone who has committed to it: the "
                       "thread's account, its part of the map, its credits and its door."}

REPOS = ["Mercenaries2", "Merc2-Mods-Exp", "mercs2-lua-essentials",
        "Mercenaries-Fan-Build/mercs2-modkit", "Mercenaries-Fan-Build/mercs2-qol-mods",
        "Mercenaries-Fan-Build/mercs2-wad-simulator", "Mercenaries-Fan-Build/notes-on-the-released-game"]

NOREPLY = re.compile(r"^(\d+)\+([^@]+)@users\.noreply\.github\.com$", re.I)


def account_of(email):
    """The account behind a commit's author email, grouped never by the name
    on the commit (docs/ROUND1.md's P2 section; the brief's own reading:
    Headless Rebase / Rebase Headless / Rebase are one account). A GitHub
    noreply address is grouped by its <id>+<login> pair, which names no
    person. Any other address is grouped by itself, case-folded (the same
    person can commit under either case of their own address) - but never
    printed or logged: CLAUDE.md trap 14 refuses a published email address
    other than the site's own contact, so the key is a short hash of the
    folded address, not the address."""
    e = email.strip()
    m = NOREPLY.match(e)
    if m:
        return "id:%s+%s" % (m.group(1), m.group(2).lower())
    return "email-sha256:%s" % hashlib.sha256(e.lower().encode("utf-8")).hexdigest()[:16]


def login_of(account):
    """The GitHub login an account's key carries, if it was derived from a
    noreply address; None for a plain email, which carries no login this
    site can read."""
    return account.split("+", 1)[1] if account.startswith("id:") else None


def _emails(name):
    p = facts.pin(name)
    return p.git("log", p.full, "--format=%ae").splitlines()


def accounts_in(name):
    """{account: commit count} for one pinned repository, read fresh - not
    cached, so a re-derivation and the page agree by construction."""
    out = {}
    for e in _emails(name):
        k = account_of(e)
        out[k] = out.get(k, 0) + 1
    return out


@fact
def contributor_commits(name, account):
    """One account's commits in one pinned repository, of all commits there,
    at the pin. Grouped by account (see account_of), not by the name on the
    commit."""
    emails = _emails(name)
    n = sum(1 for e in emails if account_of(e) == account)
    if n == 0:
        raise Refusal("%s: no commits by the account %s" % (name, account))
    p = facts.pin(name)
    return V(str(n), p.src("git", "git log", "commits authored by this account (grouped, never by the name on "
                                             "the commit), of %d total" % len(emails)), raw=str(n), num=True)


def all_accounts():
    """account -> {repo: count}, over every Preservation repository."""
    out = {}
    for name in REPOS:
        for acct, n in accounts_in(name).items():
            out.setdefault(acct, {})[name] = n
    return out


def _logan_account(accounts):
    """Which account is Logan's own - found structurally, never by writing
    Logan's address in this repository: every non-noreply (plain-email)
    account here is Logan's, since Logan is the only Preservation
    contributor without a GitHub noreply address (Austin Kregel's and
    Headless Rebase's both are). Refuses rather than guess if that ever
    stops holding."""
    plain = [a for a in accounts if not a.startswith("id:")]
    if len(plain) != 1:
        raise Refusal("expected exactly one plain-email account among the Preservation contributors (Logan's "
                      "own); found %d: %s" % (len(plain), ", ".join(sorted(plain))))
    return plain[0]


def credits_block():
    accounts = all_accounts()
    logan_account = _logan_account(accounts)
    others = sorted((a for a in accounts if a != logan_account),
                    key=lambda a: (login_of(a) or a).lower())
    rows = []

    def row(acct, display, href):
        cells = []
        for name in REPOS:
            n = accounts[acct].get(name)
            cells.append('<td>%s</td>' % render(contributor_commits(name, acct)) if n else '<td>—</td>')
        who = ('<a href="%s">%s</a>' % (esc(href), esc(display))) if href else esc(display)
        rows.append('<tr><td class="p">%s</td>%s</tr>' % (who, "".join(cells)))

    row(logan_account, "Logan", "")
    for acct in others:
        login = login_of(acct)
        row(acct, login or acct, ("https://github.com/%s" % login) if login else "")
    head = "".join('<th>%s</th>' % esc(n.split("/")[-1]) for n in REPOS)
    table = ('<div class="table-wrap"><table class="credits"><thead><tr><th>contributor</th>%s</tr></thead>'
            '<tbody>%s</tbody></table></div>' % (head, "".join(rows)))
    wally = render(facts.stated("@Wally is my discord username", "Logan", "2026-09-29"))
    cap = ("Every cell is a commit count read at the repository's pin, for one GitHub account, grouped by its "
          "noreply id+login pair, or by a hash of its email address (folded to one case first) - never by the "
          "address itself, and never by the name on the commit, since the same account can commit under several "
          "names. A dash is zero commits there, not a missing figure. Logan goes by %s in this community. "
          "Direct links: %s." % (wally,
          ", ".join("<a href=\"https://github.com/%s\">%s</a>" % (esc(login_of(a)), esc(login_of(a)))
                    for a in others if login_of(a)) or "none derivable"))
    return table + '<p class="cap">%s</p>' % cap


def account():
    P = facts.prose
    paras = []
    paras.append(render([
        P("Mercenaries2", "README.md", r"^(A revival project for \*\*Mercenaries 2: World in Flames\*\*)"),
        ", with online play through ", P("Mercenaries2", "README.md", r"The public server at `(refesl\.live)`"),
        ". Its mod line continues in Merc2-Mods-Exp: ",
        P("Mercenaries2", "README.md", r"(For the mods developed during this phase of the project, visit "
                                       r"\[Merc2-Mods-Exp\])",
          display="the project's own pointer to where that work moved")]))
    paras.append(render([
        ". The modding side runs on ", C("Ess"), ", ",
        P("mercs2-lua-essentials", "README.md", r"^`Ess` — (the foundational Lua library for Mercenaries 2 "
                                               r"modding)"),
        ", one of ", facts.family("(mercs2-|merc2-|wad-simulator)", ["Merc2-Mods-Exp"]),
        " public mercs2 repositories under Logan's own account. The credits below name every contributor to "
        "Mercenaries2, Merc2-Mods-Exp and mercs2-lua-essentials, and to the Mercenaries-Fan-Build organisation's "
        "own repositories."]))
    return "".join('<p>%s</p>' % p for p in paras)


def door():
    return facts.stated("dead things (services, formats, communities — refesl.live is the precedent)",
                        "Logan", "2026-09-29")


def render_page(ctx):
    door_html = render(door())
    if "Propose" in ctx["built"]:
        door_body = '<p class="cta">%s <a href="%s">Propose a thread</a>.</p>' % (door_html, ctx["built"]["Propose"])
    else:
        door_body = '<p class="cta">%s The Propose page isn’t built yet, so this isn’t a link.</p>' % door_html
    return ('<div class="measure"><p class="lede">A game community’s own tooling, kept running past the '
           'people who shipped the game.</p></div>'
           '<h2><small>I</small>The account</h2>%s'
           '<h2><small>II</small>This thread’s part of the map</h2>%s'
           '<h2><small>III</small>Credits</h2><div class="measure">%s</div>'
           '<h2><small>IV</small>Its door</h2>%s'
           % (account(), mapgen.lane_slice(2), credits_block(), door_body))


def controls():
    """Grouping by account, not by the name on the commit: mercs2-modkit's
    real history carries two names for Austin Kregel's account ("Austin
    Kregel", "AUstin Kregel") and two for Headless Rebase's ("Headless
    Rebase", "Rebase"), four distinct name strings over two accounts. A
    version that grouped by name would show four contributors instead of
    two - the exact fault the brief names."""
    # Unavailable (no clone, LOGANW_FETCH not set) is not caught here: it
    # propagates, and build.py's runner skips this control by name, as the
    # brief's own rule for a control needing every pinned clone says.
    name = "Mercenaries-Fan-Build/mercs2-modkit"
    p = facts.pin(name)
    emails = _emails(name)
    by_account = len({account_of(e) for e in emails})
    names = set(p.git("log", p.full, "--format=%an").splitlines())
    by_name = len(names)
    caught = by_name > by_account
    out = [("credits-grouping", caught,
            "%s: %d account(s) grouped by email/GitHub login, %d distinct name string(s) on their commits; a "
            "version that grouped by name would show %d contributors where account_of shows %d"
            % (name, by_account, by_name, by_name, by_account))]

    # credits-grouping's only fixture (mercs2-modkit) never exercises the
    # plain-email branch of account_of - every account there is a GitHub
    # noreply address - so a regression that dropped the case-fold from
    # that branch alone would pass it unchanged while silently splitting a
    # real plain-email account's two cases into two people on the page
    # (verifier-P2's finding, on the real data: Logan's own two identities).
    # Proven here with a made-up address, never a real contributor's one -
    # nothing about a real address is written into this repository.
    def naive_account_of(email):
        e = email.strip()
        m = NOREPLY.match(e)
        if m:
            return "id:%s+%s" % (m.group(1), m.group(2).lower())
        return "email-sha256:%s" % hashlib.sha256(e.encode("utf-8")).hexdigest()[:16]  # no .lower(): the fault

    variants = ["Planted@example.invalid", "planted@example.invalid"]
    real_n = len({account_of(e) for e in variants})
    naive_n = len({naive_account_of(e) for e in variants})
    out.append(("credits-case-fold", naive_n > real_n,
               "two case variants of one made-up address group to %d account(s) by account_of; a copy with the "
               "case-fold dropped from the plain-email branch alone shows %d" % (real_n, naive_n)))
    return out
