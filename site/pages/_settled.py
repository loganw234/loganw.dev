"""Pages printed in Logan's own words, About and the front page (decisions 26
and 29): every statement such a page prints must be settled, its words, who
said them and when exactly as the page's SETTLED has them, or carry a draft
label (decision 14's pattern). One rule in one place, so the two pages can't
part. verifier-close found each of its holes on About (2026-09-30), and
controls() plants each one again into a page's own blocks.

The check reads stated() figures. A sentence printed as plain text, not
through stated(), is outside it: the check reads figures, and plain text is
none.
"""
import re

import facts
from facts import Refusal, fact
from render import render


def printed(body, page):
    """The log's record for every figure body prints. Each mark is read by
    the numbers stage's own reader (build._Marks, Python's HTML parser), so
    it is found however its attribute is cased or its id encoded, exactly as
    that stage finds it. A mark whose id isn't plain digits, or that no
    logged fact has, is refused."""
    import build   # here, not at the top: build imports the pages
    p = build._Marks()
    p.feed(body)
    p.close()
    recs = []
    for f in sorted({m["f"] for m in p.marks}):
        i = int(f) if re.fullmatch(r"[0-9]+", f) else 0
        rec = facts.LOG[i - 1] if 0 < i <= len(facts.LOG) else None
        if rec is None or rec["id"] != i:
            raise Refusal("%s prints a mark for fact %r, which no logged fact has" % (page, f))
        recs.append(rec)
    return recs


def unsettled(recs, settled):
    """The statements among recs that carry no draft label and aren't
    settled: their words, who said them and when, exactly as settled has
    them. A draft is read from its label's start, so a who that only reads
    like a draft label is no draft."""
    return [r["text"] for r in recs if r["kind"] == "stated" and settled.get(r["text"]) != r["where"]
            and not r["where"].startswith("drafted from ")]


def refuse(body, page, settled):
    """body, or a refusal naming the first statement in it that isn't settled
    and carries no draft label."""
    bad = unsettled(printed(body, page), settled)
    if bad:
        raise Refusal("%s states %r, which Logan hasn't approved as printed (its words, who and when), with no "
                      "draft label" % (page, bad[0][:60]))
    return body


@fact
def relayed(text, who, when):
    """A statement returned through a fact of its own, so that its record's
    method isn't facts.stated. Only controls() calls it: the check must know
    a statement by its kind, whichever fact returned it."""
    return facts.stated(text, who, when)


def controls(g, blocks, render_page, ctx, prefix, sample, S, D):
    """A page's controls on its own settled words. g is the page module's
    globals(), blocks the names of the functions that render its blocks,
    render_page(ctx) renders everything the check reads, and S and D make a
    statement and a draft. sample is one settled (text, who, when).
    - In each block, a statement planted before the block's content and one
      planted after it, with no draft label, must each be refused by name,
      and the same statement with its label must pass.
    - A statement rendered before the page starts, then printed inside it,
      must be refused.
    - So must a settled sentence given another who or another date, a
      statement whose who reads like a draft label, a statement returned
      through another fact, and marks written the other ways the numbers
      stage still reads as marks: an upper-case attribute name, and an id
      written as character references.
    Each control also needs the real page to pass."""
    planted = "A sentence no one approved."

    def attempt(name=None, statement=None, before=False, early=False, rewrite=None):
        saved = g[name] if name else None
        facts.reset_log()
        if name:
            pre = "<p>%s</p>" % render([statement()]) if early else None

            def planted_block(*a):
                p = pre or "<p>%s</p>" % render([statement()])
                p = rewrite(p) if rewrite else p
                return p + saved(*a) if before else saved(*a) + p
            g[name] = planted_block
        try:
            render_page(ctx)
            return None
        except Refusal as e:
            return str(e)
        finally:
            if name:
                g[name] = saved

    def refused(e):
        return bool(e) and "hasn't approved" in e

    real = attempt()
    fine = real or "passed, as it must"
    text, who, when = sample
    other_day = "2026-09-29" if when != "2026-09-29" else "2026-09-30"
    first = blocks[0]
    out = []
    for name in blocks:
        for before in (True, False):
            where = "%s, %s its content" % (name, "before" if before else "after")
            bare = attempt(name, lambda: S(planted), before)
            labelled = attempt(name, lambda: D(planted), before)
            out.append(("%s-draft-label" % prefix, refused(bare) and labelled is None and real is None,
                        "in %s, an unapproved statement with no draft label: %s; the same with its label: %s; "
                        "the real page: %s" % (where, bare or "passed", labelled or "passed, as it must", fine)))
    early = attempt(first, lambda: S(planted), before=True, early=True)
    out.append(("%s-rendered-before" % prefix, refused(early) and real is None,
                "a statement rendered before the page starts, printed inside it: %s; the real page: %s"
                % (early or "passed", fine)))
    for cname, what, statement in (
            ("settled-who", "a settled sentence given to someone else",
             lambda: facts.stated(text, "Someone Else", when)),
            ("settled-when", "a settled sentence given another date", lambda: facts.stated(text, who, other_day)),
            ("draft-who", "a statement whose who reads like a draft label",
             lambda: facts.stated(planted, "drafted from " + who, when)),
            ("relayed", "a statement returned through another fact", lambda: relayed(planted, who, when))):
        e = attempt(first, statement)
        out.append(("%s-%s" % (prefix, cname), refused(e) and real is None,
                    "%s: %s; the real page: %s" % (what, e or "passed", fine)))
    for cname, what, rewrite in (
            ("mark-case", "a mark whose attribute name is upper case", lambda h: h.replace('data-f="', 'DATA-F="')),
            ("mark-reference", "a mark whose id is written as character references",
             lambda h: re.sub(r'data-f="([0-9]+)"',
                              lambda m: 'data-f="%s"' % "".join("&#%d;" % ord(c) for c in m.group(1)), h))):
        e = attempt(first, lambda: S(planted), rewrite=rewrite)
        out.append(("%s-%s" % (prefix, cname), refused(e) and real is None,
                    "%s: %s; the real page: %s" % (what, e or "passed", fine)))
    facts.reset_log()
    return out
