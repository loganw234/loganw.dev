"""Rendering: the page shell and how a figure shows where it came from.

The design is experiment E (design/README.md): D's single column, A's colour,
B's type and header. A figure is printed with its source after it, in small
mono, and a source path may break after each "/" rather than inside a word.

Every figure passed to fig() must carry an id from @fact (facts.py). One
without is refused by name: a figure that no fact produced would be a figure
that facts.json cannot re-read, which is the one thing the site promises it
does not print.
"""
import dataclasses
import html

import facts
from facts import V, Refusal

# The navigation, in the spec's order (docs/SPEC.md). A page module declares
# which of these it is; an entry with no page is shown and not linked.
NAV = ["Home", "Threads", "Work", "Method", "Record", "Verify", "Corrections", "Propose", "About"]

SOURCE_REPO = "https://github.com/%s/loganw.dev" % facts.OWNER


def esc(s):
    return html.escape(str(s), quote=True)


@dataclasses.dataclass(frozen=True)
class C:                 # code
    text: str


@dataclasses.dataclass(frozen=True)
class L:                 # a link around a string or a figure
    href: str
    inner: object


def fig(v, href=None):
    if not isinstance(v, V):
        raise TypeError(v)
    if not v.id:
        raise Refusal("a figure no fact produced reached a page: %r" % (v.text,))
    if v.text == "":
        return ""        # a recorded absence: logged in facts.json, printed as nothing
    s = v.src
    cls = "stated" if s.kind == "stated" else ("fig" if v.num else "q")
    t = esc(v.text)
    if href:
        t = '<a href="%s">%s</a>' % (esc(href), t)
    if s.kind == "stated":
        label = "(stated)"
    else:
        label = "(%s%s)" % (s.short, ", private for now" if s.private else "")
    label = esc(label).replace("/", "/<wbr>")
    if s.href:
        label = '<a href="%s">%s</a>' % (esc(s.href), label)
    return '<span class="%s">%s</span><span class="src"> %s</span>' % (cls, t, label)


def render(segs):
    if not isinstance(segs, list):
        segs = [segs]
    out = []
    for s in segs:
        if isinstance(s, str):
            out.append(esc(s))
        elif isinstance(s, V):
            out.append(fig(s))
        elif isinstance(s, C):
            out.append("<code>%s</code>" % esc(s.text))
        elif isinstance(s, L):
            if isinstance(s.inner, V):
                out.append(fig(s.inner, href=s.href))
            else:
                out.append('<a href="%s">%s</a>' % (esc(s.href), render(s.inner)))
        elif s is None:
            continue
        else:
            raise TypeError(s)
    return "".join(out)


def nav(current, built):
    """built: nav label -> file, for every page that exists."""
    items = []
    for n in NAV:
        if n == current:
            items.append('<a class="here" href="%s" aria-current="page">%s</a>' % (esc(built[n]), esc(n)))
        elif n in built:
            items.append('<a href="%s">%s</a>' % (esc(built[n]), esc(n)))
        else:
            items.append('<span title="not built yet">%s</span>' % esc(n))
    return "".join(items)


def stamp(built):
    n = len(built)
    return render([facts.pin_count(), " commits pinned · GitHub snapshot ", facts.snapshot_date(),
                   " · %d of %d pages built · a figure whose source stops matching stops the build"
                   % (n, len(NAV))])


def footer():
    li = []
    for name, cfg in facts.PINS["repos"].items():
        p = facts.pin(name)
        if p.private:
            li.append('<li>%s <span class="fig">%s</span> <i>private for now</i></li>' % (esc(name), esc(p.short)))
        else:
            li.append('<li>%s <a class="fig" href="https://github.com/%s/%s/commit/%s">%s</a></li>'
                      % (esc(name), esc(p.owner), esc(p.ghname), p.full, esc(p.short)))
    return (
        '<p>Every figure on this page is read at these commits, or from the GitHub snapshot of %s, and '
        '<a href="facts.json">facts.json</a> lists each one with where it was read. <code>python site/build.py '
        '--verify-facts</code>, in a clone of <a href="%s">this site\'s repository</a>, reads them all again.</p>'
        '<ul class="pins">%s</ul>'
        '<p><a href="BUILD">BUILD</a> names the commit this copy was deployed from. MIT licence.</p>'
        % (esc(facts.snapdate()), SOURCE_REPO, "".join(li)))


def page(title, current, built, body, description):
    """Home's heading is the name; every other page's is its own, in its body."""
    tag = "h1" if current == "Home" else "p"
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title><meta name="description" content="%s">'
            '<link rel="stylesheet" href="style.css"><link rel="icon" href="data:,"></head>\n'
            '<body><main>'
            '<header><div class="site">loganw.dev</div><%s class="name">Logan W.</%s><nav>%s</nav>'
            '<p class="stamp">%s</p></header>\n%s\n<footer>%s</footer></main></body></html>\n'
            % (esc(title), esc(description), tag, tag, nav(current, built), stamp(built), body, footer()))
