#!/usr/bin/env python3
"""Build loganw.dev: read the pinned sources, render the pages, write public/.

    python site/build.py                 # write public/ from the pins
    python site/build.py --check         # exit 1 if public/ differs from a fresh render
    python site/build.py --manifest      # public/ matches its own MANIFEST, and so does what the build read
    python site/build.py --verify-facts  # read every figure in public/facts.json again
    python site/build.py --numbers       # every numeral on a page is a figure marked with its own fact
    python site/build.py --links         # every relative link resolves to a published file, exactly
    python site/build.py --local-only    # only allowed tags and attributes; nothing loads from another host
    python site/build.py --docs          # the documents' links resolve, and none states the stage count
    python site/build.py --privacy       # no tracked file names a private repository the site does not read
    python site/build.py --control       # the negative controls; exit 0 only if each fails as it must

Exit codes: 0 pass; 1 a check found a problem; 2 a refusal or misuse; 3 a
source this machine cannot read (a private repository with no clone here), so
the runner can skip the stage by name rather than pass it.

public/ is committed and deployed as it stands (docs/SPEC.md, decisions 3 and
4): the desktop, which has every clone, builds it; --check proves the
committed copy is what the pins render. CI cannot render - it has no private
clone - so it checks the committed copy against its MANIFEST, re-reads every
figure it can, and holds the pages to the numbers, links and local-only rules.

Pages are found by glob in site/pages/, so adding one edits no list here.
"""
import argparse
import contextlib
import hashlib
import html.parser
import io
import json
import os
import pathlib
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import urllib.parse

SITE = pathlib.Path(__file__).resolve().parent
ROOT = SITE.parent
PUBLIC = ROOT / "public"
sys.path.insert(0, str(SITE))

import facts                    # noqa: E402
from facts import Refusal, Unavailable   # noqa: E402
import pages as page_modules    # noqa: E402
import render                   # noqa: E402

BUILD_NOTE = ("This is the committed copy of the site. The deploy replaces this file with the commit it was "
              "deployed from, so a reader can ask which commit a live page came from.\n")
MANIFEST_HEAD = ("# sha256 of every file in public/ except BUILD, which the deploy replaces with the commit it was "
                 "deployed from, and this file. The source lines hash what the build read besides the pinned "
                 "repositories: pins.json, the snapshot, the site's own ledger, and every file under site/.")


def sha256(b):
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def pages():
    mods = page_modules.discover()
    validate(mods)
    return mods


EXTRA_NAME = re.compile(r"[a-z0-9][a-z0-9.-]*\.txt")


def validate(mods):
    for m in mods:
        for need in ("PAGE", "render_page"):
            if not hasattr(m, need):
                raise Refusal("%s defines no %s" % (m.__name__, need))
        if m.PAGE["nav"] not in render.NAV:
            raise Refusal("%s claims nav entry %r, which is not in the navigation" % (m.__name__, m.PAGE["nav"]))
        # Every page is published flat, beside index.html, so that one set of
        # relative links works at loganw.dev/ and at loganw234.github.io/loganw.dev/.
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*\.html", m.PAGE["file"]):
            raise Refusal("%s publishes %r; a page is a flat, lower-case .html name" % (m.__name__, m.PAGE["file"]))
    files = [m.PAGE["file"] for m in mods]
    dup = {x for x in files if files.count(x) > 1}
    if dup:
        raise Refusal("two pages publish the same file: %s" % sorted(dup))
    # A navigation entry may have several pages (a section: the three threads,
    # the dossiers); exactly one of them is the section's own page, which the
    # navigation links to. A lone page is its section's own page.
    for label in {m.PAGE["nav"] for m in mods}:
        group = [m for m in mods if m.PAGE["nav"] == label]
        heads = [m for m in group if m.PAGE.get("index", len(group) == 1)]
        if len(heads) != 1:
            raise Refusal("navigation entry %r has %d pages marked as its own page (index: True); it needs exactly one"
                          % (label, len(heads)))
    for m in mods:
        if hasattr(m, "NUMERAL_NAMES"):
            raise Refusal("%s allows names of its own; a name with a numeral goes in site/data/numeral_names.json, "
                          "which the lead reviews" % m.__name__)


def collect_extras(m, ctx, text):
    """A page may publish text files of its own - a dossier's plain-text twin -
    through extra_files(ctx) -> {flat name: text}. The one place they are taken
    in, so the control below exercises the path the build uses."""
    if not hasattr(m, "extra_files"):
        return
    for name, t in m.extra_files(ctx).items():
        if not EXTRA_NAME.fullmatch(name):
            raise Refusal("%s publishes %r; an extra file is a flat, lower-case .txt name" % (m.__name__, name))
        if name in text:
            raise Refusal("%s publishes %s, which another page already publishes" % (m.__name__, name))
        text[name] = t


def section_index(mods):
    """-> {navigation label: the file the navigation links to}."""
    out = {}
    for m in mods:
        group = [g for g in mods if g.PAGE["nav"] == m.PAGE["nav"]]
        if m.PAGE.get("index", len(group) == 1):
            out[m.PAGE["nav"]] = m.PAGE["file"]
    return out


BINARY_SOURCES = {".woff2", ".png", ".jpg", ".jpeg", ".webp"}   # .gitattributes: stored as they are


def sources():
    """What the build read besides the pins, by path: pins.json, the snapshot,
    the site's own ledger, and every file under site/ - the code, its data,
    the fonts and the stylesheets. CI checks each against the checkout, so a
    change to any of them that was not rebuilt into public/ fails there too.

    A text file holding a carriage return is refused. The repository stores
    LF (.gitattributes), so git calls a CRLF copy unchanged, while its hash
    here would not be the committed file's: the desktop would pass what CI
    then fails (verifier-seam)."""
    site = sorted(f.relative_to(ROOT).as_posix() for f in SITE.rglob("*")
                  if f.is_file() and "__pycache__" not in f.parts)
    return lf_only([(p, (ROOT / p).read_bytes())
                    for p in ["pins.json", facts.PINS["snapshot"]] + list(facts.OWN) + site])


def lf_only(pairs):
    """pairs, or a refusal naming the first text file that holds a carriage
    return (sources() says why)."""
    for p, b in pairs:
        if b"\r" in b and posixpath.splitext(p)[1].lower() not in BINARY_SOURCES:
            raise Refusal("%s holds a carriage return; the repository stores it with LF line endings, so this copy's "
                          "hash is not the committed file's. Save it with LF." % p)
    return pairs


def render_all():
    """-> (text files, binary files), each {published path: content}."""
    facts.reset_log()
    facts.check_workflows()
    facts.check_pins()
    mods = pages()
    built = section_index(mods)
    pages_by_nav = {}
    for m in mods:
        pages_by_nav.setdefault(m.PAGE["nav"], []).append(m.PAGE["file"])
    text, binary = {}, {}
    for m in mods:
        ctx = {"built": built, "pages": pages_by_nav}
        body = m.render_page(ctx)
        text[m.PAGE["file"]] = render.page(m.PAGE["title"], m.PAGE["nav"], built, body, m.PAGE["description"])
        for dest, repo, path in getattr(m, "ASSETS", []):
            data = facts.pin(repo).show(path, binary=True)
            check_asset(dest, data)
            if dest in binary:
                raise Refusal("%s publishes %s, which another page already publishes" % (m.__name__, dest))
            binary[dest] = data
        collect_extras(m, ctx, text)
    # One stylesheet per parcel under site/styles/, found by glob, so no two
    # parcels edit the same file (ParcelRound section 2: aim for a glob). It is
    # UTF-8 and says so, so no escape is needed in it; local-only refuses one.
    text["style.css"] = '@charset "utf-8";\n' + "".join(
        f.read_text(encoding="utf-8") for f in
        [SITE / "fonts" / "fontfaces.css", SITE / "style.css"] + sorted((SITE / "styles").glob("*.css")))
    for f in sorted((SITE / "fonts").iterdir()):
        if f.suffix == ".woff2":
            binary["fonts/" + f.name] = f.read_bytes()
        elif f.name.startswith("OFL") or f.name == "SOURCES.txt":
            text["fonts/" + f.name] = f.read_text(encoding="utf-8")
    text["BUILD"] = BUILD_NOTE
    text["facts.json"] = json.dumps({
        "about": "Every figure on this site, where it was read, and how to read it again: "
                 "python site/build.py --verify-facts",
        "pins": {k: v["commit"] for k, v in facts.PINS["repos"].items()},
        "snapshot": facts.PINS["snapshot"],
        "facts": facts.LOG,
    }, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    lines = [MANIFEST_HEAD,
             "# pins: " + " ".join("%s@%s" % (k, v["commit"]) for k, v in facts.PINS["repos"].items())]
    lines += ["# source %s %s" % (p, sha256(b)) for p, b in sources()]
    for path in sorted(list(text) + list(binary)):
        if path == "BUILD":
            continue
        data = text[path].encode("utf-8") if path in text else binary[path]
        lines.append("%s  %s" % (sha256(data), path))
    text["MANIFEST"] = "\n".join(lines) + "\n"
    return text, binary


def published(root):
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())


def inside(root, rel):
    """rel names a file under root: relative, no '..', no drive. verifier-P0
    wrote into site/data/ through an asset named '../site/data/...'."""
    parts = rel.split("/")
    return bool(rel) and not rel.startswith("/") and "\\" not in rel and ":" not in rel \
        and all(p not in ("", ".", "..") for p in parts)


def write(text, binary, root=PUBLIC):
    bad = sorted(r for r in set(text) | set(binary) if not inside(root, r))
    if bad:
        raise Refusal("the build would write outside public/: %s" % ", ".join(bad))
    root.mkdir(parents=True, exist_ok=True)
    want = set(text) | set(binary)
    for rel in published(root):
        if rel not in want:
            (root / rel).unlink()     # a page that is no longer rendered is no longer published
    for rel, t in text.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(t, encoding="utf-8", newline="\n")
    for rel, b in binary.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_bytes(b)


def compare(text, binary, root=PUBLIC):
    problems = []
    for rel, want in text.items():
        f = root / rel
        if not f.is_file():
            problems.append("%s is missing" % rel)
            continue
        have = f.read_bytes().decode("utf-8", "replace")
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
            problems.append("%s is missing, or not the bytes its source gives" % rel)
    extra = set(published(root)) - set(text) - set(binary) if root.is_dir() else set()
    problems += ["%s is published and no longer rendered" % e for e in sorted(extra)]
    return problems


# ---------------------------------------------------------------------------
# Checks on what is published. Each reads public/ alone, so CI runs them.
# ---------------------------------------------------------------------------

def check_manifest(root=PUBLIC):
    """public/ is what its MANIFEST says, file for file, and what the build
    read besides the pins (sources()) is the bytes it read. What CI can hold without rendering:
    a deleted page, or a page edited by hand without its MANIFEST line, fails
    here. A hand edit that also rewrites MANIFEST passes; only --check, on the
    desktop, sees that (a stated limit)."""
    mf = root / "MANIFEST"
    if not mf.is_file():
        return ["MANIFEST is missing"]
    problems, listed, srcs = [], {}, {}
    for line in mf.read_text(encoding="utf-8").splitlines():
        if line.startswith("# source "):
            _, _, path, h = line.split(" ")
            srcs[path] = h
        elif line and not line.startswith("#"):
            h, path = line.split("  ", 1)
            listed[path] = h
    for path, h in sorted(listed.items()):
        f = root / path
        if not f.is_file():
            problems.append("%s is in MANIFEST and not published" % path)
        elif sha256(f.read_bytes()) != h:
            problems.append("%s is not the bytes MANIFEST lists" % path)
    for path in published(root):
        if path not in listed and path not in ("BUILD", "MANIFEST"):
            problems.append("%s is published and not in MANIFEST" % path)
    if not (root / "BUILD").is_file():
        problems.append("BUILD is missing")
    elif root == PUBLIC and (root / "BUILD").read_text(encoding="utf-8") != BUILD_NOTE:
        problems.append("BUILD is not the committed note; only the deploy rewrites it")
    now = {p for p, _ in sources()}
    for path in sorted(now | set(srcs)):
        if path not in srcs:
            problems.append("MANIFEST does not hash %s, which the build reads: public/ was built before it existed" % path)
        elif path not in now:
            problems.append("MANIFEST hashes %s, which no longer exists: public/ was built from a tree that had it" % path)
        elif sha256((ROOT / path).read_bytes()) != srcs[path]:
            problems.append("%s is not the bytes the build read: it changed, and public/ was not rebuilt" % path)
    return problems + check_font_sources(root)


def check_font_sources(root=PUBLIC):
    """fonts/SOURCES.txt is published with figures in it - each file's size
    and sha256, and the total of the eight - which the numbers stage does not
    read, since no fact holds them. They are checked here instead, against the
    files in site/fonts/ that the build copies."""
    f = root / "fonts" / "SOURCES.txt"
    if not f.is_file():
        return ["fonts/SOURCES.txt is missing"]
    problems, total, n = [], 0, 0
    t = f.read_text(encoding="utf-8")
    for name, size, h in re.findall(r"^(\S+)\s+(\d+) bytes\s+sha256 ([0-9a-f]{64})$", t, re.M):
        src = SITE / "fonts" / name
        if not src.is_file():
            problems.append("fonts/SOURCES.txt lists %s, which site/fonts/ does not have" % name)
            continue
        b = src.read_bytes()
        if len(b) != int(size) or sha256(b) != h:
            problems.append("fonts/SOURCES.txt's size or sha256 for %s is not the file's" % name)
        if name.endswith(".woff2") or name.startswith("OFL"):
            total, n = total + len(b), n + 1
    m = re.search(r"all (\w+) files, ([\d,]+) bytes", t)
    words = {"eight": 8}
    if not m or words.get(m.group(1), -1) != n or int(m.group(2).replace(",", "")) != total:
        problems.append("fonts/SOURCES.txt's total is not the %d files' %d bytes" % (n, total))
    for g in sorted((SITE / "fonts").iterdir()):
        if (g.suffix == ".woff2" or g.name.startswith("OFL")) and not re.search(r"^%s\s" % re.escape(g.name), t, re.M):
            problems.append("site/fonts/%s is published and fonts/SOURCES.txt does not list it" % g.name)
    return problems


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
TICK = re.compile(r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?: \d{4})?")


class _Marks(html.parser.HTMLParser):
    """Every figure mark (data-f) with its text, and every run of text outside one."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.marks, self.loose, self.attr_text, self.problems = [], [], [], [], []
        self.last = None       # the figure that just closed, until anything but its label follows it

    def _mark(self):
        return next((n for n in reversed(self.stack) if n["f"] is not None), None)

    def _attrs(self, tag, attrs):
        # Every value, not a dict's last one: a browser keeps the first of two
        # same-named attributes, and dict() keeps the last (verifier-P0 hid
        # "3397 prints" in the first of two alt attributes).
        for k, v in attrs:
            if k in ("alt", "title", "aria-label") and v:
                self.attr_text.append("%s %s=%r" % (tag, k, v))
        a = dict(attrs)
        if tag == "meta" and a.get("name") == "description":
            self.attr_text.append("meta description %r" % a.get("content", ""))
        if dupes(attrs):
            self.problems.append("<%s> repeats %s" % (tag, ", ".join(dupes(attrs))))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self._attrs(tag, attrs)
        if tag in VOID:
            return
        cls, f = (a.get("class") or "").split(), a.get("data-f")
        if f is None and tag == "span" and set(cls) & {"fig", "q", "stated", "src"}:
            self.problems.append("a span of class %r has no fact id" % " ".join(cls))
        if f is not None and self._mark() is not None:
            self.problems.append("a mark for fact %s sits inside the mark for fact %s" % (f, self._mark()["f"]))
        if tag == "a" and self._mark() is not None:
            self._mark()["href"] = a.get("href", "")
        inside = lambda t, c=None: tag == t or any(n["tag"] == t and (c is None or c in n["cls"]) for n in self.stack)
        node = dict(tag=tag, cls=cls, f=f, buf=[], href=None, beside=False, footer=inside("footer"),
                    svg=inside("svg"), evidence=any(n["tag"] == "details" and "evidence" in n["cls"] for n in self.stack))
        # A label opening straight after its own figure is the label beside it.
        if f is not None and "src" in cls and self.last is not None and self.last["f"] == f:
            self.last["beside"] = True
        if self._mark() is None:
            self.last = None
        self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self._attrs(tag, attrs)
        if self._mark() is None:
            self.last = None

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        closed = None
        while self.stack:
            n = self.stack.pop()
            if n["f"] is not None:
                self.marks.append(n)
            if n["tag"] == tag:
                closed = n
                break
        if self._mark() is None:
            self.last = closed if closed is not None and closed["f"] is not None and "src" not in closed["cls"] else None

    def handle_data(self, data):
        m = self._mark()
        if m is not None:
            m["buf"].append(data)
        elif data.strip():
            self.last = None
            # A month tick on a chart's axis: SVG text of class tick, inside an
            # svg, and nothing else, however it is classed.
            tick = bool(self.stack) and self.stack[-1]["tag"] == "text" and "tick" in self.stack[-1]["cls"] \
                and any(n["tag"] == "svg" for n in self.stack)
            self.loose.append((data, tick))


def dupes(attrs):
    names = [k for k, _ in attrs]
    return sorted({k for k in names if names.count(k) > 1})


NAMES_FILE = SITE / "data" / "numeral_names.json"


NAME_SHAPE = re.compile(r"[A-Z][A-Za-z]*(?:[ -][A-Z][A-Za-z]*)*[ -]\d+(?:\.\d+)?")


def numeral_names():
    """{name: why}: names with a numeral in them that are not figures. One
    file, the lead's, so an allowance is a reviewed change and not a line in a
    page module (verifier-P0 allowed "4096 tests" from a page). Each name must
    also appear in some fact's text, so no name is invented here."""
    return json.loads(NAMES_FILE.read_text(encoding="utf-8"))["names"] if NAMES_FILE.is_file() else {}


def _loose_problems(where, text, tick, names, allowed):
    out = []
    if tick and TICK.fullmatch(text.strip()):
        return out
    for n in sorted(names, key=len, reverse=True):
        if n in text:
            allowed[n] = allowed.get(n, 0) + text.count(n)
            text = text.replace(n, " ")
    for n in facts.numerals(text):
        out.append("%s: %r is a numeral outside any figure's mark, in %r" % (where, n, " ".join(text.split())[:80]))
    for w in facts.NUMBER_WORDS.findall(text):
        out.append("%s: %r is a number word outside any figure's mark, in %r" % (where, w, " ".join(text.split())[:80]))
    return out



# Declarations that hide an element or its text. A page's figures and their
# sources are in its HTML, and a stylesheet could hide them there: verifier-P0
# added `.src{display:none}` and 49 of 124 labels vanished, then
# `.src{color:rgba(0,0,0,0)}` and all 124 did, with every stage passing. A
# rule that hides is refused unless site/data/css_hides.json - the lead's -
# names its selector and the declaration it may use, with why.
#
# The check reads CSS text; it does not render. What it refuses is exactly
# this list, and the README gives the same list and says that anything else
# passes. Property names are read without a vendor prefix (-webkit-clip-path
# is clip-path).
#   * display:none; visibility:hidden or collapse; content-visibility:hidden.
#   * opacity, fill-opacity, font-size, scale or zoom at zero or below, or
#     computed with calc(), min(), max() or clamp(); a font shorthand whose
#     size is zero or computed; a transform with scale() at zero or computed,
#     or with matrix(); an opacity() filter at zero or below, or computed.
#   * In color, fill and text-fill-color: the word transparent; a hex colour
#     whose alpha is zero; a colour function whose alpha is zero or below, or
#     computed. And fill:none.
#   * clip, clip-path, mask and mask-image, other than none or auto; and
#     text-indent other than zero.
# A custom property is read as every value the stylesheet gives it: in a
# rule, as a var() fallback, or as an @property's initial-value.
HIDES_FILE = SITE / "data" / "css_hides.json"
_NUM = r"[+-]?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?"
_MATH = re.compile(r"\b(?:calc|min|max|clamp)\s*\(", re.I)


def _nonpositive(tok):
    """A number token, with or without a unit, that is zero or below."""
    m = re.fullmatch(r"(%s)(?:[a-z]+|%%)?" % _NUM, tok.strip(), re.I)
    return bool(m) and float(m.group(1)) <= 0


def css_tokens(css):
    """A stylesheet as CSS Syntax 3 cuts it, as far as this site needs:
    [(kind, text, flaw)], where kind is 'comment', 'string', 'url' or 'char'.
    A string ends at its closing quote or, left open, at the end of its line
    (flaw 'open'); an unquoted url( runs to its first ')', and a quote,
    space, '(' or '{', '}' or ';' inside it makes it malformed (flaw 'bad'),
    as a browser reads it - never a string (verifier-P0 hid display:none
    behind url(x.png') ). One reading, used by every check of a stylesheet."""
    # CSS Syntax 3 first turns CR LF, CR and form feed into LF, and NUL into
    # U+FFFD; a browser ends a string at a form feed, and so must this
    # (verifier-P0 hid display:none behind one).
    css = css.replace("\r\n", "\n").replace("\r", "\n").replace("\f", "\n").replace("\0", "�")
    out, i, n = [], 0, len(css)
    while i < n:
        if css.startswith("/*", i):
            j = css.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append(("comment", css[i:j], "" if css.endswith("*/", 0, j) and j - i >= 4 else "open"))
            i = j
        elif css[i] in "\"'":
            q, j = css[i], i + 1
            while j < n and css[j] != q and css[j] != "\n":
                j += 2 if css[j] == "\\" else 1
            closed = j < n and css[j] == q
            out.append(("string", css[i:j + 1 if closed else j], "" if closed else "open"))
            i = j + 1 if closed else j
        elif css[i:i + 4].lower() == "url(" and (i == 0 or not re.match(r"[\w-]", css[i - 1])):
            k = i + 4
            while k < n and css[k] in " \t\n":
                k += 1
            if k < n and css[k] in "\"'":
                out.append(("char", css[i:k], ""))       # url( with a string: the string comes next
                i = k
                continue
            j = css.find(")", k)
            j = n if j < 0 else j + 1
            body = css[k:j - 1].rstrip(" \t\n")
            out.append(("url", css[i:j], "bad" if re.search(r"[\"'(\s{};]", body) else ""))
            i = j
        else:
            out.append(("char", css[i], ""))
            i += 1
    return out


def css_parts(css):
    """-> (code, strings, urls): the stylesheet with its comments dropped and
    each string emptied to "", so a pattern searched in code never matches
    inside a string or a comment; every string's contents; and every url()'s
    address, quoted or not. Every check of a stylesheet reads it through
    this, so none can be misled by a comment marker a regex would see and
    CSS would not (verifier-P0)."""
    code, strings, urls, pending = [], [], [], False
    for kind, text, _ in css_tokens(css):
        if kind == "comment":
            code.append(" ")
        elif kind == "string":
            body = text[1:-1] if len(text) > 1 and text[-1] == text[0] else text[1:]
            strings.append(body)
            code.append('""')
            if pending:
                urls.append(body)
        elif kind == "url":
            urls.append(text[4:-1].strip() if text.endswith(")") else text[4:].strip())
            code.append("url()")
        else:
            code.append(text)
        pending = kind == "char" and text.lower().replace(" ", "").endswith("url(")
    return "".join(code), strings, urls


def _decls(css):
    """[(prelude, [(property, value)])] for every block, at any depth: the
    declarations directly inside it, beside any block nested in it. With CSS
    nesting, `.src{display:none; .x{...}}` and `.src{@media all{display:none}}`
    both apply display:none to .src, and verifier-P0 hid 49 labels with the
    second while a reader of innermost rules alone passed it. Built on
    css_tokens, so a brace or a semicolon inside a string or a url() is not
    structure, and comments are dropped as CSS drops them."""
    stack, out, seg = [["", []]], [], []
    for kind, text, _ in css_tokens(css):
        if kind == "comment":
            continue
        if kind != "char" or text not in "{};":
            seg.append(text)
            continue
        if text == "{":
            stack.append(["".join(seg).strip(), []])
            seg = []
            continue
        d = "".join(seg).strip()
        if d:
            stack[-1][1].append(d)
        seg = []
        if text == "}" and len(stack) > 1:
            out.append(tuple(stack.pop()))
    rules = []
    for prelude, parts in out:
        pairs = []
        for d in parts:
            if ":" in d:
                k, _, v = d.partition(":")
                pairs.append((k.strip().lower(), re.sub(r"!\s*important", "", v, flags=re.I).strip()))
        rules.append((" ".join(prelude.split()), pairs))
    return rules


def _var(v):
    """The first var() in v, as (start, end, name, fallback or None), reading
    its parentheses as nested, so a fallback like rgb(1 2 3) is whole."""
    m = re.search(r"var\(\s*(--[\w-]+)\s*", v)
    if not m:
        return None
    depth, i, comma = 1, m.end(), None
    while i < len(v) and depth:
        c = v[i]
        depth += c == "("
        depth -= c == ")"
        if c == "," and depth == 1 and comma is None:
            comma = i
        i += 1
    end = i
    fallback = v[comma + 1:end - 1].strip() if comma is not None else None
    return m.start(), end, m.group(1), fallback


def _variants(v, defs, depth=0):
    """Every value v can take once each var() is replaced by any definition
    of its custom property, or by its fallback."""
    found = _var(v)
    if not found or depth > 6:
        return [v]
    start, end, name, fallback = found
    subs = list(defs.get(name, [])) + ([fallback] if fallback is not None else [])
    out = []
    for s in subs or [""]:
        out += _variants(v[:start] + s + v[end:], defs, depth + 1)
    return out


def _alpha_hides(alpha):
    alpha = alpha.strip()
    return bool(_MATH.search(alpha)) or _nonpositive(alpha)


def _zero_alpha(v):
    v = v.lower()
    if "transparent" in v:
        return True
    for h in re.findall(r"#([0-9a-f]{4}|[0-9a-f]{8})\b", v):
        if (len(h) == 4 and h[3] == "0") or (len(h) == 8 and h[6:] == "00"):
            return True
    for m in re.finditer(r"\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\(", v):
        depth, i = 1, m.end()
        while i < len(v) and depth:
            depth += v[i] == "("
            depth -= v[i] == ")"
            i += 1
        args = v[m.end():i - 1]
        top = re.sub(r"\([^()]*\)", lambda x: x.group(0).replace(",", " ").replace("/", " "), args)
        if "/" in top:
            alpha = args[top.index("/") + 1:]
        elif top.count(",") >= 3:
            alpha = args[[k for k, c in enumerate(top) if c == ","][2] + 1:]
        else:
            continue
        if _alpha_hides(alpha):
            return True
    return False


def _hides(prop, v):
    """Why (prop: v) hides what it styles, or None."""
    prop = re.sub(r"^-(?:webkit|moz|ms|o)-", "", prop)
    lv = v.lower().strip()
    if prop == "display" and lv == "none":
        return "display:none"
    if prop == "visibility" and lv in ("hidden", "collapse"):
        return "visibility:%s" % lv
    if prop == "content-visibility" and lv == "hidden":
        return "content-visibility:hidden"
    if prop in ("opacity", "fill-opacity", "font-size", "scale", "zoom"):
        if _MATH.search(lv):
            return "%s computed with a function this does not evaluate" % prop
        if any(_nonpositive(part) for part in lv.split()):
            return "%s at zero or below" % prop
    if prop == "font":
        size = re.search(r"(?:^|\s)(%s)(?:[a-z]+|%%)?(?=\s*/|\s|$)" % _NUM, lv)
        if (size and float(size.group(1)) <= 0) or _MATH.search(lv):
            return "a font shorthand whose size is zero or computed"
    if prop == "transform":
        for m in re.finditer(r"scale[xyz3d]*\(([^()]*(?:\([^()]*\)[^()]*)*)\)", lv):
            if _MATH.search(m.group(1)) or any(_nonpositive(p) for p in re.split(r"[\s,]+", m.group(1)) if p):
                return "a transform that scales to nothing"
        if re.search(r"\bmatrix(?:3d)?\(", lv):
            return "a transform with matrix()"
    if prop == "filter":
        for m in re.finditer(r"opacity\(([^()]*(?:\([^()]*\)[^()]*)*)\)", lv):
            if _alpha_hides(m.group(1)):
                return "an opacity filter at zero"
    if prop in ("color", "fill", "text-fill-color") and (_zero_alpha(lv) or (prop == "fill" and lv == "none")):
        return "%s with no colour" % prop
    if prop in ("clip", "clip-path", "mask", "mask-image") and lv not in ("none", "auto"):
        return prop
    if prop == "text-indent" and not re.fullmatch(r"[+-]?0*\.?0+(?:[a-z]+|%)?", lv):
        return "text-indent"
    return None


def hiding_problems(css):
    """Every rule that hides what it styles, as the list above reads it."""
    return hiding_in(_decls(css))


def tinycss2_blocks(css):
    """The same [(prelude, [(property, value)])] as _decls, every block at any
    depth, children before their parent - but read by tinycss2, a parser that
    follows CSS Syntax 3 and CSS nesting. The controls compare the two
    readings of the published stylesheet (verifier-P0 found four ways, one
    after another, in which a hand-written reading and a browser's parted;
    Logan approved installing a parser for this, 2026-09-29)."""
    import tinycss2
    out = []

    def walk(node):
        pre = tinycss2.serialize(node.prelude)
        if node.type == "at-rule":
            pre = "@%s %s" % (node.at_keyword, pre)
        decls = []
        for x in tinycss2.parse_blocks_contents(node.content, skip_comments=True, skip_whitespace=True):
            if x.type == "declaration":
                decls.append((x.lower_name, tinycss2.serialize([v for v in x.value if v.type != "comment"]).strip()))
            elif x.type in ("qualified-rule", "at-rule") and x.content is not None:
                walk(x)
        out.append((" ".join(pre.split()), decls))

    for r in tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True):
        if r.type in ("qualified-rule", "at-rule") and r.content is not None:
            walk(r)
    return out


def crosscheck_css(css, reader=None):
    """Where this build's reading of a stylesheet and tinycss2's part: [str].
    Empty when every block has the same prelude and the same properties in
    the same order, and the hiding check finds the same problems in both."""
    mine, theirs = (reader or _decls)(css), tinycss2_blocks(css)
    squash = lambda s: "".join(s.split())
    out = []
    if len(mine) != len(theirs):
        out.append("this build reads %d blocks, and tinycss2 reads %d" % (len(mine), len(theirs)))
    for (p1, d1), (p2, d2) in zip(mine, theirs):
        if squash(p1) != squash(p2) or [k for k, _ in d1] != [k for k, _ in d2]:
            out.append("the block %r reads as %r here and as %r in tinycss2"
                       % (p2, [k for k, _ in d1], [k for k, _ in d2]))
            break
    if hiding_in(mine) != hiding_in(theirs):
        out.append("the hiding check finds %r here and %r in tinycss2's reading"
                   % (hiding_in(mine)[:1], hiding_in(theirs)[:1]))
    return out


class _Holders(html.parser.HTMLParser):
    """Every element carrying one of the given classes: its tag, the tags of
    its direct children, and whether text sits directly in it."""
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self, classes):
        super().__init__(convert_charrefs=True)
        self.classes, self.stack, self.found = classes, [], []

    def _open(self, tag, attrs, closes):
        if self.stack and self.stack[-1] is not None:
            self.stack[-1]["children"].append(tag)
        hit = set((dict(attrs).get("class") or "").split()) & self.classes
        rec = dict(tag=tag, classes=hit, children=[], text=False) if hit else None
        if rec:
            self.found.append(rec)
        if not closes and tag not in self.VOID:
            self.stack.append(rec)

    def handle_starttag(self, tag, attrs):
        self._open(tag, attrs, False)

    def handle_startendtag(self, tag, attrs):
        self._open(tag, attrs, True)

    def handle_endtag(self, tag):
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if self.stack and self.stack[-1] is not None and data.strip():
            self.stack[-1]["text"] = True


def holder_problems(page):
    """css_hides.json lets a selector hide what it styles, and names the
    elements its class may be on: "div>svg" is a div holding one svg and
    nothing else. The class on any other element is refused, since that
    element would be hidden with it. verifier-seam gave Verify's source
    labels the narrow map's class, and at one width they vanished while
    every stage passed."""
    allowed = json.loads(HIDES_FILE.read_text(encoding="utf-8"))["selectors"] if HIDES_FILE.is_file() else {}
    on, out = {}, []
    for sel, entry in sorted(allowed.items()):
        m = re.search(r"\.([\w-]+)$", sel.strip())
        if not m or not entry.get("on"):
            out.append("%s's entry %r names no class, or no element that class may be on" % (HIDES_FILE.name, sel))
            continue
        on.setdefault(m.group(1), set()).update(entry["on"])
    p = _Holders(set(on))
    p.feed(page)
    p.close()
    for rec in p.found:
        for cls in sorted(rec["classes"]):
            forms = on[cls]
            if rec["tag"] in forms or ("div>svg" in forms and rec["tag"] == "div"
                                       and rec["children"] == ["svg"] and not rec["text"]):
                continue
            out.append("a <%s> carries the class %r, which %s lets a stylesheet hide only on %s"
                       % (rec["tag"], cls, HIDES_FILE.name, ", ".join(sorted(forms))))
    return out


def hiding_in(rules):
    """The hiding check over one reading of a stylesheet's blocks."""
    allowed = json.loads(HIDES_FILE.read_text(encoding="utf-8"))["selectors"] if HIDES_FILE.is_file() else {}
    defs = {}
    for sel, pairs in rules:
        prop_rule = re.fullmatch(r"@property\s+(--[\w-]+)", sel)
        for k, v in pairs:
            if k.startswith("--"):
                defs.setdefault(k, []).append(v)
            elif prop_rule and k == "initial-value":
                defs.setdefault(prop_rule.group(1), []).append(v)
    out = []
    for sel, pairs in rules:
        # Every block is read, at-rules too: @media, @supports, @scope and the
        # rest hold declarations that apply (verifier-P0). A nested block is
        # named by its own prelude, and css_hides.json names flat selectors,
        # so a nested hiding rule is refused however it is allowed flat.
        ok = {re.sub(r"\s+", "", d.lower()) for d in allowed.get(sel, {}).get("allow", [])}
        for k, v in pairs:
            if k.startswith("--") or re.sub(r"\s+", "", "%s:%s" % (k, v)).lower() in ok:
                continue
            why = next((w for w in (_hides(k, x) for x in _variants(v, defs)) if w), None)
            if why:
                out.append("%r hides what it styles (%s: %s); a selector that may hide goes in %s, with the "
                           "declaration it may use, which the lead reviews" % (sel, k, v, HIDES_FILE.name))
                break
    return out


def check_numbers(root=PUBLIC, names=None):
    """Every numeral a page prints sits inside a mark (data-f) for a fact whose
    text is exactly the mark's text; every source label is its own fact's
    label; and a text file writes each figure as `text [fact N]`. So a figure
    typed as a plain string, or copied with its text changed, fails. A number
    written in words is caught only for the words facts.NUMBER_WORDS lists.
    A stylesheet can print text too - generated content, quotes, list
    markers, counters - so every string in one is held to the same rule, and
    counters, which print numbers without a string, are refused. The text
    files under fonts/ are not read here: the licences are published as
    given, and the figures in SOURCES.txt are checked by --manifest against
    the fonts' own bytes."""
    fj = root / "facts.json"
    if not fj.is_file():
        return ["facts.json is missing"], None
    recs = json.loads(fj.read_text(encoding="utf-8"))["facts"]
    by_id = {r["id"]: r for r in recs}
    names = numeral_names() if names is None else names
    allowed, problems, n_marks = {}, [], 0
    for n in sorted(names):
        if not any(n in r["text"] or n in r["raw"] for r in recs):
            problems.append("%s allows %r, and no fact's text holds it" % (NAMES_FILE.name, n))
        # A name is a proper name ending in its number - "Mercenaries 2",
        # "IEEE 754", "UTF-8" - never a phrase a figure could hide in ("28 of
        # 41" appears in a fact's text too; verifier-P0).
        if not NAME_SHAPE.fullmatch(n):
            problems.append("%s allows %r, which is not the shape of a name: capitalised words, then one number"
                            % (NAMES_FILE.name, n))
    files = published(root)
    if not any(f.endswith(".html") for f in files):
        return ["no page is published"], None
    for rel in files:
        if rel.endswith(".html"):
            p = _Marks()
            p.feed((root / rel).read_text(encoding="utf-8"))
            p.close()
            problems += ["%s: %s" % (rel, x) for x in p.problems]
            problems += ["%s: %s" % (rel, x) for x in holder_problems((root / rel).read_text(encoding="utf-8"))]
            for m in p.marks:
                n_marks += 1
                rec = by_id.get(int(m["f"])) if m["f"].isdigit() else None
                got = "".join(m["buf"])
                if rec is None:
                    problems.append("%s: a mark names fact %s, which facts.json does not have" % (rel, m["f"]))
                elif "src" in m["cls"]:
                    if got != " " + facts.label(rec):
                        problems.append("%s: fact %d's source reads %r, and its own label is %r"
                                        % (rel, rec["id"], got.strip(), facts.label(rec)))
                    if (m["href"] or "") != rec["href"]:
                        problems.append("%s: fact %d's source links to %r, not %r" % (rel, rec["id"], m["href"], rec["href"]))
                else:
                    if got != rec["text"]:
                        problems.append("%s: the mark for fact %d reads %r, and the fact is %r"
                                        % (rel, rec["id"], got, rec["text"]))
                    if m["tag"] == "span" and render.cls_of(rec) not in m["cls"]:
                        problems.append("%s: fact %d is marked as %r, not %r" % (rel, rec["id"], " ".join(m["cls"]), render.cls_of(rec)))
            # Every figure above the footer names its source as the footer
            # says: beside it, or - for a figure the map draws - in the list
            # under the map. "Somewhere on the page" was the first rule, and a
            # second, unlabelled copy of a figure passed it (verifier-P0).
            # The footer's own pins and date are printed bare, and its
            # sentence says so.
            in_list = {m["f"] for m in p.marks if "src" in m["cls"] and m["evidence"]}
            for m in p.marks:
                rec = by_id.get(int(m["f"])) if m["f"].isdigit() else None
                if not rec or "src" in m["cls"] or m["footer"] or not rec["text"]:
                    continue
                if m["svg"] and m["f"] not in in_list:
                    problems.append("%s: fact %s is drawn in the map, and the list under the map does not give "
                                    "its source" % (rel, m["f"]))
                elif not m["svg"] and not m["beside"]:
                    problems.append("%s: fact %s is printed above the footer without its source beside it"
                                    % (rel, m["f"]))
            for text, tick in p.loose:
                problems += _loose_problems(rel, text, tick, names, allowed)
            for t in p.attr_text:
                problems += _loose_problems(rel, t, False, names, allowed)
        elif rel.endswith(".css"):
            # Text a reader sees and no page holds: a numeral typed there would
            # pass every check on the HTML (generated content, 45b8d01; quotes
            # and list markers, verifier-P0 on bc2ffbc).
            css = re.sub(r'^@charset "utf-8";', "", (root / rel).read_text(encoding="utf-8"))
            code, strings, _ = css_parts(css)
            for m in re.finditer(r"content\s*:\s*([^;}]*)", code, re.I):
                if re.search(r"\b(?:counters?|attr)\s*\(", m.group(1), re.I):
                    problems.append("%s: generated content %r prints what no fact holds" % (rel, m.group(1).strip()))
            for m in re.finditer(r"@counter-style|counter-(?:reset|set|increment)\s*:", code, re.I):
                problems.append("%s: %s can print a number no fact holds" % (rel, m.group(0).rstrip(": ")))
            for s in strings:
                problems += _loose_problems("%s string" % rel, s, False, names, allowed)
            problems += ["%s: %s" % (rel, x) for x in hiding_problems(css)]
        elif rel.endswith(".txt") and not rel.startswith("fonts/"):
            t = (root / rel).read_text(encoding="utf-8")
            cut, last = [], 0
            for m in re.finditer(r" \[fact (\d+)\]", t):
                rec = by_id.get(int(m.group(1)))
                n_marks += 1
                if rec is None or not t[:m.start()].endswith(rec["text"]) or m.start() - len(rec["text"]) < last:
                    problems.append("%s: [fact %s] does not follow its fact's text" % (rel, m.group(1)))
                    continue
                cut.append(t[last:m.start() - len(rec["text"])])
                last = m.end()
            cut.append(t[last:])
            problems += _loose_problems(rel, " ".join(cut), False, names, allowed)
    return problems, (n_marks, allowed, len(files))


ALLOWED = {
    "html": {"lang"}, "head": set(), "body": set(), "title": {"id"},
    "meta": {"charset", "name", "content", "http-equiv"}, "link": {"rel", "href"},
    "main": set(), "header": set(), "footer": set(), "nav": set(), "section": {"class", "id"},
    "article": {"class", "id"}, "div": {"class", "id"}, "p": {"class", "id"},
    "h1": {"class", "id"}, "h2": {"class", "id"}, "h3": {"class", "id"}, "h4": {"class", "id"},
    "small": set(), "span": {"class", "data-f", "title"}, "a": {"href", "class", "aria-current", "id"},
    "code": set(), "pre": set(), "i": set(), "b": set(), "em": set(), "strong": set(), "sup": set(), "sub": set(),
    "abbr": {"title"}, "br": set(), "wbr": set(), "hr": set(), "blockquote": set(),
    "ul": {"class"}, "ol": {"class"}, "li": {"class", "id"}, "dl": {"class"}, "dt": set(), "dd": set(),
    "table": {"class"}, "caption": set(), "thead": set(), "tbody": set(), "tr": {"class", "id"},
    "th": {"class", "colspan", "rowspan", "scope"}, "td": {"class", "colspan", "rowspan"},
    "figure": {"class", "id"}, "figcaption": set(), "details": {"class", "id"}, "summary": set(),
    "img": {"src", "alt", "width", "height", "loading"},
    # SVG, drawn by the build: shapes and text, nothing that loads
    "svg": {"viewbox", "role", "aria-labelledby", "aria-hidden", "xmlns", "width", "height"},
    "defs": set(), "marker": {"id", "viewbox", "refx", "refy", "markerwidth", "markerheight", "orient"},
    "g": {"class"}, "path": {"class", "d", "marker-end"}, "line": {"class", "x1", "x2", "y1", "y2"},
    "rect": {"class", "x", "y", "width", "height"}, "circle": {"class", "cx", "cy", "r"},
    "text": {"class", "x", "y", "text-anchor"}, "tspan": {"class", "data-f"},
}
SCHEME = re.compile(r"^\s*([a-z][a-z0-9+.-]*):", re.I)


class _Tags(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.problems, self.head = [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if dupes(attrs):
            # A browser keeps the first of two same-named attributes, and dict()
            # the last: a page with two content= on its policy ran under the
            # first while this check read the second (verifier-P0, bc2ffbc).
            self.problems.append("<%s> repeats %s, which a browser and this check would read differently"
                                 % (tag, ", ".join(dupes(attrs))))
        if tag == "meta" or tag == "link" or tag == "title":
            self.head.append((tag, a))
        if tag not in ALLOWED:
            self.problems.append("<%s> is not an allowed element" % tag)
            return
        for k, v in attrs:
            if k not in ALLOWED[tag]:
                self.problems.append("<%s %s> is not an allowed attribute" % (tag, k))
        v = a.get("href") or ""
        if tag == "a" and SCHEME.match(v) and SCHEME.match(v).group(1).lower() not in ("http", "https", "mailto"):
            self.problems.append("<a href=%r>: only http, https and mailto links leave the site" % v)
        if tag == "link":
            if a.get("rel") not in ("stylesheet", "icon"):
                self.problems.append("<link rel=%r> is not a stylesheet or the icon" % a.get("rel"))
            elif (a.get("rel") == "icon" and v != "data:,") or (a.get("rel") == "stylesheet" and (SCHEME.match(v) or v.startswith("//"))):
                self.problems.append("<link rel=%s href=%r> loads from another host" % (a.get("rel"), v))
        if tag == "img" and (SCHEME.match(a.get("src") or "") or (a.get("src") or "").startswith("//")):
            self.problems.append("<img src=%r> loads from another host" % a.get("src"))
        if tag == "meta" and "http-equiv" in a and (a["http-equiv"] != "Content-Security-Policy" or a.get("content") != render.CSP):
            self.problems.append("<meta http-equiv=%r content=%r> is not the site's Content-Security-Policy"
                                 % (a["http-equiv"], a.get("content")))
        elif tag == "meta" and "http-equiv" not in a and a != {"charset": "utf-8"} \
                and a.get("name") not in ("viewport", "description"):
            # Only the four this site writes: a preview card's text (a
            # twitter:description, say) is text a reader sees that no check reads.
            self.problems.append("<meta %s> is not one of the site's own" % " ".join("%s=%r" % kv for kv in attrs))
        if tag == "meta" and a.get("name") == "viewport" and a.get("content") != "width=device-width,initial-scale=1":
            self.problems.append("<meta name=viewport content=%r> is not the site's" % a.get("content"))
        if tag == "path" and "marker-end" in a and not re.fullmatch(r"url\(#[\w-]+\)", a["marker-end"]):
            self.problems.append("<path marker-end=%r> is not a reference within the page" % a["marker-end"])
        if tag == "svg" and a.get("xmlns", "http://www.w3.org/2000/svg") != "http://www.w3.org/2000/svg":
            self.problems.append("<svg xmlns=%r>" % a["xmlns"])

    handle_startendtag = handle_starttag

    # The build writes no comment, no processing instruction and no CDATA
    # section. Each is refused: a browser shows none of them, so one inside a
    # word joins it back up for a reader while a check on text sees two
    # words (verifier-seam split an address with a comment), and in SVG a
    # CDATA section is text.
    def handle_comment(self, data):
        self.problems.append("an HTML comment, which the build never writes: %r" % data[:40])

    def handle_pi(self, data):
        self.problems.append("a processing instruction, which the build never writes: %r" % data[:40])

    def unknown_decl(self, data):
        self.problems.append("a declaration or CDATA section, which the build never writes: %r" % data[:40])


# The strings a stylesheet may hold that have a letter or a digit in them: the
# font names, the charset, a font's format, and the two theme names. Any other
# is refused. A string can be rendered as text, by content, a list marker or
# quotes, so it could spell a word or a figure that no check on a page reads.
# verifier-seam printed a name after the site's own, from two content strings.
CSS_STRINGS = {"JetBrains Mono", "Newsreader", "Times New Roman", "dark", "light", "utf-8", "woff2"}


def css_problems(css):
    """A stylesheet's loads. Comments go first, then anything that could spell
    a load in another case or through an escape is refused outright. So are
    the shapes this build knows of in which a reading of the text and a
    browser's can part: an ASCII control character other than a line feed or a tab
    (a form feed ends a string in a browser), a string left open at the end
    of its line, a comment left open, a comment marker inside a string, and a
    malformed url() - one whose unquoted address holds a quote, a space, '(',
    '{', '}' or ';'. Shapes this build does not know of are what the controls'
    cross-check holds: the published stylesheet read again by tinycss2."""
    out = []
    ctl = sorted({"U+%04X" % ord(c) for c in css if (ord(c) < 32 and c not in "\n\t") or ord(c) == 127})
    if ctl:
        out.append("an ASCII control character other than a line feed or a tab: %s" % ", ".join(ctl))
    for kind, text, flaw in css_tokens(css):
        if flaw == "open":
            out.append("a %s left open: %r" % (kind, text[:40]))
        elif kind == "url" and flaw == "bad":
            out.append("a malformed url(): %r" % text[:60])
        elif kind == "string" and ("/*" in text or "*/" in text):
            out.append("a comment marker inside a string: %r" % text[:40])
        elif kind == "string" and re.search(r"[^\W_]", text[1:-1]) and text[1:-1] not in CSS_STRINGS:
            out.append("a string holding a letter or a digit, which a stylesheet can render as text (content, a list "
                       "marker, quotes): %r. Only build.CSS_STRINGS may, and a url() is written unquoted" % text[:40])
    if "\\" in css:
        out.append("a backslash escape, which could spell a load")
    code, _, urls = css_parts(css)
    for pat, what in ((r"@import", "@import"), (r"image-set\(", "image-set()"), (r"(?<![\w-])src\(", "src()"),
                      (r"expression\(", "expression()"), (r"-moz-binding", "-moz-binding"), (r"behavior\s*:", "behavior")):
        if re.search(pat, code, re.I):
            out.append("uses %s" % what)
    for u in urls:
        if (SCHEME.match(u) and not u.lower().startswith("data:")) or u.startswith("//"):
            out.append("url(%s) loads from another host" % u)
    return out


def check_local_only(root=PUBLIC):
    """Every element and attribute on a page is on an allowlist, so a form of
    load nobody thought of is refused by default (verifier-P0 found 18 forms
    past the first check, which listed loads to refuse). Every page carries the
    site's Content-Security-Policy as the first element after its charset, so
    the browser refuses a load or a script the check missed."""
    problems = []
    for rel in published(root):
        f = root / rel
        if rel.endswith(".html"):
            p = _Tags()
            p.feed(f.read_text(encoding="utf-8"))
            p.close()
            problems += ["%s: %s" % (rel, x) for x in p.problems]
            h = p.head
            if len(h) < 2 or h[0] != ("meta", {"charset": "utf-8"}) or h[1][0] != "meta" \
                    or h[1][1].get("http-equiv") != "Content-Security-Policy" or h[1][1].get("content") != render.CSP:
                problems.append("%s: the Content-Security-Policy is not the first element after the charset" % rel)
        elif rel.endswith(".css"):
            problems += ["%s: %s" % (rel, x) for x in css_problems(f.read_text(encoding="utf-8"))]
        problems += ["%s: %s" % (rel, x) for x in type_problems(rel, f.read_bytes())]
        problems += ["%s: %s" % (rel, x) for x in email_problems(rel, f.read_bytes())]
        problems += ["%s: %s" % (rel, x) for x in only_in_problems(rel, f.read_bytes())]
    if not any(r.endswith(".html") for r in published(root)):
        problems.append("no page is published")
    return problems


# What may be published, by name: the page and text types these checks read,
# the images and fonts they vouch for by their bytes, and BUILD and MANIFEST.
# Anything else - .htm, .svg, .js, .xml - is a document or a script no check
# reads, served by its extension (verifier-P0 published a .htm through ASSETS).
MAGIC = {".png": b"\x89PNG\r\n\x1a\n", ".jpg": b"\xff\xd8\xff", ".jpeg": b"\xff\xd8\xff", ".webp": b"RIFF",
         ".woff2": b"wOF2"}
TEXT_TYPES = {".html", ".css", ".txt", ".json"}


def type_problems(rel, data):
    ext = posixpath.splitext(rel)[1].lower()
    if rel in ("BUILD", "MANIFEST") or ext in TEXT_TYPES:
        return []
    if ext not in MAGIC:
        return ["a %s file, which is not a type this site publishes" % (ext or "extensionless")]
    if not data.startswith(MAGIC[ext]) or (ext == ".webp" and data[8:12] != b"WEBP"):
        return ["not a %s by its bytes" % ext]
    return []


# No published file holds an email address except the site's own contact
# (decision 14). A commit's author email is in its repository's history, but
# the site is a new and more prominent place to publish it: parcel P2's first
# credits keyed an account by its address, in facts.json's arguments.
SITE_CONTACTS = {"logan@loganw.dev"}
# In any script (an IDN domain, a non-ASCII top-level domain), with a quoted
# local part or an address literal, as verifier-seam wrote them.
EMAIL = re.compile(r'(?:"[^"\r\n]+"|[\w.%+-]+)@(?:\[[^\]\s]+\]|[\w-]+(?:\.[\w-]+)*\.(?:[^\W\d_]{2,}|xn--[\w-]+))')


# How each allowed tag is laid out, for reading a page's text as a reader
# sees it. An inline tag sits inside a word without breaking it, so it is
# read as nothing and a word it splits is whole again; any other tag breaks
# a word, and is read as a space. Every tag ALLOWED names is in one of the
# two sets, and the import refuses one that isn't, so a tag added to ALLOWED
# is placed here before any page can use it.
INLINE = {"a", "abbr", "b", "code", "em", "i", "small", "span", "strong", "sub", "sup", "wbr", "tspan"}
BREAKING = {"html", "head", "body", "title", "meta", "link", "main", "header", "footer", "nav", "section",
            "article", "div", "p", "h1", "h2", "h3", "h4", "pre", "br", "hr", "blockquote", "ul", "ol", "li",
            "dl", "dt", "dd", "table", "caption", "thead", "tbody", "tr", "th", "td", "figure", "figcaption",
            "details", "summary", "img", "svg", "defs", "marker", "g", "path", "line", "rect", "circle", "text"}
if set(ALLOWED) != INLINE | BREAKING or INLINE & BREAKING:
    raise Refusal("build.ALLOWED and build.INLINE/BREAKING disagree: %s; place every allowed tag in exactly one"
                  % sorted(set(ALLOWED) ^ (INLINE | BREAKING) | (INLINE & BREAKING)))
# Code points a browser draws as nothing, besides the format characters
# (Unicode category Cf: a soft hyphen, zero-width spaces and joiners, a
# byte-order mark): the combining grapheme joiner, the Hangul fillers, the
# Khmer inherent vowels, and the variation selectors. Unicode's
# Default_Ignorable_Code_Point, as far as this site needs it.
IGNORABLE = frozenset([0x34F, 0x115F, 0x1160, 0x17B4, 0x17B5, 0x3164, 0xFFA0] + list(range(0x180B, 0x1810))
                      + list(range(0xFE00, 0xFE10)) + list(range(0xE0100, 0xE01F0)))


def visible(s):
    """s without the characters a browser draws as nothing."""
    if s.isascii():
        return s
    return "".join(c for c in s if ord(c) not in IGNORABLE and unicodedata.category(c) != "Cf")


def _json_strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield k
            yield from _json_strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from _json_strings(v)


def readings(rel, data):
    """Each way a reader could decode a published text file (verifier-seam
    published an address past a check that read raw bytes only):
    - as it is;
    - with its character references decoded;
    - decoded, with comments and inline tags removed and every other tag
      read as a space;
    - each of those percent-decoded, as a link's target is;
    and each of those without the characters a browser draws as nothing. A
    JSON file is read as its strings, each decoded the same way. A
    stylesheet needs no more: local-only refuses a backslash escape in one,
    and any string with a letter in it that build.CSS_STRINGS doesn't list.
    What this can't see is text put together by layout alone: two elements
    positioned side by side, say. The gates don't render (README)."""
    t = data.decode("utf-8", "replace")
    texts = [t]
    if rel.endswith(".json"):
        try:
            texts = list(_json_strings(json.loads(t)))
        except ValueError:
            pass
    inline = re.compile(r"</?(?:%s)\b[^>]*>" % "|".join(sorted(INLINE, key=len, reverse=True)), re.I)
    out = []
    for s in texts:
        flat = re.sub(r"<[^>]*>", " ", inline.sub("", re.sub(r"<!--.*?(?:-->|$)", "", s, flags=re.S)))
        for v in (s, html.unescape(s), html.unescape(flat)):
            for w in (v, urllib.parse.unquote(v)):
                out.append(visible(w))
    return out


def texts_of(rel, data):
    """What a published file says, for the checks on what may be published:
    a text file in each of its readings(); a PNG, its text chunks, inflated.
    A font is not read: its tables are compressed, and fonts/SOURCES.txt
    holds each font to its published hash instead. The site publishes no
    other kind of file (ASSET_NAME allows JPEG and WebP images, whose
    metadata is not read; none is published)."""
    ext = posixpath.splitext(rel)[1].lower()
    if ext in TEXT_TYPES or rel in ("BUILD", "MANIFEST"):
        return readings(rel, data)
    if ext == ".png":
        return readings(".txt", png_text(data))
    return []


def email_problems(rel, data):
    found = sorted({m.group(0).lower() for v in texts_of(rel, data) for m in EMAIL.finditer(v)} - SITE_CONTACTS)
    return ["an email address (%d found); only the site's contact, %s, may be published"
            % (len(found), ", ".join(sorted(SITE_CONTACTS)))] if found else []


# Decision 16: Wally, Logan's Discord username, appears only on the game
# thread's page. A name here may be published only in the files listed with
# it; facts.json, which records the text of every figure and statement, holds
# that page's statement of it. A file is read in each of the ways readings()
# gives, so neither an entity, an attribute, percent-encoding nor markup
# inside the word hides it.
ONLY_IN = {"Wally": ("thread-preservation.html", "facts.json")}


def only_in_problems(rel, data):
    names = [(name, files) for name, files in sorted(ONLY_IN.items()) if rel not in files]
    views = texts_of(rel, data) if names else []
    return ["names %s, which may be published only in %s" % (name, ", ".join(files))
            for name, files in names if any(re.search(r"(?i)\b%s\b" % re.escape(name), v) for v in views)]


ASSET_NAME = re.compile(r"assets/[a-z0-9][a-z0-9-]*\.(?:png|jpg|jpeg|webp)")


def check_asset(dest, data):
    """An asset a page copies from a pin: an image, under assets/, that is
    what its name says by its bytes."""
    if not ASSET_NAME.fullmatch(dest):
        raise Refusal("an asset is published as %r; an asset is a lower-case .png, .jpg or .webp under assets/" % dest)
    bad = type_problems(dest, data)
    if bad:
        raise Refusal("the asset %s is %s" % (dest, bad[0]))


class _Refs(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k == "id" and v:
                self.ids.add(v)
            if k in ("href", "src") and v is not None:
                self.refs.append(v)

    handle_startendtag = handle_starttag


def _target(rel, u, files):
    """The published file a relative reference names, exactly, or None. No
    normalising: 'style.css/', './x', 'INDEX.HTML' and 'index.html.' name no
    published file, and GitHub Pages would not serve them as one."""
    path = u.split("#")[0].split("?")[0]
    if path == "":
        return rel
    if path.startswith("/") or "\\" in path or "%" in path or any(s in ("", ".", "..") for s in path.split("/")):
        return None
    t = posixpath.join(posixpath.dirname(rel), path)
    return t if t in files else None


def check_links(root=PUBLIC):
    files = set(published(root))
    ids, refs, problems = {}, [], []
    for rel in sorted(files):
        if rel.endswith(".html"):
            p = _Refs()
            p.feed((root / rel).read_text(encoding="utf-8"))
            ids[rel] = p.ids
            refs += [(rel, u) for u in p.refs]
        elif rel.endswith(".css"):
            refs += [(rel, u) for u in css_parts((root / rel).read_text(encoding="utf-8"))[2]]
    for rel, u in refs:
        # GitHub opens a Markdown file's rendered view at its top and ignores
        # #L; ?plain=1 shows the line (facts.line_anchor; verifier-seam).
        if re.match(r"https://github\.com/[^?#]+\.(?:md|markdown)#L\d+$", u, re.I):
            problems.append("%s links to %s: GitHub opens a Markdown file at its top whatever the #L; put "
                            "?plain=1 before it" % (rel, u))
        if SCHEME.match(u) or u.startswith("//"):
            continue
        t = _target(rel, u, files)
        if t is None:
            problems.append("%s links to %s, which is not a published file" % (rel, u))
        elif "#" in u and u.split("#", 1)[1] and u.split("#", 1)[1] not in ids.get(t, set()):
            problems.append("%s links to %s, and %s has no such id" % (rel, u, t))
    if not any(f.endswith(".html") for f in files):
        problems.append("no page is published")
    return problems + check_connections(root)


# The map on Home and each dossier's Connections, read as they are
# published: a dossier lists exactly the edges the map draws that touch its
# project. verifier-seam dropped an edge where each is rendered, and the
# control then in place, which compared two functions, said they agreed.
_EDGE_TITLE = re.compile(r'<path class="edge [^"]*"[^>]*><title>([^<]*)</title>')
_CONNECTIONS = re.compile(r"<h2><small>[IVX]+</small>Connections</h2>(.*?)(?=<h2|</main>)", re.S)
# A Connections section is one list, and each item in it is an edge written
# the one way the dossiers write it. Anything else in the section is refused,
# so an edge written another way can't pass unread (verifier-seam added one
# with a parenthesis before its colon).
_CONNECTION_LIST = re.compile(r"<ul>((?:<li>.*?</li>)+)</ul>", re.S)


def check_connections(root=PUBLIC):
    home = root / "index.html"
    if not home.is_file():
        return []
    kinds = json.loads((SITE / "data" / "relations.json").read_text(encoding="utf-8"))["kinds"]
    labels = sorted({label for _, label in kinds}, key=len, reverse=True)
    item = re.compile(r"<li><code>([^<]*)</code> (%s) <code>([^<]*)</code>: (?:(?!<li>).)*</li>"
                      % "|".join(re.escape(x) for x in labels), re.S)
    problems, drawn = [], set()
    for title in _EDGE_TITLE.findall(home.read_text(encoding="utf-8")):
        title = html.unescape(title)
        for label in labels:
            tail, sep, head = title.partition(" %s " % label)
            if sep:
                drawn.add((tail, label, head))
                break
        else:
            problems.append("index.html draws an edge titled %r, of no kind relations.json names" % title)
    nodes = {n for t, _, h in drawn for n in (t, h)}
    for rel in sorted(published(root)):
        if not (rel.startswith("work-") and rel.endswith(".html")):
            continue
        stem = rel[len("work-"):-len(".html")]
        node = next((n for n in nodes if n.lower() == stem), None)
        sec = _CONNECTIONS.search((root / rel).read_text(encoding="utf-8"))
        if node is None:
            problems.append("%s is a dossier for %r, which the map on index.html doesn't draw" % (rel, stem))
            continue
        if sec is None:
            problems.append("%s has no Connections section" % rel)
            continue
        whole = _CONNECTION_LIST.fullmatch(sec.group(1))
        if whole is None:
            problems.append("%s's Connections section is not one list of edges and nothing else" % rel)
            continue
        items = re.findall(r"<li>.*?</li>", whole.group(1), re.S)
        odd = [x for x in items if not item.fullmatch(x)]
        problems += ["%s's Connections has an item that is not an edge as the dossiers write one: %r"
                     % (rel, re.sub(r"<[^>]*>", "", x)[:80]) for x in odd]
        listed = {tuple(html.unescape(g) for g in item.fullmatch(x).groups()) for x in items if x not in odd}
        want = {e for e in drawn if node in (e[0], e[2])}
        problems += ["%s doesn't list the map's edge %r" % (rel, " ".join(e)) for e in sorted(want - listed)]
        problems += ["%s lists %r, which the map doesn't draw" % (rel, " ".join(e)) for e in sorted(listed - want)]
    return problems


COUNT_EXEMPT = {"VALIDATION.md"}   # the ledger: a count in it is a fact about its date, but its links are checked


def doc_files():
    fs = [ROOT / "README.md", ROOT / "CLAUDE.md", ROOT / "design" / "README.md"]
    fs += sorted((ROOT / "docs").glob("*.md"))
    return [f for f in fs if f.is_file()]


def runner_stages():
    return len(re.findall(r'^stage [a-z0-9-]+ "', (ROOT / "verify" / "run.sh").read_text(encoding="utf-8"), re.M))


def _prose(t):
    """A document's text outside fenced code blocks."""
    outside, fence = [], None
    for line in t.splitlines():
        m = re.match(r" {0,3}(`{3,}|~{3,})", line)
        if m and fence is None:
            fence = m.group(1)
            continue
        if m and fence and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and line.strip() == m.group(1):
            fence = None
            continue
        if fence is None:
            outside.append(line)
    return "\n".join(outside)


COUNT_WORDS = ("one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|"
               "sixteen|seventeen|eighteen|nineteen|twenty|dozen")
# A count within three words of "stages", on either side, or of "stage count"
# and "number of stages": "10 stages", "ten separate, independent stages",
# "10 (ten) stages", "Stages: 10", "The stage count is 10" (verifier-P0 found
# the last four past the first rule). "stage 2", an index, is not a count.
_N = r"(?:\d+|%s)\b" % COUNT_WORDS
STAGE_COUNT = re.compile(r"\b%s(?:\W+\w+){0,3}?\W+stages?\b|\b(?:stages|stage count|number of stages)\b(?:\W+\w+){0,3}?\W+%s"
                         % (_N, _N), re.I)


def slugs(t):
    """GitHub's anchors for a Markdown file's headings."""
    out, seen = set(), {}
    for line in _prose(t).splitlines():
        m = re.match(r" {0,3}#{1,6}\s+(.*?)\s*#*\s*$", line)
        if not m:
            continue
        s = re.sub(r"[^\w\- ]", "", md_text(m.group(1)).lower()).replace(" ", "-")
        n = seen.get(s, 0)
        seen[s] = n + 1
        out.add(s if n == 0 else "%s-%d" % (s, n))
    return out


def md_text(s):
    return re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s).replace("`", "").replace("*", "")


def check_docs(files=None):
    """No document states how many stages the runner has: `run.sh --list`
    prints them, and a count in prose goes stale (verifier-P0 found one in a
    code fence that no check read). What counts as stating one is STAGE_COUNT
    above: a count near "stages", in digits or in the words it lists. The
    ledger, docs/VALIDATION.md, may state one, as a fact about its date.
    Every relative link in every document resolves - inline, with a title, by
    reference, or a raw <a> or <img> - and so does its #anchor."""
    problems = []
    for f in files if files is not None else doc_files():
        rel = f.name if files is not None else f.relative_to(ROOT).as_posix()
        t = f.read_text(encoding="utf-8")
        if f.name not in COUNT_EXEMPT:
            for m in STAGE_COUNT.finditer(" ".join(t.split())):
                problems.append("%s states a stage count, %r; `bash verify/run.sh --list` prints the stages instead"
                                % (rel, m.group(0)))
        prose = _prose(t)
        defs = {k.lower(): v for k, v in re.findall(r"^ {0,3}\[([^\]]+)\]:\s*<?(\S+?)>?(?:\s+.*)?$", prose, re.M)}
        hrefs = re.findall(r"\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)", prose)
        hrefs += re.findall(r"<a\s[^>]*href=[\"']([^\"']+)[\"']", prose, re.I)
        hrefs += re.findall(r"<img\s[^>]*src=[\"']([^\"']+)[\"']", prose, re.I)
        hrefs += list(defs.values())
        for text, ref in re.findall(r"\[([^\]]+)\]\[([^\]]*)\]", prose):
            if (ref or text).lower() not in defs:
                problems.append("%s: the reference [%s] is never defined" % (rel, ref or text))
        for href in hrefs:
            if SCHEME.match(href) or href.startswith("//"):
                continue
            path, _, frag = href.partition("#")
            target = (f.parent / path) if path else f
            if not target.exists():
                problems.append("%s links to %s, which does not exist" % (rel, href))
            elif frag and target.suffix == ".md" and frag not in slugs(target.read_text(encoding="utf-8")):
                problems.append("%s links to %s, and %s has no heading with that anchor" % (rel, href, target.name))
    return problems


def _git_out(root, *args, stdin=None):
    return subprocess.run(["git", "-C", str(root), *args], input=stdin, capture_output=True).stdout


def tracked_blobs(root=ROOT):
    """[(where, bytes)]: what a push of this repository would publish, as
    text this search can read:
      * every file git would commit now (tracked, or new and not ignored);
      * every blob reachable from any ref, so a name that survives only in an
        earlier commit is found (verifier-P0);
      * every path, now and in history, since a name can be a file's name;
      * every commit message, every annotated tag's message, and every
        branch and tag name;
      * every author, committer and tagger: name and email.
    What it cannot read: text drawn as pixels, and text inside compressed
    data other than a PNG's text chunks (a font's tables, say)."""
    out, seen = [], set()
    ls = _git_out(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard").decode("utf-8", "replace")
    for rel in sorted(set(x for x in ls.split("\0") if x)):
        f = root / rel
        if f.is_file():
            out.append((rel, f.read_bytes()))
    paths = {}
    for line in _git_out(root, "rev-list", "--all", "--objects").decode("utf-8", "replace").splitlines():
        sha, _, path = line.partition(" ")
        if path:
            paths.setdefault(sha, path)
    kinds = _git_out(root, "cat-file", "--batch-check", stdin="\n".join(paths).encode()).decode().splitlines()
    blobs = [k.split()[0] for k in kinds if k.split()[1:2] == ["blob"]]
    data = _git_out(root, "cat-file", "--batch", stdin="\n".join(blobs).encode())
    pos = 0
    while pos < len(data):
        nl = data.index(b"\n", pos)
        sha, _, size = data[pos:nl].decode().split()
        body = data[nl + 1:nl + 1 + int(size)]
        pos = nl + 1 + int(size) + 1
        if sha not in seen:
            seen.add(sha)
            out.append(("%s in history (blob %s)" % (paths[sha], sha[:7]), body))
    out.append(("paths", "\n".join(sorted(set(ls.split("\0")) | set(paths.values()))).encode()))
    for what, args in (("commit messages", ["log", "--all", "--format=%B"]),
                       ("tag messages", ["for-each-ref", "refs/tags", "--format=%(contents)"]),
                       ("commit identities", ["log", "--all", "--format=%an%n%ae%n%cn%n%ce"]),
                       ("tagger identities", ["for-each-ref", "refs/tags", "--format=%(taggername)%0a%(taggeremail)"]),
                       ("branch and tag names", ["for-each-ref", "--format=%(refname)"])):
        out.append((what, _git_out(root, *args)))
    return out


def png_text(b):
    """The text chunks of a PNG, compressed ones inflated: tEXt, zTXt and
    iTXt. verifier-P0 hid a name in a compressed chunk, which a byte search
    cannot see."""
    import zlib
    out, pos = [], 8
    while pos + 8 <= len(b):
        n, kind = int.from_bytes(b[pos:pos + 4], "big"), b[pos + 4:pos + 8]
        data = b[pos + 8:pos + 8 + n]
        pos += 12 + n
        try:
            if kind == b"tEXt":
                out.append(data.replace(b"\0", b" "))
            elif kind == b"zTXt":
                key, _, rest = data.partition(b"\0")
                out.append(key + b" " + zlib.decompress(rest[1:]))
            elif kind == b"iTXt":
                key, _, rest = data.partition(b"\0")
                compressed, rest = rest[0], rest[2:]
                lang, _, rest = rest.partition(b"\0")
                tkey, _, text = rest.partition(b"\0")
                out.append(key + b" " + tkey + b" " + (zlib.decompress(text) if compressed else text))
        except (zlib.error, IndexError):
            out.append(b"(an unreadable text chunk)")
    return b"\n".join(out)


def _as_text(b):
    """A file's text in the encoding it is in: UTF-16 by its byte-order mark,
    or by a NUL in nearly every other byte; otherwise UTF-8. None for any
    other binary file."""
    if b[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return b.decode("utf-16", "replace")
    if b"\0" in b:
        for enc, alt in (("utf-16-le", b[1::2]), ("utf-16-be", b[0::2])):
            if len(alt) >= 2 and alt.count(0) > 0.9 * len(alt):
                return b[:len(b) - len(b) % 2].decode(enc, "replace")
        return None
    return b.decode("utf-8", "replace")


def find_named(names, blobs):
    """Where any of names appears: ['where:line'] in text, whatever its
    encoding, and ['where (bytes)'] in any other file, for the name in UTF-8
    or UTF-16. The names are not printed, since printing them is the leak this
    looks for."""
    pats = [re.compile(r"(?<![\w.-])%s(?![\w-])" % re.escape(n), re.I) for n in names]
    raw = [enc for n in names for enc in (n.lower().encode("utf-8"), n.lower().encode("utf-16-le"),
                                          n.lower().encode("utf-16-be"))]
    hits = []
    for where, b in blobs:
        t = b if isinstance(b, str) else _as_text(b)
        if t is None:
            if b.startswith(b"\x89PNG\r\n\x1a\n"):
                b = b + b"\n" + png_text(b)
            if any(r in b.lower() for r in raw):
                hits.append("%s (bytes)" % where)
            continue
        lines = t.splitlines()
        for i, line in enumerate(lines, 1):
            # a name wrapped at one of its own hyphens is read as one word
            joined = line + lines[i].lstrip() if line.endswith("-") and i < len(lines) else line
            if any(p.search(joined) for p in pats):
                hits.append("%s:%d" % (where, i))
    return hits


def check_github(only=None):
    """Every pin, asked of GitHub now: it must resolve there, to the SHA the
    snapshot recorded. The build takes the snapshot's word that GitHub has a
    pin; this stage takes GitHub's own, with the owner's login, so it reaches
    private repositories too (verifier-P0 hand-edited a snapshot to vouch for
    a local-only commit, and every other stage passed). Desktop only: CI has
    no login that can read the private pins, and is skipped by name; there,
    `facts` fetches each public pin from GitHub, which fails on a commit
    GitHub does not have."""
    if os.environ.get("CI"):
        raise Unavailable("CI cannot read the private pins on GitHub; the desktop runs this stage")
    problems, n = [], 0
    for name, cfg in facts.PINS["repos"].items():
        if only is not None and name not in only:
            continue
        try:
            r = subprocess.run(["gh", "api", "repos/%s/%s/commits/%s" % (*facts.split(name), cfg["commit"]),
                                "--jq", ".sha"], capture_output=True)
        except FileNotFoundError:
            raise Unavailable("gh is not installed here")
        out = r.stdout.decode().strip()
        if r.returncode != 0:
            status = re.search(r'"status":\s*"(\d+)"', out)
            if status and status.group(1) in ("404", "422"):
                problems.append("%s: GitHub does not have the pinned commit %s" % (name, cfg["commit"]))
                continue
            raise Unavailable("gh cannot ask GitHub about %s here: %s" % (name, r.stderr.decode().strip()[:120]))
        n += 1
        rec = facts.snap().get("pins", {}).get(name, {})
        if out != rec.get("sha"):
            problems.append("%s: GitHub resolves %s to %s, and the snapshot recorded %s"
                            % (name, cfg["commit"], out[:12], (rec.get("sha") or "nothing")[:12]))
    return problems, n


def check_privacy():
    """No file this repository would publish, no commit message and no branch
    name names a private repository the site does not read. It needs the
    owner's own GitHub login to list those names, so it runs on the desktop and
    is skipped by name anywhere else. It can see only names: a private project
    described without its name is outside it (a stated limit)."""
    if os.environ.get("CI"):
        raise Unavailable("CI cannot list the owner's private repositories; the desktop runs this stage")
    try:
        r = subprocess.run(["gh", "repo", "list", facts.OWNER, "--visibility", "private", "--limit", "500",
                            "--json", "name"], capture_output=True)
    except FileNotFoundError:
        raise Unavailable("gh is not installed here")
    if r.returncode != 0:
        raise Unavailable("gh cannot list %s's private repositories here" % facts.OWNER)
    names = [x["name"] for x in json.loads(r.stdout)]
    if len(names) >= 500:
        raise Refusal("500 or more private repositories; raise the limit, or this check is partial")
    read = {facts.split(k)[1] for k in facts.PINS["repos"] if facts.split(k)[0] == facts.OWNER}
    read |= set(facts.PINS["github_only"])
    unread = [n for n in names if n not in read]
    blobs = tracked_blobs()
    return find_named(unread, blobs), len(unread), blobs


def verify_facts(root=PUBLIC, require_all=False):
    data = json.loads((root / "facts.json").read_text(encoding="utf-8"))
    ok, bad, skipped, stated = 0, [], [], 0
    for rec in data["facts"]:
        try:
            same, now = facts.rederive(rec)
        except Refusal as e:
            bad.append("fact %d (%s) cannot be read again: %s" % (rec["id"], rec["method"], e))
            continue
        if rec["kind"] == "stated":
            stated += 1        # no source to read; a statement tied to a pin is refused once the pin moves
        elif same is None:
            skipped.append("fact %d (%s): %s" % (rec["id"], rec["where"], now))
        elif same:
            ok += 1
        else:
            bad.append("fact %d (%s) printed %r, and its source now gives %r" % (rec["id"], rec["where"], rec["text"], now))
    for s in skipped:
        print("SKIPPED %s" % s)
    for b in bad:
        print("MISMATCH %s" % b, file=sys.stderr)
    print("verify-facts: %d read again and the same, %d different, %d stated, %d skipped by name"
          % (ok, len(bad), stated, len(skipped)))
    if bad:
        return 1
    if skipped and require_all:
        print("verify-facts: %d skipped, and --require-all makes a skip a failure" % len(skipped), file=sys.stderr)
        return 1
    return 0


def planted_link():
    """The runner's own control: the links check on a copy with a broken link.
    It says CAUGHT only when the check named the plant, so a crash, which also
    exits 1, is not mistaken for the check saying no."""
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        shutil.copytree(PUBLIC, root, dirs_exist_ok=True)
        page = root / "index.html"
        page.write_text(page.read_text(encoding="utf-8").replace("</footer>", '<a href="planted.html">x</a></footer>', 1),
                        encoding="utf-8", newline="\n")
        found = [f for f in check_links(root) if "planted.html" in f]
        print("CAUGHT: %s" % found[0] if found else "planted-link: the broken link passed")
        return 1 if found else 0


# ---------------------------------------------------------------------------
# The negative controls. Each must FAIL; if one passes, the check it controls
# cannot see the defect it exists for, and everything it passed is decoration.
# A control that needs a source this machine cannot read is skipped by name,
# and the count of those is on the last line, for the runner to enforce.
# ---------------------------------------------------------------------------

def controls():
    results, skipped = [], []

    def report(name, caught, how):
        results.append(caught)
        print("control %-14s %s - %s" % (name, "caught, as it must be" if caught else "NEGATIVE CONTROL DID NOT FAIL", how))

    def skip(name, why):
        skipped.append(name)
        print("control %-14s SKIPPED by name - %s" % (name, why))

    def refused(name, what, fn, must=""):
        try:
            fn()
            report(name, False, "%s passed" % what)
        except Unavailable as e:
            skip(name, "%s: %s" % (what, e))
        except Refusal as e:
            report(name, must in str(e), "%s: %s" % (what, e))

    # A. Faults planted in a copy of the committed public/, so CI runs them.
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        shutil.copytree(PUBLIC, root, dirs_exist_ok=True)
        page = root / "index.html"
        t = page.read_text(encoding="utf-8")

        def planted(name, what, new, check, want=None):
            if new == t:
                report(name, False, "could not plant %s: the page does not have what it replaces" % what)
                return
            page.write_text(new, encoding="utf-8", newline="\n")
            try:
                found = check(root)
                found = found[0] if isinstance(found, tuple) else found
                hit = [f for f in found if want is None or want in f]
                report(name, bool(hit), "%s: %s" % (what, hit[0] if hit else "passed"))
            finally:
                page.write_text(t, encoding="utf-8", newline="\n")

        # the manifest: a page deleted, and a page edited by hand
        page.unlink()
        found = check_manifest(root)
        report("manifest", any("index.html" in f for f in found), "index.html deleted: %s" % (found[0] if found else "passed"))
        src_txt = root / "fonts" / "SOURCES.txt"
        saved_src = src_txt.read_text(encoding="utf-8")
        for what, new, want in (("a font size changed", re.sub(r"(newsreader-normal-latin\.woff2\s+)\d+", r"\g<1>132001",
                                                               saved_src, count=1), "newsreader-normal-latin.woff2"),
                                ("the fonts' total changed", saved_src.replace("512,869", "512,870", 1), "total")):
            if new == saved_src:
                report("manifest", False, "could not plant %s" % what)
                continue
            src_txt.write_text(new, encoding="utf-8")
            found = [f for f in check_font_sources(root) if want in f]
            report("manifest", bool(found), "%s in fonts/SOURCES.txt: %s" % (what, found[0] if found else "passed"))
        src_txt.write_text(saved_src, encoding="utf-8")
        mf = root / "MANIFEST"
        saved_mf = mf.read_text(encoding="utf-8")
        for what, new, want in (("site/render.py changed after the build",
                                 re.sub(r"(# source site/render\.py )[0-9a-f]{64}", r"\g<1>" + "0" * 64, saved_mf),
                                 "site/render.py is not the bytes"),
                                ("site/mapgen.py added after the build",
                                 re.sub(r"# source site/mapgen\.py [0-9a-f]{64}\n", "", saved_mf), "does not hash site/mapgen.py"),
                                ("the site's own ledger changed after the build",
                                 re.sub(r"(# source docs/VALIDATION\.md )[0-9a-f]{64}", r"\g<1>" + "0" * 64, saved_mf),
                                 "docs/VALIDATION.md is not the bytes")):
            if new == saved_mf:
                report("manifest", False, "could not plant %s" % what)
                continue
            mf.write_text(new, encoding="utf-8")
            found = [f for f in check_manifest(root) if want in f]
            report("manifest", bool(found), "%s: %s" % (what, found[0] if found else "passed"))
        mf.write_text(saved_mf, encoding="utf-8")
        planted("manifest", "a byte of index.html changed", t.replace("Ledger", "Ledgeг", 1), check_manifest, "index.html")

        # numbers: a typed figure, a figure copied with its text changed, a
        # number word, a figure span with no fact, and a source label changed
        data = json.loads((root / "facts.json").read_text(encoding="utf-8"))
        agent = next(r for r in data["facts"] if r["method"] == "facts.agents" and r["args"]["name"] == "cft-fp256")
        mark = '<span class="fig" data-f="%d">%s</span>' % (agent["id"], agent["text"])
        if mark not in t:
            report("numbers", False, "could not plant: %r is not in the page" % mark)
        else:
            planted("numbers", "a typed count", t.replace("</footer>", "<p>152 ledger entries</p></footer>", 1),
                    check_numbers, "'152'")
            planted("numbers", "a figure's text changed in its mark",
                    t.replace(mark, mark.replace(agent["text"], "1079/1079")), check_numbers, "fact %d" % agent["id"])
            planted("numbers", "a number word", t.replace("</footer>", "<p>three rounds</p></footer>", 1),
                    check_numbers, "three")
            planted("numbers", "a figure span with no fact",
                    t.replace("</footer>", '<span class="fig">x</span></footer>', 1), check_numbers, "no fact id")
            planted("numbers", "a figure's source label removed",
                    re.sub(r'<span class="src" data-f="%d">.*?</span>(?=</td>)' % agent["id"], "", t, count=1, flags=re.S),
                    check_numbers, "fact %d is printed above the footer without its source beside it" % agent["id"])
            planted("numbers", "a second copy of a figure, with no label beside it",
                    t.replace("<footer>", "<p>%s</p><footer>" % mark, 1),
                    check_numbers, "fact %d is printed above the footer without its source beside it" % agent["id"])
            snap_id = next(r["id"] for r in data["facts"] if r["method"] == "facts.snapshot_date")
            planted("numbers", "a figure the map draws, with its line under the map removed",
                    re.sub(r'<li>the line marked "snapshot": .*?</li>', "", t, count=1, flags=re.S),
                    check_numbers, "fact %d is drawn in the map" % snap_id)
            planted("numbers", "a source label changed",
                    re.sub(r'(<span class="src" data-f="%d"> (?:<a [^>]*>)?\()' % agent["id"], r"\1planted ", t, count=1),
                    check_numbers, "fact %d's source" % agent["id"])
            planted("numbers", "a figure in a page's alt text", t.replace('alt="The Pauli print"', 'alt="The 3 prints"', 1),
                    check_numbers, "'3'")
            planted("numbers", "a figure behind a sign", t.replace("</footer>", "<p>costs $5</p></footer>", 1),
                    check_numbers, "'$5'")
            planted("numbers", "a date in an HTML element classed as a tick",
                    t.replace("</footer>", '<p>shipped <span class="tick">Sep 2026</span></p></footer>', 1),
                    check_numbers, "'2026'")
            planted("numbers", "a figure in the first of two alt attributes",
                    t.replace('alt="The Pauli print"', 'alt="3397 prints" alt=""', 1), check_numbers, "'3397'")
            planted("numbers", "a name allowed with no fact behind it",
                    t.replace("</footer>", "<p>after 4096 tests</p></footer>", 1),
                    lambda r: check_numbers(r, names={"4096 tests": "planted"}), "no fact's text holds it")
            held = next(r["text"] for r in data["facts"] if r["method"] == "facts.agents")
            planted("numbers", "a figure allowed as a name because a fact holds it",
                    t.replace("</footer>", "<p>%s</p></footer>" % held, 1),
                    lambda r: check_numbers(r, names={held: "planted"}), "not the shape of a name")
            css = root / "style.css"
            saved_css = css.read_text(encoding="utf-8")
            for what, rule, want in (("a figure in CSS generated content", '.stamp::after{content:" 3397 tests"}', "'3397'"),
                                     ("a counter in CSS generated content", "li::after{content:counter(list-item)}", "counter"),
                                     ("a figure in CSS quotes", '.stamp::after{content:open-quote}.stamp{quotes:" | 3397 tests" ""}',
                                      "'3397'"),
                                     ("a figure as a list marker", 'li{list-style-type:"3397 "}', "'3397'"),
                                     ("a counter set to a figure", "ol{counter-reset:list-item 3396}", "counter-reset"),
                                     ("a counter style", "@counter-style x{system:cyclic;symbols:A}", "@counter-style"),
                                     ("a stylesheet hiding every source", ".src{display:none}", "'.src' hides"),
                                     ("a stylesheet hiding every figure", ".fig{visibility:hidden}", "'.fig' hides"),
                                     ("a stylesheet shrinking the sources away", "main .src{font-size:0}", "hides"),
                                     ("sources in a colour with zero alpha", ".src{color:rgba(0,0,0,0)}", "'.src' hides"),
                                     ("sources in a four-digit hex colour with zero alpha", ".src{color:#0000}", "'.src' hides"),
                                     ("a transparent colour through a custom property",
                                      ":root{--planted:transparent}.q{color:var(--planted)}", "'.q' hides"),
                                     ("a font size computed to zero", ".src{font-size:calc(0px)}", "'.src' hides"),
                                     ("the standalone scale property at zero", ".src{scale:0}", "'.src' hides"),
                                     ("map text with fill none", ".map svg text{fill:none}", "hides"),
                                     ("a custom property read past a fallback in parentheses",
                                      ":root{--planted:transparent}.src{color:var(--planted, rgb(1 2 3))}", "'.src' hides"),
                                     ("a registered property whose initial value is transparent",
                                      '@property --planted{syntax:"<color>";inherits:false;initial-value:transparent}'
                                      ".src{color:var(--planted)}", "'.src' hides"),
                                     ("an alpha computed with calc()", ".src{color:rgb(0 0 0 / calc(0))}", "'.src' hides"),
                                     ("a negative alpha, which a browser clamps to zero", ".src{color:rgb(0 0 0 / -1)}",
                                      "'.src' hides"),
                                     ("a negative opacity", ".src{opacity:-1}", "'.src' hides"),
                                     ("a vendor-prefixed clip-path", ".src{-webkit-clip-path:inset(50%)}", "'.src' hides"),
                                     ("an allowed selector hiding by a declaration it was not allowed",
                                      ".map .edge{display:none}", "'.map .edge' hides"),
                                     ("a hiding rule nested in @media inside a style rule",
                                      ".src{@media all{display:none}}", "'@media all' hides"),
                                     ("a hiding rule in @scope", "@scope (.src){display:none}", "'@scope (.src)' hides"),
                                     ("a hiding rule nested in @supports",
                                      ".src{@supports (display:block){display:none}}", "hides"),
                                     ("a hiding declaration beside a nested rule",
                                      ".src{display:none;.x{color:red}}", "'.src' hides"),
                                     ("a keyframe that fades to nothing", "@keyframes planted{to{opacity:0}}",
                                      "'to' hides"),
                                     ("an allowed declaration, nested under its parent",
                                      ".map{.edge{fill:none}}", "'.edge' hides"),
                                     ("a hiding declaration after a quote inside an unquoted url()",
                                      ".src{background:url(assets/pauli-print.png');display:none}\n}", "'.src' hides"),
                                     ("a hiding rule between comment markers held in strings",
                                      '.a{content:"/*"} .src{display:none} .b{content:"*/"}', "'.src' hides"),
                                     ("a hiding declaration after a form feed, which ends a string in a browser",
                                      ".src{content:'a\f;display:none;x:'\n}", "'.src' hides")):
                css.write_text(saved_css + rule + "\n", encoding="utf-8")
                found = [f for f in check_numbers(root)[0] if want in f]
                report("numbers", bool(found), "%s: %s" % (what, found[0] if found else "passed"))
            css.write_text(saved_css, encoding="utf-8")
            # the scanner itself: it must read every block of the real
            # stylesheet, or a rule it lost its place in is a rule unread
            n_read = len(_decls(saved_css))
            n_open = sum(1 for kind, text, _ in css_tokens(saved_css) if kind == "char" and text == "{")
            report("numbers", n_read == n_open, "the stylesheet's %d blocks, each read: %d" % (n_open, n_read))
            # the reading itself, against tinycss2's, on the published
            # stylesheet; and the comparison watched failing on a reader that
            # sees only innermost blocks, as this build's first one did
            try:
                found = crosscheck_css(saved_css)
                report("numbers", not found, "the stylesheet read by this build and by tinycss2: %s"
                       % (found[0] if found else "the same %d blocks, the same properties, the same verdicts"
                          % len(_decls(saved_css))))
                naive = lambda s: [(" ".join(p.split()), [(d.split(":", 1)[0].strip().lower(), d.split(":", 1)[1].strip())
                                                          for d in body.split(";") if ":" in d])
                                   for p, body in re.findall(r"([^{}]+)\{([^{}]*)\}", s)]
                found = crosscheck_css(".src{display:none;.x{color:red}}", reader=naive)
                report("numbers", bool(found), "a reader that misses a declaration beside a nested rule, against "
                       "tinycss2: %s" % (found[0] if found else "passed"))
            except ImportError:
                skip("numbers", "tinycss2 is not installed here, so the stylesheet is not read a second way")
            # a string left open ends at its line, as a browser ends it, so a
            # stray quote cannot swallow the rules after it
            found = hiding_problems(saved_css + "\n.planted{content:'open}\n.src{display:none}\n")
            report("numbers", any("(display: none)" in f for f in found),
                   "a hiding rule after a string left open (which, as in a browser, also swallows the brace that "
                   "would close its block): %s" % (found[0] if found else "passed"))

        # links: a missing page, and shapes a server would not serve as a file
        for bad in ("nowhere.html", "style.css/", "index.html/.", "INDEX.HTML", "./index.html", "index.html#no-such-id"):
            planted("links", "a link to %s" % bad, t.replace("</footer>", '<a href="%s">x</a></footer>' % bad, 1),
                    check_links, bad)

        # local-only: loads and scripts in several forms, and a missing policy
        for what, plant in (("an external stylesheet", '<link rel="stylesheet" href="https://fonts.googleapis.com/css2">'),
                            ("a script", "<script>1</script>"),
                            ("srcset", '<img src="assets/pauli-print.png" srcset="https://x.invalid/a.png 2x" alt="">'),
                            ("a style attribute", '<p style="background:url(https://x.invalid/a.png)">x</p>'),
                            ("an event handler", '<img src="assets/pauli-print.png" onerror="alert(1)" alt="">'),
                            ("a base element", '<base href="https://x.invalid/">'),
                            ("a meta refresh", '<meta http-equiv="refresh" content="0;url=https://x.invalid/">'),
                            ("an SVG image", '<svg><image href="https://x.invalid/a.png"/></svg>'),
                            ("a javascript: link", '<a href="javascript:alert(1)">x</a>')):
            planted("local-only", what, t.replace("</footer>", plant + "</footer>", 1), check_local_only)
        planted("local-only", "no Content-Security-Policy",
                re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]*>', "", t, count=1), check_local_only,
                "Content-Security-Policy")
        planted("local-only", "a second content= on the policy, which a browser reads first",
                t.replace('<meta http-equiv="Content-Security-Policy" content=',
                          '<meta http-equiv="Content-Security-Policy" content="default-src * data:" content=', 1),
                check_local_only, "repeats content")
        planted("local-only", "an email address on a page",
                t.replace("</footer>", "<p>write to someone@example.com</p></footer>", 1), check_local_only,
                "an email address")
        fjp = root / "facts.json"
        saved_fj = fjp.read_text(encoding="utf-8")
        fjp.write_text(saved_fj.replace('"about": "', '"about": "planted@example.org ', 1), encoding="utf-8")
        found = [f for f in check_local_only(root) if f.startswith("facts.json") and "an email address" in f]
        report("local-only", bool(found), "an email address in facts.json: %s" % (found[0] if found else "passed"))
        fjp.write_text(saved_fj, encoding="utf-8")
        # Wally on a page other than the game thread's (decision 16), in each
        # shape a page could print it.
        for what, shape in (("in a sentence", "<p>Wally made this</p>"),
                            ("in lower case", "<p>ask wally</p>"),
                            ("split by markup", "<p>Wal<b>ly</b> made this</p>"),
                            ("as a character reference", "<p>&#87;ally made this</p>"),
                            ("in an attribute", '<p title="by Wally">made</p>')):
            planted("local-only", "Wally on Home, %s" % what, t.replace("</footer>", shape + "</footer>", 1),
                    check_local_only, "index.html: names Wally")
        # An address in each shape a browser or a parser decodes, as
        # verifier-seam published one past the first version of the gate.
        for what, shape in (("as a character reference", "<p>write to someone&#64;example.com</p>"),
                            ("as a named character reference", "<p>write to someone&commat;example.com</p>"),
                            ("percent-encoded in a mailto link", '<p><a href="mailto:someone%40example.com">x</a></p>'),
                            ("split by a word-break tag", "<p>someone@<wbr>example.com</p>"),
                            ("split by inline markup", "<p>some<span>one</span>@example.com</p>")):
            planted("local-only", "an email address on a page, %s" % what,
                    t.replace("</footer>", shape + "</footer>", 1), check_local_only, "index.html: an email address")
        for what, shape in (("percent-encoded", "planted%40example.org "),
                            ("as a JSON escape", "planted" + chr(92) + "u0040example.org ")):
            fjp.write_text(saved_fj.replace('"about": "', '"about": "' + shape, 1), encoding="utf-8")
            found = [f for f in check_local_only(root) if f.startswith("facts.json") and "an email address" in f]
            report("local-only", bool(found), "an email address in facts.json, %s: %s" % (what, found[0] if found else "passed"))
        fjp.write_text(saved_fj, encoding="utf-8")

        # A dossier's Connections against the map, as published.
        dossier = root / "work-cft-rebound.html"
        saved_d = dossier.read_text(encoding="utf-8")
        sec = _CONNECTIONS.search(saved_d)
        item = re.search(r"<li><code>[^<]*</code> [^<]*? <code>[^<]*</code>:.*?</li>", sec.group(1), re.S) if sec else None
        drawn = re.findall(r'<path class="edge [^"]*"[^>]*><title>cft-fp256 underlies cft-rebound</title></path>', t)
        for what, target, new, want in (
                ("a dossier missing one of the map's edges", dossier,
                 saved_d.replace(item.group(0), "", 1) if item else saved_d, "doesn't list the map's edge"),
                ("a dossier listing an edge the map doesn't draw", dossier,
                 saved_d.replace(item.group(0), item.group(0) + "<li><code>cft-rebound</code> verifies "
                                 "<code>planted-node</code>: x</li>", 1) if item else saved_d,
                 "lists 'cft-rebound verifies planted-node', which the map doesn't draw"),
                ("the map no longer drawing an edge a dossier lists", page,
                 re.sub(r'<path class="edge [^"]*"[^>]*><title>cft-fp256 underlies cft-rebound</title></path>', "", t)
                 if drawn else t, "lists 'cft-fp256 underlies cft-rebound', which the map doesn't draw")):
            before = target.read_text(encoding="utf-8")
            if new == before:
                report("links", False, "could not plant %s" % what)
                continue
            target.write_text(new, encoding="utf-8", newline="\n")
            try:
                found = [f for f in check_links(root) if want in f]
                report("links", bool(found), "%s: %s" % (what, found[0] if found else "passed"))
            finally:
                target.write_text(before, encoding="utf-8", newline="\n")
        # ...and anything in the section that is not an edge written the one
        # way, as verifier-seam added one.
        if sec:
            end = sec.end(1)
            for what, new, want in (
                    ("a Connections item written another way",
                     saved_d[:end - len("</ul>")] + "<li><code>StoryDocs</code> documents <code>cft-rebound</code> "
                     "(in its projects): x</li></ul>" + saved_d[end:], "is not an edge as the dossiers write one"),
                    ("a sentence in the Connections section after its list",
                     saved_d[:end] + "<p>StoryDocs documents cft-rebound too.</p>" + saved_d[end:],
                     "is not one list of edges")):
                dossier.write_text(new, encoding="utf-8", newline="\n")
                try:
                    found = [f for f in check_links(root) if want in f]
                    report("links", bool(found), "%s: %s" % (what, found[0] if found else "passed"))
                finally:
                    dossier.write_text(saved_d, encoding="utf-8", newline="\n")
        else:
            report("links", False, "could not plant: work-cft-rebound.html has no Connections section")
        planted("links", "a link to a line of a Markdown file without ?plain=1",
                t.replace("</footer>", '<a href="https://github.com/x/y/blob/abc/README.md#L3">x</a></footer>', 1),
                check_links, "?plain=1")

        # The readings, in each shape verifier-seam used after the first fix.
        for what, shape in (("split by a comment", "<p>some<!-- -->one@example.com</p>"),
                            ("split by a zero-width space", "<p>someone@exa&#8203;mple.com</p>"),
                            ("split by a soft hyphen", "<p>someone@exam&shy;ple.com</p>"),
                            ("split by an SVG tspan", "<svg><text>some<tspan>one@example.com</tspan></text></svg>"),
                            ("with a domain in another script", "<p>someone@ex%smple.com</p>" % chr(0xE4)),
                            ("with a top-level domain in another script",
                             "<p>someone@example.%s%s</p>" % (chr(0x440), chr(0x444))),
                            ("as an address literal", "<p>someone@[192.0.2.1]</p>"),
                            ("with a quoted local part", '<p>"some one"@example.com</p>')):
            planted("local-only", "an email address on a page, %s" % what,
                    t.replace("</footer>", shape + "</footer>", 1), check_local_only, "index.html: an email address")
        for what, shape in (("split by a comment", "<p>Wal<!-- -->ly</p>"),
                            ("split by a soft hyphen", "<p>Wal&shy;ly</p>"),
                            ("split by a zero-width space", "<p>W&#8203;ally</p>"),
                            ("split by an SVG tspan", "<svg><text>Wal<tspan>ly</tspan></text></svg>")):
            planted("local-only", "Wally on Home, %s" % what, t.replace("</footer>", shape + "</footer>", 1),
                    check_local_only, "index.html: names Wally")
        for what, shape, want in (("an HTML comment", "<p>a<!-- b -->c</p>", "an HTML comment"),
                                  ("a CDATA section in SVG text", "<svg><text>Wal<![CDATA[ly]]></text></svg>", "CDATA"),
                                  ("a processing instruction", "<?xml-stylesheet href=x?>", "a processing instruction")):
            planted("local-only", what, t.replace("</footer>", shape + "</footer>", 1), check_local_only, want)
        style = root / "style.css"
        saved_style = style.read_text(encoding="utf-8")
        for what, rule in (("a name put together from two content strings", 'header::after{content:" / Wal" "ly"}'),
                           ("an address put together from two content strings",
                            'p::after{content:"someone@" "example.com"}'),
                           ("a word as a list marker", 'li{list-style-type:"Wally "}')):
            style.write_text(saved_style + rule + "\n", encoding="utf-8")
            found = [f for f in check_local_only(root) if "a string holding a letter or a digit" in f]
            report("local-only", bool(found), "%s: %s" % (what, found[0] if found else "passed"))
        style.write_text(saved_style, encoding="utf-8")
        import zlib
        png = root / "assets" / "pauli-print.png"
        saved_png = png.read_bytes()
        for what, chunk, want in (
                ("an email address in a PNG text chunk", b"tEXt" + b"Comment\0write to someone@example.com",
                 "an email address"),
                ("an email address in a compressed PNG text chunk",
                 b"zTXt" + b"Comment\0\0" + zlib.compress(b"write to someone@example.com"), "an email address"),
                ("Wally in a PNG text chunk", b"tEXt" + b"Author\0Wally", "names Wally")):
            png.write_bytes(saved_png[:33] + (len(chunk) - 4).to_bytes(4, "big") + chunk + b"\0\0\0\0" + saved_png[33:])
            found = [f for f in check_local_only(root) if f.startswith("assets/pauli-print.png") and want in f]
            report("local-only", bool(found), "%s: %s" % (what, found[0] if found else "passed"))
        png.write_bytes(saved_png)
        # A class css_hides.json lets a stylesheet hide, on an element it
        # doesn't name (verifier-seam: the narrow map's class on Verify's
        # source labels).
        for what, shape, want in (("the narrow map's class on a source label",
                                   '<span class="src map-narrow">x</span>', "'map-narrow'"),
                                  ("the wide map's class on a div holding text", '<div class="map-wide"><p>x</p></div>',
                                   "'map-wide'"),
                                  ("the arrows' class on SVG text", '<svg><text class="edge">x</text></svg>', "'edge'")):
            planted("numbers", what, t.replace("</footer>", shape + "</footer>", 1), check_numbers, want)
        planted("local-only", "a preview card's text in a meta tag",
                t.replace("</head>", '<meta name="twitter:description" content="3397 tests"></head>', 1),
                check_local_only, "twitter:description")
        planted("local-only", "a second src on an image",
                t.replace('<img src="assets/pauli-print.png"',
                          '<img src="https://x.invalid/pixel.png" src="assets/pauli-print.png"', 1),
                check_local_only, "repeats src")
        for name, blob, want in (("remote.htm", b"<script>1</script>", "not a type"),
                                 ("assets/fake.png", b"<!doctype html><script>1</script>", "by its bytes")):
            (root / name).parent.mkdir(parents=True, exist_ok=True)
            (root / name).write_bytes(blob)
            found = [f for f in check_local_only(root) if name in f and want in f]
            report("local-only", bool(found), "a published %s: %s" % (name, found[0] if found else "passed"))
            (root / name).unlink()
        for what, dest, blob in (("an asset published as .htm", "remote.htm", b"<script>1</script>"),
                                 ("an asset whose bytes are not its type", "assets/x.png", b"<script>1</script>")):
            refused("assets", what, lambda dest=dest, blob=blob: check_asset(dest, blob))
        # Each is caught only by the rule it names: once CSS_STRINGS refused a
        # string with a letter in it, @import and image-set() were refused by
        # that rule and no longer showed their own.
        css_wants = {"URL( in capitals": "loads from another host", "@IMPORT": "uses @import",
                     "image-set": "uses image-set()", "an escaped url": "a backslash escape",
                     "a quote inside an unquoted url()": "a malformed url()",
                     "a semicolon inside an unquoted url()": "a malformed url()",
                     "a comment marker inside a string": "a comment marker inside a string",
                     "a string left open": "a string left open", "a comment left open": "a comment left open",
                     "a form feed": "an ASCII control character"}
        for what, css in (("URL( in capitals", "a{background:URL(https://x.invalid/a.png)}"),
                          ("@IMPORT", "@IMPORT 'https://x.invalid/a.css';"),
                          ("image-set", 'a{background:image-set("https://x.invalid/a.png" 1x)}'),
                          ("an escaped url", "a{background:u\\72l(https://x.invalid/a.png)}"),
                          ("a quote inside an unquoted url()", ".src{background:url(assets/pauli-print.png');color:red}"),
                          ("a semicolon inside an unquoted url()", ".x{background:url(a;b)}"),
                          ("a comment marker inside a string", '.a{content:"/*"}'),
                          ("a string left open", ".a{content:'open\n}"),
                          ("a comment left open", ".a{color:red} /* never closed"),
                          ("a form feed", ".a{content:'x\fy'}")):
            found = [f for f in css_problems(css) if css_wants[what] in f]
            report("local-only", bool(found), "%s in CSS: %s" % (what, found[0] if found else "passed"))

        # facts: a stale figure in facts.json, which must be named by its id
        fj = root / "facts.json"
        rec = next(r for r in data["facts"] if r["method"] == "facts.macros")
        saved = fj.read_text(encoding="utf-8")
        rec["text"] = rec["raw"] = "0.14"
        fj.write_text(json.dumps(data), encoding="utf-8")
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                rc = verify_facts(root)
            named = [line for line in out.getvalue().splitlines() if line.startswith("MISMATCH fact %d " % rec["id"])]
            if "skipped by name" in out.getvalue() and not named and rc == 0:
                skip("facts", "fact %d's source is unavailable here" % rec["id"])
            else:
                report("facts", rc == 1 and bool(named), "fact %d planted at 0.14: %s" % (rec["id"], named[0] if named else "not named"))
        finally:
            fj.write_text(saved, encoding="utf-8")

    # B. The documents: a stage count in every shape it has taken, and links in
    #    every shape Markdown has, each on a copy of a real document.
    doc = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as d:
        copy = pathlib.Path(d) / "CLAUDE.md"
        (pathlib.Path(d) / "README.md").write_text("# The front door\n", encoding="utf-8")
        copy.write_text(doc, encoding="utf-8")
        base = [f for f in check_docs([copy]) if "does not exist" not in f]   # its links point outside the copy
        for what, plant, want in (("7 stages", "The runner has 7 stages.", "'7 stages'"),
                                  ("seven stages", "It runs seven stages.", "'seven stages'"),
                                  ("8-stage", "An 8-stage runner.", "'8-stage'"),
                                  ("a count across a line break", "It has 8\nstages.", "'8 stages'"),
                                  ("a count in a code fence", "```bash\nbash verify/run.sh   # 7 stages\n```", "'7 stages'"),
                                  ("8 runner stages", "All 8 runner stages.", "'8 runner stages'"),
                                  ("a link to a missing file", "[x](planted.md)", "planted.md"),
                                  ("a link with a title", '[x](planted.md "title")', "planted.md"),
                                  ("a reference link", "[x][r]\n\n[r]: planted.md", "planted.md"),
                                  ("an undefined reference", "[x][nowhere]", "[nowhere]"),
                                  ("a raw anchor", '<a href="planted.md">x</a>', "planted.md"),
                                  ("a missing heading anchor", "[x](README.md#no-such-heading)", "#no-such-heading"),
                                  ("Stages: 10", "Stages: 10.", "'Stages: 10'"),
                                  ("the stage count is 10", "The stage count is 10.", "'stage count is 10'"),
                                  ("a dozen stages", "It has a dozen stages.", "'dozen stages'"),
                                  ("ten separate, independent stages", "It runs ten separate, independent stages.",
                                   "'ten separate, independent stages'"),
                                  ("10 (ten) stages", "It runs 10 (ten) stages.", "'10 (ten) stages'"),
                                  ("a raw image to a missing file", '<img src="planted.png" alt="">', "planted.png")):
            if base:
                report("docs", False, "could not plant %s: CLAUDE.md already fails: %s" % (what, base[0]))
                continue
            copy.write_text(doc + "\n" + plant + "\n", encoding="utf-8")
            found = [f for f in check_docs([copy]) if want in f]
            report("docs", bool(found), "%s: %s" % (what, found[0] if found else "passed"))
        # the ledger: its links are checked, and a stage count in it is a fact about its date
        ledger = pathlib.Path(d) / "VALIDATION.md"
        ledger.write_text("# ledger\n\nIt ran 10 stages.\n\n[x](planted.md)\n", encoding="utf-8")
        found = check_docs([ledger])
        report("docs", any("planted.md" in f for f in found) and not any("stage count" in f for f in found),
               "the ledger, with a stage count and a broken link: %s" % (found or "passed"))

    # C. Rules that need no source: the page seam, workflow classes, pins
    #    GitHub must have, paraphrases, statements tied to a pin, fenced
    #    headings, a figure copied with its text changed, and names.
    import types
    fake = lambda f, nav, idx=None: types.SimpleNamespace(
        __name__="planted." + f, render_page=lambda ctx: "",
        PAGE=dict(file=f, nav=nav, title="t", description="d", **({} if idx is None else {"index": idx})))
    for what, mods in (("a nested page", [fake("work/x.html", "Work")]),
                       ("two section pages", [fake("threads.html", "Threads", True), fake("thread-a.html", "Threads", True)])):
        refused("seam", what, lambda mods=mods: validate(mods))
    m = fake("x.html", "Work")
    m.NUMERAL_NAMES = ["4096 tests"]
    refused("seam", "a page module allowing names of its own", lambda m=m: validate([m]), "numeral_names.json")
    for bad in ("work/x.txt", "X.TXT", "index.html"):
        m = fake("x.html", "Work")
        m.extra_files = lambda ctx, bad=bad: {bad: "planted"}
        refused("seam", "an extra file named %s" % bad, lambda m=m: collect_extras(m, {}, {}))

    listed = facts.snap()["workflows"]
    for what, plant, undo in (
            ("an unclassed workflow", lambda: listed.setdefault("atlas-optical", []).append("planted-tests"),
             lambda: listed["atlas-optical"].remove("planted-tests")),
            ("a class for a missing workflow", lambda: facts.PINS["repos"]["atlas-optical"]["workflows"].update(ghost="verifies"),
             lambda: facts.PINS["repos"]["atlas-optical"]["workflows"].pop("ghost"))):
        plant()
        try:
            refused("workflows", what, facts.check_workflows)
        finally:
            undo()

    recs = facts.snap()["pins"]
    for what, plant in (("a pin moved without a new snapshot", dict(recs["cft-fp256"], commit="644ee2d")),
                        ("a pin GitHub does not have", dict(recs["cft-fp256"], sha=None))):
        saved = recs["cft-fp256"]
        recs["cft-fp256"] = plant
        try:
            refused("pin-github", what, facts.check_pins, "cft-fp256")
        finally:
            recs["cft-fp256"] = saved

    refused("paraphrase", "a display with a date its source does not have",
            lambda: facts.check_display("merged into main on 2026-09-27", "Whether atlas-film's pinned merges into its main"),
            "2026-09-27")
    refused("paraphrase", "a display with a number word its source does not have",
            lambda: facts.check_display("its merge left open for twelve days",
                                        "Whether atlas-film's pinned merges into its main"), "twelve")
    refused("paraphrase", "a pattern that matches more than once",
            lambda: facts.prose("cft-fp256", "README.md", r"(cft-fp256)"), "matches")
    # The site's own record: only the files it declares, the same prose rules,
    # and every heading dated at its start.
    refused("own", "a file that is not part of the site's own record",
            lambda: facts.own_text("README.md"), "not part of this site's own record")
    refused("own", "a pattern that matches more than once in the site's own ledger",
            lambda: facts.own_prose("docs/VALIDATION.md", r"^## (\d{4}-\d{2}-\d{2})"), "matches")
    refused("own", "a pattern the site's own ledger does not have",
            lambda: facts.own_prose("docs/VALIDATION.md", r"(planted words no ledger has)"), "no longer matches")
    refused("own", "a paraphrase of the site's own ledger with a date its words do not have",
            lambda: facts.own_prose("docs/VALIDATION.md", r"^## \d{4}-\d{2}-\d{2} - (the biography approved)$",
                                    display="the biography, approved on 2026-09-30"), "2026-09-30")
    refused("own", "an entry asked for by a heading the ledger doesn't have",
            lambda: facts.own_entry("docs/VALIDATION.md", "2026-01-01 - planted"), "has 0 entries headed")
    saved_own = facts.own_text
    try:
        facts.own_text = lambda path: "## 2026-01-01 - a\n\ntext\n\n## an undated heading\n"
        refused("own", "a heading in the site's own ledger not dated at its start",
                lambda: facts.own_entries("docs/VALIDATION.md"), "not dated at its start")
        facts.own_text = lambda path: "## 2026-01-01 - a\n\ntext\n\n## 2026-01-01 - a\n\nmore\n"
        refused("own", "an entry cited by a heading two entries share",
                lambda: facts.own_entry("docs/VALIDATION.md", "2026-01-01 - a"), "has 2 entries headed")
        # An entry inserted above a cited one: by its line the fact returned
        # the entry now there; by its heading it returns the same entry, at
        # its new line.
        facts.own_text = lambda path: "# L\n\n## 2026-01-01 - a\n\n## 2026-01-02 - b\n"
        before = facts.own_entry("docs/VALIDATION.md", "2026-01-02 - b")
        facts.own_text = lambda path: "# L\n\n## 2026-01-01 - a\n\n## 2026-01-01 - inserted\n\n## 2026-01-02 - b\n"
        after = facts.own_entry("docs/VALIDATION.md", "2026-01-02 - b")
        report("own", before.text == after.text and before.src.short != after.src.short,
               "an entry inserted above a cited one: cited as %s, then as %s, the same entry %r"
               % (before.src.short, after.src.short, after.text))
    finally:
        facts.own_text = saved_own
    # Read again, a figure cited at another line than it was published at is
    # a difference, even when its words are the same.
    facts.reset_log()
    v = facts.own_prose("docs/VALIDATION.md", r"^## \d{4}-\d{2}-\d{2} - (the biography approved)$")
    rec = dict(facts.LOG[v.id - 1])
    moved = dict(rec, where=rec["where"].rsplit(":", 1)[0] + ":1")
    same, now = facts.rederive(moved)
    report("own", same is False, "a citation published at another line, the words the same: %s"
           % ("read again as different: %s" % now if same is False else "read again as the same"))
    facts.reset_log()
    refused("own", "a commit cited by a name rather than a hash, as HEAD~1 moves with history",
            lambda: facts.own_commit("HEAD~1", "planted"), "not a commit hash")
    saved_own = facts.own_text
    try:
        facts.own_text = lambda path: "## 2026-01-01 - a\n\nthe planted words\n\n## an undated heading\n"
        refused("own", "a quotation from a ledger with a heading not dated at its start",
                lambda: facts.own_prose("docs/VALIDATION.md", r"(the planted words)"), "not dated at its start")
    finally:
        facts.own_text = saved_own
    refused("manifest", "a source saved with CRLF line endings, which git would call unchanged",
            lambda: lf_only([("site/planted.py", b"x = 1\r\n")]), "carriage return")
    import mapgen
    sp = mapgen.DATA.get("storydocs_projects", {})
    multi = next((k for k, c in sorted(sp.items()) if len(c.get("nodes", [])) > 1), None)
    if multi is None:
        report("map", False, "could not plant: no StoryDocs directory maps to more than one node")
    else:
        saved_cfg = sp[multi]
        sp[multi] = dict(saved_cfg, bend=[0] * (len(saved_cfg["nodes"]) - 1))
        try:
            refused("map", "a StoryDocs directory given one bend fewer than its nodes, which zip() would drop",
                    mapgen._storydocs_edges, "bends for its")
        finally:
            sp[multi] = saved_cfg
    # A commit of the site's own that a page cites: on the history being
    # built, in a repository planted for the purpose, so CI runs it too.
    with tempfile.TemporaryDirectory() as d:
        g = lambda *a: subprocess.run(["git", "-C", d, "-c", "user.name=planted", "-c", "user.email=planted@invalid",
                                       *a], capture_output=True, text=True)
        g("init", "-q")
        g("commit", "-q", "--allow-empty", "-m", "main's commit")
        g("checkout", "-q", "-b", "side")
        g("commit", "-q", "--allow-empty", "-m", "a commit only the side branch holds")
        side = g("rev-parse", "--short", "HEAD").stdout.strip()
        g("checkout", "-q", "-")
        shallow = pathlib.Path(d) / "shallow"
        subprocess.run(["git", "clone", "-q", "--depth", "1", pathlib.Path(d).as_uri(), str(shallow)],
                       capture_output=True)
        saved_root = facts.ROOT
        try:
            facts.ROOT = pathlib.Path(d)
            refused("own", "a cited commit only a side branch holds, as a squashed parcel's are",
                    lambda: facts.own_commit(side, "planted"), "does not descend from it")
            refused("own", "a cited commit this site's history does not have",
                    lambda: facts.own_commit("0000000", "planted"), "has no commit 0000000")
            facts.ROOT = shallow
            try:
                facts.own_commit(side, "planted")
                report("own", False, "a cited commit read from a shallow checkout passed")
            except Unavailable as e:
                report("own", "shallow" in str(e), "a cited commit read from a shallow checkout: %s" % e)
            except Refusal as e:
                report("own", False, "a shallow checkout was refused, but not as shallow: %s" % e)
        finally:
            facts.ROOT = saved_root
    refused("stated", "a statement about a pin that has since moved",
            lambda: facts.stated("planted", "Logan", "2026-09-29", holds_at={"cft-fp256": "0000000"}), "restate")
    heads = facts.ledger_headings("## 2026-01-01 - a\n```\n## 2026-01-02 - fenced\n```\n## 2026-01-03 - b\n")
    report("ledger", len(heads) == 2, "a heading inside a code fence: %d headings read of 2 outside fences" % len(heads))
    for what, text in (("a fence never closed", "## 2026-01-01 - a\n```\n## 2026-01-02 - b\n"),
                       ("four backticks closed by three", "## 2026-01-01 - a\n````\n```\n## 2026-01-02 - b\n"),
                       ("a heading underlined with dashes", "## 2026-01-01 - a\n\n2026-01-02 - b\n---\n"),
                       ("a heading underlined with a single dash", "## 2026-01-01 - a\n\n2026-01-02 - b\n-\n"),
                       ("a heading inside a quote", "## 2026-01-01 - a\n> ## 2026-01-02 - b\n"),
                       ("a heading inside a list item", "## 2026-01-01 - a\n- ## 2026-01-02 - b\n"),
                       ("a heading in a quote inside a list item", "## 2026-01-01 - a\n- > ## 2026-01-02 - b\n"),
                       ("a heading in a list item inside a quote", "## 2026-01-01 - a\n> - ## 2026-01-02 - b\n"),
                       ("an HTML heading", "## 2026-01-01 - a\n<h2>2026-01-02 - b</h2>\n"),
                       ("an HTML heading inside another HTML block", "## 2026-01-01 - a\n<div><h2>2026-01-02</h2></div>\n"),
                       ("an HTML comment never closed", "## 2026-01-01 - a\n<!--\n## 2026-01-02 - b\n")):
        refused("ledger", what, lambda text=text: facts.ledger_headings(text))
    heads = facts.ledger_headings("## 2026-01-01 - a\n<!--\n## 2026-01-02 - hidden\n-->\n## 2026-01-03 - c\n")
    report("ledger", [h[1] for h in heads] == ["## 2026-01-01 - a", "## 2026-01-03 - c"],
           "a heading inside an HTML comment, which renders as nothing: %d read of the 2 outside it" % len(heads))
    heads = facts.ledger_headings("## 2026-01-01 - a\n<pre>\nx\n\n## 2026-01-02 - hidden\n</pre>\n## 2026-01-03 - c\n")
    report("ledger", [h[1] for h in heads] == ["## 2026-01-01 - a", "## 2026-01-03 - c"],
           "a heading inside a <pre> that spans a blank line, which renders as text: %d read of the 2 outside it" % len(heads))
    heads = facts.ledger_headings("## 2026-01-01 - a\n<!-->\n## 2026-01-02 - b\n")
    report("ledger", len(heads) == 2, "an empty comment, which CommonMark closes on its own line: %d read of 2" % len(heads))
    # Every real ledger, against CommonMark's own count of its level-2
    # headings: an independent reading, where markdown-it-py is installed.
    try:
        from markdown_it import MarkdownIt
        md = MarkdownIt("commonmark")
        for name in sorted(n for n, c in facts.PINS["repos"].items() if c.get("verified_by", {}).get("ledger")) \
                + ["cft-fp256"]:
            try:
                t, ents = facts.entries(name, "docs/VALIDATION.md")
            except Unavailable as e:
                skip("ledger", "%s: %s" % (name, e))
                continue
            toks = md.parse(t)
            theirs = [(tok.map[0] + 1, toks[k + 1].content.strip()) for k, tok in enumerate(toks)
                      if tok.type == "heading_open" and tok.tag == "h2"]
            mine = [(e["line"], e["title"]) for e in ents]
            odd = [x for x in mine if x not in theirs][:1] + [x for x in theirs if x not in mine][:1]
            report("ledger", mine == theirs, "%s: %d entries read, and CommonMark renders %d level-2 headings%s"
                   % (name, len(mine), len(theirs), ", each at the same line with the same title" if mine == theirs
                      else "; they differ at %r" % odd))
    except ImportError:
        skip("ledger", "markdown-it-py is not installed here, so no ledger is read a second way")
    heads = facts.ledger_headings("## 2026-01-01 - a\n   ## 2026-01-02 - indented\n##\t2026-01-03 - a tab\n")
    report("ledger", len(heads) == 3, "headings indented, and after a tab: %d read of 3" % len(heads))
    refused("write", "a published path that climbs out of public/",
            lambda: write({"../site/data/planted.json": "{}"}, {}, pathlib.Path(tempfile.gettempdir()) / "planted-root"))
    facts.reset_log()
    v = facts.stated("planted", "Logan", "2026-09-29")
    import dataclasses
    for what, bad in (("no fact produced", facts.V("0.15", facts.Src("file", "typed by hand"))),
                      ("its text changed after the fact", dataclasses.replace(v, text="1079/1079")),
                      ("its source changed after the fact", dataclasses.replace(v, src=facts.Src("file", "elsewhere")))):
        refused("unlogged", "a figure with %s" % what, lambda bad=bad: render.fig(bad))
    hits = find_named(["planted-private-repo"], [("planted.md", "see\nplanted-private-repo for more")])
    report("privacy", hits == ["planted.md:2"], "a private name in a tracked file: %s" % (hits or "passed"))
    hits = find_named(["planted-private-repo"], [("planted.md", "see planted-private-\nrepo for more")])
    report("privacy", hits == ["planted.md:1"], "a private name wrapped at its hyphen: %s" % (hits or "passed"))
    for what, blob in (("in a UTF-16 file with a byte-order mark", "see planted-private-repo".encode("utf-16")),
                       ("in a UTF-16 file without one", "see planted-private-repo".encode("utf-16-le")),
                       ("inside a binary file", b"\x89PNG\r\n\x1a\n\0\0planted-private-repo\0")):
        hits = find_named(["planted-private-repo"], [("planted.bin", blob)])
        report("privacy", bool(hits), "a private name %s: %s" % (what, hits or "passed"))
    with tempfile.TemporaryDirectory() as d:
        g = lambda *a: subprocess.run(["git", "-C", d, "-c", "user.name=planted", "-c", "user.email=planted@invalid",
                                       *a], capture_output=True)
        g("init", "-q")
        (pathlib.Path(d) / "notes.md").write_text("see planted-private-repo\n", encoding="utf-8")
        g("add", "-A")
        g("commit", "-qm", "a note")
        (pathlib.Path(d) / "notes.md").write_text("nothing here\n", encoding="utf-8")
        g("commit", "-qam", "the note removed")
        hits = find_named(["planted-private-repo"], tracked_blobs(pathlib.Path(d)))
        report("privacy", any("in history" in h for h in hits),
               "a private name only in an earlier commit: %s" % (hits or "passed"))
        (pathlib.Path(d) / "planted-private-repo").mkdir()
        (pathlib.Path(d) / "planted-private-repo" / "readme.md").write_text("nothing\n", encoding="utf-8")
        g("add", "-A")
        g("commit", "-qm", "a folder")
        g("tag", "-a", "v0", "-m", "the tag message names planted-private-repo")
        (pathlib.Path(d) / "other.md").write_text("x\n", encoding="utf-8")
        g("add", "-A")
        subprocess.run(["git", "-C", d, "-c", "user.name=planted-private-repo bot", "-c", "user.email=bot@invalid",
                        "commit", "-qm", "an ordinary message"], capture_output=True)
        hits = find_named(["planted-private-repo"], tracked_blobs(pathlib.Path(d)))
        for what, want in (("as a folder's name", "paths"), ("in an annotated tag's message", "tag messages"),
                           ("in a commit's author name", "commit identities")):
            report("privacy", any(h.startswith(want) for h in hits), "a private name %s: %s" % (what, hits or "passed"))
    import zlib
    chunk = b"zTXt" + b"Comment\0\0" + zlib.compress(b"made in planted-private-repo")
    png = b"\x89PNG\r\n\x1a\n" + (len(chunk) - 4).to_bytes(4, "big") + chunk + b"\0\0\0\0"
    hits = find_named(["planted-private-repo"], [("planted.png", png)])
    report("privacy", bool(hits), "a private name in a compressed PNG text chunk: %s" % (hits or "passed"))

    # D. Faults that need every pinned clone: a stale page, a stale pin, and
    #    each page's own controls.
    try:
        text, binary = render_all()
    except Unavailable as e:
        text = None
        for name in ("drift", "stale-pin"):
            skip(name, "needs every pinned clone: %s" % e)
    if text is not None:
        abi = [r for r in facts.LOG if r["method"] == "facts.macros"][0]
        needle = '<span class="fig" data-f="%d">%s</span>' % (abi["id"], abi["text"])
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            write(text, binary, root)
            page = root / "index.html"
            t = page.read_text(encoding="utf-8")
            if needle not in t:
                report("drift", False, "could not plant: %r is not in the page" % needle)
            else:
                page.write_text(t.replace(needle, needle.replace(abi["text"], "0.14")), encoding="utf-8", newline="\n")
                found = compare(text, binary, root)
                report("drift", bool(found), found[0] if found else "a stale ABI passed --check")

        # cft-fp256 pinned to its first commit, with the snapshot saying GitHub
        # has it, so the refusal has to come from the sources themselves
        p = facts.pin("cft-fp256")
        first = facts._git(p.dir, "rev-list", "--max-parents=0", p.full).split()[0]
        saved_pin, saved_rec = facts.PINS["repos"]["cft-fp256"]["commit"], recs["cft-fp256"]
        facts.PINS["repos"]["cft-fp256"]["commit"] = first[:7]
        recs["cft-fp256"] = {"commit": first[:7], "sha": first}
        facts.forget_pins()
        try:
            render_all()
            report("stale-pin", False, "the pages built from cft-fp256's first commit")
        except Refusal as e:
            report("stale-pin", "cft-fp256" in str(e) and "snapshot" not in str(e), str(e))
        finally:
            facts.PINS["repos"]["cft-fp256"]["commit"], recs["cft-fp256"] = saved_pin, saved_rec
            facts.forget_pins()

    # "Last verified" takes the newest pass. verifier-P0 made it take the
    # oldest, and every stage passed: a newer passing run is planted for
    # atlas-film, and each ledger's newest pass is found again a second way,
    # by walking its entries from the newest back.
    try:
        name = "atlas-film"
        wf, p = facts.verifying(name)[0], facts.pin(name)
        runs = facts.snap()["runs"].setdefault(name, [])
        plant = dict(workflow=wf, sha=p.full, branch="main", status="completed", conclusion="success",
                     created="2099-01-01T12:00:00Z", url="https://example.invalid/planted")
        runs.append(plant)
        try:
            v = facts.last_verified(name)
        finally:
            runs.remove(plant)
        report("newest", v.raw == plant["created"], "a newer passing run planted for %s: last verified %s" % (name, v.text))
        # A run on a commit outside the pin's history says nothing about the
        # pinned tree, pass or fail (verifier-P0 removed the ancestry check,
        # and nothing changed at these pins).
        before, red_before = facts.last_verified(name).text, facts.ci_red(name).text
        for conclusion in ("success", "failure"):
            plant = dict(workflow=wf, sha="f" * 40, branch="elsewhere", status="completed", conclusion=conclusion,
                         created="2099-01-01T12:00:00Z", url="https://example.invalid/planted")
            runs.append(plant)
            try:
                v, red = facts.last_verified(name), facts.ci_red(name)
            finally:
                runs.remove(plant)
            ok = v.text == before and red.text == red_before
            report("newest", ok, "a newer %s run on a commit outside %s's history: last verified %s, open %r"
                   % (conclusion, name, v.text, red.text))
        for name in sorted(n for n, c in facts.PINS["repos"].items() if c.get("verified_by", {}).get("ledger")):
            led = facts.PINS["repos"][name]["verified_by"]["ledger"]
            t, ents = facts.entries(name, led["path"])
            want = next((e["date"] for e in sorted(ents, key=lambda e: (e["date"], e["start"]), reverse=True)
                         if any(re.search(pat, t[e["start"]:e["end"]], re.M) for pat in led["passes"].values())), None)
            got = facts.last_verified(name)
            ci = got.src.kind == "api"
            report("newest", ci or got.text == want, "%s's newest ledger pass, found again from its newest entry back: "
                   "%s; last verified shows %s" % (name, want, got.text))
    except Unavailable as e:
        skip("newest", "needs atlas-film, cft-rebound and Quantum-Film at their pins: %s" % e)

    # The map and every dossier's Connections read one list of edges
    # (mapgen.all_edges), and the links stage holds each dossier's published
    # list to the published map (check_connections; its planted faults are in
    # section A). The invariant that stood here compared two functions, not
    # the pages, and reported itself as a control (verifier-seam). What
    # stays is the reading P3 first had, relations.json alone, rendered and
    # shown to be refused by the published-page check.
    try:
        from pages import _dossier
        saved_edges = _dossier.edges_for
        _dossier.edges_for = lambda node: [(e, facts.prose(e["repo"], e["path"], e["pattern"]))
                                           for e in _dossier.RELATIONS["edges"] if node in (e["tail"], e["head"])]
        try:
            planted_text, _ = render_all()
        finally:
            _dossier.edges_for = saved_edges
        with tempfile.TemporaryDirectory() as d:
            for rel, body in planted_text.items():
                if rel.endswith(".html") and "/" not in rel:
                    (pathlib.Path(d) / rel).write_text(body, encoding="utf-8", newline="\n")
            found = [f for f in check_connections(pathlib.Path(d)) if "doesn't list the map's edge" in f]
        report("connections", bool(found), "the dossiers rendered from relations.json alone, as P3 first read it: %s"
               % (found[0] if found else "passed"))
    except Unavailable as e:
        skip("connections", "needs every pinned clone: %s" % e)

    # The GitHub stage, asked about one pin whose recorded SHA is planted wrong
    recs = facts.snap()["pins"]
    saved = recs["cft-fp256"]
    recs["cft-fp256"] = dict(saved, sha="0" * 40)
    try:
        found = check_github(only=["cft-fp256"])[0]
        report("github", bool(found), "a snapshot's SHA for cft-fp256 planted wrong: %s" % (found[0] if found else "passed"))
    except Unavailable as e:
        skip("github", str(e))
    finally:
        recs["cft-fp256"] = saved

    for m in pages():
        try:
            for name, caught, how in getattr(m, "controls", lambda: [])():
                report(name, caught, "%s: %s" % (m.__name__, how))
        except Unavailable as e:
            skip(m.__name__, "its own controls need a source this machine cannot read: %s" % e)

    print("controls: %d caught, %d did not fail, %d skipped by name"
          % (sum(results), len(results) - sum(results), len(skipped)))
    return 0 if all(results) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group()
    for flag, what in (("--check", "fail if public/ differs from a fresh render"),
                       ("--manifest", "public/ matches its MANIFEST, and so do pins.json, the snapshot and the site's own ledger"),
                       ("--verify-facts", "read every published figure again"),
                       ("--numbers", "every numeral on a page is a figure marked with its own fact"),
                       ("--links", "every relative link resolves to a published file, exactly, and each dossier's "
                                    "Connections are the map's edges touching its project"),
                       ("--local-only", "only allowed tags and attributes; nothing loads from another host; no email "
                                         "address but the contact; Wally only on the game thread's page"),
                       ("--docs", "the documents' links resolve, and none states the stage count"),
                       ("--privacy", "no tracked file names a private repository the site does not read"),
                       ("--github", "every pin is a commit GitHub has now, as the snapshot recorded"),
                       ("--planted-link", "the runner's own control: the links check on a planted copy"),
                       ("--control", "run the negative controls")):
        g.add_argument(flag, action="store_true", help=what)
    ap.add_argument("--require-all", action="store_true", help="with --verify-facts, a skip is a failure")
    a = ap.parse_args(argv)

    def problems_out(name, problems, tail):
        for p in problems:
            print("PROBLEM %s" % p, file=sys.stderr)
        print("%s: %d problem(s)%s" % (name, len(problems), tail))
        return 1 if problems else 0

    try:
        if a.verify_facts:
            return verify_facts(require_all=a.require_all)
        if a.manifest:
            return problems_out("manifest", check_manifest(), " in %d published files" % len(published(PUBLIC)))
        if a.numbers:
            problems, counts = check_numbers()
            n, allowed, files = counts if counts else (0, {}, 0)
            return problems_out("numbers", problems, "; %d marks tied to their own facts in %d files; allowed as "
                                "part of a name: %s" % (n, files, ", ".join("%r %d time(s)" % kv for kv in
                                                                           sorted(allowed.items())) or "none"))
        if a.links:
            return problems_out("links", check_links(), " in %d published files" % len(published(PUBLIC)))
        if a.local_only:
            return problems_out("local-only", check_local_only(), " in %d published files" % len(published(PUBLIC)))
        if a.docs:
            return problems_out("docs", check_docs(), " in %d documents" % len(doc_files()))
        if a.privacy:
            hits, n, blobs = check_privacy()
            hist = sum(1 for w, _ in blobs if " in history (blob " in w)
            other = {"paths", "commit messages", "tag messages", "commit identities", "tagger identities",
                     "branch and tag names"}
            files = sum(1 for w, _ in blobs if " in history (blob " not in w and w not in other)
            return problems_out("privacy", ["%s names a private repository the site does not read" % h for h in hits],
                                "; %d private repositories the site does not read, looked for in %d files, %d blobs "
                                "reachable in history, every path, the commit and tag messages, every author, "
                                "committer and tagger, and the branch and tag names" % (n, files, hist))
        if a.github:
            problems, n = check_github()
            return problems_out("github", problems, "; %d pins asked of GitHub, each the commit the snapshot "
                                "recorded" % n)
        if a.planted_link:
            return planted_link()
        if a.control:
            return controls()
        text, binary = render_all()
        if a.check:
            problems = compare(text, binary)
            for p in problems:
                print("DRIFT %s" % p, file=sys.stderr)
            if not problems:
                print("check: %d published files are exactly what the pins render" % (len(text) + len(binary)))
            return 1 if problems else 0
        write(text, binary)
        print("wrote %d files to public/ from %d pins; %d figures in facts.json"
              % (len(text) + len(binary), len(facts.PINS["repos"]), len(facts.LOG)))
        return 0
    except Unavailable as e:
        print("UNAVAILABLE: %s" % e, file=sys.stderr)
        return 3
    except Refusal as e:
        print("REFUSED: %s" % e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
