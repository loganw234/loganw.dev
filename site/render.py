"""Rendering: the page shell and how a figure shows where it came from.

The design is experiment E (design/README.md): D's single column, A's colour,
B's type and header. A figure is printed with its source after it, in small
mono, and a source path may break after each "/" rather than inside a word.

fig() prints a figure only if it is exactly what the log holds for its id
(facts.logged): one that no fact produced, or a copy with its text or source
changed, is refused by name. The figure carries its id as data-f, and so does
its source; the numbers stage (build.py --numbers) holds the published page to
the same rule, without the pins.
"""
import dataclasses
import html

import facts
from facts import V, Src, Refusal, fact

# The navigation, in the spec's order (docs/SPEC.md). A page module declares
# which of these it is; an entry with no page is shown and not linked.
NAV = ["Home", "Threads", "Work", "Method", "Record", "Verify", "Corrections", "Propose", "About"]

SOURCE_REPO = "https://github.com/%s/loganw.dev" % facts.OWNER

# The browser's own enforcement of "nothing loads from another host, and no
# page runs a script" (verifier-P0's suggestion). It must come before anything
# that loads, so it is the first element after the charset; the local-only
# stage requires this exact text on every page.
CSP = ("default-src 'none'; style-src 'self'; font-src 'self'; img-src 'self' data:; "
       "base-uri 'none'; form-action 'none'")


def esc(s):
    return html.escape(str(s), quote=True)


@dataclasses.dataclass(frozen=True)
class C:                 # code
    text: str


@dataclasses.dataclass(frozen=True)
class L:                 # a link around a string or a figure
    href: str
    inner: object


def cls_of(rec):
    return "stated" if rec["kind"] == "stated" else ("fig" if rec["num"] else "q")


def checked(v):
    """The log's record for a figure about to be printed, or a refusal."""
    if not isinstance(v, V):
        raise TypeError(v)
    if not v.id:
        raise Refusal("a figure no fact produced reached a page: %r" % (v.text,))
    rec = facts.logged(v)
    if rec is None:
        raise Refusal("a figure that is not what fact %d returned reached a page: %r" % (v.id, v.text))
    return rec


def mark(v):
    """A figure inside SVG text, where no source can follow it: an SVG tspan
    carrying its id. The list under the map gives each one's source."""
    checked(v)
    return '<tspan data-f="%d">%s</tspan>' % (v.id, esc(v.text))


def fig(v, href=None, src=True):
    """A figure, then its source. src=False leaves the source out, for a list
    whose heading says where every item was read (the footer's pins); the
    figure still carries its id, and facts.json its source."""
    rec = checked(v)
    if v.text == "":
        return ""        # a recorded absence: logged in facts.json, printed as nothing
    t = esc(v.text)
    if href:
        t = '<a href="%s">%s</a>' % (esc(href), t)
    out = '<span class="%s" data-f="%d">%s</span>' % (cls_of(rec), v.id, t)
    if src:
        label = esc(facts.label(rec)).replace("/", "/<wbr>")
        if rec["href"]:
            label = '<a href="%s">%s</a>' % (esc(rec["href"]), label)
        out += '<span class="src" data-f="%d"> %s</span>' % (v.id, label)
    return out


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


def plain(segs):
    """The same segments as plain text, for a page's text twin: a figure is
    written `text [fact N]`, which the numbers stage checks against facts.json
    as it checks a page's marks. A link keeps its text and drops its target."""
    if not isinstance(segs, list):
        segs = [segs]
    out = []
    for s in segs:
        if isinstance(s, str):
            out.append(s)
        elif isinstance(s, V) or (isinstance(s, L) and isinstance(s.inner, V)):
            v = s if isinstance(s, V) else s.inner
            if facts.logged(v) is None:
                raise Refusal("a figure that is not what its fact returned reached a text file: %r" % (v.text,))
            if v.text:
                out.append("%s [fact %d]" % (v.text, v.id))
        elif isinstance(s, C):
            out.append(s.text)
        elif isinstance(s, L):
            out.append(plain(s.inner))
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


@fact
def pages_built():
    """How many entries of the navigation have a page, of all of them: the page
    modules under site/pages/, by the entry each claims."""
    import pages as pkg
    have = {m.PAGE["nav"] for m in pkg.discover()}
    n = sum(1 for x in NAV if x in have)
    return V("%d of %d" % (n, len(NAV)),
             Src("file", "site/pages/", "navigation entries with a page, of the %d in the navigation" % len(NAV)),
             raw=",".join(x for x in NAV if x in have), num=True)


def stamp():
    return render([facts.pin_count(), " commits pinned · GitHub snapshot ", facts.snapshot_date(), " · ",
                   pages_built(), " pages built · a figure whose source stops matching stops the build"])


def footer():
    li = []
    for name in facts.PINS["repos"]:
        c = facts.pin_commit(name)
        if c.src.private:
            li.append('<li>%s %s %s for now</li>' % (esc(name), fig(c, src=False),
                                                     fig(facts.api_visibility([name]), src=False)))
        else:
            li.append('<li>%s %s</li>' % (esc(name), fig(c, href=c.src.href, src=False)))
    return (
        '<p>Every figure above this footer names where it was read: beside it, or, for what the map draws, in the '
        'list under the map. The commits below are the ones pins.json '
        'names, and <a href="facts.json">facts.json</a> lists every figure on the page, with where it was read. '
        '<code>python site/build.py --verify-facts</code>, in a clone of <a href="%s">this site\'s repository</a>, '
        'reads each one again: from its repository at the commit below, or from the committed GitHub snapshot of '
        '%s. It names each figure it cannot read, and a stated one has no source to read.</p>'
        '<ul class="pins">%s</ul>'
        '<p><a href="BUILD">BUILD</a> names the commit this copy was deployed from. MIT licence.</p>'
        % (SOURCE_REPO, fig(facts.snapshot_date(), src=False), "".join(li)))


def page(title, current, built, body, description):
    """Home's heading is the name; every other page's is its own, in its body."""
    tag = "h1" if current == "Home" else "p"
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            '<meta http-equiv="Content-Security-Policy" content="%s">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title><meta name="description" content="%s">'
            '<link rel="stylesheet" href="style.css"><link rel="icon" href="data:,"></head>\n'
            '<body><main>'
            '<header><div class="site">loganw.dev</div><%s class="name">Logan W.</%s><nav>%s</nav>'
            '<p class="stamp">%s</p></header>\n%s\n<footer>%s</footer></main></body></html>\n'
            % (esc(CSP), esc(title), esc(description), tag, tag, nav(current, built), stamp(), body, footer()))
