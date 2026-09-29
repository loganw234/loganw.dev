"""The site's facts: every figure it prints, and where each was read.

A figure is read from one of three places, and from nowhere else:

  * a repository at the commit pins.json names - `git show` and `git log`
    at that SHA, never a working tree, where another session may be
    mid-round (docs/SPEC.md, decision 3);
  * the GitHub snapshot pins.json names, taken once by snapshot_github.py;
  * the owner's word, which is rendered as STATED and never as sourced.

Every figure comes out of a function decorated with @fact. The decorator
logs what was read and how - the method, its arguments, the value - and gives
the figure an id. The renderer refuses a figure without an id, so nothing
reaches a page that is not in facts.json. facts.json is what `build.py
--verify-facts` re-reads, on this machine or on anyone else's.

What a check here proves, and what it does not. A figure lifted from prose
proves that the page quotes the source faithfully at the pin. It does not
prove the source's claim is true; the source's own gates do that. That is a
stated limit, not a gap to be closed with more patterns (ParcelRound,
CASE-STUDY-4, observation 14).

A page module may define facts of its own with @fact. Re-derivation imports
the module a fact was defined in, so no parcel needs to edit this file to add
one.
"""
import dataclasses
import functools
import importlib
import inspect
import json
import os
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
PINS = json.loads((ROOT / "pins.json").read_text(encoding="utf-8"))
OWNER = PINS["owner"]
SNAPSHOT = ROOT / PINS["snapshot"]
REPOS = pathlib.Path(os.environ.get("LOGANW_REPOS") or ROOT.parent)
CACHE = ROOT / ".cache" / "repos"


class Refusal(Exception):
    """A figure that cannot be read from its source. Never rendered around."""


class Unavailable(Refusal):
    """The source exists and this machine cannot read it: a private repository
    with no local clone, or a public one with fetching turned off."""


@dataclasses.dataclass(frozen=True)
class Src:
    kind: str           # file | git | api | stated
    short: str          # where, in one line
    detail: str = ""    # what was read there
    href: str = ""      # where a reader can check it; empty while the repository is private
    private: bool = False


@dataclasses.dataclass(frozen=True)
class V:
    text: str
    src: Src
    raw: str = ""
    num: bool = False   # set in mono: a number, a date or a hash
    id: int = 0         # given by @fact; 0 means no fact produced it


# ---------------------------------------------------------------------------
# The log, and the decorator that fills it
# ---------------------------------------------------------------------------

LOG = []
REGISTRY = {}
_depth = [0]
_recording = [True]


def reset_log():
    LOG.clear()


def fact(fn):
    key = "%s.%s" % (fn.__module__, fn.__name__)
    sig = inspect.signature(fn)

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        _depth[0] += 1
        try:
            v = fn(*args, **kwargs)
        finally:
            _depth[0] -= 1
        if not isinstance(v, V):
            raise TypeError("%s returned %r, not a figure" % (key, v))
        if _depth[0] or not _recording[0]:
            return v
        v = dataclasses.replace(v, id=len(LOG) + 1)
        LOG.append({"id": v.id, "method": key, "args": dict(bound.arguments),
                    "text": v.text, "raw": v.raw, "kind": v.src.kind, "where": v.src.short,
                    "detail": v.src.detail, "href": v.src.href, "private": v.src.private})
        return v

    REGISTRY[key] = fn
    return wrapper


def rederive(rec):
    """Run a logged fact again and say whether it gives the same figure.
    -> (ok, text): ok is True, False, or None when the source is unavailable."""
    mod, _, name = rec["method"].rpartition(".")
    if rec["method"] not in REGISTRY:
        importlib.import_module(mod)
    fn = REGISTRY.get(rec["method"])
    if fn is None:
        raise Refusal("facts.json names %s, which no module defines" % rec["method"])
    _recording[0] = False
    try:
        v = fn(**rec["args"])
    except Unavailable as e:
        return None, str(e)
    finally:
        _recording[0] = True
    same = v.text == rec["text"] and v.raw == rec["raw"]
    return same, v.text


# ---------------------------------------------------------------------------
# The snapshot
# ---------------------------------------------------------------------------

_SNAP = {}


def split(key):
    """A repository key: 'owner/name', or a bare name for the default owner
    (pins.json's "owner"). The Preservation thread's organisation,
    Mercenaries-Fan-Build, is the reason for the first form: a name like
    mercs2-qol-mods exists under both owners."""
    return tuple(key.split("/", 1)) if "/" in key else (OWNER, key)


def snap():
    if not _SNAP:
        if not SNAPSHOT.is_file():
            raise Refusal("%s is missing; run site/snapshot_github.py" % SNAPSHOT.relative_to(ROOT))
        s = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        s["by_name"] = {}
        for r in s["repos"]:
            owner = r.get("owner", OWNER)
            s["by_name"]["%s/%s" % (owner, r["name"])] = r
        _SNAP.update(s)
    return _SNAP


def snapdate():
    return snap()["taken"][:10]


def repo_meta(key):
    r = snap()["by_name"].get("%s/%s" % split(key))
    if r is None:
        raise Refusal("%s is not in %s" % (key, SNAPSHOT.name))
    return r


def is_public(name):
    return repo_meta(name)["visibility"] == "PUBLIC"


def api_src(name, detail):
    pub = is_public(name)
    return Src("api", "GitHub snapshot %s" % snapdate(), "%s: %s" % (name, detail),
               repo_meta(name)["url"] if pub else "", private=not pub)


# ---------------------------------------------------------------------------
# The pins
# ---------------------------------------------------------------------------

def _git(cwd, *args, binary=False, ok=(0,)):
    r = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True)
    if r.returncode not in ok:
        msg = r.stderr.decode("utf-8", "replace").strip() or "exit %d" % r.returncode
        raise Refusal("git -C %s %s: %s" % (cwd.name, " ".join(args), msg))
    return r if ok != (0,) else (r.stdout if binary else r.stdout.decode("utf-8", "replace"))


def _checkout(name, d):
    """A pin with a "dir" is read from the owner's clone of that name, at the
    pin. A pin with none is read only from the site's own clone under .cache/:
    the organisation's repositories are pinned where GitHub has them, and the
    owner's clones of them were behind it, one with a commit GitHub never had."""
    local = REPOS / d if d else None
    if local is not None and (local / ".git").exists():
        return local
    cached = CACHE / name.replace("/", "--")
    if (cached / "HEAD").exists() or (cached / ".git").exists():
        return cached
    where = local if local is not None else cached
    if not is_public(name):
        raise Unavailable("%s is private and has no clone at %s" % (name, where))
    if os.environ.get("LOGANW_FETCH") != "1":
        raise Unavailable("%s has no clone at %s; set LOGANW_FETCH=1 to fetch it" % (name, where))
    cached.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["git", "clone", "--quiet", "--filter=blob:none", "--no-checkout",
                        "https://github.com/%s/%s" % split(name), str(cached)], capture_output=True)
    if r.returncode != 0:
        raise Refusal("%s: fetching it failed: %s" % (name, r.stderr.decode("utf-8", "replace").strip()))
    return cached


class Pin:
    def __init__(self, name):
        cfg = PINS["repos"].get(name)
        if cfg is None:
            raise Refusal("%s has no pin in pins.json" % name)
        self.name, self.short, self.cfg = name, cfg["commit"], cfg
        self.owner, self.ghname = split(name)
        self.private = not is_public(name)
        self.dir = _checkout(name, cfg.get("dir"))
        self._memo, self._anc = {}, None
        self.full = self.git("rev-parse", "--verify", "--quiet", self.short + "^{commit}").strip()

    def git(self, *args, binary=False):
        # Every read names the pinned commit or is relative to it, so an answer
        # cannot change within a build: ask git once. (The first build spawned
        # a process per CI run and per repeated read, and took 76 s.)
        key = (args, binary)
        if key not in self._memo:
            self._memo[key] = _git(self.dir, *args, binary=binary)
        return self._memo[key]

    def show(self, path, binary=False):
        return self.git("show", "%s:%s" % (self.full, path), binary=binary)

    def has(self, path):
        return _git(self.dir, "cat-file", "-e", "%s:%s" % (self.full, path), ok=(0, 1, 128)).returncode == 0

    def is_ancestor(self, sha):
        """The pinned commit itself, or any commit it descends from."""
        if self._anc is None:
            self._anc = set(self.git("rev-list", self.full).split())
        return sha in self._anc

    def href(self, path="", line=0):
        if self.private:
            return ""
        u = "https://github.com/%s/%s/%s/%s" % (self.owner, self.ghname, "blob" if path else "tree", self.full)
        if path:
            u += "/" + path
        if line:
            u += "#L%d" % line
        return u

    def src(self, kind, where, detail="", path="", line=0):
        return Src(kind, "%s %s %s" % (self.name, self.short, where) if where else "%s %s" % (self.name, self.short),
                   detail, self.href(path, line), self.private)


_PIN = {}


def pin(name):
    if name not in _PIN:
        _PIN[name] = Pin(name)
    return _PIN[name]


def forget_pins():
    _PIN.clear()


# ---------------------------------------------------------------------------
# The facts
# ---------------------------------------------------------------------------

def md_plain(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    return " ".join(s.replace("**", "").replace("`", "").split())


def _line(text, pos):
    return text.count("\n", 0, pos) + 1


@fact
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
             p.src("file", "%s:%d" % (path, line), detail, path, line), raw=quoted, num=num)


@fact
def macros(name, path, names, sep="."):
    """Values of #define lines, joined: read from the definition, not quoted from prose."""
    p = pin(name)
    t = p.show(path)
    vals, first = [], None
    for n in names:
        m = re.search(r"^#define %s (\S+)" % re.escape(n), t, re.M)
        if not m:
            raise Refusal("%s %s %s: no #define %s" % (name, p.short, path, n))
        vals.append(m.group(1))
        first = first or m
    line = _line(t, first.start())
    return V(sep.join(vals), p.src("file", "%s:%d" % (path, line), " and ".join(names), path, line),
             raw=sep.join(vals), num=True)


@fact
def born(name):
    """The day a repository began: its earliest author date at the pin."""
    p = pin(name)
    dates = p.git("log", p.full, "--format=%ad", "--date=short").split()
    if not dates:
        raise Refusal("%s %s: no commits" % (name, p.short))
    return V(min(dates), p.src("git", "git log", "the earliest author date of %d commits" % len(dates)),
             raw=min(dates), num=True)


@fact
def agents(name):
    """Commits carrying a Claude or Gemini Co-Authored-By trailer, of all
    commits at the pin. A trailer, not a line count: it cannot see help that
    was never credited."""
    p = pin(name)
    out = p.git("log", p.full, "--format=%x1e%(trailers:key=Co-Authored-By,valueonly)")
    recs = out.split("\x1e")[1:]
    ai = sum(1 for r in recs if re.search(r"claude|gemini", r, re.I))
    return V("%d/%d" % (ai, len(recs)),
             p.src("git", "git log", "commits with a Claude or Gemini Co-Authored-By trailer, of all commits"),
             raw="%d/%d" % (ai, len(recs)), num=True)


@fact
def api_born(name):
    c = snap()["github_only"][name]
    return V(c["first"], api_src(name, "the earliest of its %d commits" % c["total"]), raw=c["first"], num=True)


@fact
def api_agents(name):
    c = snap()["github_only"][name]
    t = "%d/%d" % (c["agent_coauthored"], c["total"])
    return V(t, api_src(name, "commits with a Claude or Gemini Co-Authored-By trailer, of all commits"),
             raw=t, num=True)


@fact
def api_description(name):
    d = repo_meta(name)["description"] or ""
    if not d:
        raise Refusal("%s has no description on GitHub" % name)
    return V(d, api_src(name, "its description"), raw=d)


@fact
def api_visibility(names):
    """One word for a set of repositories that must share a visibility."""
    vis = {repo_meta(n)["visibility"] for n in names}
    if len(vis) != 1:
        raise Refusal("%s do not share a visibility: %s" % (", ".join(names), sorted(vis)))
    w = vis.pop().lower()
    return V(w, Src("api", "GitHub snapshot %s" % snapdate(), "%s: visibility %s" % (" and ".join(names), w.upper()),
                    "", private=(w == "private")), raw=w)


@fact
def exists(name, path):
    p = pin(name)
    if not p.has(path):
        raise Refusal("%s %s has no %s" % (name, p.short, path))
    return V(path, p.src("git", "", "%s exists at the pin" % path, path), raw=path)


def entries(name, path):
    """A ledger's entries: every `## ` heading, with its date. A heading is
    dated at the start (`## 2026-09-29 - ...`), dated at the end in brackets
    (`## div/sqrt as sequencer programs (2026-09-01)` - one such heading in
    cft-fp256's ledger), or numbered (`## 37. ...`). A numbered one is dated
    by the commit that first wrote its heading, found with `git log -S` at the
    pin: cft-rebound's entries 30 to 33 carry no date anywhere, and the first
    date in a body can be a date the entry only mentions. Anything else is
    refused by name, because a parser that skipped it would drop an entry
    without a word."""
    p = pin(name)
    t = p.show(path)
    heads = list(re.finditer(r"^## (.+)$", t, re.M))
    out = []
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(t)
        title, line = h.group(1).strip(), _line(t, h.start())
        m = re.match(r"(\d{4}-\d{2}-\d{2})\b", title) or re.search(r"\((\d{4}-\d{2}-\d{2})\)$", title)
        if m:
            date, how = m.group(1), "dated"
        elif re.match(r"\d+\.", title):
            dates = p.git("log", "--reverse", "--format=%ad", "--date=short", "-S", h.group(0),
                          p.full, "--", path).split()
            if not dates:
                raise Refusal("%s %s %s:%d: no commit wrote this numbered heading" % (name, p.short, path, line))
            date, how = dates[0], "numbered; dated by the commit that wrote its heading"
        else:
            raise Refusal("%s %s %s:%d: a heading that is neither dated nor numbered: %r"
                          % (name, p.short, path, line, title[:70]))
        out.append(dict(date=date, how=how, title=title, line=line, start=h.start(), end=end))
    return t, out


@fact
def last_verified(name):
    """The newest recorded pass of a repository's own gate, at or before its
    pin. Two records count, each declared in pins.json under verified_by: a run
    of a named CI workflow that succeeded on the pinned commit or an ancestor
    of it, and a ledger line matching a declared pattern, dated by its entry.
    A repository declaring neither shows a dash, and says so."""
    p = pin(name)
    cfg = p.cfg.get("verified_by")
    if not cfg:
        return V("—", p.src("git", "", "records no gate run this site can read (no verified_by in pins.json)"),
                 raw="", num=True)
    cands = []
    for wf in cfg.get("ci", []):
        runs = [r for r in snap()["runs"].get(name, []) if r["workflow"] == wf]
        if not runs:
            raise Refusal("%s: pins.json declares CI workflow %r, and the snapshot has no run of it" % (name, wf))
        ok = [r for r in runs if r["conclusion"] == "success" and p.is_ancestor(r["sha"])]
        if ok:
            r = max(ok, key=lambda r: r["created"])
            src = Src("api", "GitHub snapshot %s" % snapdate(),
                      "%s: workflow %s passed on %s at %s, the newest pass at or before the pin"
                      % (name, wf, r["sha"][:7], r["created"]), "" if p.private else r["url"], p.private)
            cands.append(((r["created"][:10], 1), V(r["created"][:10], src, raw=r["created"], num=True)))
    if "ledger" in cfg:
        path, pat = cfg["ledger"]["path"], cfg["ledger"]["pattern"]
        t, ents = entries(name, path)
        ms = list(re.finditer(pat, t, re.M))
        if not ms:
            raise Refusal("%s %s %s: the declared pass pattern %r matches nothing" % (name, p.short, path, pat))
        m = ms[-1]
        e = [e for e in ents if e["start"] <= m.start() < e["end"]]
        if not e:
            raise Refusal("%s %s %s: the last pass line is above every entry" % (name, p.short, path))
        e, line = e[0], _line(t, m.start())
        src = p.src("file", "%s:%d" % (path, line),
                    "the last of %d lines matching %r, in the entry dated %s" % (len(ms), pat, e["date"]), path, line)
        cands.append(((e["date"], 0), V(e["date"], src, raw=md_plain(m.group(0)), num=True)))
    if not cands:
        return V("—", p.src("git", "", "no recorded pass at or before the pin"), raw="", num=True)
    return max(cands, key=lambda c: c[0])[1]


@fact
def ci_red(name):
    """An open regression the site can see: the newest finished run of a
    declared CI workflow, at or before the pin, that did not pass. Empty when
    every declared workflow's newest run passed - a recorded absence."""
    p = pin(name)
    red = []
    for wf in p.cfg.get("verified_by", {}).get("ci", []):
        runs = [r for r in snap()["runs"].get(name, []) if r["workflow"] == wf and r["status"] == "completed"
                and r["conclusion"] in ("success", "failure", "timed_out") and p.is_ancestor(r["sha"])]
        if runs:
            r = max(runs, key=lambda r: r["created"])
            if r["conclusion"] != "success":
                red.append("%s red since %s" % (wf, r["created"][:10]))
    t = "; ".join(red)
    return V(t, Src("api", "GitHub snapshot %s" % snapdate(),
                    "%s: the newest finished run of each declared workflow at or before the pin" % name,
                    "", p.private), raw=t)


@fact
def stage_count(name, path):
    p = pin(name)
    n = len(re.findall(r'^stage [a-z0-9-]+ "', p.show(path), re.M))
    if not n:
        raise Refusal("%s %s %s: no stage lines" % (name, p.short, path))
    return V(str(n), p.src("file", path, "its stage lines, counted", path), raw=str(n), num=True)


@fact
def last_change(name, path):
    p = pin(name)
    d = p.git("log", "-1", "--format=%ad", "--date=short", p.full, "--", path).strip()
    if not d:
        raise Refusal("%s %s: nothing ever touched %s" % (name, p.short, path))
    return V(d, p.src("git", "git log -- %s" % path, "the last commit touching it", path), raw=d, num=True)


@fact
def count_paths(name, pattern, what):
    p = pin(name)
    n = sum(1 for f in p.git("ls-tree", "-r", "--name-only", p.full).splitlines() if re.fullmatch(pattern, f))
    if not n:
        raise Refusal("%s %s: no path matches %r" % (name, p.short, pattern))
    return V(str(n), p.src("git", "ls-tree", what), raw=str(n), num=True)


@fact
def family(match, exclude):
    """Public repositories whose names match, counted, with the span of their
    creation dates: -> 'N' with raw 'N first last'."""
    rs = [r for r in snap()["repos"] if r["visibility"] == "PUBLIC" and r["name"] not in exclude
          and r.get("owner", OWNER) == OWNER and re.match(match, r["name"], re.I)]
    if not rs:
        raise Refusal("no public repository matches %r" % match)
    first, last = min(r["createdAt"][:10] for r in rs), max(r["createdAt"][:10] for r in rs)
    return V(str(len(rs)), Src("api", "GitHub snapshot %s" % snapdate(),
                               "public repositories under %s matching %r, except %s; created %s to %s"
                               % (OWNER, match, ", ".join(exclude) or "none", first, last)),
             raw="%d %s %s" % (len(rs), first, last), num=True)


@fact
def stated(text, who="Logan", when="2026-09-29"):
    """The owner's word. Rendered as stated, never as sourced."""
    return V(text, Src("stated", "stated", "by %s, %s; no file backs it" % (who, when)), raw=text)


@fact
def pin_count():
    return V(str(len(PINS["repos"])), Src("file", "pins.json", "the repositories this site reads"),
             raw=str(len(PINS["repos"])), num=True)


@fact
def snapshot_date():
    return V(snapdate(), Src("file", PINS["snapshot"], "when the snapshot was taken"), raw=snap()["taken"], num=True)
