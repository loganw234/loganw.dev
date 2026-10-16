"""The resume's printout (decision 45): a plain PDF of the page, laid out like
Logan's own draft, and the text twin it is built from.

The page is read once, as built, into a twin: one block a line, each figure
followed by its id as the dossiers' twins write it, `text [fact N]`, and each
link written [text](url). The PDF is written from the twin and from nothing
else. So the gates hold the PDF through its twin: the numbers stage reads
the twin as it reads any text file, and refuses a PDF that is not exactly
the bytes pdf() writes from it (build.check_numbers). A PDF can carry what
no check reads - a script, an action, hidden text - and this one can't,
since every byte of it is this module's output.

The twin's lines:
  the first three   the name, the role, the contact line;
  "== "             a section's heading;
  "=== "            a project's heading, then " | " and its dates;
  "- "              a bullet;
  "-- "             the note at the foot of the last page, in monospace;
  any other         a paragraph.
A blank line separates blocks and says nothing.

The PDF uses three of the standard 14 fonts, unembedded, in WinAnsi encoding:
Helvetica, Helvetica-Bold and Courier. A character outside cp1252 is
refused. Every byte of a string outside printable ASCII is written as an
octal escape, so the file is ASCII from end to end. It holds no date, so the
same twin always gives the same bytes.
"""
import html.parser
import re

from facts import Refusal

NAME = "Logan W."
SITE = "https://loganw.dev/"
NOTE = ("This PDF is built, not written: the site's build prints it from the page at [%sresume.html](%sresume.html), "
        "which names the source of every line, or marks it as Logan's own word." % (SITE, SITE))

PAGE_W, PAGE_H, MARGIN = 612, 792, 54
WIDTH = PAGE_W - 2 * MARGIN
FONTS = (("F1", "Helvetica"), ("F2", "Helvetica-Bold"), ("F3", "Courier"))

# Base 14 advance widths, in thousandths of the size, for the cp1252 bytes 32
# to 255 (an undefined byte is 0), read from PyMuPDF's copies of the AFM
# metrics on 2026-10-16. Courier's are 600 throughout.
HELVETICA = [
    278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556, 556,
    556, 556, 556, 556, 278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667,
    556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556,
    556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722,
    500, 500, 500, 334, 260, 334, 584, 0, 556, 0, 222, 556, 333, 1000, 556, 556, 333, 1000, 667, 333, 1000, 0, 611,
    0, 0, 222, 222, 333, 333, 350, 556, 1000, 333, 1000, 500, 333, 944, 0, 500, 667, 278, 333, 556, 556, 556, 556,
    260, 556, 333, 737, 370, 556, 584, 333, 737, 333, 400, 584, 333, 333, 333, 556, 537, 278, 333, 333, 365, 556,
    834, 834, 834, 611, 667, 667, 667, 667, 667, 667, 1000, 722, 667, 667, 667, 667, 278, 278, 278, 278, 722, 722,
    778, 778, 778, 778, 778, 584, 778, 722, 722, 722, 722, 667, 667, 611, 556, 556, 556, 556, 556, 556, 889, 500,
    556, 556, 556, 556, 278, 278, 278, 278, 556, 556, 556, 556, 556, 556, 556, 584, 611, 556, 556, 556, 556, 500,
    556, 500]
HELVETICA_BOLD = [
    278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556, 556,
    556, 556, 556, 556, 333, 333, 584, 584, 584, 611, 975, 722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722,
    611, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 333, 278, 333, 584, 556, 333, 556,
    611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611, 611, 611, 389, 556, 333, 611, 556, 778,
    556, 556, 500, 389, 280, 389, 584, 0, 556, 0, 278, 556, 500, 1000, 556, 556, 333, 1000, 667, 333, 1000, 0, 611,
    0, 0, 278, 278, 500, 500, 350, 556, 1000, 333, 1000, 556, 333, 944, 0, 500, 667, 278, 333, 556, 556, 556, 556,
    280, 556, 333, 737, 370, 556, 584, 333, 737, 333, 400, 584, 333, 333, 333, 611, 556, 278, 333, 333, 365, 556,
    834, 834, 834, 611, 722, 722, 722, 722, 722, 722, 1000, 722, 667, 667, 667, 667, 278, 278, 278, 278, 722, 722,
    778, 778, 778, 778, 778, 584, 778, 722, 722, 722, 722, 667, 667, 611, 556, 556, 556, 556, 556, 556, 889, 556,
    556, 556, 556, 556, 278, 278, 278, 278, 611, 611, 611, 611, 611, 611, 611, 584, 611, 611, 611, 611, 611, 556,
    611, 556]

MARKER = re.compile(r" \[fact \d+\]")
LINK = re.compile(r"\[([^\[\]]+)\]\(((?:https://|mailto:)[^()\s]+)\)")


class Refused(Refusal):
    """A page or a twin the printout can't print as it is."""


# ---------------------------------------------------------------------------
# The page, read into its twin
# ---------------------------------------------------------------------------

class _Reader(html.parser.HTMLParser):
    """The resume's own markup (its <div class="cv">), read into twin lines.
    It reads the subset pages/resume.py writes and refuses any other element
    by name, so a change to the page can't drop text from the printout
    unseen. A source label is left out, and so are the paragraphs about the
    page itself ("how") and its links for the web ("look")."""

    BLOCKS = {"p": None, "h2": "== ", "h3": "=== ", "li": "- "}
    INLINE = {"span", "a", "code", "em", "strong", "wbr"}
    HOLDERS = {"div", "ul"}
    LEFT_OUT = {"how", "look"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lines, self.block, self.prefix = [], None, ""
        self.skip = []          # the elements whose text the printout leaves out
        self.fig = []           # [fact id, its text so far] while a figure is read
        self.link = []          # [href, its text so far] while a link is read

    def _put(self, s):
        if self.link:
            self.link[-1][1] += s
        elif self.fig:
            self.fig[-1][1] += s
        elif self.block is not None:
            self.block.append(s)
        elif s.strip():
            raise Refused("text outside any block: %r" % s[:40])

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = set((a.get("class") or "").split())
        if self.skip:
            if tag not in ("wbr",):
                self.skip.append(tag)
            return
        if tag in self.HOLDERS:
            return
        if tag in self.BLOCKS:
            if self.block is not None:
                raise Refused("<%s> inside another block" % tag)
            if tag == "p" and cls & self.LEFT_OUT:
                self.skip.append(tag)
                return
            self.block, self.prefix = [], self.BLOCKS[tag] or ""
            if "lede" in cls:
                self.prefix = "role"
            elif "contact" in cls:
                self.prefix = "contact"
            return
        if tag not in self.INLINE:
            raise Refused("an element the printout doesn't read: <%s>" % tag)
        if tag == "span" and "src" in cls:
            self.skip.append(tag)
        elif tag == "span" and "when" in cls:
            self._put(" | ")
        elif tag == "span" and a.get("data-f"):
            if self.fig:
                raise Refused("a figure inside a figure")
            self.fig.append([a["data-f"], ""])
        elif tag == "a":
            if self.link or self.fig:
                raise Refused("a link inside a link or a figure")
            href = a.get("href") or ""
            if not re.fullmatch(r"(?:https://|mailto:)\S+", href):
                href = SITE + ("" if href == "index.html" else href)
            self.link.append([href, ""])

    def handle_endtag(self, tag):
        if self.skip:
            self.skip.pop()
            return
        if tag == "span" and self.fig:
            f, text = self.fig.pop()
            self._put(text + " [fact %s]" % f)
        elif tag == "a" and self.link:
            href, text = self.link.pop()
            self._put("[%s](%s)" % (text, href))
        elif tag in self.BLOCKS and self.block is not None:
            text = " ".join("".join(self.block).split())
            self.lines.append((self.prefix, text))
            self.block = None

    def handle_data(self, data):
        if not self.skip:
            self._put(data)


def twin(cv_html):
    """The twin of the resume's markup: NAME, then the role, the contact line
    and every block in order, and NOTE last."""
    r = _Reader()
    r.feed(cv_html)
    r.close()
    if r.block is not None or r.fig or r.link or r.skip:
        raise Refused("the page's resume ends inside an element")
    role = [text for kind, text in r.lines if kind == "role"]
    contact = [text for kind, text in r.lines if kind == "contact"]
    if len(role) != 1 or len(contact) != 1:
        raise Refused("the resume has %d role lines and %d contact lines; it needs one of each"
                      % (len(role), len(contact)))
    out = [NAME, role[0], contact[0]]
    for kind, text in r.lines:
        if kind in ("role", "contact"):
            continue
        if kind in ("== ", "=== "):
            out.append("")
        out.append(kind + text)
    out += ["", "-- " + NOTE]
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# The twin, read back into blocks
# ---------------------------------------------------------------------------

def runs(text):
    """A twin line's text without its fact ids, as [(text, href or None)]."""
    text, out, pos = MARKER.sub("", text), [], 0
    for m in LINK.finditer(text):
        if m.start() > pos:
            out.append((text[pos:m.start()], None))
        out.append((m.group(1), m.group(2)))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], None))
    return out


def blocks(twin_text):
    lines = [l for l in twin_text.split("\n") if l.strip()]
    if len(lines) < 3:
        raise Refused("a twin needs its name, its role and its contact line")
    out = [("name", runs(lines[0])), ("role", runs(lines[1])), ("contact", runs(lines[2]))]
    for l in lines[3:]:
        if l.startswith("=== "):
            name, sep, when = l[4:].partition(" | ")
            out.append(("project", runs(name), runs(when)))
        elif l.startswith("== "):
            out.append(("section", runs(l[3:])))
        elif l.startswith("-- "):
            out.append(("note", runs(l[3:])))
        elif l.startswith("- "):
            out.append(("bullet", runs(l[2:])))
        else:
            out.append(("para", runs(l)))
    return out


def links(twin_text):
    """Every link a twin's PDF carries, as its target."""
    return [m.group(2) for m in LINK.finditer(MARKER.sub("", twin_text))]


# ---------------------------------------------------------------------------
# The PDF
# ---------------------------------------------------------------------------

def width(text, font, size):
    if font == "F3":
        return 0.6 * size * len(text)
    table = HELVETICA if font == "F1" else HELVETICA_BOLD
    return sum(table[b - 32] if b >= 32 else 0 for b in text.encode("cp1252")) * size / 1000.0


def _string(text):
    """A PDF literal string: every byte outside printable ASCII, and the
    parentheses and the backslash, written as an octal escape (built from
    code points, CLAUDE.md trap 8)."""
    try:
        raw = text.encode("cp1252")
    except UnicodeEncodeError as e:
        raise Refused("%r has a character WinAnsi can't print" % text[max(0, e.start - 10):e.end + 10])
    back = chr(92)
    return "(" + "".join(chr(b) if 32 <= b < 127 and b not in (40, 41, 92) else back + "%03o" % b
                         for b in raw) + ")"


def _words(rs):
    """Runs as words, split at spaces: each word a list of (text, href)
    fragments, since a link can start or end inside one ("(the")."""
    words, cur = [], []
    for text, href in rs:
        for i, part in enumerate(text.split(" ")):
            if i and cur:
                words.append(cur)
                cur = []
            if part:
                cur.append((part, href))
    if cur:
        words.append(cur)
    return words


def _wrap(rs, font, size, avail):
    """Runs wrapped into lines of whole words."""
    lines, cur, cur_w = [], [], 0.0
    space = width(" ", font, size)
    for word in _words(rs):
        w = sum(width(t, font, size) for t, _ in word)
        if cur and cur_w + space + w > avail:
            lines.append(cur)
            cur, cur_w = [], 0.0
        cur_w += (space if cur else 0.0) + w
        cur.append(word)
    if cur:
        lines.append(cur)
    return lines


def _line_text(line):
    """A wrapped line's text, and each link's [start, end, href] within it; a
    link that runs across a space stays one link."""
    out, spans = "", []
    for word in line:
        if out:
            out += " "
        for text, href in word:
            start = len(out)
            out += text
            if href:
                if spans and spans[-1][2] == href and spans[-1][1] in (start, start - 1):
                    spans[-1][1] = len(out)
                else:
                    spans.append([start, len(out), href])
    return out, spans


class _Writer:
    def __init__(self):
        self.pages = [([], [])]       # (content operators, link annotations)
        self.y = PAGE_H - MARGIN

    def new_page(self):
        self.pages.append(([], []))
        self.y = PAGE_H - MARGIN

    def room(self, h, floor=MARGIN):
        if self.y - h < floor:
            self.new_page()

    def text(self, x, y, s, font, size):
        self.pages[-1][0].append("BT /%s %s Tf 1 0 0 1 %.2f %.2f Tm %s Tj ET" % (font, _num(size), x, y, _string(s)))

    def link(self, x0, y, x1, size, href):
        self.pages[-1][1].append((x0, y - 0.22 * size, x1, y + 0.82 * size, href))

    def lines(self, rs, font, size, leading, x=MARGIN, avail=WIDTH, floor=MARGIN):
        """Runs set as wrapped lines. -> (page, baseline) of the first line,
        which a page break before it can move to the next page."""
        first = None
        for line in _wrap(rs, font, size, avail):
            self.room(leading, floor)
            self.y -= leading
            if first is None:
                first = (len(self.pages) - 1, self.y)
            s, spans = _line_text(line)
            self.text(x, self.y, s, font, size)
            for a, b, href in spans:
                self.link(x + width(s[:a], font, size), self.y, x + width(s[:b], font, size), size, href)
        return first


def _num(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


def pdf(twin_text):
    """The PDF a twin prints as: Logan's draft's shape, in Helvetica, with the
    note at the foot of the last page in Courier."""
    w = _Writer()
    note = None
    for b in blocks(twin_text):
        kind = b[0]
        if kind == "name":
            w.lines(b[1], "F2", 20, 22)
        elif kind == "role":
            w.lines(b[1], "F2", 11, 15)
        elif kind == "contact":
            w.lines(b[1], "F1", 9.5, 13)
            w.y -= 6
        elif kind == "section":
            w.room(9 + 14 + 3 * 13)
            w.y -= 9
            w.lines(b[1], "F2", 11, 14)
            w.y -= 1
        elif kind == "project":
            w.room(6 + 14 + 2 * 13)
            w.y -= 6
            when = "".join(t for t, _ in b[2])
            name_w = WIDTH - width(when, "F1", 9.5) - 12
            w.lines(b[1], "F2", 10.5, 14, avail=name_w)
            w.text(MARGIN + WIDTH - width(when, "F1", 9.5), w.y, when, "F1", 9.5)
        elif kind == "bullet":
            page, y = w.lines(b[1], "F1", 10, 13, x=MARGIN + 12, avail=WIDTH - 12)
            # the bullet goes beside the item's first line, on whichever page
            # that line was set
            w.pages[page][0].append("BT /F1 10 Tf 1 0 0 1 %.2f %.2f Tm %s Tj ET" % (MARGIN + 2, y, _string(chr(0x2022))))
            w.y -= 2
        elif kind == "para":
            w.lines(b[1], "F1", 10, 13)
            w.y -= 5
        elif kind == "note":
            note = b[1]
    if note is not None:
        lines = _wrap(note, "F3", 7, WIDTH)
        h = 9 * len(lines) + 6
        w.room(h)
        w.y = MARGIN + h
        w.y -= 6
        w.lines(note, "F3", 7, 9, floor=0)
    return _assemble(w.pages)


def _assemble(pages):
    objs = [None, None]                                   # the catalog and the page tree, written last
    fonts = []
    for _, base in FONTS:
        objs.append("<< /Type /Font /Subtype /Type1 /BaseFont /%s /Encoding /WinAnsiEncoding >>" % base)
        fonts.append(len(objs))
    font_res = " ".join("/%s %d 0 R" % (f, n) for (f, _), n in zip(FONTS, fonts))
    kids = []
    for ops, annots in pages:
        data = "\n".join(ops)
        objs.append("<< /Length %d >>\nstream\n%s\nendstream" % (len(data), data))
        content = len(objs)
        refs = []
        for x0, y0, x1, y1, href in annots:
            objs.append("<< /Type /Annot /Subtype /Link /Rect [%s %s %s %s] /Border [0 0 0] /A << /S /URI /URI %s >> >>"
                        % (_num(x0), _num(y0), _num(x1), _num(y1), _string(href)))
            refs.append("%d 0 R" % len(objs))
        objs.append("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] /Resources << /Font << %s >> >> /Contents "
                    "%d 0 R%s >>" % (PAGE_W, PAGE_H, font_res, content,
                                     " /Annots [%s]" % " ".join(refs) if refs else ""))
        kids.append(len(objs))
    objs[0] = "<< /Type /Catalog /Pages 2 0 R >>"
    objs[1] = "<< /Type /Pages /Kids [%s] /Count %d >>" % (" ".join("%d 0 R" % k for k in kids), len(kids))
    out, offsets = "%PDF-1.4\n", []
    for i, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += "%d 0 obj\n%s\nendobj\n" % (i, body)
    xref = len(out)
    out += "xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    out += "".join("%010d 00000 n \n" % o for o in offsets)
    out += "trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    return out.encode("ascii")
