#!/usr/bin/env python3
"""Design experiments for loganw.dev: one Home page in four visual directions.

A prototype to look at, not the site's generator. It is a program rather than
four hand-drawn pages because the alternative - sixty figures typed into each
of four mock-ups - is the defect the site exists to refuse (HonestFramework
METHOD section 4), and the conversation that produced it had corrected four
of its own facts before a line of it was written.

Every figure is read at build time from one of two places:

  * a local clone at a PINNED commit - `git show` and `git log` at that SHA,
    never the working tree, where another session may be mid-round;
  * sources/github-2026-09-29.json - the GitHub snapshot, taken once by
    snapshot_github.py and kept, for visibility and for the two repositories
    not cloned on this machine.

A figure lifted from prose names its file, its line and the pattern that
finds it; a pattern that no longer matches stops the build BY NAME (METHOD
section 2) rather than printing a stale value. What no file can back - the
biography, the owner's word on a round in progress - renders as STATED and
never as sourced (METHOD section 8).

    python build.py            # write the four pages, index.html and assets/
    python build.py --check    # exit 1 if a written file differs from a fresh render
    python build.py --control  # both negative controls; each must fail as it must

The pages load fonts from Google Fonts because they are experiments. The
site would serve its own fonts: a third-party request per visitor is the
kind of thing it says it does not do.
"""
import argparse
import dataclasses
import datetime
import hashlib
import html
import json
import math
import os
import pathlib
import re
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
REPOS = pathlib.Path(os.environ.get("LOGANW_REPOS") or HERE.parents[2])
SNAPSHOT = HERE / "sources" / "github-2026-09-29.json"
OWNER = "loganw234"

# The pins. A pin that resolved HEAD at build time would not be a pin: each is
# the commit this page's figures are read at, and the footer names every one.
PINS = {
    # name on GitHub          directory under REPOS       commit
    "PrettyCloud":           ("PrettyCloud",             "5161daa"),
    "atlas-darkroom":        ("atlas-darkroom",          "6a33735"),
    "atlas-optical":         ("atlas-optical",           "dbccafe"),
    "atlas-film":            ("atlas-film",              "be1d674"),
    "atlas-engine":          ("atlas-engine",            "867c57a"),
    "cft-fp256":             ("cft-fp256",               "77b8440"),
    "cft-rebound":           ("cft-rebound",             "039e3c3"),
    "ParcelRound":           ("ParcelRound",             "8767e23"),
    "HonestFramework":       ("HonestFramework",         "65447fd"),
    "Quantum-Film":          ("moth-quantum",            "a7f02db"),
    "Mercenaries2":          ("Merc2Reborn",             "e51dcbe"),
    "Merc2-Mods-Exp":        ("Merc2-Mods-Exp",          "0ec1db2"),
    "mercs2-lua-essentials": ("mercs2-lua-essentials",   "3430c0b"),
}


class Refusal(Exception):
    """A figure that cannot be read from its source. Never rendered around."""


@dataclasses.dataclass(frozen=True)
class Src:
    kind: str           # file | git | api | stated
    short: str          # where, in one line
    detail: str = ""    # what was read there, or the quoted text
    href: str = ""      # where a reader can check it, if it is public

    def text(self):
        return self.short + (" - " + self.detail if self.detail else "")


@dataclasses.dataclass(frozen=True)
class V:                # a figure, and the source it was read from
    text: str
    src: Src
    raw: str = ""
    num: bool = False   # set in mono only if it is a number, a date or a hash


@dataclasses.dataclass(frozen=True)
class C:                # code
    text: str


@dataclasses.dataclass(frozen=True)
class L:                # a link around a string or a figure
    href: str
    inner: object


def esc(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------------------
# Sources: the snapshot and the pinned clones
# ---------------------------------------------------------------------------

_SNAP = {}


def snap():
    if not _SNAP:
        if not SNAPSHOT.is_file():
            raise Refusal("%s is missing; run snapshot_github.py" % SNAPSHOT.name)
        s = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        s["by_name"] = {r["name"]: r for r in s["repos"]}
        _SNAP.update(s)
    return _SNAP


def repo_meta(name):
    r = snap()["by_name"].get(name)
    if r is None:
        raise Refusal("%s is not in %s" % (name, SNAPSHOT.name))
    return r


def is_public(name):
    return repo_meta(name)["visibility"] == "PUBLIC"


def api_src(name, detail):
    return Src("api", "GitHub snapshot %s" % snap()["taken"][:10],
               "%s: %s" % (name, detail), repo_meta(name)["url"])


class Pin:
    def __init__(self, name):
        if name not in PINS:
            raise Refusal("%s has no pin" % name)
        d, want = PINS[name]
        self.name, self.dir, self.short = name, REPOS / d, want
        if not (self.dir / ".git").exists():
            raise Refusal("%s: no clone at %s" % (name, self.dir))
        self.full = self.git("rev-parse", "--verify", "--quiet", want + "^{commit}").strip()

    def git(self, *args, binary=False):
        r = subprocess.run(["git", "-C", str(self.dir), *args], capture_output=True)
        if r.returncode != 0:
            msg = r.stderr.decode("utf-8", "replace").strip() or "exit %d" % r.returncode
            raise Refusal("%s: git %s: %s" % (self.name, " ".join(args), msg))
        return r.stdout if binary else r.stdout.decode("utf-8", "replace")

    def show(self, path, binary=False):
        return self.git("show", "%s:%s" % (self.full, path), binary=binary)

    def href(self, path="", line=0, tree=False):
        if not is_public(self.name):
            return ""
        u = "https://github.com/%s/%s/%s/%s" % (OWNER, self.name,
                                               "tree" if (tree or not path) else "blob", self.full)
        if path:
            u += "/" + path
        if line:
            u += "#L%d" % line
        return u


_PIN = {}


def pin(name):
    if name not in _PIN:
        _PIN[name] = Pin(name)
    return _PIN[name]


# ---------------------------------------------------------------------------
# Facts. Each returns a V or refuses by name.
# ---------------------------------------------------------------------------

def md_plain(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    return " ".join(s.replace("**", "").replace("`", "").split())


def _line(text, pos):
    return text.count("\n", 0, pos) + 1


def prose(name, path, pattern, display=None, last=False, num=False):
    """A figure lifted from a sentence: the file, the line, and the words."""
    p = pin(name)
    text = p.show(path)
    ms = list(re.finditer(pattern, text, re.M))
    if not ms:
        raise Refusal("%s %s %s: the pattern %r no longer matches" % (name, p.short, path, pattern))
    m = ms[-1] if last else ms[0]
    line = _line(text, m.start(1))
    quoted = md_plain(m.group(1))
    detail = "“%s”" % quoted if display is not None else ""
    if last and len(ms) > 1:
        detail = (detail + " " if detail else "") + "(the last of %d matches)" % len(ms)
    return V(display if display is not None else quoted,
             Src("file", "%s %s %s:%d" % (name, p.short, path, line), detail, p.href(path, line)),
             raw=quoted, num=num)


def abi():
    """Derived, not quoted: the header's own macros are the definition."""
    p = pin("cft-fp256")
    t = p.show("host/include/cft.h")
    ma = re.search(r"^#define CFT_ABI_VERSION_MAJOR (\d+)", t, re.M)
    mi = re.search(r"^#define CFT_ABI_VERSION_MINOR (\d+)", t, re.M)
    if not (ma and mi):
        raise Refusal("cft-fp256 %s host/include/cft.h: the ABI macros are gone" % p.short)
    line = _line(t, ma.start())
    return V("%s.%s" % (ma.group(1), mi.group(1)),
             Src("file", "cft-fp256 %s host/include/cft.h:%d" % (p.short, line),
                 "CFT_ABI_VERSION_MAJOR and _MINOR", p.href("host/include/cft.h", line)), num=True)


def born_first(name):
    p = pin(name)
    dates = p.git("log", p.full, "--format=%ad", "--date=short").split()
    if not dates:
        raise Refusal("%s %s: no commits" % (name, p.short))
    return V(min(dates), Src("git", "%s %s git log" % (name, p.short),
                             "the earliest author date of %d commits" % len(dates), p.href()), num=True)


def agents(name):
    """-> (V "agent/total", agent count). The trailer is the measure, and it
    says nothing about commits an agent helped with and was not credited on."""
    p = pin(name)
    out = p.git("log", p.full, "--format=%x1e%(trailers:key=Co-Authored-By,valueonly)")
    recs = out.split("\x1e")[1:]
    ai = sum(1 for r in recs if re.search(r"claude|gemini", r, re.I))
    return V("%d/%d" % (ai, len(recs)),
             Src("git", "%s %s git log" % (name, p.short),
                 "commits with a Claude or Gemini Co-Authored-By trailer, of all commits",
                 p.href()), num=True), ai


def api_first(name):
    c = snap()["not_cloned"][name]
    return V(c["first"], api_src(name, "the earliest of %d commits" % c["total"]), num=True)


def api_agents(name):
    c = snap()["not_cloned"][name]
    return V("%d/%d" % (c["agent_coauthored"], c["total"]),
             api_src(name, "commits with a Claude or Gemini Co-Authored-By trailer, of all commits"),
             num=True), \
        c["agent_coauthored"]


def api_desc(name):
    return V(repo_meta(name)["description"], api_src(name, "its description"))


def has(name, path):
    p = pin(name)
    r = subprocess.run(["git", "-C", str(p.dir), "cat-file", "-e", "%s:%s" % (p.full, path)],
                       capture_output=True)
    return r.returncode == 0


def exists(name, path, display=None):
    p = pin(name)
    if not has(name, path):
        raise Refusal("%s %s has no %s" % (name, p.short, path))
    return V(display or path, Src("git", "%s %s" % (name, p.short),
                                  "%s exists at the pin" % path, p.href(path)))


def ledger(name, path="docs/VALIDATION.md"):
    """The newest entry's date: its heading's, or - where the newest heading
    is numbered rather than dated - the first date in that entry's body."""
    p = pin(name)
    if not has(name, path):
        return V("—", Src("git", "%s %s" % (name, p.short), "no %s at the pin" % path, p.href()), num=True)
    t = p.show(path)
    heads = list(re.finditer(r"^## (.+)$", t, re.M))
    if not heads:
        raise Refusal("%s %s %s: no entry headings" % (name, p.short, path))
    h = heads[-1]
    title = h.group(1)
    line = _line(t, h.start())
    m = re.match(r"(\d{4}-\d{2}-\d{2})\b", title)
    if m:
        date, how = m.group(1), "the newest of %d headings, dated" % len(heads)
    elif re.match(r"\d+\.", title):
        d = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", t[h.start():])
        if not d:
            raise Refusal("%s %s %s:%d: a numbered entry with no date in it" % (name, p.short, path, line))
        date = d.group(1)
        how = ("the newest of %d headings is numbered (%s), so the first date in its body"
               % (len(heads), title.split(".")[0]))
    else:
        raise Refusal("%s %s %s:%d: the newest heading is neither dated nor numbered: %r"
                      % (name, p.short, path, line, title[:60]))
    return V(date, Src("file", "%s %s %s:%d" % (name, p.short, path, line), how, p.href(path, line)), num=True)


def stages(name, path="verify/run.sh"):
    p = pin(name)
    n = len(re.findall(r'^stage [a-z0-9-]+ "', p.show(path), re.M))
    if not n:
        raise Refusal("%s %s %s: no stage lines" % (name, p.short, path))
    return V(str(n), Src("file", "%s %s %s" % (name, p.short, path), "its stage lines, counted",
                         p.href(path)), num=True)


def last_change(name, path):
    p = pin(name)
    d = p.git("log", "-1", "--format=%ad", "--date=short", p.full, "--", path).strip()
    if not d:
        raise Refusal("%s %s: nothing ever touched %s" % (name, p.short, path))
    return V(d, Src("git", "%s %s git log -- %s" % (name, p.short, path),
                    "the last commit touching it", p.href(path)), num=True)


def count_paths(name, pattern, what):
    p = pin(name)
    n = sum(1 for f in p.git("ls-tree", "-r", "--name-only", p.full).splitlines()
            if re.fullmatch(pattern, f))
    if not n:
        raise Refusal("%s %s: no path matches %r" % (name, p.short, pattern))
    return V(str(n), Src("git", "%s %s ls-tree" % (name, p.short), what, p.href()), num=True)


def stated(text, detail="by Logan, 2026-09-29; no file backs it"):
    return V(text, Src("stated", "stated", detail))


def private_pair(a, b):
    for n in (a, b):
        if is_public(n):
            raise Refusal("%s is public in the snapshot; the sentence calling it private is false" % n)
    return V("private", Src("api", "GitHub snapshot %s" % snap()["taken"][:10],
                            "%s and %s: visibility PRIVATE" % (a, b)))


def mercs2_tools():
    rs = [r for r in snap()["repos"]
          if r["visibility"] == "PUBLIC" and r["name"] != "Merc2-Mods-Exp"
          and re.match(r"(mercs2-|merc2-|wad-simulator)", r["name"], re.I)]
    if not rs:
        raise Refusal("the snapshot lists no mercs2 tools")
    first = min(r["createdAt"][:10] for r in rs)
    last = max(r["createdAt"][:10] for r in rs)
    src = Src("api", "GitHub snapshot %s" % snap()["taken"][:10],
              "public repositories named mercs2-*, merc2-* or wad-simulator*, other than "
              "Merc2-Mods-Exp; created %s to %s" % (first, last))
    return V(str(len(rs)), src, num=True), first, last


# ---------------------------------------------------------------------------
# The map: position is a date, and every line cites a file
# ---------------------------------------------------------------------------

MAIN0, MAIN1 = datetime.date(2026, 6, 20), datetime.date(2026, 9, 30)
MAIN_X0, MAIN_X1 = 230.0, 985.0
PX = (MAIN_X1 - MAIN_X0) / (MAIN1 - MAIN0).days
STUB0, STUB1 = datetime.date(2025, 11, 1), datetime.date(2025, 11, 9)
STUB_X0 = 140.0

LANES = [("DETERMINISM", 30), ("FILM & PHOTOGRAPHY", 178), ("PRESERVATION", 306)]
ROWY = {0: [58, 88, 118, 148], 1: [210, 240, 270], 2: [332, 358, 384]}
AXIS_Y = 418

NODES = [
    # name, lane, row, born: None = the first commit at the pin (or in the
    # snapshot, if not cloned here); otherwise (file, pattern) for a stated date
    ("PrettyCloud", 0, 1, None),
    ("atlas-engine", 0, 0, None),
    ("cft-fp256", 0, 2, None),
    ("cft-rebound", 0, 1, None),
    ("ParcelRound", 0, 0, None),
    ("HonestFramework", 0, 3, None),
    ("CanonBracketTool", 1, 0, None),
    ("Microscope-Stacker", 1, 2, None),
    ("atlas-darkroom", 1, 0, None),
    ("atlas-optical", 1, 1, ("README.md", r"Extracted whole from\s+atlas-darkroom on (\d{4}-\d{2}-\d{2})")),
    ("atlas-film", 1, 2, ("README.md", r"Born (\d{4}-\d{2}-\d{2}) by extraction")),
    ("Quantum-Film", 1, 0, None),
    ("Mercenaries2", 2, 0, None),
    ("Merc2-Mods-Exp", 2, 1, None),
]

# Read each as a sentence: tail, relation, head.
KINDS = [
    ("grew-into", "grew into"),
    ("extracted", "spun out"),
    ("built-on", "underlies"),
    ("ports", "hosts a port of"),
    ("verified-by", "verifies"),
    ("distilled-from", "was distilled into"),
]
KIND = dict(KINDS)

EDGES = [
    # tail, head, kind, (repository, file, pattern), bend
    ("PrettyCloud", "atlas-darkroom", "grew-into",
     ("atlas-darkroom", "README.md",
      r"^(A print engine for the \[Atlas of Mathematical Forms\]\(https://github\.com/loganw234/PrettyCloud\))"), 0),
    ("PrettyCloud", "atlas-engine", "grew-into",
     ("atlas-engine", "README.md", r"(Sixty-eight plates in PrettyCloud)"), 0),
    ("atlas-engine", "cft-fp256", "grew-into",
     ("cft-fp256", "README.md", r"(The workload this tile exists to serve is\s+\[atlas-engine\])"), -16),
    ("atlas-engine", "cft-fp256", "verified-by",
     ("cft-fp256", "README.md", r"(A GPU agrees, bit for bit, on a real workload)"), 16),
    ("atlas-engine", "atlas-darkroom", "built-on",
     ("atlas-darkroom", "README.md", r"(presentation from PrettyCloud, shape from atlas-engine)"), 0),
    ("atlas-darkroom", "atlas-optical", "extracted",
     ("atlas-optical", "README.md", r"(Extracted whole from\s+atlas-darkroom on \d{4}-\d{2}-\d{2})"), 0),
    ("atlas-darkroom", "atlas-film", "extracted",
     ("atlas-film", "README.md", r"(Born \d{4}-\d{2}-\d{2} by extraction from the darkroom's develop monolith)"), 0),
    ("cft-fp256", "cft-rebound", "built-on",
     ("cft-rebound", "README.md", r"^(REBOUND's IAS15 integrator with its arithmetic routed through libcft)"), 0),
    ("cft-fp256", "Quantum-Film", "built-on",
     ("Quantum-Film", ".gitmodules", r"path = (vendor/cft-fp256)"), 0),
    ("atlas-film", "Quantum-Film", "built-on",
     ("Quantum-Film", ".gitmodules", r"path = (vendor/atlas-film)"), 0),
    ("cft-fp256", "atlas-film", "ports",
     ("ParcelRound", "CASE-STUDY-4.md", r"(P2 moves atlas-film)"), 66),
    ("cft-rebound", "ParcelRound", "distilled-from",
     ("cft-rebound", "docs/PARCEL-ROUNDS.md", r"(lifted into a standalone repository)"), 0),
    ("cft-fp256", "HonestFramework", "distilled-from",
     ("HonestFramework", "CASE-STUDY.md", r"^\| `(cft-fp256)` \|"), 0),
    ("Mercenaries2", "Merc2-Mods-Exp", "grew-into",
     ("Mercenaries2", "README.md", r"visit \[(Merc2-Mods-Exp)\]"), 0),
]

LABEL_NOTES = {  # a figure hung on a node's label
    "Mercenaries2": ("Mercenaries2", "README.md", r"The public server at `(refesl\.live)`", "server %s"),
}


def xpos(iso, what):
    d = datetime.date.fromisoformat(iso)
    if MAIN0 <= d <= MAIN1:
        return MAIN_X0 + (d - MAIN0).days * PX
    if STUB0 <= d <= STUB1:
        return STUB_X0 + (d - STUB0).days * PX
    raise Refusal("%s: %s falls outside both stretches of the map's axis (%s to %s, %s to %s); "
                  "redraw the axis rather than clamp the date" % (what, iso, STUB0, STUB1, MAIN0, MAIN1))


def build_map():
    nodes = {}
    for name, lane, row, born in NODES:
        cloned = name in PINS
        if born:
            bv = prose(name, born[0], born[1])
        else:
            bv = born_first(name) if cloned else api_first(name)
        _, ai = agents(name) if cloned else api_agents(name)
        note = None
        if name in LABEL_NOTES:
            r, f, pat, fmt = LABEL_NOTES[name]
            v = prose(r, f, pat)
            note = V(fmt % v.text, v.src, raw=v.raw)
        nodes[name] = dict(name=name, lane=lane, x=xpos(bv.text, name), y=ROWY[lane][row], born=bv,
                           private=not is_public(name), pre=(ai == 0), trunk=(name == "cft-fp256"),
                           note=note)
    edges = []
    for a, b, kind, (r, f, pat), bend in EDGES:
        for n in (a, b):
            if n not in nodes:
                raise Refusal("an edge names %s, which is not on the map" % n)
        edges.append(dict(a=a, b=b, kind=kind, v=prose(r, f, pat), bend=bend))
    tools, t0, t1 = mercs2_tools()
    return dict(nodes=nodes, edges=edges, tools=tools, t0=t0, t1=t1, now=snap()["taken"][:10])


def map_svg(M):
    o = ['<svg viewBox="0 0 1080 440" role="img" aria-labelledby="map-t" xmlns="http://www.w3.org/2000/svg">',
         '<title id="map-t">Where each project came from: born dates across, threads down, typed relations between them</title>',
         '<defs>'
         '<marker id="ah" viewBox="0 0 8 8" refX="7.5" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto">'
         '<path class="ah" d="M0 0L8 4L0 8z"/></marker>'
         '<marker id="ah-acc" viewBox="0 0 8 8" refX="7.5" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto">'
         '<path class="ah-acc" d="M0 0L8 4L0 8z"/></marker></defs>']
    for label, top in LANES:
        o.append('<text class="lane" x="14" y="%d">%s</text>' % (top + 16, esc(label)))
    for _, top in LANES[1:]:
        o.append('<line class="sep" x1="14" x2="1066" y1="%d" y2="%d"/>' % (top - 4, top - 4))
    xn = xpos(M["now"], "the snapshot")
    o.append('<line class="now" x1="%.1f" x2="%.1f" y1="28" y2="%d"/>' % (xn, xn, AXIS_Y))
    o.append('<text class="tick" x="%.1f" y="20" text-anchor="end">snapshot %s</text>' % (xn, M["now"]))
    xs1 = xpos(STUB1.isoformat(), "axis")
    o.append('<path class="axis" d="M%.1f %dH%.1f M%.1f %dH%.1f"/>'
             % (STUB_X0 - 4, AXIS_Y, xs1 + 3, MAIN_X0 - 8, AXIS_Y, MAIN_X1))
    o.append('<path class="axis" d="M%.1f %d l6 -9 M%.1f %d l6 -9"/>'
             % (xs1 + 6, AXIS_Y + 4, xs1 + 13, AXIS_Y + 4))
    for iso, label in (("2025-11-01", "Nov 2025"), ("2026-07-01", "Jul 2026"),
                       ("2026-08-01", "Aug"), ("2026-09-01", "Sep")):
        x = xpos(iso, "a tick")
        o.append('<path class="axis" d="M%.1f %dv5"/><text class="tick" x="%.1f" y="%d">%s</text>'
                 % (x, AXIS_Y, x, AXIS_Y + 17, label))
    # the family of tools, first to last created
    x0, x1 = xpos(M["t0"], "the first mercs2 tool"), xpos(M["t1"], "the last mercs2 tool")
    y = ROWY[2][2]
    o.append('<line class="range" x1="%.1f" x2="%.1f" y1="%d" y2="%d"/>' % (x0, x1, y, y))
    o.append('<text x="%.1f" y="%.1f">%s mercs2 tools<tspan class="note"> created %s to %s</tspan></text>'
             % (x1 + 9, y + 4.5, esc(M["tools"].text), M["t0"][5:], M["t1"][5:]))
    N = M["nodes"]
    for e in M["edges"]:
        a, b = N[e["a"]], N[e["b"]]
        x1_, y1_, x2_, y2_ = a["x"], a["y"], b["x"], b["y"]
        mx, my = (x1_ + x2_) / 2, (y1_ + y2_) / 2
        dx, dy = x2_ - x1_, y2_ - y1_
        ln = math.hypot(dx, dy) or 1.0
        cx, cy = mx - dy / ln * e["bend"], my + dx / ln * e["bend"]

        def toward(px, py, qx, qy, d):
            l2 = math.hypot(qx - px, qy - py) or 1.0
            return px + (qx - px) / l2 * d, py + (qy - py) / l2 * d
        sx, sy = toward(x1_, y1_, cx, cy, 6)
        ex, ey = toward(x2_, y2_, cx, cy, 8)
        o.append('<path class="edge %s" d="M%.1f %.1fQ%.1f %.1f %.1f %.1f" marker-end="url(#%s)"><title>%s %s %s</title></path>'
                 % (e["kind"], sx, sy, cx, cy, ex, ey,
                    "ah-acc" if e["kind"] == "grew-into" else "ah",
                    esc(e["a"]), esc(KIND[e["kind"]]), esc(e["b"])))
    for n in N.values():
        cls = " ".join(["node"] + [k for k in ("private", "pre", "trunk") if n[k]])
        end = False  # every label sits right of its square; the canvas is wide enough
        tx = n["x"] - 9 if end else n["x"] + 9
        tail = ""
        if n["private"]:
            tail += '<tspan class="note"> private</tspan>'
        if n["note"]:
            tail += '<tspan class="note"> %s</tspan>' % esc(n["note"].text)
        o.append('<g class="%s"><rect x="%.1f" y="%.1f" width="7" height="7"/>'
                 '<text x="%.1f" y="%.1f"%s>%s%s</text></g>'
                 % (cls, n["x"] - 3.5, n["y"] - 3.5, tx, n["y"] + 4.5,
                    ' text-anchor="end"' if end else "", esc(n["name"]), tail))
    o.append("</svg>")
    return "\n".join(o)


def legend_html():
    li = ['<li><svg width="30" height="10" aria-hidden="true"><line class="edge %s" x1="1" y1="5" x2="29" y2="5"/></svg>%s</li>'
          % (k, esc(t)) for k, t in KINDS]
    li += ['<li><svg width="10" height="10" aria-hidden="true"><g class="node"><rect x="1.5" y="1.5" width="7" height="7"/></g></svg>public</li>',
           '<li><svg width="10" height="10" aria-hidden="true"><g class="node private"><rect x="1.5" y="1.5" width="7" height="7"/></g></svg>private</li>',
           '<li><svg width="10" height="10" aria-hidden="true"><g class="node pre"><rect x="1.5" y="1.5" width="7" height="7"/></g></svg>no agent-co-authored commits</li>',
           '<li><svg width="30" height="10" aria-hidden="true"><line class="range" x1="1" y1="5" x2="29" y2="5"/></svg>a family, first to last created</li>']
    return '<ul class="legend">%s</ul>' % "".join(li)


def src_html(v):
    s = v.src
    where = '<a href="%s">%s</a>' % (esc(s.href), esc(s.short)) if s.href else esc(s.short)
    said = s.detail if s.detail else "“%s”" % v.text
    return '<span class="where">%s</span> %s' % (where, esc(said))


def blk_map(D):
    M = D["map"]
    ev = "".join('<li><b>%s</b> %s <b>%s</b>: %s</li>' % (esc(e["a"]), esc(KIND[e["kind"]]), esc(e["b"]), src_html(e["v"]))
                 for e in M["edges"])
    order = sorted(M["nodes"].values(), key=lambda n: (n["born"].text, n["name"]))
    pos = "".join('<li>%s <span class="fig">%s</span>: %s</li>' % (esc(n["name"]), esc(n["born"].text), src_html(n["born"]))
                  for n in order)
    cap = ("Across: the day each repository was born &mdash; its first commit at the pin, or the "
           "extraction date its README states. Down: the three threads. Read each arrow as a "
           "sentence, tail to head; each one names the file that says so.")
    return ('<figure class="map"><div class="map-scroll">%s</div><figcaption>%s</figcaption>%s'
            '<details class="evidence"><summary>The file behind each arrow, and behind each position</summary>'
            '<ol>%s</ol><p>Positions, earliest first:</p><ul>%s</ul></details></figure>'
            % (map_svg(M), cap, legend_html(), ev, pos))


# ---------------------------------------------------------------------------
# The content: every sentence either carries a source or says it is stated
# ---------------------------------------------------------------------------

PRINTS = [("pauli-print.png", "Pauli"), ("poisson-print.png", "Poisson"), ("trix-print.png", "TRI-X")]


def gather():
    D = {}
    D["who"] = [stated(
        "I'm Logan. I have worked as a carpenter since I was fifteen, and I have no formal "
        "training in computing. From PrettyCloud on, AI agents have written essentially all "
        "of the code; gates decide what is true, and the record keeps what they said.")]
    D["map"] = build_map()

    rows = []

    def row(thread, name, what, state, check, last=None, agent=None):
        cloned = name in PINS
        url = repo_meta(name)["url"]
        rows.append(dict(
            thread=thread,
            project=L(url, name) if is_public(name) else name,
            what=what, state=state,
            last=last if last is not None else (ledger(name) if cloned else V(
                "—", api_src(name, "no docs/VALIDATION.md on its default branch")
                if not snap()["not_cloned"][name]["files"]["docs/VALIDATION.md"]
                else api_src(name, "has a ledger this build does not read"), num=True)),
            agent=agent if agent is not None else (agents(name)[0] if cloned else api_agents(name)[0]),
            check=check))

    T = "Determinism"
    row(T, "PrettyCloud",
        [prose("PrettyCloud", "README.md", r"^(A WebGL2 point-cloud atlas)\.")],
        ["served at ", prose("PrettyCloud", "README.md", r"served at (prettycloud\.io)")],
        [L("https://prettycloud.io/", "open it")])
    row(T, "atlas-engine",
        [prose("atlas-engine", "README.md", r"^(A language for platonography),")],
        [prose("atlas-engine", "README.md", r"\*\*(Sixty-eight of sixty-eight, one hash)\.\*\*")],
        ["cft-fp256's ", C("photograph"), " stage, ",
         prose("cft-fp256", "README.md", r"`photograph`\s+stage reruns it in (a minute and a half)")])
    row(T, "cft-fp256",
        [prose("cft-fp256", "README.md", r"^\*\*(A math coprocessor that gets the same answer everywhere)\.\*\*")],
        ["ABI ", abi(), " on main; ", stated("a revision-7 round is under way off main")],
        [C("make verify-quick"), ", ",
         prose("cft-fp256", "CLAUDE.md", r"^make verify-quick\s+# (~\d+ min, \d+ of \d+ stages)", num=True)])
    row(T, "cft-rebound",
        [prose("cft-rebound", "README.md", r"^(REBOUND's IAS15 integrator with its arithmetic routed through libcft)")],
        [prose("cft-rebound", "README.md", r"(At binary64 it is\s+REBOUND's own IAS15 bit for bit)")],
        [C("make check-quick"), ", ",
         prose("cft-fp256", "CLAUDE.md", r"the (\d+-second warm)\s+`make check-quick`")])
    row(T, "ParcelRound",
        [prose("ParcelRound", "README.md",
               r"^(A method for splitting one body of work across several coding agents\s+at\s+once)")],
        [count_paths("ParcelRound", r"CASE-STUDY(-\d+)?\.md", "CASE-STUDY*.md files at the pin"),
         " rounds recorded; METHOD.md last changed ", last_change("ParcelRound", "METHOD.md")],
        [L(pin("ParcelRound").href("CASE-STUDY-4.md"), "case study 4")],
        last=V("—", Src("git", "ParcelRound %s" % pin("ParcelRound").short,
                             "no docs/VALIDATION.md; its case studies are its record"), num=True))
    row(T, "HonestFramework",
        [prose("HonestFramework", "README.md",
               r"^(A way to lay out a project so that an AI can write nearly all of it\s+and\s+"
               r"\*\*no claim about it ever rests on the AI's judgement\*\*)")],
        [prose("HonestFramework", "README.md", r"The (\w+) mechanisms\. Start here"),
         " mechanisms, and a gate of its own"],
        [C("python " + exists("HonestFramework", "tools/check_claims.py").text)])
    T = "Film & photography"
    for name in ("CanonBracketTool", "Microscope-Stacker"):
        row(T, name, [api_desc(name)], [stated("a beginning project, from before the method")],
            [L(repo_meta(name)["url"], "repository")])
    row(T, "atlas-darkroom",
        [prose("atlas-darkroom", "README.md",
               r"^(A print engine for the \[Atlas of Mathematical Forms\]\(https://github\.com/loganw234/PrettyCloud\))")],
        [private_pair("atlas-darkroom", "atlas-optical")], ["—"])
    row(T, "atlas-optical",
        [prose("atlas-optical", "README.md", r"^(The glass of the Eidograph, on its own)")],
        ["spun out of atlas-darkroom ",
         prose("atlas-optical", "README.md", r"Extracted whole from\s+atlas-darkroom on (\d{4}-\d{2}-\d{2})",
               num=True)],
        ["—"])
    row(T, "atlas-film",
        [prose("atlas-film", "README.md", r"^(The medium of the Eidograph)")],
        ["branch ", C("pinned"), " at ",
         prose("ParcelRound", "CASE-STUDY-4.md", r"\*\*atlas-film's `pinned`\*\* at `([0-9a-f]{7})`", num=True),
         ", ", prose("ParcelRound", "CASE-STUDY-4.md", r"(Whether atlas-film's `pinned` merges into its main)",
                     display="its merge left open")],
        [L(pin("atlas-film").href("PROVENANCE.md"), exists("atlas-film", "PROVENANCE.md"))])
    qf_url = prose("Quantum-Film", "README.md", r"(https://loganw234\.github\.io/Quantum-Film/)")
    row(T, "Quantum-Film",
        [prose("Quantum-Film", "README.md", r"^\*\*(Film stocks whose crystals are laid by quantum circuits)")],
        [stages("Quantum-Film"), " runner stages; its ledger's last recorded run: ",
         prose("Quantum-Film", "docs/VALIDATION.md",
               r"`run\.sh --require-all`(?: \(run [^)]+\))?:? (\d+) passed", last=True, num=True), " passed"],
        [L(qf_url.raw, V("the web demo", qf_url.src))])
    T = "Preservation"
    row(T, "Mercenaries2",
        [prose("Mercenaries2", "README.md", r"^(A revival project for \*\*Mercenaries 2: World in Flames\*\*)")],
        ["online play through ", prose("Mercenaries2", "README.md", r"The public server at `(refesl\.live)`")],
        [L(pin("Mercenaries2").href("README.md"), "README")])
    tools = D["map"]["tools"]
    row(T, "mercs2-lua-essentials",
        [C("Ess"), ", ", prose("mercs2-lua-essentials", "README.md",
                                r"^`Ess` — (the foundational Lua library for Mercenaries 2 modding)")],
        ["one of ", tools, " public mercs2 tools"],
        [L(repo_meta("mercs2-lua-essentials")["url"], "repository")])
    D["rows"] = rows

    url = prose("cft-fp256", "README.md", r"\*\*<(https://loganw234\.github\.io/cft-fp256/)>\*\*")
    D["checks"] = [
        [L(url.raw, V("Replay the published conformance vectors", url.src)), " in your browser. Nothing to install."],
        [C("make golden"), " in a clone: ",
         prose("cft-fp256", "README.md", r"^(The golden model's self-tests)", display="the golden model's self-tests"), "."],
        [C("make verify-quick"), ": ",
         prose("cft-fp256", "CLAUDE.md", r"^make verify-quick\s+# (~\d+ min, \d+ of \d+ stages)", num=True), "."],
    ]
    D["nothere"] = [
        [C("atlas-darkroom"), " and ", C("atlas-optical"), " are ", private_pair("atlas-darkroom", "atlas-optical"),
         ". HonestFramework's case study ",
         prose("HonestFramework", "CASE-STUDY.md", r"^\| `(atlas-optical)` \|", display="cites both"),
         ", so those citations cannot be checked from here."],
        [stated("Nothing here is for sale, and there is no newsletter.")],
    ]
    # darkroom's row must exist too, or "cites both" is half true
    prose("HonestFramework", "CASE-STUDY.md", r"^\| `(atlas-darkroom)` \|")

    q = pin("Quantum-Film")
    files = []
    for f, alt in PRINTS:
        data = q.show("docs/prints/" + f, binary=True)
        files.append((f, alt, data, hashlib.sha256(data).hexdigest()))
    D["prints"] = dict(files=files,
                       caption=prose("Quantum-Film", "README.md", r"(Pauli, its Poisson twin and TRI-X) below"),
                       again=prose("ParcelRound", "CASE-STUDY-4.md",
                                   r"(Every print re-developed to the same bits) \(`--check`\)"))
    D["pins"] = [(n, pin(n)) for n in PINS]
    D["snapshot"] = snap()["taken"]
    return D


# ---------------------------------------------------------------------------
# Rendering: one content, four ways of showing where a figure came from
# ---------------------------------------------------------------------------

class Prov:
    """footnote: numbered, collected at the end.   sidenote: numbered, in the margin.
    title: on hover, and a source line per panel.  inline: printed after the figure."""

    def __init__(self, mode, wbr=False):
        self.mode, self.notes, self.num, self.scope = mode, [], {}, []
        self.wbr = wbr   # offer a line break after each "/" in a printed source path

    def n(self, s):
        k = (s.kind, s.short, s.detail)
        if k not in self.num:
            self.notes.append(s)
            self.num[k] = len(self.notes)
        self.scope.append(s)
        return self.num[k]

    def mark(self):
        self.scope = []
        return len(self.notes)

    def new_since(self, m):
        return [(i + 1, s) for i, s in enumerate(self.notes[m:], start=m)]

    def used(self):
        seen, out = set(), []
        for s in self.scope:
            if s.short not in seen:
                seen.add(s.short)
                out.append(s)
        return out

    def fig(self, v, href=None):
        s = v.src
        k = "stated" if s.kind == "stated" else ("fig" if v.num else "q")
        t = esc(v.text)
        if href:
            t = '<a href="%s">%s</a>' % (esc(href), t)
        if self.mode == "footnote":
            n = self.n(s)
            return '<span class="%s">%s</span><sup class="fn"><a href="#n%d">%d</a></sup>' % (k, t, n, n)
        if self.mode == "sidenote":
            n = self.n(s)
            return '<span class="%s">%s</span><sup class="sn">%d</sup>' % (k, t, n)
        if self.mode == "title":
            self.n(s)
            tag = '<span class="tag">stated</span>' if s.kind == "stated" else ""
            return '<span class="%s" title="%s">%s</span>%s' % (k, esc(s.text()), t, tag)
        self.n(s)
        label = esc("(stated)" if s.kind == "stated" else "(%s)" % s.short)
        if self.wbr:
            label = label.replace("/", "/<wbr>")
        return '<span class="%s">%s</span><span class="src"> %s</span>' % (k, t, label)


def render(segs, prov):
    if not isinstance(segs, list):
        segs = [segs]
    out = []
    for s in segs:
        if isinstance(s, str):
            out.append(esc(s))
        elif isinstance(s, V):
            out.append(prov.fig(s))
        elif isinstance(s, C):
            out.append("<code>%s</code>" % esc(s.text))
        elif isinstance(s, L):
            if isinstance(s.inner, V):
                out.append(prov.fig(s.inner, href=s.href))
            else:
                out.append('<a href="%s">%s</a>' % (esc(s.href), render(s.inner, prov)))
        else:
            raise TypeError(s)
    return "".join(out)


def note_li(n, s):
    body = esc(s.text())
    if s.href:
        body = '<a href="%s">%s</a>' % (esc(s.href), body)
    return '<li id="n%d"><span class="k">%d</span>%s</li>' % (n, n, body)


NAV = ["Home", "Threads", "Work", "Method", "Record", "Verify", "Corrections", "Propose", "About"]


def nav():
    return "".join('<a class="here" href="#">Home</a>' if n == "Home"
                   else '<span title="not built yet">%s</span>' % n for n in NAV)


LEDGER_CAP = ("Each row is read from the repository it names, at the commit in the footer. "
              "<i>Last entry</i>: the newest entry in its <code>docs/VALIDATION.md</code>; a dash "
              "means it keeps none. <i>Agent-written</i>: commits carrying a Claude or Gemini "
              "Co-Authored-By trailer, of all its commits &mdash; a trailer, not a line count.")


def blk_ledger(D, prov):
    head = ("<thead><tr><th>project</th><th>what it is</th><th>state</th><th>last entry</th>"
            "<th class=\"n\">agent-written</th><th>check it</th></tr></thead>")
    body, thread = [], None
    for r in D["rows"]:
        if r["thread"] != thread:
            thread = r["thread"]
            body.append('<tr class="th"><td colspan="6">%s</td></tr>' % esc(thread))
        body.append('<tr><td class="p">%s</td><td>%s</td><td>%s</td><td class="d">%s</td>'
                    '<td class="n">%s</td><td>%s</td></tr>'
                    % tuple(render(r[k], prov) for k in ("project", "what", "state", "last", "agent", "check")))
    return "<table>%s<tbody>%s</tbody></table>" % (head, "".join(body))


def blk_checks(D, prov):
    return "<ol>%s</ol>" % "".join("<li>%s</li>" % render(c, prov) for c in D["checks"])


def blk_nothere(D, prov):
    return "<ul>%s</ul>" % "".join("<li>%s</li>" % render(c, prov) for c in D["nothere"])


def blk_prints(D, prov):
    P = D["prints"]
    figs = "".join('<figure><img src="assets/%s" alt="The %s print" width="512" height="512" loading="lazy">'
                   '<figcaption>%s</figcaption></figure>' % (f, esc(alt), esc(alt)) for f, alt, _d, _h in P["files"])
    q = pin("Quantum-Film")
    cap = render([P["caption"], ", laid by Quantum-Film at ", L(q.href(), C(q.short)), ". ",
                  P["again"], " when checked."], prov)
    return '<div class="prints">%s</div><p class="cap">%s</p>' % (figs, cap)


def blk_footer(D):
    li = []
    for name, p in D["pins"]:
        if is_public(name):
            li.append('<li>%s <a href="https://github.com/%s/%s/commit/%s">%s</a></li>'
                      % (esc(name), OWNER, esc(name), p.full, p.short))
        else:
            li.append('<li>%s %s <i>private</i></li>' % (esc(name), p.short))
    return ('<p>Pinned: every figure on this page is read at these commits.</p><ul class="pins">%s</ul>'
            '<p>GitHub snapshot <code>sources/%s</code>, taken %s. Generated by '
            '<code>design/experiments/build.py</code>. The experiments write no plain-text twin.</p>'
            % ("".join(li), SNAPSHOT.name, esc(D["snapshot"])))


def banner(letter, name):
    n = count_word()
    return ('Design experiment <b>%s of %s</b>: %s. Not the site &mdash; a prototype whose figures '
            'are read from the pinned commits in the footer; <i>stated</i> marks what no file backs. '
            '<a href="index.html">All %s</a>' % (letter, n, name, n))


def stamp(D):
    return ("%d commits pinned &middot; GitHub snapshot %s &middot; a figure whose source stops "
            "matching stops the build" % (len(D["pins"]), esc(D["snapshot"][:10])))


def head(title, fonts, css):
    f = ""
    if fonts:
        f = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link rel="stylesheet" href="%s">' % fonts)
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title>%s<style>%s%s</style></head>\n' % (esc(title), f, CSS_MAP, css))


# ---- the shared map and legend styling, driven by each page's --map-* tokens

CSS_MAP = """
.map{margin:0}.map-scroll{overflow-x:auto}.map-scroll>svg{display:block;width:100%;height:auto;min-width:820px}
.map svg text{font-family:var(--map-font);font-size:13px;fill:var(--map-ink)}
.map .lane{font-size:10.5px;letter-spacing:.14em;fill:var(--map-muted)}
.map .sep{stroke:var(--map-muted);stroke-width:.6;stroke-dasharray:2 3}
.map .axis{stroke:var(--map-muted);stroke-width:.8;fill:none}
.map .tick{font-size:11px;fill:var(--map-muted)}
.map .now{stroke:var(--map-accent);stroke-width:.8;stroke-dasharray:3 3}
.map .node rect{fill:var(--map-ink)}
.map .node.private rect{fill:var(--map-paper);stroke:var(--map-ink);stroke-width:1.3}
.map .node.pre rect{fill:var(--map-muted)}.map .node.pre text{fill:var(--map-muted)}
.map .node.trunk text{font-weight:700}
.map .note{fill:var(--map-muted);font-size:11.5px}
.map .edge{fill:none;stroke:var(--map-ink);stroke-width:1.2;opacity:.75}
.map .edge.grew-into{stroke:var(--map-accent);stroke-width:1.9;opacity:1}
.map .edge.extracted{stroke-width:3;opacity:.3}
.map .edge.ports{stroke-dasharray:6 4}
.map .edge.verified-by{stroke-dasharray:.5 4;stroke-linecap:round;stroke-width:2}
.map .edge.distilled-from{stroke-dasharray:9 3 2 3}
.map .range{stroke:var(--map-ink);stroke-width:5;opacity:.28}
.map .ah{fill:var(--map-ink)}.map .ah-acc{fill:var(--map-accent)}
.legend{list-style:none;padding:0;margin:12px 0 0;display:flex;flex-wrap:wrap;gap:6px 20px}
.legend li{white-space:nowrap}.legend svg{vertical-align:middle;margin-right:7px;overflow:visible}
.evidence{margin-top:12px}.evidence summary{cursor:pointer}
.evidence ol,.evidence ul{margin:.5em 0;padding-left:1.4em}.evidence li{margin:.25em 0}
"""


# ---------------------------------------------------------------------------
# A - Datasheet
# ---------------------------------------------------------------------------

FONTS_A = ("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600"
           "&family=IBM+Plex+Sans:wght@400;500;600&display=swap")
CSS_A = """
:root{--bg:#fbfbf9;--ink:#15171a;--muted:#5b616a;--rule:#d9dbde;--faint:#f0f1f2;--accent:#1f4fd1;
--sans:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
--map-ink:var(--ink);--map-muted:#8b9199;--map-accent:var(--accent);--map-font:var(--mono);--map-paper:var(--bg)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0f1114;--ink:#e6e8eb;--muted:#99a0aa;--rule:#2b3038;--faint:#181b20;--accent:#86a8ff;--map-muted:#6b737e}}
:root[data-theme="dark"]{--bg:#0f1114;--ink:#e6e8eb;--muted:#99a0aa;--rule:#2b3038;--faint:#181b20;--accent:#86a8ff;--map-muted:#6b737e}
*{box-sizing:border-box}html{background:var(--bg);color:var(--ink);font:15px/1.55 var(--sans);-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg)}a{color:var(--accent);text-underline-offset:2px}
.banner{font:12px/1.45 var(--mono);color:var(--muted);background:var(--faint);border-bottom:1px solid var(--rule);padding:8px 16px}
.banner b{color:var(--ink);font-weight:600}
.wrap{max-width:1100px;margin:0 auto;padding:0 16px 56px}
.doc{display:grid;grid-template-columns:1fr auto;gap:14px 32px;align-items:end;padding:34px 0 14px;border-bottom:2px solid var(--ink)}
.doc h1{font:600 30px/1.1 var(--sans);letter-spacing:-.015em;margin:0}.doc .sub{color:var(--muted);margin:6px 0 0}
.docmeta{display:grid;grid-template-columns:auto auto;gap:2px 14px;margin:0;font:12px/1.45 var(--mono)}
.docmeta dt{color:var(--muted)}.docmeta dd{margin:0}
nav{display:flex;flex-wrap:wrap;border-bottom:1px solid var(--rule);font:500 12px/1 var(--sans);letter-spacing:.07em;text-transform:uppercase}
nav a,nav span{padding:12px 0 11px;margin-right:22px;color:var(--muted);text-decoration:none}
nav .here{color:var(--ink);box-shadow:inset 0 -2px 0 var(--accent)}
section{padding:30px 0;border-bottom:1px solid var(--rule)}
h2{display:flex;gap:14px;align-items:baseline;margin:0 0 18px;font:600 12px/1 var(--sans);letter-spacing:.09em;text-transform:uppercase}
h2 .no{font-family:var(--mono);color:var(--accent);letter-spacing:0}
.lede{font-size:20px;line-height:1.5;max-width:60ch;margin:0}
.fig{font-family:var(--mono);font-size:.93em;font-variant-numeric:tabular-nums}
.stated{border-bottom:1px dotted var(--muted)}
sup.fn{font:10px/0 var(--mono);margin-left:2px}sup.fn a{text-decoration:none}
code{font-family:var(--mono);font-size:.9em;background:var(--faint);padding:1px 4px;border-radius:2px}
.table-wrap{overflow-x:auto}
table{border-collapse:collapse;width:100%;min-width:900px;font-size:13.5px}
th{text-align:left;font:600 11px/1.25 var(--sans);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);border-bottom:1.5px solid var(--ink);padding:0 14px 8px 0;vertical-align:bottom}
td{border-bottom:1px solid var(--rule);padding:9px 14px 9px 0;vertical-align:top}
td.p{font-family:var(--mono);font-weight:500;white-space:nowrap}td.d,td.n{white-space:nowrap}th.n,td.n{text-align:right}
tr.th td{padding:22px 0 6px;border-bottom:1px solid var(--ink);font:600 11px var(--sans);letter-spacing:.09em;text-transform:uppercase}
.cap{color:var(--muted);font-size:12.5px;margin:12px 0 0;max-width:86ch}
.map figcaption{color:var(--muted);font-size:12.5px;margin:10px 0 0;max-width:86ch}
.legend{font:12px var(--mono);color:var(--muted)}.evidence{font-size:12.5px;color:var(--muted)}
.evidence summary{font:12px var(--mono)}.evidence b{color:var(--ink);font-weight:500}.evidence .where{font-family:var(--mono)}
.prints{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;max-width:780px}
.prints figure{margin:0}.prints img{display:block;width:100%;height:auto;border:1px solid var(--rule)}
.prints figcaption{font:11.5px/1.4 var(--mono);color:var(--muted);margin-top:6px}
.two{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,2fr);gap:32px}
.cta{border:1.5px solid var(--ink);padding:18px 22px}.cta p{margin:0 0 10px;font:600 22px/1.2 var(--sans);letter-spacing:-.01em}
.cta ol{margin:0;padding-left:1.3em}.cta li,.box li{margin:7px 0}.box ul{margin:0;padding-left:1.1em}
.notes{font:11.5px/1.55 var(--mono);color:var(--muted);columns:2 400px;column-gap:36px;padding:0;list-style:none;margin:0}
.notes li{break-inside:avoid;margin:0 0 5px;padding-left:2.8em;text-indent:-2.8em;overflow-wrap:anywhere}
.notes .k{display:inline-block;width:2.8em;text-indent:0;color:var(--accent)}
footer{font:11.5px/1.6 var(--mono);color:var(--muted);padding:22px 0 0}
.pins{list-style:none;padding:0;margin:6px 0;display:flex;flex-wrap:wrap;gap:4px 20px}
@media (max-width:760px){.doc{grid-template-columns:1fr}.two{grid-template-columns:1fr}.lede{font-size:18px}}
"""


def page_a(D):
    p = Prov("footnote")
    who = render(D["who"], p)
    ledger_html = blk_ledger(D, p)
    checks = blk_checks(D, p)
    nothere = blk_nothere(D, p)
    prints = blk_prints(D, p)
    notes = "".join(note_li(i + 1, s) for i, s in enumerate(p.notes))
    return (head("loganw.dev · experiment A · Datasheet", FONTS_A, CSS_A) +
            '<body><div class="banner">%s</div><div class="wrap">'
            '<header class="doc"><div><h1>Logan W.</h1><p class="sub">loganw.dev &mdash; the top of the record, not the top of a pitch</p></div>'
            '<dl class="docmeta"><dt>document</dt><dd>HOME</dd><dt>revision</dt><dd>experiment A</dd>'
            '<dt>pinned</dt><dd>%d commits</dd><dt>snapshot</dt><dd>%s</dd></dl></header>'
            '<nav>%s</nav>'
            '<section><h2><span class="no">1</span>Who</h2><p class="lede">%s</p></section>'
            '<section><h2><span class="no">2</span>Where each project came from</h2>%s</section>'
            '<section><h2><span class="no">3</span>Ledger</h2><div class="table-wrap">%s</div><p class="cap">%s</p></section>'
            '<section class="two"><div><h2><span class="no">4</span>Check it yourself</h2><div class="cta"><p>Don\'t trust this page.</p>%s</div></div>'
            '<div class="box"><h2><span class="no">5</span>Not here</h2>%s</div></section>'
            '<section><h2><span class="no">6</span>The film thread, in its own prints</h2>%s</section>'
            '<section><h2><span class="no">7</span>Sources</h2><ol class="notes">%s</ol></section>'
            '<footer>%s</footer></div></body></html>\n'
            % (banner("A", "Datasheet"), len(D["pins"]), esc(D["snapshot"][:10]), nav(), who, blk_map(D),
               ledger_html, LEDGER_CAP, checks, nothere, prints, notes, blk_footer(D)))


# ---------------------------------------------------------------------------
# B - Notebook
# ---------------------------------------------------------------------------

FONTS_B = ("https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;"
           "1,6..72,400;1,6..72,500&family=JetBrains+Mono:wght@400;500&display=swap")
CSS_B = """
:root{--bg:#f6f2e9;--ink:#1f1c17;--muted:#6e675c;--rule:#d8cfbf;--faint:#efe9dc;--accent:#b3261e;
--serif:"Newsreader",Georgia,"Times New Roman",serif;--mono:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;
--map-ink:var(--ink);--map-muted:#9a917f;--map-accent:var(--accent);--map-font:var(--mono);--map-paper:var(--bg)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1a1814;--ink:#ebe5d8;--muted:#a59c8c;--rule:#3b362d;--faint:#23201b;--accent:#ff8f80;--map-muted:#7d7566}}
:root[data-theme="dark"]{--bg:#1a1814;--ink:#ebe5d8;--muted:#a59c8c;--rule:#3b362d;--faint:#23201b;--accent:#ff8f80;--map-muted:#7d7566}
*{box-sizing:border-box}html{background:var(--bg);color:var(--ink);font:18px/1.62 var(--serif);-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg)}a{color:inherit;text-decoration-color:var(--accent);text-underline-offset:3px}
.banner{font:12px/1.5 var(--mono);color:var(--muted);padding:10px 16px;border-bottom:1px solid var(--rule);text-align:center}
.banner a{color:var(--accent)}
.page{max-width:1120px;margin:0 auto;padding:0 16px 64px}
header{padding:46px 0 0}header .site{font:500 12.5px var(--mono);letter-spacing:.05em;color:var(--muted)}
header h1{font:italic 500 46px/1.05 var(--serif);margin:.18em 0 .2em;letter-spacing:-.01em}
nav{font:italic 17px/1.6 var(--serif);color:var(--muted);display:flex;flex-wrap:wrap}
nav>*+*::before{content:"\\00b7";margin:0 .55em;color:var(--rule);font-style:normal}
nav a{color:var(--ink);text-decoration:underline;text-decoration-color:var(--accent);text-underline-offset:4px}
.stamp{font:12.5px/1.5 var(--mono);color:var(--muted);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:8px 0;margin:22px 0 0}
.row{display:grid;grid-template-columns:minmax(0,42rem) minmax(0,15rem);gap:0 3.2rem;padding:38px 0 0}
.row.wide{grid-template-columns:minmax(0,1fr)}
.margin{font-size:13.5px;line-height:1.45;color:var(--muted);padding-top:2.9em;min-width:0}
.row.wide .margin{padding-top:1em}.row.wide .margin ol{columns:3 16rem;column-gap:2.4rem}
.margin ol{list-style:none;padding:0;margin:0}.margin li{margin:0 0 .75em;break-inside:avoid;overflow-wrap:anywhere}
.margin .k{font:11px var(--mono);color:var(--accent);margin-right:.4em}.margin a{color:inherit}
h2{font:italic 500 27px/1.2 var(--serif);margin:0 0 .45em}
h2 small{font:500 11px var(--mono);color:var(--muted);letter-spacing:.08em;margin-right:.7em;font-style:normal;vertical-align:.32em}
p{margin:0 0 .8em}.lede{font-size:21px;line-height:1.55}
.fig{font-family:var(--mono);font-size:.8em;font-variant-numeric:tabular-nums}.stated{font-style:italic}
sup.sn{font:10.5px/0 var(--mono);color:var(--accent);margin-left:1px}
code{font-family:var(--mono);font-size:.8em}
.table-wrap{overflow-x:auto}
table{border-collapse:collapse;width:100%;min-width:920px;font-size:15.5px;line-height:1.45;border-top:1.5px solid var(--ink);border-bottom:1.5px solid var(--ink)}
th{text-align:left;font:italic 500 15px var(--serif);color:var(--muted);border-bottom:1px solid var(--ink);padding:8px 16px 6px 0}
td{padding:7px 16px 7px 0;vertical-align:top}th.n,td.n{text-align:right}td.d,td.n{white-space:nowrap}
td.p{font:500 .8em var(--mono);white-space:nowrap;padding-top:.55em}
tr.th td{font:italic 500 16px var(--serif);color:var(--accent);padding-top:.9em}
.cap{font-size:15px;color:var(--muted);margin-top:.8em;max-width:44rem}
.map figcaption{font-size:15px;color:var(--muted);margin:.7em 0 0;max-width:44rem}
.legend{font:12px var(--mono);color:var(--muted)}.evidence{font-size:14px;color:var(--muted)}
.evidence summary{font:italic 15px var(--serif)}.evidence b{color:var(--ink);font-weight:500}.evidence .where{font:12px var(--mono)}
.prints{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.prints figure{margin:0}.prints img{display:block;width:100%;height:auto;border:1px solid var(--rule)}
.prints figcaption{font:italic 15px var(--serif);color:var(--muted);margin-top:.35em}
.cta{border-left:3px solid var(--accent);padding:.1em 0 .1em 1.2em}.cta h2{color:var(--accent)}
.cta ol{padding-left:1.2em;margin:.3em 0 0}.cta li{margin:.3em 0}
ul.plain{padding-left:1.1em;margin:0}ul.plain li{margin:.35em 0}
footer{font:12px/1.65 var(--mono);color:var(--muted);border-top:1px solid var(--rule);margin-top:3.2em;padding-top:1em}
footer a{color:var(--accent)}.pins{list-style:none;padding:0;margin:.4em 0;display:flex;flex-wrap:wrap;gap:3px 20px}
@media (max-width:980px){.row{grid-template-columns:minmax(0,1fr)}.margin{padding-top:.6em;border-top:1px dashed var(--rule);margin-top:.6em}.margin ol{columns:2 14rem}}
@media (max-width:600px){header h1{font-size:38px}.lede{font-size:19px}}
"""


def page_b(D):
    p = Prov("sidenote")

    def row(inner, wide=False):
        notes = "".join('<li id="n%d"><span class="k">%d</span>%s</li>'
                        % (n, n, ('<a href="%s">%s</a>' % (esc(s.href), esc(s.text())) if s.href else esc(s.text())))
                        for n, s in p.new_since(m[0]))
        aside = '<aside class="margin"><ol>%s</ol></aside>' % notes if notes else '<aside class="margin"></aside>'
        return '<div class="row%s"><div class="main">%s</div>%s</div>' % (" wide" if wide else "", inner, aside)

    m = [p.mark()]
    s1 = row('<h2><small>I</small>Who</h2><p class="lede">%s</p>' % render(D["who"], p))
    m = [p.mark()]
    s2 = row('<h2><small>II</small>Where each project came from</h2>%s' % blk_map(D), wide=True)
    m = [p.mark()]
    s3 = row('<h2><small>III</small>The ledger</h2><div class="table-wrap">%s</div><p class="cap">%s</p>'
             % (blk_ledger(D, p), LEDGER_CAP), wide=True)
    m = [p.mark()]
    s4 = row('<div class="cta"><h2><small>IV</small>Don\'t trust this page</h2><p>Three checks, cheapest first:</p>%s</div>'
             % blk_checks(D, p))
    m = [p.mark()]
    s5 = row('<h2><small>V</small>The film thread</h2>%s' % blk_prints(D, p))
    m = [p.mark()]
    s6 = row('<h2><small>VI</small>Not here</h2><ul class="plain">%s</ul>'
             % "".join("<li>%s</li>" % render(c, p) for c in D["nothere"]))
    return (head("loganw.dev · experiment B · Notebook", FONTS_B, CSS_B) +
            '<body><div class="banner">%s</div><div class="page">'
            '<header><div class="site">loganw.dev</div><h1>Logan W.</h1><nav>%s</nav><p class="stamp">%s</p></header>'
            '%s%s%s%s%s%s<footer>%s</footer></div></body></html>\n'
            % (banner("B", "Notebook"), nav(), stamp(D), s1, s2, s3, s4, s5, s6, blk_footer(D)))


# ---------------------------------------------------------------------------
# C - Instrument panel
# ---------------------------------------------------------------------------

FONTS_C = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600"
           "&family=JetBrains+Mono:wght@400;500;600&display=swap")
CSS_C = """
:root{--bg:#0d0f11;--panel:#13161a;--ink:#e4e7ea;--muted:#8a939c;--rule:#262c33;--faint:#1b1f24;--accent:#f0a33c;
--sans:"Inter",system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;
--map-ink:var(--ink);--map-muted:#66707a;--map-accent:var(--accent);--map-font:var(--mono);--map-paper:var(--panel)}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]){--bg:#ecece8;--panel:#f8f8f5;--ink:#16181a;--muted:#5d656c;--rule:#d0d3cf;--faint:#eeeeea;--accent:#a35f00;--map-muted:#9aa19f}}
:root[data-theme="light"]{--bg:#ecece8;--panel:#f8f8f5;--ink:#16181a;--muted:#5d656c;--rule:#d0d3cf;--faint:#eeeeea;--accent:#a35f00;--map-muted:#9aa19f}
*{box-sizing:border-box}html{background:var(--bg);color:var(--ink);font:14px/1.5 var(--sans);-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg)}a{color:var(--accent);text-underline-offset:2px}
.banner{font:11.5px/1.5 var(--mono);color:var(--muted);padding:8px 16px;border-bottom:1px solid var(--rule)}.banner b{color:var(--ink)}
.bar{display:flex;flex-wrap:wrap;gap:8px 24px;align-items:center;font:500 11px/1.2 var(--mono);letter-spacing:.07em;text-transform:uppercase;color:var(--muted);padding:12px 16px;border-bottom:1px solid var(--rule)}
.bar .id{color:var(--ink);font-weight:600;letter-spacing:.16em}.bar .v{color:var(--ink)}.bar .ok{color:var(--accent)}
.shell{max-width:1240px;margin:0 auto;padding:14px 16px 48px}
nav{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 14px}
nav a,nav span{font:500 11px/1 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--muted);text-decoration:none;border:1px solid var(--rule);padding:8px 10px;background:var(--panel)}
nav .here{color:var(--bg);background:var(--accent);border-color:var(--accent)}
.grid{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:12px}
.panel{grid-column:span 12;background:var(--panel);border:1px solid var(--rule);padding:14px 16px 12px;min-width:0}
.s4{grid-column:span 4}.s5{grid-column:span 5}.s7{grid-column:span 7}.s8{grid-column:span 8}
.panel h2{display:flex;justify-content:space-between;gap:12px;margin:0 0 12px;font:500 11px/1 var(--mono);letter-spacing:.15em;text-transform:uppercase;color:var(--muted)}
.panel h2 .i{color:var(--accent)}
.who p{font-size:17px;line-height:1.5;margin:0}
.fig{font-family:var(--mono);font-size:.94em;font-variant-numeric:tabular-nums}
.fig[title],.q[title],.stated[title]{text-decoration:underline dotted var(--muted);text-underline-offset:3px;cursor:help}
.tag{font:600 9px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;border:1px solid var(--rule);color:var(--muted);padding:2px 4px;margin-left:6px;vertical-align:2px}
.src{font:10.5px/1.6 var(--mono);color:var(--muted);border-top:1px dashed var(--rule);margin-top:12px;padding-top:8px;overflow-wrap:anywhere}
.src b{color:var(--ink);font-weight:500;letter-spacing:.12em;margin-right:6px}.src a{color:var(--muted)}
code{font-family:var(--mono);font-size:.92em;color:var(--ink);background:var(--faint);padding:1px 4px}
.table-wrap{overflow-x:auto}
table{border-collapse:collapse;width:100%;min-width:940px;font-size:13px}
th{font:500 10.5px/1.2 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--muted);text-align:left;padding:0 12px 8px 0;border-bottom:1px solid var(--rule)}
td{padding:8px 12px 8px 0;border-bottom:1px solid var(--faint);vertical-align:top}
td.p{font:500 12.5px var(--mono);white-space:nowrap}td.d,td.n{white-space:nowrap;font-family:var(--mono)}th.n,td.n{text-align:right}
tr.th td{font:500 10.5px var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--accent);padding-top:16px;border-bottom:1px solid var(--rule)}
.cap,.map figcaption{color:var(--muted);font-size:12px;margin:10px 0 0}
.legend{font:11px var(--mono);color:var(--muted)}.evidence{font-size:12px;color:var(--muted)}.evidence summary{font:11px var(--mono);letter-spacing:.06em;text-transform:uppercase}
.evidence b{color:var(--ink);font-weight:500}.evidence .where{font-family:var(--mono)}
.prints{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.prints figure{margin:0}
.prints img{display:block;width:100%;height:auto;border:1px solid var(--rule)}.prints figcaption{font:10.5px var(--mono);color:var(--muted);letter-spacing:.08em;text-transform:uppercase;margin-top:6px}
.cta .big{font:600 22px/1.2 var(--sans);letter-spacing:-.01em;margin:0 0 10px}
.cta ol{margin:0;padding-left:1.3em}.cta li,.nothere li{margin:6px 0}.nothere ul{margin:0;padding-left:1.1em}
footer{font:11px/1.6 var(--mono);color:var(--muted);margin-top:14px;border:1px solid var(--rule);background:var(--panel);padding:12px 16px}
.pins{list-style:none;padding:0;margin:6px 0;display:flex;flex-wrap:wrap;gap:3px 18px}
@media (max-width:900px){.s4,.s5,.s7,.s8{grid-column:span 12}}
"""


def page_c(D):
    p = Prov("title")

    def panel(cls, title, idx, inner):
        used = p.used()
        src = ""
        if used:
            src = '<div class="src"><b>SRC</b>%s</div>' % " &middot; ".join(
                ('<a href="%s">%s</a>' % (esc(s.href), esc(s.short)) if s.href else esc(s.short)) for s in used)
        return ('<section class="panel %s"><h2><span>%s</span><span class="i">%02d</span></h2>%s%s</section>'
                % (cls, esc(title), idx, inner, src))

    p.mark()
    who = panel("s5 who", "Who", 1, "<p>%s</p>" % render(D["who"], p))
    p.mark()
    cta = panel("s7 cta", "Check it yourself", 2,
                '<p class="big">Don\'t trust this page.</p>%s' % blk_checks(D, p))
    p.mark()
    mp = panel("", "Where each project came from", 3, blk_map(D))
    p.mark()
    led = panel("", "Ledger", 4, '<div class="table-wrap">%s</div><p class="cap">%s</p>' % (blk_ledger(D, p), LEDGER_CAP))
    p.mark()
    pr = panel("s8", "The film thread", 5, blk_prints(D, p))
    p.mark()
    nh = panel("s4 nothere", "Not here", 6, blk_nothere(D, p))
    bar = ('<div class="bar"><span class="id">LOGANW.DEV</span><span>build <span class="v">experiment C</span></span>'
           '<span>pinned <span class="v">%d</span></span><span>snapshot <span class="v">%s</span></span>'
           '<span class="ok">a source that stops matching stops the build</span></div>'
           % (len(D["pins"]), esc(D["snapshot"][:10])))
    return (head("loganw.dev · experiment C · Instrument panel", FONTS_C, CSS_C) +
            '<body><div class="banner">%s</div>%s<div class="shell"><nav>%s</nav><div class="grid">%s%s%s%s%s%s</div>'
            '<footer>%s</footer></div></body></html>\n'
            % (banner("C", "Instrument panel"), bar, nav(), who, cta, mp, led, pr, nh, blk_footer(D)))


# ---------------------------------------------------------------------------
# D - Plain
# ---------------------------------------------------------------------------

CSS_D = """
:root{--bg:#ffffff;--ink:#1b1b1b;--muted:#6a6a6a;--rule:#e6e6e6;--faint:#f5f5f4;--accent:#1b6b4c;
--sans:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;
--map-ink:var(--ink);--map-muted:#9a9a9a;--map-accent:var(--accent);--map-font:var(--mono);--map-paper:var(--bg)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121212;--ink:#e9e9e9;--muted:#9b9b9b;--rule:#2b2b2b;--faint:#1b1b1b;--accent:#6fd0a0;--map-muted:#6d6d6d}}
:root[data-theme="dark"]{--bg:#121212;--ink:#e9e9e9;--muted:#9b9b9b;--rule:#2b2b2b;--faint:#1b1b1b;--accent:#6fd0a0;--map-muted:#6d6d6d}
*{box-sizing:border-box}html{background:var(--bg);color:var(--ink);font:16px/1.65 var(--sans);-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg)}a{color:var(--accent);text-underline-offset:2px}
.banner{font:12px/1.5 var(--mono);color:var(--muted);padding:10px 16px;border-bottom:1px solid var(--rule)}
main{max-width:1040px;margin:0 auto;padding:36px 16px 64px}.measure{max-width:42rem}
header{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px 24px;align-items:baseline;margin-bottom:44px}
header .site{font-weight:600}nav{display:flex;flex-wrap:wrap;gap:2px 14px;font-size:14px}
nav a,nav span{color:var(--muted);text-decoration:none}nav .here{color:var(--ink);font-weight:600}
h1{font:600 32px/1.2 var(--sans);letter-spacing:-.015em;margin:0 0 .35em}
h2{font:600 18px/1.3 var(--sans);margin:2.6em 0 .7em}
.stamp{font:12.5px/1.5 var(--mono);color:var(--muted);margin:0 0 1.6em}
.lede{font-size:19px;line-height:1.55;margin:0}
.fig{font-family:var(--mono);font-size:.9em;font-variant-numeric:tabular-nums}
.src{font:11.5px/1.45 var(--mono);color:var(--muted)}td .src{display:block;white-space:normal;overflow-wrap:anywhere}
code{font-family:var(--mono);font-size:.9em}
.table-wrap{overflow-x:auto}
table{border-collapse:collapse;width:100%;min-width:1000px;font-size:14px}
th{text-align:left;font-weight:600;font-size:12.5px;color:var(--muted);border-bottom:1px solid var(--ink);padding:0 14px 6px 0}
td{padding:9px 14px 9px 0;border-bottom:1px solid var(--rule);vertical-align:top}
td.p{font-family:var(--mono);font-size:13px;white-space:nowrap}th.n,td.n{text-align:right}
tr.th td{font-weight:600;padding-top:1.4em}
.cap,.map figcaption{color:var(--muted);font-size:13.5px;margin:.8em 0 0;max-width:42rem}
.legend{font:12px var(--mono);color:var(--muted)}.evidence{font-size:13.5px;color:var(--muted)}
.evidence b{color:var(--ink);font-weight:600}.evidence .where{font:12px var(--mono)}
.prints{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;max-width:42rem}
.prints figure{margin:0}.prints img{display:block;width:100%;height:auto}.prints figcaption{font-size:13px;color:var(--muted)}
.cta{background:var(--faint);padding:14px 18px;border-radius:4px}.cta p{margin:0 0 6px;font-weight:600}
.cta ol{margin:0;padding-left:1.3em}ul.plain{padding-left:1.1em}
footer{font:12px/1.6 var(--mono);color:var(--muted);margin-top:3.4em;border-top:1px solid var(--rule);padding-top:1em}
.pins{list-style:none;padding:0;margin:.4em 0;display:flex;flex-wrap:wrap;gap:2px 18px}
"""


def page_d(D):
    p = Prov("inline")
    return (head("loganw.dev · experiment D · Plain", "", CSS_D) +
            '<body><div class="banner">%s</div><main>'
            '<header><span class="site">loganw.dev</span><nav>%s</nav></header>'
            '<div class="measure"><h1>Logan W.</h1><p class="stamp">%s</p><p class="lede">%s</p></div>'
            '<h2>Where each project came from</h2>%s'
            '<h2>Ledger</h2><div class="table-wrap">%s</div><p class="cap">%s</p>'
            '<div class="measure"><h2>Check it yourself</h2><div class="cta"><p>Don\'t trust this page.</p>%s</div>'
            '<h2>The film thread</h2>%s'
            '<h2>Not here</h2><ul class="plain">%s</ul></div>'
            '<footer>%s</footer></main></body></html>\n'
            % (banner("D", "Plain"), nav(), stamp(D), render(D["who"], p), blk_map(D),
               blk_ledger(D, p), LEDGER_CAP, blk_checks(D, p), blk_prints(D, p),
               "".join("<li>%s</li>" % render(c, p) for c in D["nothere"]), blk_footer(D)))


# ---------------------------------------------------------------------------
# E - Combined: D's page, A's colour, B's type and header
# ---------------------------------------------------------------------------
# Logan, 2026-09-29: "D looks good, but the color scheme of A (the blue), and
# the font and header choice of B." The tokens and rules below were copied
# from A and B on that date. A to D stay exactly as they were, as the record
# of the options; E is the one that moves from here.

CSS_E = """
:root{--bg:#fbfbf9;--ink:#15171a;--muted:#5b616a;--rule:#d9dbde;--faint:#f0f1f2;--accent:#1f4fd1;
--serif:"Newsreader",Georgia,"Times New Roman",serif;--mono:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;
--map-ink:var(--ink);--map-muted:#8b9199;--map-accent:var(--accent);--map-font:var(--mono);--map-paper:var(--bg)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0f1114;--ink:#e6e8eb;--muted:#99a0aa;--rule:#2b3038;--faint:#181b20;--accent:#86a8ff;--map-muted:#6b737e}}
:root[data-theme="dark"]{--bg:#0f1114;--ink:#e6e8eb;--muted:#99a0aa;--rule:#2b3038;--faint:#181b20;--accent:#86a8ff;--map-muted:#6b737e}
*{box-sizing:border-box}html{background:var(--bg);color:var(--ink);font:18px/1.62 var(--serif);-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg)}a{color:var(--accent);text-underline-offset:3px}
.banner{font:12px/1.5 var(--mono);color:var(--muted);padding:10px 16px;border-bottom:1px solid var(--rule)}
main{max-width:1040px;margin:0 auto;padding:0 16px 64px}.measure{max-width:42rem}
header{padding:46px 0 0}header .site{font:500 12.5px var(--mono);letter-spacing:.05em;color:var(--muted)}
header h1{font:italic 500 46px/1.05 var(--serif);margin:.18em 0 .2em;letter-spacing:-.01em}
nav{font:italic 17px/1.6 var(--serif);color:var(--muted);display:flex;flex-wrap:wrap}
nav>*+*::before{content:"\\00b7";margin:0 .55em;color:var(--rule);font-style:normal}
nav a{color:var(--ink);text-decoration:underline;text-decoration-color:var(--accent);text-underline-offset:4px}
.stamp{font:12.5px/1.5 var(--mono);color:var(--muted);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:8px 0;margin:22px 0 30px}
h2{font:italic 500 27px/1.2 var(--serif);margin:2.1em 0 .5em}
h2 small{font:500 11px var(--mono);color:var(--muted);letter-spacing:.08em;margin-right:.7em;font-style:normal;vertical-align:.32em}
.lede{font-size:21px;line-height:1.55;margin:0}
.fig{font-family:var(--mono);font-size:.8em;font-variant-numeric:tabular-nums}
.src{font:11.5px/1.45 var(--mono);color:var(--muted)}td .src{display:block;white-space:normal;overflow-wrap:break-word}
code{font-family:var(--mono);font-size:.8em}
.table-wrap{overflow-x:auto}
table{border-collapse:collapse;width:100%;min-width:1000px;font-size:16px;line-height:1.45}
td.d{min-width:10.5em}td.n{min-width:8.5em}
th{text-align:left;font:italic 500 15px var(--serif);color:var(--muted);border-bottom:1px solid var(--ink);padding:0 14px 6px 0}
td{padding:9px 14px 9px 0;border-bottom:1px solid var(--rule);vertical-align:top}
td.p{font:500 .8em var(--mono);white-space:nowrap;padding-top:.75em}th.n,td.n{text-align:right}
tr.th td{font:italic 500 17px var(--serif);color:var(--accent);padding-top:1.1em}
.cap,.map figcaption{color:var(--muted);font-size:15px;margin:.8em 0 0;max-width:42rem}
.legend{font:12px var(--mono);color:var(--muted)}.evidence{font-size:15px;color:var(--muted)}
.evidence summary{font:italic 16px var(--serif)}.evidence b{color:var(--ink);font-weight:500}.evidence .where{font:12px var(--mono)}
.prints{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;max-width:42rem}
.prints figure{margin:0}.prints img{display:block;width:100%;height:auto}.prints figcaption{font:italic 15px var(--serif);color:var(--muted)}
.cta{background:var(--faint);padding:14px 18px;border-radius:4px}.cta p{margin:0 0 6px;font:italic 500 21px/1.3 var(--serif)}
.cta ol{margin:0;padding-left:1.3em}ul.plain{padding-left:1.1em}
footer{font:12px/1.6 var(--mono);color:var(--muted);margin-top:3.4em;border-top:1px solid var(--rule);padding-top:1em}
.pins{list-style:none;padding:0;margin:.4em 0;display:flex;flex-wrap:wrap;gap:2px 18px}
@media (max-width:600px){header h1{font-size:38px}.lede{font-size:19px}}
"""


def page_e(D):
    p = Prov("inline", wbr=True)
    return (head("loganw.dev · experiment E · Combined", FONTS_B, CSS_E) +
            '<body><div class="banner">%s</div><main>'
            '<header><div class="site">loganw.dev</div><h1>Logan W.</h1><nav>%s</nav><p class="stamp">%s</p></header>'
            '<div class="measure"><p class="lede">%s</p></div>'
            '<h2><small>I</small>Where each project came from</h2>%s'
            '<h2><small>II</small>Ledger</h2><div class="table-wrap">%s</div><p class="cap">%s</p>'
            '<div class="measure"><h2><small>III</small>Check it yourself</h2><div class="cta"><p>Don\'t trust this page.</p>%s</div>'
            '<h2><small>IV</small>The film thread</h2>%s'
            '<h2><small>V</small>Not here</h2><ul class="plain">%s</ul></div>'
            '<footer>%s</footer></main></body></html>\n'
            % (banner("E", "Combined &mdash; D&rsquo;s page, A&rsquo;s colour, B&rsquo;s type and header"),
               nav(), stamp(D), render(D["who"], p), blk_map(D), blk_ledger(D, p), LEDGER_CAP,
               blk_checks(D, p), blk_prints(D, p),
               "".join("<li>%s</li>" % render(c, p) for c in D["nothere"]), blk_footer(D)))


# ---------------------------------------------------------------------------
# The index
# ---------------------------------------------------------------------------

# One list. Each direction's page, the function that renders it and its row
# in the index all come from here, so a page cannot exist without its row, or
# a row without its page.
DIRECTIONS = [
    dict(file="a-datasheet.html", letter="A", name="Datasheet", render=page_a,
         idea="An engineering document: numbered sections, hairline tables, every source footnoted and collected at the end.",
         type="IBM Plex Sans + Mono", colour="blue", prov="footnotes, listed at the end", theme="light"),
    dict(file="b-notebook.html", letter="B", name="Notebook", render=page_b,
         idea="A lab notebook: a serif text column with its sources in the margin, ruled tables, correction red as the one colour.",
         type="Newsreader + JetBrains Mono", colour="correction red", prov="margin notes", theme="light, on paper"),
    dict(file="c-instrument.html", letter="C", name="Instrument panel", render=page_c,
         idea="Panels with mono readouts, dark first. Each figure shows its source on hover and each panel ends with what it read.",
         type="Inter + JetBrains Mono", colour="amber", prov="hover, and a source line per panel", theme="dark"),
    dict(file="d-plain.html", letter="D", name="Plain", render=page_d,
         idea="No web fonts, one column; the source is printed after every figure. The least designed, and the heaviest to read.",
         type="the reader's own system fonts", colour="green", prov="inline, after each figure", theme="light"),
    dict(file="e-combined.html", letter="E", name="Combined", render=page_e,
         idea="D's page, with A's colour and B's type and header: the choice of 2026-09-29.",
         type="Newsreader + JetBrains Mono", colour="blue", prov="inline, after each figure", theme="light"),
]

COUNT_WORDS = {4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}


def count_word():
    return COUNT_WORDS[len(DIRECTIONS)]


def page_index(D):
    rows = "".join('<tr><td><a href="%s"><b>%s</b> %s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                   % (d["file"], d["letter"], esc(d["name"]), esc(d["idea"]), esc(d["type"]),
                      esc(d["colour"]), esc(d["prov"]), esc(d["theme"])) for d in DIRECTIONS)
    # Named placeholders, one % over the whole body: a `+` inside it would bind
    # after `%`, leaving the first half's placeholders unfilled.
    body = ('<body><main><div class="measure"><h1>Design experiments</h1>'
            '<p class="lede">One Home page, %(n)s ways of looking. The content is the same in every one &mdash; the '
            'same figures, read from the same %(pins)d pinned commits &mdash; so what differs is only the type, the '
            'colour, and how a figure shows where it came from.</p>'
            '<h2>Chosen so far</h2><p>Logan, 2026-09-29: <i>&ldquo;D looks good, but the color scheme of A (the '
            'blue), and the font and header choice of B.&rdquo;</i> That is <a href="e-combined.html">E</a>. '
            'A to D stay as they were, as the record of the options.</p></div>'
            '<h2>The %(n)s</h2><div class="table-wrap"><table><thead><tr><th>direction</th><th>the idea</th>'
            '<th>type</th><th>the one colour</th><th>a figure\'s source shows as</th><th>default theme</th>'
            '</tr></thead><tbody>%(rows)s</tbody></table></div>'
            '<div class="measure"><h2>The same in every one</h2><ul class="plain">'
            '<li>The map: position across is a date read from git, and every arrow names the file that says so.</li>'
            '<li>The ledger, with the spec\'s columns, plus <i>agent-written</i> and with <i>last verified</i> '
            'renamed <i>last entry</i>, because a ledger\'s newest heading is not always a run of its gate.</li>'
            '<li>The biography and anything else no file backs are marked <i>stated</i>, never sourced.</li>'
            '<li>No script, no analytics, one colour, real tables, numbers in mono.</li></ul>'
            '<h2>What these are not</h2><ul class="plain">'
            '<li>Not the site. Only Home exists, and the other eight entries in the navigation do nothing.</li>'
            '<li>Not final copy. The biography is a draft of the spec\'s three sentences.</li>'
            '<li>Not self-hosted: every page but D loads fonts from Google Fonts. The site would serve its own.</li></ul>'
            '<h2>Rebuilding</h2><p><code>python build.py</code> writes these pages; <code>--check</code> fails '
            'if any differs from a fresh render; <code>--control</code> plants a stale figure and a stale source '
            'and requires both to be caught.</p></div></main></body></html>\n')
    return (head("loganw.dev · design experiments", "", CSS_D) +
            body % dict(n=count_word(), pins=len(D["pins"]), rows=rows))


# ---------------------------------------------------------------------------

def render_all():
    D = gather()
    text = {d["file"]: d["render"](D) for d in DIRECTIONS}
    text["index.html"] = page_index(D)
    q = pin("Quantum-Film")
    text["assets/SOURCES.txt"] = (
        "# Written by build.py from Quantum-Film at %s. Each file is `git show`\n"
        "# of that commit, byte for byte; --check re-hashes them.\n" % q.full +
        "".join("assets/%s  docs/prints/%s  sha256 %s\n" % (f, f, h) for f, _a, _d, h in D["prints"]["files"]))
    binary = {"assets/" + f: data for f, _a, data, _h in D["prints"]["files"]}
    return text, binary


def compare(text, binary, root):
    problems = []
    for rel, want in text.items():
        f = root / rel
        if not f.is_file():
            problems.append("%s is missing" % rel)
            continue
        have = f.read_text(encoding="utf-8")
        if have != want:
            for i, (a, b) in enumerate(zip(have.splitlines(), want.splitlines()), 1):
                if a != b:
                    problems.append("%s differs at line %d" % (rel, i))
                    break
            else:
                problems.append("%s differs in length" % rel)
    for rel, want in binary.items():
        f = root / rel
        if not f.is_file() or f.read_bytes() != want:
            problems.append("%s is missing or not the bytes at the pin" % rel)
    return problems


def write(text, binary, root):
    for rel, t in text.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(t, encoding="utf-8", newline="\n")
    for rel, b in binary.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_bytes(b)


def controls():
    """Both must FAIL. If either passes, this generator cannot see the defect
    it exists to refuse, and every page it wrote is decoration."""
    ok = True
    text, binary = render_all()

    # 1. a stale figure planted in a written page must be caught
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        write(text, binary, root)
        page = root / "a-datasheet.html"
        t = page.read_text(encoding="utf-8")
        needle = '<span class="fig">%s</span>' % abi().text
        if needle not in t:
            print("control 1: FAILED TO PLANT - %r is not in the page" % needle)
            ok = False
        else:
            page.write_text(t.replace(needle, '<span class="fig">0.14</span>', 1), encoding="utf-8", newline="\n")
            found = compare(text, binary, root)
            if found:
                print("control 1: caught, as it must be - %s" % found[0])
            else:
                print("control 1: NEGATIVE CONTROL DID NOT FAIL - a stale ABI passed")
                ok = False

    # 2. a stale source - cft-fp256 pinned to its first commit - must be refused by name
    saved = PINS["cft-fp256"]
    PINS["cft-fp256"] = ("cft-fp256", "644ee2d")
    _PIN.clear()
    try:
        render_all()
        print("control 2: NEGATIVE CONTROL DID NOT FAIL - the pages built from cft-fp256's first commit")
        ok = False
    except Refusal as e:
        if "cft-fp256" in str(e):
            print("control 2: refused by name, as it must be - %s" % e)
        else:
            print("control 2: refused, but not naming cft-fp256 - %s" % e)
            ok = False
    finally:
        PINS["cft-fp256"] = saved
        _PIN.clear()
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true", help="fail if a written file differs from a fresh render")
    g.add_argument("--control", action="store_true", help="run both negative controls")
    a = ap.parse_args(argv)
    try:
        if a.control:
            return 0 if controls() else 1
        text, binary = render_all()
        if a.check:
            problems = compare(text, binary, HERE)
            for p in problems:
                print("DRIFT: %s" % p, file=sys.stderr)
            if not problems:
                print("check: %d files are exactly what the pinned sources render" % (len(text) + len(binary)))
            return 1 if problems else 0
        write(text, binary, HERE)
        print("wrote %d pages and %d assets from %d pinned commits and %s"
              % (len([k for k in text if k.endswith(".html")]), len(binary), len(PINS), SNAPSHOT.name))
        return 0
    except Refusal as e:
        print("REFUSED: %s" % e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
