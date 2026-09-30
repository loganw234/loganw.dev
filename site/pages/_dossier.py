"""Shared renderer for the Work section's five dossiers (docs/SPEC.md, "Work").
A leading underscore keeps this out of pages.discover(): it is imported, not
published.

Each dossier module builds one list of nine Section()s - the spec's fixed
schema - and hands it to html() for the page body and to twin() for the
plain-text file extra_files() publishes. Both read the SAME segment lists
(str / facts.V / render.C / render.L, exactly what render.render() and
render.plain() already accept), so a figure cannot appear on the page and
vanish from its twin without one of them being edited on its own - which
is exactly the drift check() and twin_ids() exist to catch.

A dossier module's own controls() should call fits_nine(), section_gate() and
twin_ids() against a copy it deliberately breaks, per briefs/P3.md's three
named negative controls.
"""
import json
import pathlib
import re

import facts
from facts import V, Src, Refusal, fact, pin
import render as render_mod
from render import C, L, esc

ROOT = pathlib.Path(__file__).resolve().parent.parent
RELATIONS = json.loads((ROOT / "data" / "relations.json").read_text(encoding="utf-8"))
KIND = dict(RELATIONS["kinds"])

TITLES = ("What it is", "What it is not", "The contract", "Verified", "Kept failures",
          "Test it", "Prove it wrong", "Connections", "Provenance")
ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX")


class Section:
    __slots__ = ("title", "blocks")

    def __init__(self, title, blocks):
        self.title = title
        self.blocks = blocks    # a list of blocks, each {"html": str, "text": str}


# ---------------------------------------------------------------------------
# Blocks: one paragraph, one list, or one table, each built once and read
# twice (as HTML and as its plain twin) from the same segment lists.
# ---------------------------------------------------------------------------

def para(segs):
    return {"html": "<p>%s</p>" % render_mod.render(segs), "text": render_mod.plain(segs)}


def list_(items, ordered=False):
    """items: a list of segment-lists, one per <li>. An <ol>'s numbering is
    the browser's own, drawn with no digit in the markup; the text twin
    keeps the same order with a plain dash rather than a typed ordinal, so
    it states no count the page itself does not also state through a mark."""
    tag = "ol" if ordered else "ul"
    html = "<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % render_mod.render(i) for i in items), tag)
    lines = ["- " + render_mod.plain(it) for it in items]
    return {"html": html, "text": "\n".join(lines)}


def table(headers, rows):
    """rows: a list of rows, each a list of segment-lists, one per cell."""
    thead = "<thead><tr>%s</tr></thead>" % "".join("<th>%s</th>" % esc(h) for h in headers)
    trs = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % render_mod.render(c) for c in row) for row in rows)
    html = "<table>%s<tbody>%s</tbody></table>" % (thead, trs)
    lines = [" | ".join(headers)]
    for row in rows:
        lines.append(" | ".join(render_mod.plain(c) for c in row))
    return {"html": html, "text": "\n".join(lines)}


def section(title, blocks):
    if title not in TITLES:
        raise Refusal("a dossier section is titled %r, which is not one of the nine the spec fixes" % title)
    return Section(title, blocks)


# ---------------------------------------------------------------------------
# The section gate: all nine, in order, none empty. Named by dossier and
# section, so a plant lands where the control reads it.
# ---------------------------------------------------------------------------

def check_sections(dossier, sections):
    got = tuple(s.title for s in sections)
    if got != TITLES:
        missing = [t for t in TITLES if t not in got]
        if missing:
            raise Refusal("%s: missing the section %r" % (dossier, missing[0]))
        raise Refusal("%s: sections are %r, not the spec's order %r" % (dossier, got, TITLES))
    for s in sections:
        if not s.blocks or all(not b["html"].strip() and not b["text"].strip() for b in s.blocks):
            raise Refusal("%s: section %r is empty" % (dossier, s.title))


# ---------------------------------------------------------------------------
# Rendering: the page body, and the plain-text twin from the same sections.
# ---------------------------------------------------------------------------

def html(dossier, sections):
    check_sections(dossier, sections)
    out = []
    for i, s in enumerate(sections):
        out.append("<h2><small>%s</small>%s</h2>" % (ROMAN[i], esc(s.title)))
        out.append("".join(b["html"] for b in s.blocks))
    return "".join(out)


def twin(dossier, title, sections):
    check_sections(dossier, sections)
    lines = [title, "=" * len(title), ""]
    for i, s in enumerate(sections):
        lines.append("%s. %s" % (ROMAN[i], s.title))
        lines.append("")
        for b in s.blocks:
            lines.append(b["text"])
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


_MARK = re.compile(r'data-f="(\d+)"')
_TWIN = re.compile(r"\[fact (\d+)\]")


def twin_ids(dossier, html_body, text_body):
    """The set of fact ids the page carries must equal the set its twin
    carries: a figure present in one and lost from the other is refused,
    naming the dossier and the ids that differ."""
    h = {int(m) for m in _MARK.findall(html_body)}
    t = {int(m) for m in _TWIN.findall(text_body)}
    if h != t:
        raise Refusal("%s: the page carries facts %s and the twin carries %s; missing from the twin: %s; "
                      "extra in the twin: %s" % (dossier, sorted(h), sorted(t), sorted(h - t), sorted(t - h)))


# ---------------------------------------------------------------------------
# A kept failure's commit: shown to exist at the repository's pin, and part
# of the history the pin reads - never a hash that only exists elsewhere.
# ---------------------------------------------------------------------------

@fact
def kept_failure(name, sha, what):
    p = pin(name)
    p.git("cat-file", "-e", sha + "^{commit}")   # raises Refusal (via facts._git) if sha names no commit here
    full = p.git("rev-parse", sha).strip()
    if not p.is_ancestor(full):
        raise Refusal("%s: %s exists but is not part of the history the pin %s reads" % (name, sha, p.short))
    href = "" if p.private else "https://github.com/%s/%s/commit/%s" % (p.owner, p.ghname, sha)
    return V(sha, Src("git", "%s %s" % (name, sha), "the commit that fixed it: %s" % what, href, p.private),
             raw=sha, num=True)


# ---------------------------------------------------------------------------
# A ledger row, by heading line: the entry's own date and title, re-read
# through facts.entries() rather than a second parser (briefs/P1.md's trap
# applies here too).
# ---------------------------------------------------------------------------

def _entry_at(name, path, line):
    t, ents = facts.entries(name, path)
    e = next((e for e in ents if e["line"] == line), None)
    if e is None:
        raise Refusal("%s %s: no ledger entry heading at line %d" % (name, path, line))
    return e


@fact
def ledger_date(name, path, line):
    e = _entry_at(name, path, line)
    return V(e["date"], pin(name).src("file", "%s:%d" % (path, line), "the entry's own date (%s)" % e["how"],
                                       path, line), raw=e["date"], num=True)


@fact
def ledger_title(name, path, line):
    e = _entry_at(name, path, line)
    return V(e["title"], pin(name).src("file", "%s:%d" % (path, line), "the entry's heading", path, line),
             raw=e["title"])


# ---------------------------------------------------------------------------
# Connections: relations.json's edges, read the same way mapgen.py reads
# them (facts.prose(repo, path, pattern), no second parser).
# ---------------------------------------------------------------------------

def edges_for(node):
    """Every edge the map draws that touches node, with its evidence: the same
    list the map itself uses (mapgen.all_edges), so a dossier's Connections
    include the edges derived at a pin - StoryDocs' - and not only
    relations.json's own. (The lead, at P2's merge.)"""
    import mapgen
    return [(e, e["v"]) for e in mapgen.all_edges() if node in (e["tail"], e["head"])]


def connections_block(node):
    edges = edges_for(node)
    if not edges:
        raise Refusal("%s: relations.json names no edge touching it" % node)
    items = []
    for e, v in edges:
        items.append([C(e["tail"]), " ", KIND[e["kind"]], " ", C(e["head"]), ": ", v])
    return list_(items)


# ---------------------------------------------------------------------------
# Provenance: the files this dossier read, each shown to exist at the pin,
# and the pin itself.
# ---------------------------------------------------------------------------

def provenance_block(repos):
    """repos: [(name, [path, ...])], each path shown to exist at that
    repository's own pin. A dossier may read a source outside its own
    project - a citation of HonestFramework's CASE-STUDY.md, say - so this
    takes one list per repository rather than a single name."""
    blocks = []
    for name, paths in repos:
        commit = facts.pin_commit(name)
        items = [[facts.exists(name, p)] for p in paths]
        blocks.append(para([C(name), " read at ", commit, "."]))
        blocks.append(list_(items))
    return blocks
