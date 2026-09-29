#!/usr/bin/env python3
"""Build loganw.dev: read the pinned sources, render the pages, write public/.

    python site/build.py                 # write public/ from the pins
    python site/build.py --check         # exit 1 if public/ differs from a fresh render
    python site/build.py --verify-facts  # read every figure in public/facts.json again, at its pin
    python site/build.py --links         # every relative link and src in public/ resolves
    python site/build.py --local-only    # nothing in public/ loads from another host, and nothing runs
    python site/build.py --control       # the negative controls; exit 0 only if each fails as it must

Exit codes: 0 pass; 1 a check found a problem; 2 a refusal or misuse; 3 a
source this machine cannot read (a private repository with no clone here), so
the runner can skip the stage by name rather than pass it.

public/ is committed and deployed as it stands (docs/SPEC.md, decisions 3 and
4): the desktop, which has every clone, builds it; --check proves the
committed copy is what the pins render; CI re-reads every public figure with
--verify-facts and names each private one it cannot.

Pages are found by glob in site/pages/, so adding one edits no list here.
"""
import argparse
import hashlib
import html.parser
import importlib
import json
import pathlib
import re
import shutil
import sys
import tempfile

SITE = pathlib.Path(__file__).resolve().parent
ROOT = SITE.parent
PUBLIC = ROOT / "public"
sys.path.insert(0, str(SITE))

import facts                    # noqa: E402
from facts import Refusal, Unavailable   # noqa: E402
import render                   # noqa: E402

BUILD_NOTE = ("This is the committed copy of the site. The deploy replaces this file with the commit it was "
              "deployed from, so a reader can ask which commit a live page came from.\n")


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def pages():
    mods = []
    for f in sorted((SITE / "pages").glob("*.py")):
        if f.stem.startswith("_"):
            continue
        m = importlib.import_module("pages." + f.stem)
        for need in ("PAGE", "render_page"):
            if not hasattr(m, need):
                raise Refusal("site/pages/%s.py defines no %s" % (f.name, need))
        if m.PAGE["nav"] not in render.NAV:
            raise Refusal("site/pages/%s.py claims nav entry %r, which is not in the navigation" % (f.name, m.PAGE["nav"]))
        mods.append(m)
    for key in ("file", "nav"):
        seen = [m.PAGE[key] for m in mods]
        dup = {x for x in seen if seen.count(x) > 1}
        if dup:
            raise Refusal("two pages share a %s: %s" % (key, sorted(dup)))
    return mods


def render_all():
    """-> (text files, binary files), each {published path: content}."""
    facts.reset_log()
    mods = pages()
    built = {m.PAGE["nav"]: m.PAGE["file"] for m in mods}
    text, binary = {}, {}
    for m in mods:
        body = m.render_page({"built": built})
        text[m.PAGE["file"]] = render.page(m.PAGE["title"], m.PAGE["nav"], built, body, m.PAGE["description"])
        for dest, repo, path in getattr(m, "ASSETS", []):
            binary[dest] = facts.pin(repo).show(path, binary=True)
    # One stylesheet per parcel under site/styles/, found by glob, so no two
    # parcels edit the same file (ParcelRound section 2: aim for a glob).
    text["style.css"] = "".join(f.read_text(encoding="utf-8") for f in
                                [SITE / "fonts" / "fontfaces.css", SITE / "style.css"]
                                + sorted((SITE / "styles").glob("*.css")))
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
    lines = ["# sha256 of every file this build published, beside the pins it read. The deploy adds BUILD.",
             "# pins: " + " ".join("%s@%s" % (k, v["commit"]) for k, v in facts.PINS["repos"].items()),
             "# snapshot: " + facts.PINS["snapshot"]]
    for path in sorted(list(text) + list(binary)):
        if path == "BUILD":
            continue
        data = text[path].encode("utf-8") if path in text else binary[path]
        lines.append("%s  %s" % (hashlib.sha256(data).hexdigest(), path))
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
            problems.append("%s is missing or not the bytes at its pin" % rel)
    extra = set(published(root)) - set(text) - set(binary) if root.is_dir() else set()
    problems += ["%s is published and no longer rendered" % e for e in sorted(extra)]
    return problems


# ---------------------------------------------------------------------------
# Checks on what is published
# ---------------------------------------------------------------------------

class _Refs(html.parser.HTMLParser):
    LOADS = {"img": "src", "script": "src", "iframe": "src", "audio": "src", "video": "src",
             "source": "src", "embed": "src", "object": "data", "track": "src"}

    def __init__(self):
        super().__init__()
        self.links, self.loads, self.scripts = [], [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script":
            self.scripts += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "link" and a.get("href"):
            self.loads.append(("link rel=%s" % a.get("rel", ""), a["href"]))
        if tag in self.LOADS and a.get(self.LOADS[tag]):
            self.loads.append((tag, a[self.LOADS[tag]]))


def _external(u):
    return re.match(r"^(?:[a-z][a-z0-9+.-]*:|//)", u, re.I) is not None


def check_links(root=PUBLIC):
    problems = []
    for rel in published(root):
        if not rel.endswith(".html"):
            continue
        p = _Refs()
        p.feed((root / rel).read_text(encoding="utf-8"))
        for u in p.links + [u for _, u in p.loads]:
            if _external(u) or u.startswith("#"):
                continue
            target = (root / rel).parent / u.split("#")[0].split("?")[0]
            if not target.resolve().is_file() or root.resolve() not in target.resolve().parents:
                problems.append("%s links to %s, which is not published" % (rel, u))
    return problems


def check_local_only(root=PUBLIC):
    problems = []
    for rel in published(root):
        f = root / rel
        if rel.endswith(".html"):
            p = _Refs()
            p.feed(f.read_text(encoding="utf-8"))
            if p.scripts:
                problems.append("%s has %d script element(s); the site runs no script" % (rel, p.scripts))
            for what, u in p.loads:
                if _external(u) and not u.startswith("data:"):
                    problems.append("%s: %s loads %s from another host" % (rel, what, u))
        elif rel.endswith(".css"):
            css = f.read_text(encoding="utf-8")
            for u in re.findall(r"url\(\s*['\"]?([^'\")]+)", css):
                if _external(u) and not u.startswith("data:"):
                    problems.append("%s: url(%s) loads from another host" % (rel, u))
            if re.search(r"@import", css):
                problems.append("%s uses @import" % rel)
    return problems


DOCS_EXEMPT = {"docs/VALIDATION.md"}   # the ledger: a path in it is a fact about its date


def doc_files():
    fs = [ROOT / "README.md", ROOT / "CLAUDE.md", ROOT / "design" / "README.md"]
    fs += sorted((ROOT / "docs").glob("*.md"))
    return [f for f in fs if f.is_file() and f.relative_to(ROOT).as_posix() not in DOCS_EXEMPT]


def runner_stages():
    return len(re.findall(r'^stage [a-z0-9-]+ "', (ROOT / "verify" / "run.sh").read_text(encoding="utf-8"), re.M))


def _prose(f):
    """A document's text outside fenced code blocks."""
    outside, fenced = [], False
    for line in f.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            outside.append(line)
    return "\n".join(outside)


def check_stage_claims(files):
    """Every "N stages" in these files is the runner's own count of its stage lines."""
    n, problems = runner_stages(), []
    for f in files:
        for m in re.finditer(r"\b(\d+) stages\b", _prose(f)):
            if int(m.group(1)) != n:
                problems.append("%s says %s stages; verify/run.sh has %d" % (f.name, m.group(1), n))
    return problems


def check_docs():
    """Relative links in the documents resolve, and the stage count the two
    front-door files state (README.md, CLAUDE.md) is the runner's own."""
    problems = []
    for f in doc_files():
        rel = f.relative_to(ROOT).as_posix()
        for href in re.findall(r"\[[^\]]+\]\(([^)\s]+)\)", _prose(f)):
            if _external(href) or href.startswith("#"):
                continue
            if not (f.parent / href.split("#")[0]).exists():
                problems.append("%s links to %s, which does not exist" % (rel, href))
    return problems + check_stage_claims([f for f in (ROOT / "README.md", ROOT / "CLAUDE.md") if f.is_file()])


def planted_link():
    """The runner's own control: the links check on a copy with a broken link.
    Exit 1 is the check saying no, which is what the runner requires."""
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        shutil.copytree(PUBLIC, root, dirs_exist_ok=True)
        page = root / "index.html"
        page.write_text(page.read_text(encoding="utf-8").replace("</footer>", '<a href="planted.html">x</a></footer>', 1),
                        encoding="utf-8", newline="\n")
        found = check_links(root)
        print("planted-link: %s" % (found[0] if found else "the broken link passed"))
        return 1 if found else 0


def verify_facts(root=PUBLIC, require_all=False):
    data = json.loads((root / "facts.json").read_text(encoding="utf-8"))
    ok, bad, skipped, stated = 0, [], [], 0
    for rec in data["facts"]:
        if rec["kind"] == "stated":
            stated += 1
            continue
        try:
            same, now = facts.rederive(rec)
        except Refusal as e:
            bad.append("fact %d (%s) cannot be read again: %s" % (rec["id"], rec["method"], e))
            continue
        if same is None:
            skipped.append("fact %d (%s): %s" % (rec["id"], rec["where"], now))
        elif same:
            ok += 1
        else:
            bad.append("fact %d (%s) printed %r, and its source now gives %r" % (rec["id"], rec["where"], rec["text"], now))
    for s in skipped:
        print("SKIPPED %s" % s)
    for b in bad:
        print("MISMATCH %s" % b, file=sys.stderr)
    print("verify-facts: %d read again and the same, %d different, %d skipped by name, %d stated"
          % (ok, len(bad), len(skipped), stated))
    if bad:
        return 1
    if skipped and require_all:
        print("verify-facts: %d skipped, and --require-all makes a skip a failure" % len(skipped), file=sys.stderr)
        return 1
    return 0


# ---------------------------------------------------------------------------
# The negative controls. Each must FAIL; if one passes, the check it controls
# cannot see the defect it exists for, and everything it passed is decoration.
# ---------------------------------------------------------------------------

def controls():
    results = []

    def report(name, caught, how):
        results.append(caught)
        print("control %-12s %s - %s" % (name, "caught, as it must be" if caught else "NEGATIVE CONTROL DID NOT FAIL", how))

    text, binary = render_all()
    abi = [r for r in facts.LOG if r["method"] == "facts.macros"]
    if not abi:
        report("drift", False, "no ABI figure was rendered to plant against")
        return 1
    needle = '<span class="fig">%s</span>' % abi[0]["text"]
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        write(text, binary, root)

        # 1. a stale figure in a published page
        page = root / "index.html"
        t = page.read_text(encoding="utf-8")
        if needle not in t:
            report("drift", False, "could not plant: %r is not in the page" % needle)
        else:
            page.write_text(t.replace(needle, '<span class="fig">0.14</span>', 1), encoding="utf-8", newline="\n")
            found = compare(text, binary, root)
            report("drift", bool(found), found[0] if found else "a stale ABI passed --check")
            page.write_text(t, encoding="utf-8", newline="\n")

        # 2. a stale figure in facts.json
        fj = root / "facts.json"
        data = json.loads(fj.read_text(encoding="utf-8"))
        rec = next(r for r in data["facts"] if r["method"] == "facts.macros")
        rec["text"] = rec["raw"] = "0.14"
        fj.write_text(json.dumps(data), encoding="utf-8")
        rc = verify_facts(root)
        report("facts", rc == 1, "fact %d planted at 0.14 was %s" % (rec["id"], "named" if rc == 1 else "passed"))

        # 3. a broken link
        page.write_text(t.replace("</footer>", '<a href="nowhere.html">x</a></footer>', 1), encoding="utf-8", newline="\n")
        found = check_links(root)
        report("links", any("nowhere.html" in f for f in found), found[0] if found else "a broken link passed")

        # 4. a resource from another host, and a script
        page.write_text(t.replace("</head>", '<link rel="stylesheet" href="https://fonts.googleapis.com/css2">'
                                  '<script>1</script></head>', 1), encoding="utf-8", newline="\n")
        found = check_local_only(root)
        report("local-only", len(found) == 2, "; ".join(found) if found else "both plants passed")
        page.write_text(t, encoding="utf-8", newline="\n")

    # 5. a front-door document stating the wrong number of stages, through the
    #    same function check_docs applies to README.md and CLAUDE.md
    with tempfile.TemporaryDirectory() as d:
        copy = pathlib.Path(d) / "CLAUDE.md"
        copy.write_text("# planted\n\nThe runner has %d stages.\n" % (runner_stages() + 1), encoding="utf-8")
        found = check_stage_claims([copy])
        report("docs", bool(found), found[0] if found else "a wrong stage count passed")

    # 6. a figure no fact produced
    try:
        render.fig(facts.V("0.15", facts.Src("file", "typed by hand")))
        report("unlogged", False, "a figure with no fact behind it was rendered")
    except Refusal as e:
        report("unlogged", True, str(e))

    # 6. a stale source: cft-fp256 pinned to its first commit
    saved = facts.PINS["repos"]["cft-fp256"]["commit"]
    facts.PINS["repos"]["cft-fp256"]["commit"] = "644ee2d"
    facts.forget_pins()
    try:
        render_all()
        report("stale-pin", False, "the pages built from cft-fp256's first commit")
    except Refusal as e:
        report("stale-pin", "cft-fp256" in str(e), str(e))
    finally:
        facts.PINS["repos"]["cft-fp256"]["commit"] = saved
        facts.forget_pins()
    return 0 if all(results) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group()
    for flag, what in (("--check", "fail if public/ differs from a fresh render"),
                       ("--verify-facts", "read every published figure again at its pin"),
                       ("--links", "every relative link resolves"),
                       ("--local-only", "nothing loads from another host; no script"),
                       ("--docs", "the documents' links resolve and their stage counts are true"),
                       ("--planted-link", "the runner's own control: the links check on a planted copy"),
                       ("--control", "run the negative controls")):
        g.add_argument(flag, action="store_true", help=what)
    ap.add_argument("--require-all", action="store_true", help="with --verify-facts, a skip is a failure")
    a = ap.parse_args(argv)
    try:
        if a.verify_facts:
            return verify_facts(require_all=a.require_all)
        if a.links or a.local_only:
            problems = check_links() if a.links else check_local_only()
            for p in problems:
                print("PROBLEM %s" % p, file=sys.stderr)
            print("%s: %d problem(s) in %d published files" % ("links" if a.links else "local-only",
                                                              len(problems), len(published(PUBLIC))))
            return 1 if problems else 0
        if a.docs:
            problems = check_docs()
            for p in problems:
                print("PROBLEM %s" % p, file=sys.stderr)
            print("docs: %d problem(s) in %d documents" % (len(problems), len(doc_files())))
            return 1 if problems else 0
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
