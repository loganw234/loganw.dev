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
each one bites by planting the fault it exists to catch.
"""
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
# per-(name, path) cache of its result - never of its own parsing, no second
# parser - keeps one build from re-scanning the same pinned, immutable text
# hundreds of times. Pin.git memoises for the same reason (CLAUDE.md, trap 2).
_ENTRIES_CACHE = {}


def _entries(name, path):
    key = (name, path)
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


def verify_entry_link(name, path, index, line):
    """The trap: a link off by a line, which sends a reader to the wrong
    heading. A row's #L<line> must be its own entry's heading line, read
    fresh from entries(), or this refuses by name."""
    _, ents = _entries(name, path)
    want = ents[index]["line"]
    if line != want:
        raise facts.Refusal("record: %s entry %d links to %s#L%d, and entries() puts its heading at line %d"
                            % (name, index, path, line, want))


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
    p = facts.pin(name)
    date_v = ledger_date(name, path, index)
    title_v = ledger_title(name, path, index)
    verify_entry_link(name, path, index, e["line"])
    href = p.href(path, e["line"]) if not p.private else ""
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

    name = "cft-fp256"
    _, ents = facts.entries(name, path)
    real_line = ents[0]["line"]
    bad_line = real_line + 1
    try:
        verify_entry_link(name, path, 0, bad_line)
        out.append(("link-line", False,
                    "verify_entry_link did not refuse link line %d against entry 0's real line %d"
                    % (bad_line, real_line)))
    except facts.Refusal as e:
        msg = str(e)
        caught = name in msg and str(bad_line) in msg and str(real_line) in msg
        out.append(("link-line", caught, msg))

    return out
