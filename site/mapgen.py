"""The map: where each project came from, generated from data/relations.json.

Position across is the day a repository was born, read by the build: the
earliest commit at its pin, the snapshot's earliest commit for a repository
not cloned here, or - where a README states that the repository was split
out of another with its history carried - the date that README states,
because the carried history would otherwise place it where its parent began.

Every edge is a claim and names the file that makes it; its words are read at
the pin, and an edge whose words are gone refuses the build. A date that falls
outside both stretches of the axis refuses too: the axis gets redrawn, the
date is never clamped.
"""
import datetime
import json
import math
import pathlib

import facts
from facts import Refusal
from render import esc, fig

DATA = json.loads((pathlib.Path(__file__).resolve().parent / "data" / "relations.json").read_text(encoding="utf-8"))

MAIN0, MAIN1 = datetime.date(2026, 6, 20), datetime.date(2026, 9, 30)
MAIN_X0, MAIN_X1 = 230.0, 985.0
PX = (MAIN_X1 - MAIN_X0) / (MAIN1 - MAIN0).days
STUB0, STUB1 = datetime.date(2025, 11, 1), datetime.date(2025, 11, 9)
STUB_X0 = 140.0
LANE_TOP = [30, 178, 306]
ROWY = {0: [58, 88, 118, 148], 1: [210, 240, 270], 2: [332, 358, 384]}
AXIS_Y = 418
KIND = dict(DATA["kinds"])


def xpos(iso, what):
    d = datetime.date.fromisoformat(iso[:10])
    if MAIN0 <= d <= MAIN1:
        return MAIN_X0 + (d - MAIN0).days * PX
    if STUB0 <= d <= STUB1:
        return STUB_X0 + (d - STUB0).days * PX
    raise Refusal("%s: %s falls outside both stretches of the map's axis (%s to %s, %s to %s); "
                  "redraw the axis rather than clamp the date" % (what, iso, STUB0, STUB1, MAIN0, MAIN1))


def build():
    nodes = {}
    for n in DATA["nodes"]:
        name = n["name"]
        if "born" in n:
            b = facts.prose(name, n["born"]["path"], n["born"]["pattern"], num=True)
        elif name in facts.PINS["repos"]:
            b = facts.born(name)
        elif name in facts.PINS["github_only"]:
            b = facts.api_born(name)
        else:
            raise Refusal("the map names %s, which pins.json neither pins nor lists as github_only" % name)
        a = facts.agents(name) if name in facts.PINS["repos"] else facts.api_agents(name)
        note = None
        if "note" in n:
            v = facts.prose(name, n["note"]["path"], n["note"]["pattern"])
            note = n["note"]["format"] % v.text
        nodes[name] = dict(name=name, x=xpos(b.text, name), y=ROWY[n["lane"]][n["row"]], born=b, agents=a,
                           private=not facts.is_public(name), pre=a.raw.startswith("0/"),
                           trunk=n.get("trunk", False), note=note)
    edges = []
    for e in DATA["edges"]:
        for end in (e["tail"], e["head"]):
            if end not in nodes:
                raise Refusal("an edge names %s, which is not on the map" % end)
        if e["kind"] not in KIND:
            raise Refusal("an edge has kind %r, which relations.json does not define" % e["kind"])
        edges.append(dict(e, v=facts.prose(e["repo"], e["path"], e["pattern"])))
    fams = []
    for f in DATA["families"]:
        v = facts.family(f["match"], f["exclude"])
        _, first, last = v.raw.split()
        fams.append(dict(f, v=v, first=first, last=last))
    return dict(nodes=nodes, edges=edges, families=fams, now=facts.snapshot_date())


def svg(M):
    o = ['<svg viewBox="0 0 1080 440" role="img" aria-labelledby="map-t" xmlns="http://www.w3.org/2000/svg">',
         '<title id="map-t">Where each project came from: born dates across, threads down, typed relations between them</title>',
         '<defs>'
         '<marker id="ah" viewBox="0 0 8 8" refX="7.5" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto">'
         '<path class="ah" d="M0 0L8 4L0 8z"/></marker>'
         '<marker id="ah-acc" viewBox="0 0 8 8" refX="7.5" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto">'
         '<path class="ah-acc" d="M0 0L8 4L0 8z"/></marker></defs>']
    for label, top in zip(DATA["lanes"], LANE_TOP):
        o.append('<text class="lane" x="14" y="%d">%s</text>' % (top + 16, esc(label)))
    for top in LANE_TOP[1:]:
        o.append('<line class="sep" x1="14" x2="1066" y1="%d" y2="%d"/>' % (top - 4, top - 4))
    now = M["now"].text
    xn = xpos(now, "the snapshot")
    o.append('<line class="now" x1="%.1f" x2="%.1f" y1="28" y2="%d"/>' % (xn, xn, AXIS_Y))
    o.append('<text class="tick" x="%.1f" y="20" text-anchor="end">snapshot %s</text>' % (xn, esc(now)))
    xs1 = xpos(STUB1.isoformat(), "axis")
    o.append('<path class="axis" d="M%.1f %dH%.1f M%.1f %dH%.1f"/>' % (STUB_X0 - 4, AXIS_Y, xs1 + 3, MAIN_X0 - 8, AXIS_Y, MAIN_X1))
    o.append('<path class="axis" d="M%.1f %d l6 -9 M%.1f %d l6 -9"/>' % (xs1 + 6, AXIS_Y + 4, xs1 + 13, AXIS_Y + 4))
    for iso, label in (("2025-11-01", "Nov 2025"), ("2026-07-01", "Jul 2026"), ("2026-08-01", "Aug"), ("2026-09-01", "Sep")):
        x = xpos(iso, "a tick")
        o.append('<path class="axis" d="M%.1f %dv5"/><text class="tick" x="%.1f" y="%d">%s</text>' % (x, AXIS_Y, x, AXIS_Y + 17, label))
    for f in M["families"]:
        x0, x1 = xpos(f["first"], f["label"]), xpos(f["last"], f["label"])
        y = ROWY[f["lane"]][f["row"]]
        o.append('<line class="range" x1="%.1f" x2="%.1f" y1="%d" y2="%d"/>' % (x0, x1, y, y))
        o.append('<text x="%.1f" y="%.1f">%s %s<tspan class="note"> created %s to %s</tspan></text>'
                 % (x1 + 9, y + 4.5, esc(f["v"].text), esc(f["label"]), f["first"][5:], f["last"][5:]))
    N = M["nodes"]
    for e in M["edges"]:
        a, b = N[e["tail"]], N[e["head"]]
        x1, y1, x2, y2 = a["x"], a["y"], b["x"], b["y"]
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy) or 1.0
        cx, cy = (x1 + x2) / 2 - dy / ln * e["bend"], (y1 + y2) / 2 + dx / ln * e["bend"]

        def toward(px, py, qx, qy, d):
            l2 = math.hypot(qx - px, qy - py) or 1.0
            return px + (qx - px) / l2 * d, py + (qy - py) / l2 * d
        sx, sy = toward(x1, y1, cx, cy, 6)
        ex, ey = toward(x2, y2, cx, cy, 8)
        o.append('<path class="edge %s" d="M%.1f %.1fQ%.1f %.1f %.1f %.1f" marker-end="url(#%s)"><title>%s %s %s</title></path>'
                 % (e["kind"], sx, sy, cx, cy, ex, ey, "ah-acc" if e["kind"] == "grew-into" else "ah",
                    esc(e["tail"]), esc(KIND[e["kind"]]), esc(e["head"])))
    for n in N.values():
        cls = " ".join(["node"] + [k for k in ("private", "pre", "trunk") if n[k]])
        tail = '<tspan class="note"> private</tspan>' if n["private"] else ""
        if n["note"]:
            tail += '<tspan class="note"> %s</tspan>' % esc(n["note"])
        o.append('<g class="%s"><rect x="%.1f" y="%.1f" width="7" height="7"/><text x="%.1f" y="%.1f">%s%s</text></g>'
                 % (cls, n["x"] - 3.5, n["y"] - 3.5, n["x"] + 9, n["y"] + 4.5, esc(n["name"]), tail))
    o.append("</svg>")
    return "\n".join(o)


def legend():
    li = ['<li><svg width="30" height="10" aria-hidden="true"><line class="edge %s" x1="1" y1="5" x2="29" y2="5"/></svg>%s</li>'
          % (k, esc(t)) for k, t in DATA["kinds"]]
    li += ['<li><svg width="10" height="10" aria-hidden="true"><g class="node"><rect x="1.5" y="1.5" width="7" height="7"/></g></svg>public</li>',
           '<li><svg width="10" height="10" aria-hidden="true"><g class="node private"><rect x="1.5" y="1.5" width="7" height="7"/></g></svg>private for now</li>',
           '<li><svg width="10" height="10" aria-hidden="true"><g class="node pre"><rect x="1.5" y="1.5" width="7" height="7"/></g></svg>no agent-co-authored commits</li>',
           '<li><svg width="30" height="10" aria-hidden="true"><line class="range" x1="1" y1="5" x2="29" y2="5"/></svg>a family, first to last created</li>']
    return '<ul class="legend">%s</ul>' % "".join(li)


def block():
    M = build()
    ev = "".join('<li><b>%s</b> %s <b>%s</b>: %s</li>' % (esc(e["tail"]), esc(KIND[e["kind"]]), esc(e["head"]), fig(e["v"]))
                 for e in M["edges"])
    order = sorted(M["nodes"].values(), key=lambda n: (n["born"].text, n["name"]))
    pos = "".join('<li>%s: %s</li>' % (esc(n["name"]), fig(n["born"])) for n in order)
    cap = ("Across: the day each repository was born &mdash; its first commit at the pin, or the date its README "
           "states it was split out of another. Down: the three threads. Read each arrow as a sentence, tail to "
           "head; each one names the file that says so.")
    return ('<figure class="map"><div class="map-scroll">%s</div><figcaption>%s</figcaption>%s'
            '<details class="evidence"><summary>The file behind each arrow, and behind each position</summary>'
            '<ol>%s</ol><p>Positions, earliest first:</p><ul>%s</ul></details></figure>'
            % (svg(M), cap, legend(), ev, pos))
