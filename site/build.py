#!/usr/bin/env python3
"""Build loganw.dev: read the pinned sources, render the pages, write public/.

    python site/build.py                 # write public/ from the pins
    python site/build.py --check         # exit 1 if public/ differs from a fresh render
    python site/build.py --manifest      # public/ matches its own MANIFEST, and so do pins.json and the snapshot
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
                 "deployed from, and this file. The source lines hash what the build read besides the pins.")


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


def sources():
    """What the build read besides the pins, by path: pins.json and the snapshot."""
    return [(p, (ROOT / p).read_bytes()) for p in ("pins.json", facts.PINS["snapshot"])]


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
            binary[dest] = facts.pin(repo).show(path, binary=True)
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


def write(text, binary, root=PUBLIC):
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
    """public/ is what its MANIFEST says, file for file, and pins.json and the
    snapshot are the bytes the build read. What CI can hold without rendering:
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
    for path in ("pins.json", facts.PINS["snapshot"]):
        if path not in srcs:
            problems.append("MANIFEST does not hash %s, which the build reads" % path)
        elif sha256((ROOT / path).read_bytes()) != srcs[path]:
            problems.append("%s is not the bytes the build read" % path)
    return problems


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
TICK = re.compile(r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?: \d{4})?")


class _Marks(html.parser.HTMLParser):
    """Every figure mark (data-f) with its text, and every run of text outside one."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.marks, self.loose, self.attr_text, self.problems = [], [], [], [], []

    def _mark(self):
        return next((n for n in reversed(self.stack) if n["f"] is not None), None)

    def _attrs(self, tag, a):
        for k in ("alt", "title", "aria-label"):
            if a.get(k):
                self.attr_text.append("%s %s=%r" % (tag, k, a[k]))
        if tag == "meta" and a.get("name") == "description":
            self.attr_text.append("meta description %r" % a.get("content", ""))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self._attrs(tag, a)
        if tag in VOID:
            return
        cls, f = (a.get("class") or "").split(), a.get("data-f")
        if f is None and tag == "span" and set(cls) & {"fig", "q", "stated", "src"}:
            self.problems.append("a span of class %r has no fact id" % " ".join(cls))
        if f is not None and self._mark() is not None:
            self.problems.append("a mark for fact %s sits inside the mark for fact %s" % (f, self._mark()["f"]))
        if tag == "a" and self._mark() is not None:
            self._mark()["href"] = a.get("href", "")
        self.stack.append(dict(tag=tag, cls=cls, f=f, buf=[], href=None))

    def handle_startendtag(self, tag, attrs):
        self._attrs(tag, dict(attrs))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        while self.stack:
            n = self.stack.pop()
            if n["f"] is not None:
                self.marks.append(n)
            if n["tag"] == tag:
                break

    def handle_data(self, data):
        m = self._mark()
        if m is not None:
            m["buf"].append(data)
        elif data.strip():
            self.loose.append((data, any("tick" in n["cls"] for n in self.stack)))


def numeral_names():
    return sorted({n for m in page_modules.discover() for n in getattr(m, "NUMERAL_NAMES", [])}, key=len, reverse=True)


def _loose_problems(where, text, tick, names, allowed):
    out = []
    if tick and TICK.fullmatch(text.strip()):
        return out
    for n in names:
        allowed[0] += text.count(n)
        text = text.replace(n, " ")
    for n in facts.numerals(text):
        out.append("%s: %r is a numeral outside any figure's mark, in %r" % (where, n, " ".join(text.split())[:80]))
    for w in facts.NUMBER_WORDS.findall(text):
        out.append("%s: %r is a number word outside any figure's mark, in %r" % (where, w, " ".join(text.split())[:80]))
    return out


def check_numbers(root=PUBLIC):
    """Every numeral a page prints sits inside a mark (data-f) for a fact whose
    text is exactly the mark's text; every source label is its own fact's
    label; and a text file writes each figure as `text [fact N]`. So a figure
    typed as a plain string, or copied with its text changed, fails. A number
    written in words is caught only for the words facts.NUMBER_WORDS lists."""
    fj = root / "facts.json"
    if not fj.is_file():
        return ["facts.json is missing"], 0
    by_id = {r["id"]: r for r in json.loads(fj.read_text(encoding="utf-8"))["facts"]}
    names, allowed, problems, n_marks = numeral_names(), [0], [], 0
    files = published(root)
    if not any(f.endswith(".html") for f in files):
        return ["no page is published"], 0
    for rel in files:
        if rel.endswith(".html"):
            p = _Marks()
            p.feed((root / rel).read_text(encoding="utf-8"))
            p.close()
            problems += ["%s: %s" % (rel, x) for x in p.problems]
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
            for text, tick in p.loose:
                problems += _loose_problems(rel, text, tick, names, allowed)
            for t in p.attr_text:
                problems += _loose_problems(rel, t, False, names, allowed)
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
    return problems, (n_marks, allowed[0], len(files))


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
        if tag == "path" and "marker-end" in a and not re.fullmatch(r"url\(#[\w-]+\)", a["marker-end"]):
            self.problems.append("<path marker-end=%r> is not a reference within the page" % a["marker-end"])
        if tag == "svg" and a.get("xmlns", "http://www.w3.org/2000/svg") != "http://www.w3.org/2000/svg":
            self.problems.append("<svg xmlns=%r>" % a["xmlns"])

    handle_startendtag = handle_starttag


def css_problems(css):
    """A stylesheet's loads. Comments go first, then anything that could spell
    a load in another case or through an escape is refused outright."""
    out = []
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    if "\\" in css:
        out.append("a backslash escape, which could spell a load")
    for pat, what in ((r"@import", "@import"), (r"image-set\(", "image-set()"), (r"(?<![\w-])src\(", "src()"),
                      (r"expression\(", "expression()"), (r"-moz-binding", "-moz-binding"), (r"behavior\s*:", "behavior")):
        if re.search(pat, css, re.I):
            out.append("uses %s" % what)
    for u in re.findall(r"url\(\s*['\"]?([^'\")]*)", css, re.I):
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
    if not any(r.endswith(".html") for r in published(root)):
        problems.append("no page is published")
    return problems


class _Refs(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        for k in ("href", "src"):
            if a.get(k) is not None:
                self.refs.append(a[k])

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
            css = re.sub(r"/\*.*?\*/", "", (root / rel).read_text(encoding="utf-8"), flags=re.S)
            refs += [(rel, u) for u in re.findall(r"url\(\s*['\"]?([^'\")]*)", css, re.I)]
    for rel, u in refs:
        if SCHEME.match(u) or u.startswith("//"):
            continue
        t = _target(rel, u, files)
        if t is None:
            problems.append("%s links to %s, which is not a published file" % (rel, u))
        elif "#" in u and u.split("#", 1)[1] and u.split("#", 1)[1] not in ids.get(t, set()):
            problems.append("%s links to %s, and %s has no such id" % (rel, u, t))
    if not any(f.endswith(".html") for f in files):
        problems.append("no page is published")
    return problems


DOCS_EXEMPT = {"docs/VALIDATION.md"}   # the ledger: a count in it is a fact about its date


def doc_files():
    fs = [ROOT / "README.md", ROOT / "CLAUDE.md", ROOT / "design" / "README.md"]
    fs += sorted((ROOT / "docs").glob("*.md"))
    return [f for f in fs if f.is_file() and f.relative_to(ROOT).as_posix() not in DOCS_EXEMPT]


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
               "sixteen|seventeen|eighteen|nineteen|twenty")
STAGE_COUNT = re.compile(r"\b(?:\d+|%s)(?:[\s-]+[a-z]+){0,2}?[\s-]+stages?\b" % COUNT_WORDS, re.I)


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
    code fence that no check read). Every relative link resolves - inline,
    with a title, by reference, or a raw <a> - and so does its #anchor."""
    problems = []
    for f in files if files is not None else doc_files():
        rel = f.name if files is not None else f.relative_to(ROOT).as_posix()
        t = f.read_text(encoding="utf-8")
        for m in STAGE_COUNT.finditer(" ".join(t.split())):
            problems.append("%s states a stage count, %r; `bash verify/run.sh --list` prints the stages instead"
                            % (rel, m.group(0)))
        prose = _prose(t)
        defs = {k.lower(): v for k, v in re.findall(r"^ {0,3}\[([^\]]+)\]:\s*<?(\S+?)>?(?:\s+.*)?$", prose, re.M)}
        hrefs = re.findall(r"\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)", prose)
        hrefs += re.findall(r"<a\s[^>]*href=[\"']([^\"']+)[\"']", prose, re.I)
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


def tracked_texts(root=ROOT):
    """[(where, text)]: every file git would commit (tracked, or new and not
    ignored), every commit message on every branch, and every branch name."""
    out = []
    ls = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                        capture_output=True).stdout.decode("utf-8", "replace")
    for rel in sorted(set(x for x in ls.split("\0") if x)):
        f = root / rel
        if f.is_file():
            b = f.read_bytes()
            if b"\0" not in b:
                out.append((rel, b.decode("utf-8", "replace")))
    for what, args in (("commit messages", ["log", "--all", "--format=%B"]),
                       ("branch names", ["for-each-ref", "--format=%(refname)"])):
        out.append((what, subprocess.run(["git", "-C", str(root), *args], capture_output=True).stdout.decode("utf-8", "replace")))
    return out


def find_named(names, texts):
    """Where any of names appears as a word: ['where:line']. The names are not
    printed, since printing them is the leak this looks for."""
    pats = [re.compile(r"(?<![\w.-])%s(?![\w-])" % re.escape(n), re.I) for n in names]
    hits = []
    for where, t in texts:
        for i, line in enumerate(t.splitlines(), 1):
            if any(p.search(line) for p in pats):
                hits.append("%s:%d" % (where, i))
    return hits


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
    texts = tracked_texts()
    return find_named(unread, texts), len(unread), len(texts)


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
            planted("numbers", "a source label changed",
                    re.sub(r'(<span class="src" data-f="%d"> (?:<a [^>]*>)?\()' % agent["id"], r"\1planted ", t, count=1),
                    check_numbers, "fact %d's source" % agent["id"])
            planted("numbers", "a figure in a page's alt text", t.replace('alt="The Pauli print"', 'alt="The 3 prints"', 1),
                    check_numbers, "'3'")

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
        for what, css in (("URL( in capitals", "a{background:URL(https://x.invalid/a.png)}"),
                          ("@IMPORT", "@IMPORT 'https://x.invalid/a.css';"),
                          ("image-set", 'a{background:image-set("https://x.invalid/a.png" 1x)}'),
                          ("an escaped url", "a{background:u\\72l(https://x.invalid/a.png)}")):
            found = css_problems(css)
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
                                  ("a missing heading anchor", "[x](README.md#no-such-heading)", "#no-such-heading")):
            if base:
                report("docs", False, "could not plant %s: CLAUDE.md already fails: %s" % (what, base[0]))
                continue
            copy.write_text(doc + "\n" + plant + "\n", encoding="utf-8")
            found = [f for f in check_docs([copy]) if want in f]
            report("docs", bool(found), "%s: %s" % (what, found[0] if found else "passed"))

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
    refused("paraphrase", "a pattern that matches more than once",
            lambda: facts.prose("cft-fp256", "README.md", r"(cft-fp256)"), "matches")
    refused("stated", "a statement about a pin that has since moved",
            lambda: facts.stated("planted", "Logan", "2026-09-29", holds_at={"cft-fp256": "0000000"}), "restate")
    heads = facts.ledger_headings("## 2026-01-01 - a\n```\n## 2026-01-02 - fenced\n```\n## 2026-01-03 - b\n")
    report("ledger", len(heads) == 2, "a heading inside a code fence: %d headings read of 2 outside fences" % len(heads))
    facts.reset_log()
    v = facts.stated("planted", "Logan", "2026-09-29")
    import dataclasses
    for what, bad in (("no fact produced", facts.V("0.15", facts.Src("file", "typed by hand"))),
                      ("its text changed after the fact", dataclasses.replace(v, text="1079/1079")),
                      ("its source changed after the fact", dataclasses.replace(v, src=facts.Src("file", "elsewhere")))):
        refused("unlogged", "a figure with %s" % what, lambda bad=bad: render.fig(bad))
    hits = find_named(["planted-private-repo"], [("planted.md", "see\nplanted-private-repo for more")])
    report("privacy", hits == ["planted.md:2"], "a private name in a tracked file: %s" % (hits or "passed"))

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
                       ("--manifest", "public/ matches its MANIFEST, and so do pins.json and the snapshot"),
                       ("--verify-facts", "read every published figure again"),
                       ("--numbers", "every numeral on a page is a figure marked with its own fact"),
                       ("--links", "every relative link resolves to a published file, exactly"),
                       ("--local-only", "only allowed tags and attributes; nothing loads from another host"),
                       ("--docs", "the documents' links resolve, and none states the stage count"),
                       ("--privacy", "no tracked file names a private repository the site does not read"),
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
            n, allowed, files = counts if counts else (0, 0, 0)
            return problems_out("numbers", problems, "; %d marks tied to their own facts in %d files, %d numerals "
                                "allowed as part of a name" % (n, files, allowed))
        if a.links:
            return problems_out("links", check_links(), " in %d published files" % len(published(PUBLIC)))
        if a.local_only:
            return problems_out("local-only", check_local_only(), " in %d published files" % len(published(PUBLIC)))
        if a.docs:
            return problems_out("docs", check_docs(), " in %d documents" % len(doc_files()))
        if a.privacy:
            hits, n, m = check_privacy()
            return problems_out("privacy", ["%s names a private repository the site does not read" % h for h in hits],
                                "; %d private repositories the site does not read, looked for in %d files, the "
                                "commit messages and the branch names" % (n, m - 2))
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
