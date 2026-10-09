"""Thread: Film & photography (docs/SPEC.md, thread 2).

The thread's page carries one IBM print (docs/SPEC.md, decision 34): the law job of one IBM device, laid as film by
the print rule the pre-registration fixed. A print is image content, which no gate reads, so what the caption says
about it is read from records and held together here: the print's own record names the device and the job, the
results document's jobs table and the committed job line must name the same two, and the image must be the one that
record lays. What no check on this site reads is the picture itself (docs/ROUND2.md, P3's trap): the project's
own `python tools/first_prints.py --check` holds each print's arrays to its record's digests (its line 395),
not the committed PNG (verifier-P3).
"""
import json
import re
import struct

import facts
from facts import V, Refusal, fact
import mapgen
from render import C, L, esc, render

PAGE = {"file": "thread-film.html", "nav": "Threads", "title": "Film & photography — loganw.dev",
        "description": "CanonBracketTool through the darkroom to a quantum-grown film stock, with one print laid by "
                       "IBM hardware, and what StoryDocs took out of the middle of it: the thread's account, its part "
                       "of the map, and its door."}

QF = "Quantum-Film"
RESULTS = "docs/HARDWARE-RESULTS.md"
PREREG = "docs/PREREGISTRATION.md"
RUNS = "docs/records/2026-10-05/ibm"
RECORD = "docs/prints/ibm-kingston-pauli-4x4.json"
PRINT = "docs/prints/ibm-kingston-pauli-4x4-print.png"
COMPOSITE = "docs/prints/hardware.png"
ASSETS = [("assets/ibm-kingston-pauli-4x4-print.png", QF, PRINT)]
DEVICE = re.compile(r"ibm_[a-z]+")


def check_print(rec_text, results_text, line_text, png, png_path):
    """Hold a print's record beside the other records that name its device and its job, and the image beside the
    record. -> (device, job); a Refusal names the first thing that does not hold:
      * the record is a print of a qpu run of pauli-4x4, and names ONE job (a sheet's names many, the first of them
        the same job: captioning a sheet as the 4x4 law's would otherwise pass);
      * the record's own name carries its device (ibm-<device>-pauli-4x4), so a record whose device was changed
        under its name, with a job and a job line to match, is refused;
      * the results document's jobs table has a row for that device and job, and the row says "law";
      * the committed job line says the same backend and job, of kind qpu;
      * the image is the print the record names (<name>-print.png), and its size is the record's cells times one
        whole scale."""
    rec = json.loads(rec_text)
    rolls = rec["rolls"]
    if rec.get("format") != "quantum-film/print/v1" or rolls.get("kind") != "qpu" or rec.get("stock") != "pauli-4x4" \
            or rolls.get("stock") != "pauli-4x4":
        raise Refusal("the record %r is not a print of a qpu run of pauli-4x4" % rec.get("name"))
    device, jobs = rolls["device"], rolls["jobs"]
    if len(jobs) != 1:
        raise Refusal("the record %r names %d jobs; a print captioned as one law job's names exactly one, and a "
                      "sheet pools many" % (rec["name"], len(jobs)))
    job = jobs[0]
    if rec["name"] != "ibm-%s-pauli-4x4" % device[len("ibm_"):]:
        raise Refusal("the record %r names the device %s, which its own name does not carry" % (rec["name"], device))
    row = re.search(r"^\| %s \| (\S+) \| `%s` \|" % (re.escape(device), re.escape(job)), results_text, re.M)
    if row is None or row.group(1) != "law":
        raise Refusal("%s has no row for %s's law job %s" % (RESULTS, device, job))
    line = json.loads(line_text)
    if (line.get("backend"), line.get("job_id"), line.get("kind")) != (device, job, "qpu"):
        raise Refusal("the committed job line names backend %r, job %r, kind %r, not %s's qpu job %s"
                      % (line.get("backend"), line.get("job_id"), line.get("kind"), device, job))
    want = "docs/prints/%s-print.png" % rec["name"]
    if png_path != want:
        raise Refusal("the image is %s, and the record %r lays %s" % (png_path, rec["name"], want))
    if png[:8] != b"\x89PNG\r\n\x1a\n":
        raise Refusal("%s is not a PNG by its bytes" % png_path)
    w, h = struct.unpack(">II", png[16:24])
    cy, cx = rec["cells"]
    if w % cx or h % cy or w // cx != h // cy:
        raise Refusal("the image is %dx%d and the record's cells are %dx%d: not one whole scale" % (w, h, cx, cy))
    return device, job


def _texts():
    """What check_print reads, from the pin: the record, the results document, the device's committed law job line
    and the image."""
    p = facts.pin(QF)
    rec_text = p.show(RECORD)
    device = json.loads(rec_text)["rolls"]["device"]
    if not DEVICE.fullmatch(device):
        raise Refusal("%s names the device %r, which is not an ibm_ name" % (RECORD, device))
    return rec_text, p.show(RESULTS), p.show("%s/%s/run/law-line.json" % (RUNS, device)), p.show(PRINT, binary=True), PRINT


@fact
def print_record(record, field):
    """The device or the job a print's own record names, after check_print has held the record beside the results
    document's jobs table and the committed job line, and the image beside the record."""
    if record != RECORD:
        raise Refusal("this page reads one print's record, %s, not %s" % (RECORD, record))
    p = facts.pin(QF)
    texts = _texts()
    device, job = check_print(*texts)
    value = {"device": device, "job": job}.get(field)
    if value is None:
        raise Refusal("a print's record is read for its device or its job, not %r" % field)
    pat = r'^[ \t]*"device": "%s"' % re.escape(device) if field == "device" else r'^[ \t]*"%s"' % re.escape(job)
    m = re.search(pat, texts[0], re.M)
    line = texts[0].count("\n", 0, m.start()) + 1
    return V(value, p.src("file", "%s:%d" % (record, line),
                          "%s, which the print's record names, and so do the committed job line (%s/%s/run/"
                          "law-line.json) and the jobs table in %s, for a print of one qpu law job"
                          % (value, RUNS, device, RESULTS), record, line), raw=value, num=(field == "job"))


def print_figure():
    P = facts.prose
    p = facts.pin(QF)
    png = p.show(PRINT, binary=True)
    w, h = struct.unpack(">II", png[16:24])
    device, job = print_record(RECORD, "device"), print_record(RECORD, "job")
    rule = P(QF, "docs/VALIDATION.md",
             r"^  - (Each takes its device's qpu law run by compare's print rule: the shots with exactly five "
             r"crystals, in\s+canonical order, shuffled on the print's own stream)\.")
    cap = render([
        "Laid from the law job ", job, ", run on ", device, ". The rule, in Quantum-Film's ledger: “", rule,
        ".” The picture is ", L(p.href(PRINT), facts.exists(QF, PRINT)), ", last written by Quantum-Film's commit ",
        facts.last_commit(QF, PRINT), "; its record is ", L(p.href(RECORD), facts.exists(QF, RECORD)),
        ". The other devices' prints are beside it in ", L(p.href(COMPOSITE), facts.exists(QF, COMPOSITE)), "."])
    alt = "A print laid from the shots of %s's law job" % device.text
    return ('<figure class="print-one"><img src="%s" alt="%s" width="%d" height="%d" loading="lazy">'
            '<figcaption>%s</figcaption></figure>' % (ASSETS[0][0], esc(alt), w, h, cap))


def account():
    P = facts.prose
    paras = []
    paras.append(render([
        "The earliest work here is bare, by Logan's own account: CanonBracketTool, ",
        facts.api_description("CanonBracketTool"), ", and Microscope-Stacker, ",
        facts.api_description("Microscope-Stacker"), "."]))
    paras.append(render([
        "atlas-darkroom grew out of the same cloud atlas as the Determinism thread's PrettyCloud: ",
        P("atlas-darkroom", "README.md",
          r"^(A print engine for the \[Atlas of Mathematical Forms\]\(https://github\.com/loganw234/PrettyCloud\))"),
        ". It is ", facts.api_visibility(["atlas-darkroom"]), " for now. Extracted from it with their history "
        "carried: atlas-optical, ",
        P("atlas-optical", "README.md", r"^(The glass of the Eidograph, on its own)"),
        " (", facts.api_visibility(["atlas-optical"]), " for now); and atlas-film, ",
        P("atlas-film", "README.md", r"^(The medium of the Eidograph)"), "."]))
    paras.append(render([
        "atlas-film underlies Quantum-Film, ",
        P(QF, "README.md", r"^\*\*(Film stocks whose crystals are laid by quantum circuits)"),
        ", checked at ", facts.stage_count(QF, "verify/run.sh"), " runner stages — the prints on "
        "Map & Ledger, and the one on this page, are its output."]))
    paras.append(render([
        "At its pin, Quantum-Film's README reports: “",
        P(QF, "README.md", r"^- \*\*(The shelf's Pauli law ran on three IBM Quantum QPUs\*\* \(\d{4}-\d{2}-\d{2}\))"),
        "”. Below, one of the devices' prints, with the device, the job and the rule that laid it read from the "
        "records at the pin."]))
    figure = print_figure()
    after = render([
        "The results document's one-paragraph summary: “",
        P(QF, RESULTS,
          r"^\*\*In one paragraph\.\*\* (All three devices carry the law's two quantum signatures, well clear of the "
          r"classical twin: 4\.3% to 5\.4% of their five-crystal shots on forbidden layouts against the twin's "
          r"31\.1%, and coherences of \+0\.27 to \+0\.34 where a classical mixture gives 0\. And all three fall "
          r"short of what their own noise models predicted\.)$"),
        "” Of the grain the prints show, the README says: “",
        P(QF, "README.md",
          r"^- (What the grain cannot show, the tables in\s+\[docs/HARDWARE-RESULTS\.md\]\(docs/HARDWARE-RESULTS\.md\) "
          r"measure: 4\.3% to 5\.4%\s+of those shots sit on layouts the law forbids)\."),
        "”."])
    # Why this device: its place in the order the pre-registration fixed, and in the predictions' ranking, each as
    # its own words say it, so a reader sees the print was not picked for how it looks (the lead, 15:44:41). The
    # ranking is on the five-crystal share and the forbidden share only; "best" is not said.
    why = render([
        "This device is first in the order the pre-registration fixed: “",
        P(QF, PREREG, r"^1\. \*\*(The devices run in ESP order:\*\* ibm_kingston, then ibm_marrakesh, then\s+ibm_fez)\."),
        "”. The predictions ranked it first too: “",
        P(QF, PREREG, r"^- \*\*Between the devices\.\*\* (The predictions order the devices as their ESPs\s+do, kingston "
                      r"then marrakesh then fez, on the five-crystal share and the\s+forbidden share)\."),
        "”. The other devices' runs are rows of the jobs table in ",
        L(facts.pin(QF).href(RESULTS), facts.exists(QF, RESULTS)), "."])
    story = render([
        "StoryDocs, ", P("StoryDocs", "README.md", r"^Books and papers compiled from (Markdown manifests)",
                         display="a book-and-paper pipeline built from Markdown manifests"),
        ", was ", P("StoryDocs", "README.md", r"(taken out of atlas-darkroom)"),
        " — the book side is the pipeline the Eidograph volumes were made with; the paper side, new, is a hybrid "
        "of a research paper and that book's own idiom. It is ", facts.api_visibility(["StoryDocs"]),
        " for now, born ", facts.born("StoryDocs"), ". It has since touched many of the map's other projects, "
        "which the arrows out of it show, derived from its projects/ directories rather than typed by hand."])
    return "".join('<p>%s</p>' % x for x in paras) + figure + "".join('<p>%s</p>' % x for x in (after, why, story))


def door():
    return facts.stated("bring a process — a development recipe, a claimed printing method, or a historical "
                        "process's parameters — and see it reproduced to the same bits, or shown where it "
                        "doesn't.", "Logan", "2026-09-29")


def render_page(ctx):
    door_html = render(door())
    if "Propose" in ctx["built"]:
        door_body = '<p class="cta">%s <a href="%s">Propose a thread</a>.</p>' % (door_html, ctx["built"]["Propose"])
    else:
        door_body = '<p class="cta">%s The Propose page isn’t built yet, so this isn’t a link.</p>' % door_html
    return ('<div class="measure"><p class="lede">Bare beginnings, a shared darkroom, and a pipeline that outgrew '
           'the room it was built in.</p></div>'
           '<h2><small>I</small>The account</h2>%s'
           '<h2><small>II</small>This thread’s part of the map</h2>%s'
           '<h2><small>III</small>Its door</h2>%s'
           % (account(), mapgen.lane_slice(1), door_body))


def controls():
    """The print's caption is held to records, so each way to caption it wrongly must be refused, by name."""
    p = facts.pin(QF)
    good = _texts()
    rec_text, results, line_text, png, png_path = good
    sheet = p.show("docs/prints/ibm-kingston-sheet.json")
    fez_png = p.show("docs/prints/ibm-fez-pauli-4x4-print.png", binary=True)
    fez_line = p.show("%s/ibm_fez/run/law-line.json" % RUNS)
    job = json.loads(rec_text)["rolls"]["jobs"][0]
    out = []

    def planted(name, what, want, **kw):
        args = dict(zip(("rec_text", "results_text", "line_text", "png", "png_path"), good))
        args.update(kw)
        try:
            check_print(**args)
            out.append((name, False, "%s: passed" % what))
        except Refusal as e:
            out.append((name, want in str(e), "%s: %s" % (what, e)))

    planted("print-caption", "a sheet's record offered as the law print's", "a sheet pools many", rec_text=sheet)
    planted("print-caption", "a job the jobs table does not give this device as its law job", "has no row for",
            results_text=results.replace("`%s`" % job, "`db1xxxxxxxxxxxxxxxxx`", 1))
    planted("print-caption", "a committed job line of another device", "the committed job line names",
            line_text=fez_line)
    planted("print-caption", "another device's picture under this record's path", "not one whole scale",
            png=fez_png)
    planted("print-caption", "another device's picture and path", "the record 'ibm-kingston-pauli-4x4' lays",
            png=fez_png, png_path="docs/prints/ibm-fez-pauli-4x4-print.png")
    # The one the table, the job line, the path and the size cannot see: this record's device and job changed to
    # another device's own, with that device's job line, under this record's name. Only its name still says kingston.
    fez = json.loads(p.show("docs/prints/ibm-fez-pauli-4x4.json"))["rolls"]
    moved = json.loads(rec_text)
    moved["rolls"]["device"], moved["rolls"]["jobs"] = fez["device"], fez["jobs"]
    planted("print-caption", "this record's device and job changed to ibm_fez's own, with its job line",
            "which its own name does not carry", rec_text=json.dumps(moved), line_text=fez_line)
    return out
