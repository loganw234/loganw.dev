"""The map: where each project came from, generated from data/relations.json.

Two layouts are drawn from the same nodes and edges: the wide one, time
across, and a narrow one, time down the page and the threads as columns,
swapped in by CSS at 600px (site/styles/map.css) with no script. Neither
layout is written by hand from the other: svg_wide() and svg_narrow() both
read the same `nodes`/`edges` build() returns, and block() checks the two
node names and (tail, head, kind) triples they actually drew are equal,
refusing the build if a layout ever drops one - the trap a hand-written
second copy would fall into.

Position across (wide) or down (narrow) is the day a repository was born,
read by the build: the earliest commit at its pin, the snapshot's earliest
commit for a repository not cloned here, the day a README states it was
split out of another with its history carried, or - for a fork - the day
GitHub says the fork itself was made, never a commit (a fork's own commits
are mostly its parent's history). Every edge is a claim and names the file
that makes it; its words are read at the pin, and an edge whose words are
gone refuses the build. StoryDocs' edges to what it has touched are derived
from its projects/ directories at the pin, mapped to map nodes by
relations.json's storydocs_projects; a directory that mapping does not name
refuses the build, by name.

The axis has two stretches: a short one for the first projects, whose start
and end are fixed here, and the main one, which starts on a fixed day and
ends just after the latest of the snapshot and every birth in it, so time
moving on never breaks the build. A birth outside both stretches refuses:
the axis gets redrawn, the date is never clamped. Every date the map prints
is a figure, marked with its fact; the month ticks are the only text the
numbers stage lets through unmarked, and only in the shape of a month.
"""
import datetime
import json
import math
import pathlib

import facts
from facts import Refusal
from render import esc, fig, mark

DATA = json.loads((pathlib.Path(__file__).resolve().parent / "data" / "relations.json").read_text(encoding="utf-8"))

MAIN0 = datetime.date(2026, 6, 20)
MAIN_X0, MAIN_X1 = 230.0, 985.0
STUB0, STUB1 = datetime.date(2025, 11, 1), datetime.date(2025, 11, 9)
STUB_X0 = 140.0
MARGIN = datetime.timedelta(days=2)
LANE_TOP = [30, 178, 306]
ROWY = {0: [58, 88, 118, 148], 1: [210, 240, 270], 2: [332, 358, 384]}
AXIS_Y = 418
KIND = dict(DATA["kinds"])
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

# The narrow (phone) layout: time down a vertical axis at NARROW_AXIS_X, the
# three lanes as columns at COL_X. A node's column is nudged sideways by its
# row (layout only, same field the wide layout uses), so nodes born close
# together in one lane do not print on top of each other; its label sits
# centred below the marker, never to a side, so a long name cannot run past
# the viewBox and force a sideways scroll on a phone.
NARROW_VB_W = 380
NARROW_STUB_Y0 = 76.0
NARROW_Y0, NARROW_Y1 = 232.0, 900.0
NARROW_AXIS_X = 24.0
COL_X = [75.0, 190.0, 305.0]
ROW_DX = 14.0


class Axis:
    """Date <-> pixel, along whichever dimension the caller places it on: the
    wide layout's X, or the narrow layout's Y. dates: every date the map
    places, the snapshot's among them."""

    def __init__(self, dates, x0=MAIN_X0, x1=MAIN_X1, stub_x0=STUB_X0):
        ds = [datetime.date.fromisoformat(d[:10]) for d in dates]
        self.main1 = max([d for d in ds if d >= MAIN0] + [MAIN0]) + MARGIN
        self.x0, self.x1, self.stub_x0 = x0, x1, stub_x0
        self.px = (x1 - x0) / (self.main1 - MAIN0).days

    def x(self, iso, what):
        d = datetime.date.fromisoformat(iso[:10])
        if MAIN0 <= d <= self.main1:
            return self.x0 + (d - MAIN0).days * self.px
        if STUB0 <= d <= STUB1:
            return self.stub_x0 + (d - STUB0).days * self.px
        raise Refusal("%s: %s falls outside both stretches of the map's axis (%s to %s, and %s on); redraw the "
                      "axis rather than clamp the date" % (what, iso, STUB0, STUB1, MAIN0))

    def ticks(self):
        """The first day of each month on the axis: 'Nov 2025', then 'Jul 2026',
        'Aug', ... - a year where a stretch starts, and at each January."""
        out = []
        for lo, hi in ((STUB0, STUB1), (MAIN0, self.main1)):
            d, first = datetime.date(lo.year, lo.month, 1), True
            while d <= hi:
                if d >= lo:
                    out.append((d, "%s %d" % (MONTHS[d.month - 1], d.year) if first or d.month == 1
                                else MONTHS[d.month - 1]))
                    first = False
                d = datetime.date(d.year + d.month // 12, d.month % 12 + 1, 1)
        return out


# ---------------------------------------------------------------------------
# StoryDocs' edges to what it has touched: derived from projects/ at its pin,
# never typed, mapped to node(s) by relations.json's storydocs_projects.
# ---------------------------------------------------------------------------

@facts.fact
def api_created(name):
    """A fork's day of creation on GitHub, in UTC (the API gives no author's
    offset) - never a commit's date. A fork's own commits are mostly its
    parent's history (docs/SPEC.md: nextpnr-xilinx counts 45 of 3397 commits
    that are its own), so its earliest commit would place it in the parent's
    era, not when the fork itself was made."""
    meta = facts.repo_meta(name)
    if not meta.get("isFork"):
        raise Refusal("%s is not a fork; facts.born or facts.api_born places one that isn't" % name)
    iso = meta["createdAt"]
    pub = facts.is_public(name)
    where = ("GitHub snapshot %s: created (a fork - dated by GitHub's record of when the fork itself was made, "
             "in UTC, never by a commit, since its earliest commit belongs to the project it forked)"
             % facts.snapdate())
    return facts.V(iso[:10], facts.Src("api", where, "%s: createdAt %s" % (name, iso),
                                       meta["url"] if pub else "", not pub), raw=iso[:10], num=True)


def _storydocs_dirs():
    """The projects/ subdirectories StoryDocs actually has at its pin - read,
    never assumed, so a directory added or removed there is seen the next
    time the build runs."""
    p = facts.pin("StoryDocs")
    out = []
    for line in p.git("ls-tree", p.full, "projects/").splitlines():
        if not line.strip():
            continue
        info, _, name = line.partition("\t")
        parts = info.split()
        if len(parts) >= 2 and parts[1] == "tree" and name:
            out.append(name.rsplit("/", 1)[-1])
    if not out:
        raise Refusal("StoryDocs %s has no projects/ directories to derive edges from" % p.short)
    return sorted(out)


def _storydocs_edges():
    mapping = DATA.get("storydocs_projects", {})
    out = []
    for d in _storydocs_dirs():
        cfg = mapping.get(d)
        if cfg is None:
            raise Refusal("StoryDocs's projects/%s is not named in relations.json's storydocs_projects; a "
                          "directory that maps to no node refuses the build" % d)
        path = cfg.get("path", "projects/" + d)
        # Most directories are their own evidence - they exist at the pin, and
        # relations.json's mapping (reviewed, with its own reason) says what
        # they are. One ("method") needed its manifest read to find what it
        # documents, and gets a quote from it instead.
        v = facts.prose("StoryDocs", path, cfg["pattern"]) if "pattern" in cfg else facts.exists("StoryDocs", "projects/" + d)
        nodes = cfg["nodes"]
        bend = cfg.get("bend", 0)
        bends = bend if isinstance(bend, list) else [bend] * len(nodes)
        if len(bends) != len(nodes):
            # zip() would drop the edges past the shorter list, silently, and
            # the map and the dossiers read this one list (verifier-seam).
            raise Refusal("relations.json's storydocs_projects entry for %s gives %d bends for its %d nodes; give "
                          "one each" % (d, len(bends), len(nodes)))
        for node, b in zip(nodes, bends):
            out.append(dict(tail="StoryDocs", head=node, kind="documents", bend=b, repo="StoryDocs", path=path, v=v))
    return out


def all_edges():
    """Every edge the map draws, each with its evidence as a figure:
    relations.json's own edges, then those derived at a pin (StoryDocs'
    documents edges). One list, read by the map and by each dossier's
    Connections, so the two cannot disagree. At P2's merge the dossiers read
    relations.json alone, and four of the five missed StoryDocs' edges;
    cft-rebound, for which StoryDocs has no projects/ directory, had none to
    miss (verifier-seam)."""
    edges = []
    for e in DATA["edges"]:
        if e["kind"] not in KIND:
            raise Refusal("an edge has kind %r, which relations.json does not define" % e["kind"])
        edges.append(dict(e, v=facts.prose(e["repo"], e["path"], e["pattern"])))
    return edges + _storydocs_edges()


def build():
    nodes = {}
    for n in DATA["nodes"]:
        name = n["name"]
        if "born" in n:
            b = facts.prose(name, n["born"]["path"], n["born"]["pattern"], num=True)
        elif n.get("created_api"):
            b = api_created(name)
        elif name in facts.PINS["repos"]:
            b = facts.born(name)
        elif name in facts.PINS["github_only"]:
            b = facts.api_born(name)
        else:
            raise Refusal("the map names %s, which pins.json neither pins nor lists as github_only" % name)
        # No node is greyed by its count of agent co-author trailers: that count
        # is a lower bound, and Logan's word (2026-09-29) is that every project
        # was AI-driven. Styling on it would have drawn a claim the record does
        # not support.
        note = None
        if "note" in n:
            before, _, after = n["note"]["format"].partition("%s")
            note = (before, facts.prose(name, n["note"]["path"], n["note"]["pattern"]), after)
        nodes[name] = dict(name=name, lane=n["lane"], row=n["row"], born=b,
                           vis=facts.api_visibility([name]), trunk=n.get("trunk", False), note=note)
    edges = all_edges()
    for e in edges:
        for end in (e["tail"], e["head"]):
            if end not in nodes:
                raise Refusal("an edge (%s %s %s) names %s, which is not on the map"
                              % (e["tail"], e["kind"], e["head"], end))
    fams = []
    for f in DATA["families"]:
        span = facts.family_span(f["match"], f["exclude"])
        first, last = span.raw.split()
        fams.append(dict(f, v=facts.family(f["match"], f["exclude"]), span=span, first=first, last=last))
    now = facts.snapshot_date()
    return dict(nodes=nodes, edges=edges, families=fams, now=now)


# ---------------------------------------------------------------------------
# Drawing shared by both layouts
# ---------------------------------------------------------------------------

def _curve(x1, y1, x2, y2, bend):
    dx, dy = x2 - x1, y2 - y1
    ln = math.hypot(dx, dy) or 1.0
    cx, cy = (x1 + x2) / 2 - dy / ln * bend, (y1 + y2) / 2 + dx / ln * bend

    def toward(px, py, qx, qy, d):
        l2 = math.hypot(qx - px, qy - py) or 1.0
        return px + (qx - px) / l2 * d, py + (qy - py) / l2 * d
    sx, sy = toward(x1, y1, cx, cy, 6)
    ex, ey = toward(x2, y2, cx, cy, 8)
    return sx, sy, cx, cy, ex, ey


def _edge_svg(e, pos, dim=False):
    x1, y1 = pos[e["tail"]]
    x2, y2 = pos[e["head"]]
    sx, sy, cx, cy, ex, ey = _curve(x1, y1, x2, y2, e["bend"])
    return ('<path class="edge %s%s" d="M%.1f %.1fQ%.1f %.1f %.1f %.1f" marker-end="url(#%s)"><title>%s %s %s</title>'
           '</path>' % (e["kind"], " dim" if dim else "", sx, sy, cx, cy, ex, ey,
                        "ah-acc" if e["kind"] == "grew-into" else "ah",
                        esc(e["tail"]), esc(KIND[e["kind"]]), esc(e["head"])))


def _defs():
    return ('<defs><marker id="ah" viewBox="0 0 8 8" refX="7.5" refY="4" markerWidth="6.5" markerHeight="6.5" '
           'orient="auto"><path class="ah" d="M0 0L8 4L0 8z"/></marker>'
           '<marker id="ah-acc" viewBox="0 0 8 8" refX="7.5" refY="4" markerWidth="6.5" markerHeight="6.5" '
           'orient="auto"><path class="ah-acc" d="M0 0L8 4L0 8z"/></marker></defs>')


def _node_svg(n):
    """A node's CSS classes, and its tail lines (private, then any note) past
    the name - each a fragment of marked-up text. svg_wide joins them inline,
    after the name, on one line; svg_narrow, tighter on width, gives each its
    own line below the name instead, so a node with a note (Mercenaries2's
    server) is never the long, centred line that would run past the
    viewBox."""
    private = n["vis"].text == "private"
    cls = " ".join(["node"] + (["private"] if private else []) + (["trunk"] if n["trunk"] else []))
    lines = [mark(n["vis"])] if private else []
    if n["note"]:
        before, v, after = n["note"]
        lines.append("%s%s%s" % (esc(before), mark(v), esc(after)))
    return cls, lines


def _select(M, omit):
    """M's nodes and edges, with one node (and anything touching it) dropped -
    for the negative control only. Production code never passes omit."""
    if omit is None:
        return M["nodes"], M["edges"]
    nodes = {k: v for k, v in M["nodes"].items() if k != omit}
    edges = [e for e in M["edges"] if omit not in (e["tail"], e["head"])]
    return nodes, edges


def svg_wide(M, omit=None, dim_lane=None):
    """The wide map, 1080x440, time left to right. -> (svg, {node names
    drawn}, {(tail, head, kind) drawn}): the same two kinds of set
    svg_narrow returns, so block() can hold them equal. dim_lane (a thread
    page's slice): every node outside that lane, and every edge that neither
    leaves nor enters it, is drawn with the extra class "dim" - the same
    node and edge set, so the check still holds, only styled back."""
    nodes, edges = _select(M, omit)
    ax = Axis([n["born"].text for n in nodes.values()] + [M["now"].text] + [f["last"] for f in M["families"]])
    pos = {name: (ax.x(n["born"].text, name), ROWY[n["lane"]][n["row"]]) for name, n in nodes.items()}
    o = ['<svg viewBox="0 0 1080 440" role="img" aria-labelledby="map-t-wide" xmlns="http://www.w3.org/2000/svg">',
         '<title id="map-t-wide">Where each project came from: born dates across, threads down, typed relations '
         'between them</title>', _defs()]
    for label, top in zip(DATA["lanes"], LANE_TOP):
        o.append('<text class="lane" x="14" y="%d">%s</text>' % (top + 16, esc(label)))
    for top in LANE_TOP[1:]:
        o.append('<line class="sep" x1="14" x2="1066" y1="%d" y2="%d"/>' % (top - 4, top - 4))
    now = M["now"]
    xn = ax.x(now.text, "the snapshot")
    o.append('<line class="now" x1="%.1f" x2="%.1f" y1="28" y2="%d"/>' % (xn, xn, AXIS_Y))
    o.append('<text class="tick" x="%.1f" y="20" text-anchor="end">snapshot %s</text>' % (xn, mark(now)))
    xs1 = ax.x(STUB1.isoformat(), "axis")
    o.append('<path class="axis" d="M%.1f %dH%.1f M%.1f %dH%.1f"/>' % (STUB_X0 - 4, AXIS_Y, xs1 + 3, MAIN_X0 - 8, AXIS_Y, MAIN_X1))
    o.append('<path class="axis" d="M%.1f %d l6 -9 M%.1f %d l6 -9"/>' % (xs1 + 6, AXIS_Y + 4, xs1 + 13, AXIS_Y + 4))
    for d, label in ax.ticks():
        x = ax.x(d.isoformat(), "a tick")
        o.append('<path class="axis" d="M%.1f %dv5"/><text class="tick" x="%.1f" y="%d">%s</text>' % (x, AXIS_Y, x, AXIS_Y + 17, label))
    for f in M["families"]:
        x0, x1 = ax.x(f["first"], f["label"]), ax.x(f["last"], f["label"])
        y = ROWY[f["lane"]][f["row"]]
        o.append('<line class="range" x1="%.1f" x2="%.1f" y1="%d" y2="%d"/>' % (x0, x1, y, y))
        o.append('<text x="%.1f" y="%.1f">%s %s<tspan class="note"> created %s</tspan></text>'
                 % (x1 + 9, y + 4.5, mark(f["v"]), esc(f["label"]), mark(f["span"])))
    for e in edges:
        e_dim = dim_lane is not None and dim_lane not in (nodes[e["tail"]]["lane"], nodes[e["head"]]["lane"])
        o.append(_edge_svg(e, pos, dim=e_dim))
    for name, n in nodes.items():
        x, y = pos[name]
        cls, lines = _node_svg(n)
        if dim_lane is not None and n["lane"] != dim_lane:
            cls += " dim"
        tail = "".join('<tspan class="note"> %s</tspan>' % ln for ln in lines)
        o.append('<g class="%s"><rect x="%.1f" y="%.1f" width="7" height="7"/><text x="%.1f" y="%.1f">%s%s</text></g>'
                 % (cls, x - 3.5, y - 3.5, x + 9, y + 4.5, esc(name), tail))
    o.append("</svg>")
    return "\n".join(o), set(nodes), {(e["tail"], e["head"], e["kind"]) for e in edges}


def svg_narrow(M, omit=None, dim_lane=None):
    """The phone map: time down a vertical axis, the three lanes as columns.
    Every label sits centred under its marker, so a long name spreads to
    either side rather than running past the viewBox - the one thing that
    would force a sideways scroll on a phone. -> the same (svg, node names,
    edge triples) shape as svg_wide."""
    nodes, edges = _select(M, omit)
    ax = Axis([n["born"].text for n in nodes.values()] + [M["now"].text] + [f["last"] for f in M["families"]],
             x0=NARROW_Y0, x1=NARROW_Y1, stub_x0=NARROW_STUB_Y0)

    def jitter(lane, row):
        n = len(ROWY[lane])
        return COL_X[lane] + (row - (n - 1) / 2.0) * ROW_DX

    pos = {name: (jitter(n["lane"], n["row"]), ax.x(n["born"].text, name)) for name, n in nodes.items()}
    height = ax.x(ax.main1.isoformat(), "the bottom margin") + 40
    o = ['<svg viewBox="0 0 %d %.0f" role="img" aria-labelledby="map-t-narrow" xmlns="http://www.w3.org/2000/svg">'
        % (NARROW_VB_W, height),
        '<title id="map-t-narrow">Where each project came from, phone layout: born dates down the page, threads '
        'as columns, typed relations between them</title>', _defs()]
    for label, cx in zip(DATA["lanes"], COL_X):
        # A lane name too wide for its column (FILM & PHOTOGRAPHY) breaks at
        # its " & ", onto a second line; a narrower name (DETERMINISM,
        # PRESERVATION) stays on one.
        if " & " in label:
            first, second = label.split(" & ", 1)
            o.append('<text class="lane" x="%.1f" y="10" text-anchor="middle">%s &amp;</text>'
                     '<text class="lane" x="%.1f" y="19" text-anchor="middle">%s</text>'
                     % (cx, esc(first), cx, esc(second)))
        else:
            o.append('<text class="lane" x="%.1f" y="14" text-anchor="middle">%s</text>' % (cx, esc(label)))
    for cx in ((COL_X[0] + COL_X[1]) / 2, (COL_X[1] + COL_X[2]) / 2):
        o.append('<line class="sep" x1="%.1f" x2="%.1f" y1="22" y2="%.1f"/>' % (cx, cx, height - 8))
    now = M["now"]
    yn = ax.x(now.text, "the snapshot")
    o.append('<line class="now" x1="8" x2="%d" y1="%.1f" y2="%.1f"/>' % (NARROW_VB_W - 8, yn, yn))
    o.append('<text class="tick" x="%.1f" y="%.1f">snapshot %s</text>' % (NARROW_AXIS_X + 4, yn - 4, mark(now)))
    ys1 = ax.x(STUB1.isoformat(), "axis")
    o.append('<path class="axis" d="M%.1f %.1fV%.1f M%.1f %.1fV%.1f"/>'
             % (NARROW_AXIS_X, NARROW_STUB_Y0 - 4, ys1 + 3, NARROW_AXIS_X, NARROW_Y0 - 8, height - 12))
    o.append('<path class="axis" d="M%.1f %.1f l9 6 M%.1f %.1f l9 6"/>' % (NARROW_AXIS_X - 4, ys1 + 6, NARROW_AXIS_X - 4, ys1 + 13))
    for d, label in ax.ticks():
        y = ax.x(d.isoformat(), "a tick")
        o.append('<path class="axis" d="M%.1f %.1fh5"/><text class="tick" x="%.1f" y="%.1f">%s</text>'
                 % (NARROW_AXIS_X, y, NARROW_AXIS_X + 8, y + 3.5, label))
    for f in M["families"]:
        y0, y1 = ax.x(f["first"], f["label"]), ax.x(f["last"], f["label"])
        cx = COL_X[f["lane"]]
        o.append('<line class="range" x1="%.1f" x2="%.1f" y1="%.1f" y2="%.1f"/>' % (cx, cx, y0, y1))
        # Two lines, not one long centred one (the count and name, then when):
        # "N mercs2 repositories, created ... to ..." is wide enough to run
        # past the viewBox on one line at this column.
        o.append('<text x="%.1f" y="%.1f" text-anchor="middle">%s %s</text>'
                 '<text class="note" x="%.1f" y="%.1f" text-anchor="middle">created %s</text>'
                 % (cx, y1 + 20, mark(f["v"]), esc(f["label"]), cx, y1 + 32, mark(f["span"])))
    for e in edges:
        e_dim = dim_lane is not None and dim_lane not in (nodes[e["tail"]]["lane"], nodes[e["head"]]["lane"])
        o.append(_edge_svg(e, pos, dim=e_dim))
    # A label sits below its marker at y+16, but two markers in one lane born
    # close together would print one label over the other (row alone does not
    # decide this: a later date can carry an earlier row, and the two can
    # cancel out). So each lane's labels are walked earliest-born first, and
    # any label that would start less than MIN_LABEL_GAP below the previous
    # one's own bottom (its name, and, stacked under that, any private or
    # note line - each its own line here, never appended to the name, since
    # that could run a long note past the viewBox) is pushed down until it
    # doesn't: a name never prints on top of another, whatever the two dates
    # and rows are, and a long note never widens a centred line past it.
    LINE_H = 12.0
    MIN_LABEL_GAP = 15.0
    lines_of = {name: _node_svg(n)[1] for name, n in nodes.items()}
    by_lane = {}
    for name, n in nodes.items():
        by_lane.setdefault(n["lane"], []).append((pos[name][1], name))
    label_y = {}
    for items in by_lane.values():
        bottom = None
        for my, name in sorted(items):
            ly = my + 16
            if bottom is not None and ly < bottom + MIN_LABEL_GAP:
                ly = bottom + MIN_LABEL_GAP
            label_y[name] = ly
            bottom = ly + len(lines_of[name]) * LINE_H
    for name, n in nodes.items():
        x, y = pos[name]
        cls, lines = _node_svg(n)
        if dim_lane is not None and n["lane"] != dim_lane:
            cls += " dim"
        ly = label_y[name]
        texts = ['<text x="%.1f" y="%.1f" text-anchor="middle">%s</text>' % (x, ly, esc(name))]
        for i, line in enumerate(lines, 1):
            texts.append('<text class="note" x="%.1f" y="%.1f" text-anchor="middle">%s</text>' % (x, ly + i * LINE_H, line))
        o.append('<g class="%s"><rect x="%.1f" y="%.1f" width="7" height="7"/>%s</g>'
                 % (cls, x - 3.5, y - 3.5, "".join(texts)))
    o.append("</svg>")
    return "\n".join(o), set(nodes), {(e["tail"], e["head"], e["kind"]) for e in edges}


def check_parity(wide, narrow):
    """wide and narrow: (node names, edge triples) as svg_wide/svg_narrow
    return them. -> [problem]: empty when the narrow layout shows exactly
    what the wide one does."""
    wn, we = wide
    nn, ne = narrow
    problems = []
    if wn != nn:
        problems.append("the narrow map's nodes are %s, and the wide map's are %s" % (sorted(nn), sorted(wn)))
    if we != ne:
        fmt = lambda es: sorted("%s-%s(%s)" % t for t in es)
        problems.append("the narrow map's edges are %s, and the wide map's are %s" % (fmt(ne), fmt(we)))
    return problems


def legend():
    li = ['<li><svg width="30" height="10" aria-hidden="true"><line class="edge %s" x1="1" y1="5" x2="29" y2="5"/></svg>%s</li>'
          % (k, esc(t)) for k, t in DATA["kinds"]]
    li += ['<li><svg width="10" height="10" aria-hidden="true"><g class="node"><rect x="1.5" y="1.5" width="7" height="7"/></g></svg>public</li>',
           '<li><svg width="10" height="10" aria-hidden="true"><g class="node private"><rect x="1.5" y="1.5" width="7" height="7"/></g></svg>private for now</li>',
           '<li><svg width="30" height="10" aria-hidden="true"><line class="range" x1="1" y1="5" x2="29" y2="5"/></svg>a family, first to last created</li>']
    return '<ul class="legend">%s</ul>' % "".join(li)


def block():
    M = build()
    wide_svg, wide_n, wide_e = svg_wide(M)
    narrow_svg, narrow_n, narrow_e = svg_narrow(M)
    problems = check_parity((wide_n, wide_e), (narrow_n, narrow_e))
    if problems:
        raise Refusal("the map's narrow layout does not show what the wide one does: %s" % "; ".join(problems))
    ev = "".join('<li><b>%s</b> %s <b>%s</b>: %s</li>' % (esc(e["tail"]), esc(KIND[e["kind"]]), esc(e["head"]), fig(e["v"]))
                 for e in M["edges"])
    order = sorted(M["nodes"].values(), key=lambda n: (n["born"].text, n["name"]))
    pos = "".join('<li>%s: %s</li>' % (esc(n["name"]), fig(n["born"])) for n in order)
    fam = "".join('<li>%s %s, created %s</li>' % (fig(f["v"]), esc(f["label"]), fig(f["span"])) for f in M["families"])
    # Every other figure the drawing marks, with its source, so no figure on
    # the page goes without one (verifier-P0 found four that did). Both
    # layouts draw the same figures, so one list under both covers them.
    drawn = ['<li>the line marked "snapshot": %s</li>' % fig(M["now"])]
    drawn += ['<li>%s: %s</li>' % (esc(n["name"]), fig(n["vis"])) for n in order if n["vis"].text == "private"]
    drawn += ['<li>%s: %s%s%s</li>' % (esc(n["name"]), esc(n["note"][0]), fig(n["note"][1]), esc(n["note"][2]))
              for n in order if n["note"]]
    cap = ("Across on a wide screen, down on a phone: the day each repository was born &mdash; its first commit at "
           "the pin, on its author's calendar; the date its README states it was split out of another; its first "
           "commit through the GitHub snapshot, in UTC, for a repository read only there; or, for a fork, the day "
           "GitHub says the fork itself was made, never a commit. The threads run the other way. Read each arrow as "
           "a sentence, tail to head; each one names the file that says so. Both layouts draw the same nodes and "
           "edges (a check below the map holds them equal); one is shown at a time, chosen by your screen's width.")
    return ('<figure class="map">'
           '<div class="map-wide">%s</div>'
           '<div class="map-narrow">%s</div>'
           '<figcaption>%s</figcaption>%s'
           '<details class="evidence"><summary>The file behind each arrow, and behind each position</summary>'
           '<ol>%s</ol><p>Positions, earliest first:</p><ul>%s</ul><p>Families:</p><ul>%s</ul>'
           '<p>The rest of what the drawing marks:</p><ul>%s</ul></details></figure>'
           % (wide_svg, narrow_svg, cap, legend(), ev, pos, fam, "".join(drawn)))


def lane_slice(lane_index):
    """One thread's slice of the map: that lane's nodes, and every edge that
    leaves or enters it (the other end may sit in another lane); the rest of
    the map is still drawn, behind it, so a reader sees the same whole map
    Home does, pushed back rather than removed. Same two layouts, same
    parity check, as block()."""
    M = build()
    wide_svg, wide_n, wide_e = svg_wide(M, dim_lane=lane_index)
    narrow_svg, narrow_n, narrow_e = svg_narrow(M, dim_lane=lane_index)
    problems = check_parity((wide_n, wide_e), (narrow_n, narrow_e))
    if problems:
        raise Refusal("the %s thread's map slice: %s" % (DATA["lanes"][lane_index], "; ".join(problems)))
    order = sorted(M["nodes"].values(), key=lambda n: (n["born"].text, n["name"]))
    in_lane = [n for n in order if n["lane"] == lane_index]
    # Both layouts still draw the rest of the map too, dimmed rather than
    # removed (site/styles/map.css), so every node, every edge and the
    # family are covered here exactly as block() covers them for Home - the
    # numbers stage holds a dimmed figure to the same rule as a bright one.
    ev = "".join('<li><b>%s</b> %s <b>%s</b>: %s</li>' % (esc(e["tail"]), esc(KIND[e["kind"]]), esc(e["head"]), fig(e["v"]))
                for e in M["edges"])
    pos_li = "".join('<li>%s: %s</li>' % (esc(n["name"]), fig(n["born"])) for n in order)
    fam_li = "".join('<li>%s %s, created %s</li>' % (fig(f["v"]), esc(f["label"]), fig(f["span"])) for f in M["families"])
    drawn = ['<li>the line marked "snapshot": %s</li>' % fig(M["now"])]
    drawn += ['<li>%s: %s</li>' % (esc(n["name"]), fig(n["vis"])) for n in order if n["vis"].text == "private"]
    drawn += ['<li>%s: %s%s%s</li>' % (esc(n["name"]), esc(n["note"][0]), fig(n["note"][1]), esc(n["note"][2]))
              for n in order if n["note"]]
    cap = ("This thread's part of the map (site/data/relations.json), the rest of it still drawn behind: every node "
          "in this lane, and every edge that leaves or enters it, wherever the other end sits. Both layouts draw "
          "the same nodes and edges as each other and as the full map on Home (the same check holds them equal); "
          "one is shown at a time, chosen by your screen's width. This lane's own nodes: %s."
          % ", ".join(esc(n["name"]) for n in in_lane))
    return ('<figure class="map slice"><div class="map-wide">%s</div><div class="map-narrow">%s</div>'
           '<figcaption>%s</figcaption>'
           '<details class="evidence"><summary>The file behind each arrow, and behind each position, in this '
           'thread</summary><ol>%s</ol><p>Positions, earliest first:</p><ul>%s</ul><p>Families:</p><ul>%s</ul>'
           '<p>The rest of what the drawing marks:</p><ul>%s</ul></details></figure>'
           % (wide_svg, narrow_svg, cap, ev, pos_li, fam_li, "".join(drawn)))
