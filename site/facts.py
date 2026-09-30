"""The site's facts: every figure it prints, and where each was read.

A figure is read from one of three places, and from nowhere else:

  * a repository at the commit pins.json names - `git show` and `git log`
    at that SHA, never a working tree, where another session may be
    mid-round (docs/SPEC.md, decision 3);
  * the GitHub snapshot pins.json names, taken once by snapshot_github.py;
  * someone's word, which is rendered as STATED, with who said it and when,
    and never as sourced.

Every figure comes out of a function decorated with @fact. The decorator
logs what was read and how - the method, its arguments, the value - and gives
the figure an id. The renderer prints a figure only if it is exactly what the
log holds for its id, and marks it with that id; the `numbers` stage then
refuses a numeral on a page that is not inside such a mark, and any mark
whose text is not its own fact's. So every figure a page prints in digits is
in facts.json - except digits written straight after a letter, which are read
as part of a name (cft-fp256), so "x3397" would pass - and
`build.py --verify-facts` reads each one again: at its pin, or from the
committed snapshot.

What a check here proves, and what it does not:

  * A figure lifted from prose proves that the page quotes the source at the
    pin. It does not prove the source's claim is true; the source's own gates
    do that (ParcelRound, CASE-STUDY-4, observation 14).
  * A figure the page paraphrases (`display`) prints the source's own words
    beside it, and no numeral the source's words do not have. Whether the
    paraphrase keeps the meaning is not checked by any gate: the reader has
    both, side by side.
  * A figure read from the snapshot is compared, on re-reading, with the
    committed snapshot, not with GitHub today. Its label dates it.
  * A figure written in words ("seventy") is seen only for the number words
    the numbers stage lists; "one" and ordinals are ordinary English, and are
    not checked.

A page module may define facts of its own with @fact. Re-derivation imports
the module a fact was defined in, so no parcel needs to edit this file to add
one.
"""
import dataclasses
import datetime
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
    said: str = ""      # the source's own words, when `text` paraphrases them; printed beside it
    id: int = 0         # given by @fact; 0 means no fact produced it


# ---------------------------------------------------------------------------
# Numerals: one definition, used by prose() and by build.py's numbers stage
# ---------------------------------------------------------------------------

_WORD = re.compile(r"[^\s()\[\]{}<>\"'“”‘’,;!?|*`]+")
_SHA = re.compile(r"[0-9a-f]{7,40}")
NUMBER_WORDS = re.compile(
    r"\b(?:two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|"
    r"seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|"
    r"million|billion|dozen|twice|thrice)\b", re.I)


def numerals(s):
    """The tokens of s that are figures: a word with a run of digits that
    starts it or follows anything but a letter or an underscore ("2026-09-29",
    "$5", "=5", "UTF-8"), a version ("v0.9"), or a hex word of 7 to 40
    characters with a digit in it (a commit). A name whose digits follow a
    letter - cft-fp256, binary32.com, Mercenaries2 - is not a figure. A name
    that is caught anyway, like "UTF-8", goes in a page's NUMERAL_NAMES.
    Digits are Arabic digits; "½" and roman numerals are not read."""
    out = []
    for m in _WORD.finditer(s):
        w = m.group(0).rstrip(".:")
        if (re.search(r"(?:^|[^A-Za-z_\d])\d", w) or re.match(r"v\d", w)
                or (_SHA.fullmatch(w) and re.search(r"\d", w))):
            out.append(w)
    return out


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
        LOG.append(record(v, key, dict(bound.arguments)))
        return v

    REGISTRY[key] = fn
    return wrapper


def record(v, method="", args=None):
    return {"id": v.id, "method": method, "args": args or {}, "text": v.text, "raw": v.raw, "said": v.said,
            "num": v.num, "kind": v.src.kind, "where": v.src.short, "detail": v.src.detail,
            "href": v.src.href, "private": v.src.private}


def logged(v):
    """The log's record for a figure, if the figure is exactly what its fact
    returned; None otherwise. A figure copied with its text or source changed
    (dataclasses.replace keeps the id) is not what the log holds."""
    if not isinstance(v, V) or not 0 < v.id <= len(LOG):
        return None
    rec = LOG[v.id - 1]
    mine = record(v, rec["method"], rec["args"])
    return rec if mine == rec else None


def label(rec):
    """A figure's source, as the page prints it after the figure. One
    definition, so the numbers stage can rebuild it from facts.json."""
    body = rec["where"]
    if rec["kind"] != "stated" and rec["private"]:
        body += ", private for now"
    if rec["said"]:
        body += ": “%s”" % rec["said"]
    return "(%s)" % body


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


def github_sha(name):
    """The full SHA GitHub gave for a pin when the snapshot was taken. A pin
    GitHub does not have is refused: its figures could be checked by no one
    else, and its links would not open (atlas-darkroom was pinned at a local
    commit, 2026-09-29). A pin the snapshot never looked up is refused too, so
    moving a pin means taking a new snapshot."""
    short = PINS["repos"][name]["commit"]
    rec = snap().get("pins", {}).get(name)
    if rec is None or rec["commit"] != short:
        raise Refusal("%s: %s did not look up the pin %s; take a new snapshot after moving a pin"
                      % (name, SNAPSHOT.name, short))
    if not rec["sha"]:
        raise Refusal("%s: GitHub did not have the pinned commit %s when %s was taken; push it, or pin a "
                      "commit GitHub has" % (name, short, SNAPSHOT.name))
    return rec["sha"]


def check_pins():
    for name in PINS["repos"]:
        github_sha(name)


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
        want = github_sha(name)
        self.dir = _checkout(name, cfg.get("dir"))
        self._memo, self._anc = {}, None
        self.full = self.git("rev-parse", "--verify", "--quiet", self.short + "^{commit}").strip()
        # A short SHA names a commit only within one repository: a directory
        # that happens to share the name could resolve it to another commit.
        if self.full != want:
            raise Refusal("%s: %s resolves to %s in %s, and to %s on GitHub"
                          % (name, self.short, self.full or "nothing", self.dir, want))

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

    def local(self, iso):
        """A UTC time from the API, on the calendar of the pinned commit's
        author: ledger dates and born dates are the author's own days, and one
        calendar keeps them comparable (verifier-P0: a run three seconds after
        its commit showed as the next day). -> (date, 'YYYY-MM-DD HH:MM +hhmm')."""
        off = self.git("log", "-1", "--format=%ai", self.full).split()[-1]
        sign = -1 if off[0] == "-" else 1
        tz = datetime.timezone(sign * datetime.timedelta(hours=int(off[1:3]), minutes=int(off[3:5])))
        t = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(tz)
        return t.date().isoformat(), "%s %s" % (t.strftime("%Y-%m-%d %H:%M"), off)

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


def check_display(display, quoted):
    """A paraphrase may not bring a numeral or a number word its source's words
    do not have: 'merged into main on 2026-09-27' for 'whether it merges' is
    refused, and so is 'left open for twelve days' (verifier-P0, bc2ffbc)."""
    words = [w.lower() for w in NUMBER_WORDS.findall(quoted)]
    extra = [n for n in numerals(display) if n not in numerals(quoted)]
    extra += [w for w in NUMBER_WORDS.findall(display) if w.lower() not in words]
    if extra:
        raise Refusal("the display %r has %s, which the words it paraphrases (%r) do not"
                      % (display, ", ".join(extra), quoted))


@fact
def prose(name, path, pattern, display=None, last=False, num=False):
    """A figure lifted from a sentence: the file, the line, and the words. A
    pattern must match once; one that matches more than once is refused unless
    the caller asks for the last match, because taking the first silently would
    quote whichever sentence happens to come first."""
    p = pin(name)
    text = p.show(path)
    ms = list(re.finditer(pattern, text, re.M))
    if not ms:
        raise Refusal("%s %s %s: the pattern %r no longer matches" % (name, p.short, path, pattern))
    if len(ms) > 1 and not last:
        raise Refusal("%s %s %s: the pattern %r matches %d times, at lines %s; make it match once, or ask for "
                      "the last" % (name, p.short, path, pattern, len(ms), ", ".join(str(_line(text, m.start())) for m in ms)))
    m = ms[-1]
    line = _line(text, m.start(1))
    quoted = md_plain(m.group(1))
    if display is not None:
        try:
            check_display(display, quoted)
        except Refusal as e:
            raise Refusal("%s %s %s:%d: %s" % (name, p.short, path, line, e))
    detail = "the last of %d matches" % len(ms) if len(ms) > 1 else ""
    return V(display if display is not None else quoted,
             p.src("file", "%s:%d" % (path, line), detail, path, line), raw=quoted, num=num,
             said=quoted if display is not None else "")


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
    """The day a repository began: its earliest author date at the pin, on the
    author's own calendar."""
    p = pin(name)
    dates = p.git("log", p.full, "--format=%ad", "--date=short").split()
    if not dates:
        raise Refusal("%s %s: no commits" % (name, p.short))
    return V(min(dates), p.src("git", "git log", "the earliest author date of %d commits" % len(dates)),
             raw=min(dates), num=True)


AGENT = re.compile(r"^Co-Authored-By:.*\b(?:claude|gemini)\b", re.I | re.M)


def agent_credited(message):
    """The one rule for an agent-credited commit, here and in
    snapshot_github.py: its message has a Co-Authored-By line naming Claude or
    Gemini. It counts commits, so a commit crediting both counts once."""
    return AGENT.search(message) is not None


@fact
def agents(name):
    """Agent-credited commits, of all commits at the pin. A trailer, not a line
    count, and a lower bound: it cannot see help that was never credited."""
    p = pin(name)
    recs = p.git("log", p.full, "--format=%x1e%B").split("\x1e")[1:]
    ai = sum(1 for r in recs if agent_credited(r))
    return V("%d/%d" % (ai, len(recs)),
             p.src("git", "git log", "commits with a Co-Authored-By line naming Claude or Gemini, of all commits"),
             raw="%d/%d" % (ai, len(recs)), num=True)


@fact
def api_born(name):
    c = snap()["github_only"][name]
    return V(c["first"], api_src(name, "the earliest of its %d commits, as a UTC date (the API gives no author's "
                                       "offset)" % c["total"]), raw=c["first"], num=True)


@fact
def api_agents(name):
    c = snap()["github_only"][name]
    t = "%d/%d" % (c["agent_coauthored"], c["total"])
    return V(t, api_src(name, "commits with a Co-Authored-By line naming Claude or Gemini, of all commits"),
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
def pin_commit(name):
    """The commit pins.json names, as GitHub resolved it when the snapshot was
    taken. Read from pins.json and the snapshot alone, so a machine with no
    clone of a private repository can still read it again."""
    sha, (owner, gh) = github_sha(name), split(name)
    pub = is_public(name)
    return V(PINS["repos"][name]["commit"],
             Src("file", "pins.json", "%s is read at %s" % (name, sha),
                 "https://github.com/%s/%s/commit/%s" % (owner, gh, sha) if pub else "", not pub),
             raw=sha, num=True)


@fact
def exists(name, path):
    p = pin(name)
    if not p.has(path):
        raise Refusal("%s %s has no %s" % (name, p.short, path))
    return V(path, p.src("git", "", "%s exists at the pin" % path, path), raw=path)


@fact
def last_commit(name, path):
    """The commit that last wrote a path, at or before the pin."""
    p = pin(name)
    h = p.git("log", "-1", "--format=%H", p.full, "--", path).strip()
    if not h:
        raise Refusal("%s %s: nothing ever touched %s" % (name, p.short, path))
    return V(h[:7], Src("git", "%s %s git log -- %s" % (name, p.short, path), "the last commit touching it: %s" % h,
                        "" if p.private else "https://github.com/%s/%s/commit/%s" % (p.owner, p.ghname, h), p.private),
             raw=h, num=True)


BLOCK_TAGS = ("address|article|aside|base|basefont|blockquote|body|caption|center|col|colgroup|dd|details|"
              "dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|form|frame|frameset|h1|h2|h3|h4|h5|h6|"
              "head|header|hr|html|iframe|legend|li|link|main|menu|menuitem|nav|noframes|ol|optgroup|option|p|"
              "param|search|section|summary|table|tbody|td|tfoot|th|thead|title|tr|track|ul")
_OPEN_TAG = (r"<[A-Za-z][A-Za-z0-9-]*(?:\s+[A-Za-z_:][\w.:-]*(?:\s*=\s*(?:[^\s\"'=<>`]+|'[^']*'|\"[^\"]*\"))?)*"
             r"\s*/?>|</[A-Za-z][A-Za-z0-9-]*\s*>")


def raw_block(s):
    """CommonMark's HTML blocks of types 1 to 5, which end at a marker rather
    than at a blank line: (where the marker may start, the marker as a
    pattern), or None for a line that starts no such block."""
    m = re.match(r" {0,3}<(pre|script|style|textarea)(?=[\s>]|$)", s, re.I)
    if m:
        return m.end(), r"</(?:pre|script|style|textarea)>"
    for start, end in ((r" {0,3}<!--", r"-->"), (r" {0,3}<\?", r"\?>"), (r" {0,3}<![A-Za-z]", r">"),
                       (r" {0,3}<!\[CDATA\[", r"\]\]>")):
        m = re.match(start, s)
        if m:
            return m.end(), end
    return None


def ledger_headings(t):
    """A ledger's level-2 headings: [(offset, '## title', the line as
    written)]. A heading may be indented up to three spaces, or have a tab
    after its marks, as CommonMark allows.

    Not headings, as in CommonMark: a line inside a fenced code block, and a
    line inside an HTML block. An HTML block ends where CommonMark ends it:
      * <pre>, <script>, <style> or <textarea> at the line holding their
        closing tag;
      * a comment at -->, <?...?> at ?>, <!...> at >, and <![CDATA[ at ]]>;
      * a block-level tag's block, or a lone tag's, at the next blank line.
    verifier-P0 built a heading inside a fence that the first parser counted,
    one inside a comment, and one inside a <pre> that spans a blank line.

    Refused, because each renders as a level-2 heading this parser does not
    read, and would drop an entry without a word:
      * a fence or an HTML block still open at the end of the file, where it
        would swallow every heading after it;
      * a setext heading: a line underlined with dashes, even a single one;
      * a heading inside a quote or a list item, however they nest;
      * an HTML <h2>, anywhere outside a code span.
    A refusal can be too eager - a rule after an indented list line, say. It
    is loud, and the ledger can say it another way.

    What holds the rest: the controls read every real ledger a second way,
    with CommonMark's own parser (markdown-it-py, on the desktop and in CI),
    and compare the line and title of every level-2 heading with this
    parser's entries.
    """
    out, fence, html, pos, prev, opened = [], None, None, 0, "", 0
    lines = t.splitlines(keepends=True)
    for i, line in enumerate(lines, 1):
        s = line.rstrip("\r\n")
        m = re.match(r" {0,3}(`{3,}|~{3,})", s)
        code_free = re.sub(r"(`+).*?\1", "", s)
        if html is None and fence is None and re.search(r"<h2\b", code_free, re.I):
            raise Refusal("line %d has an HTML heading, which this parser does not read; write it as '## ...'" % i)
        if fence is not None:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and s.strip() == m.group(1):
                fence = None
        elif html is not None:
            if re.search(r"<h2\b", s, re.I):
                raise Refusal("line %d has an HTML heading inside an HTML block, which this parser does not read" % i)
            if (html == "" and not s.strip()) or (html and re.search(html, s, re.I)):
                html = None
        elif m:
            fence, opened = m.group(1), i
        elif raw_block(s) is not None:
            end = raw_block(s)[1]
            # CommonMark tests the end condition on the whole first line, so
            # <!--> and <!---> are complete comments (verifier-P0)
            if not re.search(end, s, re.I):
                html, opened = end, i
        elif re.match(r" {0,3}</?(?:%s)(?:[\s/>]|$)" % BLOCK_TAGS, s, re.I) \
                or (not prev.strip() and re.match(r" {0,3}(?:%s)\s*$" % _OPEN_TAG, s)):
            html = "" if s.strip() else None
        else:
            h = re.match(r" {0,3}##(?!#)[ \t]+(.*?)\s*$", s)
            if h:
                out.append((pos, "## " + h.group(1), s))
            elif re.match(r" {0,3}-+[ \t]*$", s) and prev.strip() \
                    and not re.match(r" {0,3}(?:#|[-*+] |\d+[.)] |\||>|-+[ \t]*$)", prev):
                raise Refusal("line %d underlines the line above it with dashes, which makes a heading this parser "
                              "does not read; write it as '## ...', or put a blank line before the rule" % i)
            elif re.match(r" {0,3}(?:(?:>|[-*+]|\d{1,9}[.)])[ \t]*)+##(?!#)(?:[ \t]|$)", s):
                raise Refusal("line %d is a heading inside a quote or a list item, which this parser does not read; "
                              "write it as '## ...' at the start of the line" % i)
        # a fence's or an HTML block's own lines end a paragraph, so a rule after one is only a rule
        prev = s if fence is None and html is None and not m else ""
        pos += len(line)
    if fence is not None:
        raise Refusal("the code fence opened at line %d is never closed, so every heading after it would be "
                      "dropped" % opened)
    if html:
        raise Refusal("the HTML block opened at line %d is never closed, so every heading after it would be "
                      "dropped" % opened)
    return out


def entries(name, path):
    """A ledger's entries: every `## ` heading outside a code fence, with its
    date. A heading is dated at the start (`## 2026-09-29 - ...`), dated at the
    end in brackets (`## div/sqrt as sequencer programs (2026-09-01)` - one
    such heading in cft-fp256's ledger), or numbered (`## 37. ...`).

    A numbered one is dated by the first commit, at or before the pin, that
    added its heading's exact text to the file (`git log -S`): cft-rebound's
    entries 30 to 33 carry no date anywhere, and the first date in a body can
    be a date the entry only mentions. That is a stated limit: a heading
    retitled later is dated at its retitling, and one whose exact text sat in
    the file before (in a fence, say) is dated at that earlier commit.

    Anything else is refused by name, because a parser that skipped it would
    drop an entry without a word."""
    p = pin(name)
    t = p.show(path)
    try:
        heads = ledger_headings(t)
    except Refusal as e:
        raise Refusal("%s %s %s: %s" % (name, p.short, path, e))
    out = []
    for i, (start, head, raw) in enumerate(heads):
        end = heads[i + 1][0] if i + 1 < len(heads) else len(t)
        title, line = head[3:].strip(), _line(t, start)
        m = re.match(r"(\d{4}-\d{2}-\d{2})\b", title) or re.search(r"\((\d{4}-\d{2}-\d{2})\)$", title)
        if m:
            date, how = m.group(1), "dated"
        elif re.match(r"\d+\.", title):
            dates = p.git("log", "--reverse", "--format=%ad", "--date=short", "-S", raw,
                          p.full, "--", path).split()
            if not dates:
                raise Refusal("%s %s %s:%d: no commit wrote this numbered heading" % (name, p.short, path, line))
            date, how = dates[0], "numbered; dated by the first commit that added its heading"
        else:
            raise Refusal("%s %s %s:%d: a heading that is neither dated nor numbered: %r"
                          % (name, p.short, path, line, title[:70]))
        out.append(dict(date=date, how=how, title=title, line=line, start=start, end=end))
    return t, out


def verifying(name):
    """The workflows pins.json classes as "verifies" for a pinned repository."""
    return sorted(w for w, c in PINS["repos"][name].get("workflows", {}).items() if c == "verifies")


CLASSES = ("verifies", "builds", "deploys")


def check_workflows():
    """Every workflow the snapshot lists for a pinned repository is classed in
    pins.json, and every class names a workflow that exists. A test workflow
    nothing classed is how Home showed a dash for two repositories whose
    tests had passed (verifier-P0, 2026-09-29)."""
    listed = snap().get("workflows")
    if listed is None:
        raise Refusal("%s lists no workflows; take a new snapshot" % SNAPSHOT.name)
    for name, cfg in PINS["repos"].items():
        have = set(listed.get(name, []))
        classed = cfg.get("workflows", {})
        for w in sorted(have - set(classed)):
            raise Refusal("%s has a workflow %r that pins.json does not class (verifies, builds or deploys)" % (name, w))
        for w, c in sorted(classed.items()):
            if w not in have:
                raise Refusal("pins.json classes %s's workflow %r, which the snapshot does not list" % (name, w))
            if c not in CLASSES:
                raise Refusal("pins.json classes %s's workflow %r as %r; the classes are %s" % (name, w, c, ", ".join(CLASSES)))


def runs(name, wf):
    return [r for r in snap()["runs"].get(name, []) if r["workflow"] == wf]


@fact
def last_verified(name):
    """The newest recorded pass of a repository's own gate, at or before its
    pin, as a date on the pinned commit's author's calendar. Two records count:
    a run of a workflow pins.json classes as "verifies" that succeeded on the
    pinned commit or an ancestor of it; and a ledger line matching one of the
    pass forms pins.json declares under verified_by, dated by its entry. A pass
    recorded in a form nobody declared is not seen; that is the limit of a
    declared form. A repository with neither record shows a dash, and says so."""
    p = pin(name)
    ledger = p.cfg.get("verified_by", {}).get("ledger")
    wfs = verifying(name)
    if not wfs and not ledger:
        return V("—", p.src("git", "", "no workflow of it verifies, and no ledger line is declared as a pass"),
                 raw="", num=True)
    cands = []
    for wf in wfs:
        ok = [r for r in runs(name, wf) if r["conclusion"] == "success" and p.is_ancestor(r["sha"])]
        if ok:
            r = max(ok, key=lambda r: r["created"])
            day, when = p.local(r["created"])
            src = Src("api", "GitHub snapshot %s" % snapdate(),
                      "%s: workflow %s passed on %s, created %s (%s on the pinned commit's calendar); the newest "
                      "pass at or before the pin" % (name, wf, r["sha"][:7], r["created"], when),
                      "" if p.private else r["url"], p.private)
            cands.append(((day, 1), V(day, src, raw=r["created"], num=True)))
    if ledger:
        path = ledger["path"]
        t, ents = entries(name, path)
        found = []
        for what, pat in sorted(ledger["passes"].items()):
            for m in re.finditer(pat, t, re.M):
                e = [e for e in ents if e["start"] <= m.start() < e["end"]]
                if not e:
                    raise Refusal("%s %s %s:%d: a pass line above every entry" % (name, p.short, path, _line(t, m.start())))
                found.append((e[0]["date"], m.start(), what, m))
        if not found:
            raise Refusal("%s %s %s: no declared pass form matches (%s)" % (name, p.short, path, ", ".join(ledger["passes"])))
        date, pos, what, m = max(found, key=lambda f: (f[0], f[1]))
        line = _line(t, pos)
        src = p.src("file", "%s:%d" % (path, line),
                    "the newest of %d lines matching a declared pass form; this one is %s, in the entry dated %s"
                    % (len(found), what, date), path, line)
        cands.append(((date, 0), V(date, src, raw=md_plain(m.group(0)), num=True)))
    if not cands:
        return V("—", p.src("git", "", "no pass recorded at or before the pin, by %s"
                                 % (", ".join(wfs + (["a declared ledger line"] if ledger else [])))),
                 raw="", num=True)
    return max(cands, key=lambda c: c[0])[1]


# A run's conclusion, as the site reads it: a pass, red, or no verdict at all.
# cancelled, skipped, neutral, stale and action_required say nothing about the
# tree, so they are passed over; docs/SPEC.md section 4 says the same.
RED = ("failure", "timed_out", "startup_failure")


@fact
def ci_red(name):
    """An open regression the site can see: for each workflow classed
    "verifies", its newest finished run with a verdict at or before the pin, if
    that verdict is red. Empty when every newest verdict is a pass: a recorded
    absence."""
    p = pin(name)
    red = []
    for wf in verifying(name):
        rs = [r for r in runs(name, wf) if r["status"] == "completed"
              and r["conclusion"] in ("success",) + RED and p.is_ancestor(r["sha"])]
        if rs:
            r = max(rs, key=lambda r: r["created"])
            if r["conclusion"] != "success":
                # "on", not "since": the newest verdict's date says nothing of
                # when the failures began.
                red.append("%s red on %s" % (wf, p.local(r["created"])[0]))
    t = "; ".join(red)
    return V(t, Src("api", "GitHub snapshot %s" % snapdate(),
                    "%s: the newest verdict of each verifying workflow at or before the pin, on the pinned "
                    "commit's calendar" % name, "", p.private), raw=t)


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


def _family(match, exclude):
    rs = [r for r in snap()["repos"] if r["visibility"] == "PUBLIC" and r["name"] not in exclude
          and r.get("owner", OWNER) == OWNER and re.match(match, r["name"], re.I)]
    if not rs:
        raise Refusal("no public repository matches %r" % match)
    return rs, min(r["createdAt"][:10] for r in rs), max(r["createdAt"][:10] for r in rs)


@fact
def family(match, exclude):
    """Public repositories under the owner whose names match, counted."""
    rs, first, last = _family(match, exclude)
    return V(str(len(rs)), Src("api", "GitHub snapshot %s" % snapdate(),
                               "public repositories under %s matching %r, except %s"
                               % (OWNER, match, ", ".join(exclude) or "none")),
             raw=str(len(rs)), num=True)


@fact
def family_span(match, exclude):
    """The first and last creation dates of the same repositories, as month-day
    (UTC, as the API gives them); raw has both in full."""
    rs, first, last = _family(match, exclude)
    return V("%s to %s" % (first[5:], last[5:]),
             Src("api", "GitHub snapshot %s" % snapdate(),
                 "the creation dates of the %d public repositories under %s matching %r, except %s: the first "
                 "and the last, in UTC" % (len(rs), OWNER, match, ", ".join(exclude) or "none")),
             raw="%s %s" % (first, last), num=True)


@fact
def stated(text, who, when, holds_at=None, draft=False):
    """Someone's word, with no file behind it: printed as stated, with who said
    it and when, and never counted as sourced.

    holds_at ties a statement about a repository to the pin it was made at
    ({name: commit}): when that pin moves, the statement refuses the build
    until it is restated or removed, so a statement cannot outlive what it was
    about. draft marks words the lead drafted from someone's own, which they
    have yet to approve; the label says so until they do."""
    for name, commit in (holds_at or {}).items():
        now = PINS["repos"][name]["commit"]
        if now != commit:
            raise Refusal("%s's word of %s, %r, was about %s at %s, and the pin is now %s; restate it or remove it"
                          % (who, when, text, name, commit, now))
    short = ("drafted from %s's words of %s, not yet approved" if draft else "stated by %s, %s") % (who, when)
    return V(text, Src("stated", short, "no file backs it"), raw=text)


@fact
def pin_count():
    return V(str(len(PINS["repos"])), Src("file", "pins.json", "the repositories this site reads"),
             raw=str(len(PINS["repos"])), num=True)


@fact
def snapshot_date():
    return V(snapdate(), Src("file", PINS["snapshot"], "when the snapshot was taken"), raw=snap()["taken"], num=True)


# ---------------------------------------------------------------------------
# The site's own record
# ---------------------------------------------------------------------------
# Two pages state facts about this site's own history: the corrections it has
# made, and the rounds that built it. Their source is this repository's own
# ledger, read from the tree being built. It is not read from a pin, since
# this repository is not one of its own pins. The build's MANIFEST hashes the
# file, so CI checks the published figures against the committed ledger, and
# --verify-facts reads it again from the checkout. The ledger is append-only,
# so a line number, once written, keeps pointing at the same entry, and a
# link to it on main stays true.

OWN = ("docs/VALIDATION.md",)
OWN_REPO = "https://github.com/%s/loganw.dev" % OWNER


def own_text(path):
    if path not in OWN:
        raise Refusal("%s is not part of this site's own record (%s)" % (path, ", ".join(OWN)))
    return (ROOT / path).read_text(encoding="utf-8")


def own_src(path, line, detail=""):
    return Src("file", "this site's %s:%d" % (path, line), detail,
               "%s/blob/main/%s#L%d" % (OWN_REPO, path, line))


@fact
def own_prose(path, pattern, display=None, last=False, num=False):
    """prose(), for this site's own record: the file, the line, and the words,
    under the same rules. The pattern must match once unless the last match
    is asked for, and a paraphrase prints its source's words beside it."""
    text = own_text(path)
    ms = list(re.finditer(pattern, text, re.M))
    if not ms:
        raise Refusal("this site's %s: the pattern %r no longer matches" % (path, pattern))
    if len(ms) > 1 and not last:
        raise Refusal("this site's %s: the pattern %r matches %d times, at lines %s; make it match once, or ask "
                      "for the last" % (path, pattern, len(ms), ", ".join(str(_line(text, m.start())) for m in ms)))
    m = ms[-1]
    line = _line(text, m.start(1))
    quoted = md_plain(m.group(1))
    if display is not None:
        try:
            check_display(display, quoted)
        except Refusal as e:
            raise Refusal("this site's %s:%d: %s" % (path, line, e))
    return V(display if display is not None else quoted,
             own_src(path, line, "the last of %d matches" % len(ms) if len(ms) > 1 else ""),
             raw=quoted, num=num, said=quoted if display is not None else "")


def own_entries(path):
    """This site's own ledger's entries: [dict(date, title, line, start,
    end)], every heading dated at its start (docs/VALIDATION.md writes them so),
    read with the same heading reader as a pinned ledger. A heading that
    is not dated at its start is refused by name."""
    t = own_text(path)
    heads = ledger_headings(t)
    out = []
    for i, (start, head, _) in enumerate(heads):
        title, line = head[3:].strip(), _line(t, start)
        m = re.match(r"(\d{4}-\d{2}-\d{2})\b", title)
        if not m:
            raise Refusal("this site's %s:%d: a heading not dated at its start: %r" % (path, line, title[:70]))
        end = heads[i + 1][0] if i + 1 < len(heads) else len(t)
        out.append(dict(date=m.group(1), title=title, line=line, start=start, end=end))
    return t, out


@fact
def own_entry(path, line):
    """One entry of this site's own ledger, by its heading's line: its title,
    dated. raw is the date alone."""
    for e in own_entries(path)[1]:
        if e["line"] == line:
            return V(e["title"], own_src(path, line, "the entry's own heading"), raw=e["date"])
    raise Refusal("this site's %s has no entry heading at line %d" % (path, line))


@fact
def own_commit(sha, what):
    """A commit in this site's own history, by its hash: one the commit being
    built descends from, so GitHub has it once this build is on main. A
    commit that only a local branch holds, such as a squashed parcel's, is
    refused. A shallow checkout can't show either, and is skipped by name."""
    if _git(ROOT, "rev-parse", "--is-shallow-repository").strip() == "true":
        raise Unavailable("this checkout is shallow, so this site's own history can't be read; "
                          "fetch it whole (fetch-depth: 0)")
    r = _git(ROOT, "rev-parse", "--verify", "-q", sha + "^{commit}", ok=(0, 1))
    if r.returncode != 0:
        raise Refusal("this site's history has no commit %s" % sha)
    full = r.stdout.decode().strip()
    if _git(ROOT, "merge-base", "--is-ancestor", full, "HEAD", ok=(0, 1)).returncode != 0:
        raise Refusal("%s is a commit here, but the commit being built does not descend from it, "
                      "so it is not on main" % sha)
    return V(sha, Src("git", "this site's commit %s" % sha, what, "%s/commit/%s" % (OWN_REPO, full)),
             raw=sha, num=True)
