"""Record: the append-only, dated timeline (docs/SPEC.md, "Record";
briefs/P1.md). Every entry of every pinned repository's docs/VALIDATION.md,
merged, oldest first. Runs only, no essays, no blog.

The ledger parser is facts.entries(name, path); this page never writes a
second one. Which repositories keep a ledger is asked of every pin
(Pin.has), never a hand-written list, so a repository that gains a ledger
later is picked up without an edit here.

The trap: a silently dropped entry, or a link pointing at the wrong line.
Both are held by a live check, not only by a comment: verify_row_count and
verify_entry_link run on every row this page builds, and controls() proves
each one bites by planting the fault it exists to catch. verify_entry_link
reads the href this page actually renders for a row's title (the one a
reader clicks) - not a line number fed back to itself - so it catches a
fault anywhere in how that href gets built, not only a hand-edited call.
"""
import re

import facts
from facts import V, Src, fact
from render import L, esc, render

PAGE = {"file": "record.html", "nav": "Record", "title": "Record - loganw.dev",
        "description": "Every entry of every pinned repository's ledger, merged, oldest first."}

LEDGER_PATH = "docs/VALIDATION.md"

# facts.entries() re-parses its whole file on every call, by design (it is a
# plain function, not a @fact, so it is never assumed fresh - briefs/P1.md).
# cft-fp256's ledger alone is past 15,000 lines, and this page calls entries()
# several times per row (the date fact, the title fact, the link check), so a
# cache of its result - never of its own parsing, no second parser - keeps
# one build from re-scanning the same pinned, immutable text hundreds of
# times. Pin.git memoises for the same reason (CLAUDE.md, trap 2).
#
# Keyed by the pin's own commit, not just (name, path): build.py's
# stale-pin control moves a pin within a single process (the lead's note,
# verifier-P1's re-check), and a key of (name, path) alone would go on
# serving a moved pin's old entries() result for the rest of that run.
_ENTRIES_CACHE = {}


def _entries(name, path):
    key = (name, facts.pin(name).full, path)
    if key not in _ENTRIES_CACHE:
        _ENTRIES_CACHE[key] = facts.entries(name, path)
    return _ENTRIES_CACHE[key]

# Logan, 2026-09-29 (docs/SPEC.md, decision 12): only some of the pinned
# repositories keep a ledger, and the Record is weighted toward them on
# purpose. The exact count is not stated here as prose - it is read out
# below, in ledger_count and ledger_total, so it can never drift from what
# entries() actually parses.
FRAMING = ("Some of the pinned repositories keep a docs/VALIDATION.md ledger, and the Record below is weighted "
           "toward them; that is accepted as how the method grew.")


def S(text, **kw):
    return facts.stated(text, "Logan", "2026-09-29", **kw)


def ledger_repo_names():
    """Repositories with a docs/VALIDATION.md at their pin: asked of every
    pin (Pin.has), never a hand-written list, so a repository that gains a
    ledger and is not added here still shows up."""
    return sorted(name for name in facts.PINS["repos"] if facts.pin(name).has(LEDGER_PATH))


def verify_row_count(name, path, n_rows):
    """The trap: a row dropped between parsing and rendering, silently. The
    rows a repository would show must equal the entries entries() parses for
    it right now, or this refuses by name, with both counts."""
    _, ents = _entries(name, path)
    if n_rows != len(ents):
        raise facts.Refusal("record: %s has %d entries parsed at its pin, and %d rows would be rendered"
                            % (name, len(ents), n_rows))


_LINE_HREF = re.compile(r"#L(\d+)$")


def verify_entry_link(name, path, index, href):
    """The trap: a link off by a line, which sends a reader to the wrong
    heading. Takes the href this page actually renders for a row's title -
    the one a reader clicks - not a line number handed back to itself, so a
    fault anywhere in how that href gets built is caught, not only a
    hand-edited call site. A private repository's href is empty; there is
    no rendered link to check, so this passes it through."""
    if not href:
        return
    _, ents = _entries(name, path)
    want = ents[index]["line"]
    m = _LINE_HREF.search(href)
    if not m or int(m.group(1)) != want:
        raise facts.Refusal("record: %s entry %d's rendered link is %r, and entries() puts its heading at "
                            "line %d" % (name, index, href, want))


@fact
def ledger_date(name, path, index):
    """entries()'s own date for its index-th entry, re-read every time."""
    p = facts.pin(name)
    _, ents = _entries(name, path)
    e = ents[index]
    return V(e["date"], p.src("file", "%s:%d" % (path, e["line"]),
                              "entry %d of %d (%s)" % (index + 1, len(ents), e["how"]), path, e["line"]),
             raw=e["date"], num=True)


@fact
def ledger_title(name, path, index):
    """entries()'s own heading text for its index-th entry, re-read every
    time: the entry's title exactly as its ledger titles it."""
    p = facts.pin(name)
    _, ents = _entries(name, path)
    e = ents[index]
    return V(e["title"], p.src("file", "%s:%d" % (path, e["line"]), "entry %d's own heading" % (index + 1),
                               path, e["line"]),
             raw=e["title"])


@fact
def ledger_count(name, path):
    """A repository's entry count, read at its pin."""
    p = facts.pin(name)
    _, ents = _entries(name, path)
    n = len(ents)
    return V(str(n), p.src("file", path, "its %s entries, counted" % path, path), raw=str(n), num=True)


@fact
def ledger_total(names, path):
    """The entries of every named repository's ledger, summed, at their pins."""
    total = 0
    for n in names:
        _, ents = _entries(n, path)
        total += len(ents)
    return V(str(total), Src("file", path, "%s: entries at their pins, summed" % ", ".join(names)),
             raw=str(total), num=True)


def _row(name, path, index, e):
    date_v = ledger_date(name, path, index)
    title_v = ledger_title(name, path, index)
    # The same href the citation carries (ledger_title's own logged source),
    # not a second, separately computed one: the link a reader clicks and
    # the one the check reads are now one value, not two that merely agree
    # today.
    href = title_v.src.href
    verify_entry_link(name, path, index, href)
    entry = L(href, title_v) if href else title_v
    return ('<tr><td class="d">%s</td><td class="p">%s</td><td>%s</td></tr>'
            % (render(date_v), esc(name), render(entry)))


def timeline():
    """-> (names, table html). Every entry of every ledger-keeping
    repository, merged oldest first; entries sharing a date are ordered by
    repository and then by line, a stable tie-break."""
    names = ledger_repo_names()
    merged = []
    for name in names:
        _, ents = _entries(name, LEDGER_PATH)
        for i, e in enumerate(ents):
            merged.append((name, i, e))
    merged.sort(key=lambda r: (r[2]["date"], r[0], r[2]["line"]))
    counts = {name: 0 for name in names}
    body = []
    for name, i, e in merged:
        counts[name] += 1
        body.append(_row(name, LEDGER_PATH, i, e))
    for name in names:
        verify_row_count(name, LEDGER_PATH, counts[name])
    head = "<thead><tr><th>date</th><th>repository</th><th>entry</th></tr></thead>"
    return names, ("<table>%s<tbody>%s</tbody></table>" % (head, "".join(body)))


def render_page(ctx):
    names, table = timeline()
    counts_html = "".join(
        "<li>%s</li>" % render([name, ": ", ledger_count(name, LEDGER_PATH), " entries"]) for name in names)
    total_html = render(["That makes ", ledger_total(names, LEDGER_PATH), " entries below, oldest first."])
    return (
        '<h1>Record</h1>'
        '<div class="measure"><p class="lede">%s</p></div>'
        '<h2><small>I</small>Entry counts</h2>'
        '<ul class="plain">%s</ul><p class="cap">%s</p>'
        '<h2><small>II</small>Every entry</h2>'
        '<div class="table-wrap">%s</div>'
        '<p class="cap">Rows are merged oldest first. Entries sharing a date are ordered by repository, then by '
        'the line their own heading sits at - a stable order, not a claim about which happened first that day.</p>'
        % (render(S(FRAMING)), counts_html, total_html, table)
    )


def controls():
    """Named by the property that makes them bite (briefs/P1.md, "The
    negative controls"):

    1. row-count: a dropped entry. cft-rebound's real entry count, minus
       one, must be refused by name.
    2. link-line: a link off by a line. cft-fp256's first entry, linked one
       line later than its own heading, must be refused by name.
    """
    out = []
    path = LEDGER_PATH

    name = "cft-rebound"
    _, ents = facts.entries(name, path)
    short = len(ents) - 1
    try:
        verify_row_count(name, path, short)
        out.append(("row-count", False,
                    "verify_row_count(%r, %d) did not refuse against %d entries parsed" % (name, short, len(ents))))
    except facts.Refusal as e:
        msg = str(e)
        caught = name in msg and str(len(ents)) in msg and str(short) in msg
        out.append(("row-count", caught, msg))

    # Planted in the rendering path itself - Pin.href, which ledger_title's
    # own p.src(...) call goes through - not by calling verify_entry_link
    # with a hand-fed line. This is the same route the verifier used to
    # find the original defect (a title link built from its own separately
    # computed href), so the control now proves the fix, not just the
    # guard's arithmetic.
    name = "cft-fp256"
    _, ents = facts.entries(name, path)
    real_line = ents[0]["line"]
    original_href = facts.Pin.href

    def _off_by_one(self, path="", line=0, _orig=original_href):
        return _orig(self, path, line + 1 if line else line)

    facts.Pin.href = _off_by_one
    try:
        bad_href = ledger_title(name, path, 0).src.href
    finally:
        facts.Pin.href = original_href
    try:
        verify_entry_link(name, path, 0, bad_href)
        out.append(("link-line", False,
                    "verify_entry_link did not refuse %r, planted one line off entry 0's real line %d via "
                    "Pin.href" % (bad_href, real_line)))
    except facts.Refusal as e:
        msg = str(e)
        caught = name in msg and bad_href in msg and str(real_line) in msg
        out.append(("link-line", caught, msg))

    return out
