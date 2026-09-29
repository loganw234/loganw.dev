# Design

Work toward the site's look, kept here once it has been decided. That way the
reasons for the chosen design, and the options passed over, stay on record.

## Chosen (2026-09-29)

Logan's words: *"D looks good, but the color scheme of A (the blue), and the
font and header choice of B."* That combination is experiment E:

- **Layout: D's.** One column, a text measure of 42rem, and the map and ledger
  at full width. Every figure is followed by its source.
- **Colour: A's.** An off-white page with one blue accent. The dark theme uses
  A's dark palette.
- **Type and header: B's.** Newsreader for text and JetBrains Mono for
  numbers. The header has the site name in small mono, "Logan W." in large
  italic, an italic navigation line separated by middots, and the stamp
  between two rules. Section headings are italic with small roman numerals.

E copies the tokens and rules it took from A and B. A to D stay exactly as
they were, as the record of the options; E is the one that changes from here.

## experiments/ (2026-09-29)

One Home page in five visual directions: four options and the combination
chosen from them. It is a prototype to look at, not the site.

| page | direction | a figure's source shows as |
|---|---|---|
| `a-datasheet.html` | an engineering document, IBM Plex, one blue | numbered footnotes collected at the end |
| `b-notebook.html` | a lab notebook, Newsreader on paper, correction red | margin notes |
| `c-instrument.html` | dark-first panels, Inter and JetBrains Mono, amber | on hover, plus a source line per panel |
| `d-plain.html` | system fonts, one column, green | printed inline after every figure |
| `e-combined.html` | **chosen:** D's page, A's colour, B's type and header | printed inline after every figure |

The content is identical in all five, so the pages differ only in type, colour
and how provenance is shown. `build.py` generates every figure:

- Most figures come from a local clone, read at a pinned commit with
  `git show` and `git log`. It never reads a working tree.
- The rest come from `sources/github-2026-09-29.json`, a GitHub snapshot taken
  once by `snapshot_github.py`.
- A figure lifted from prose names its file, line and pattern. When a pattern
  stops matching, the build refuses by name.
- Anything no file can back, such as the biography, is rendered as *stated*.

```bash
python build.py            # write the pages
python build.py --check    # exit 1 if a written file differs from a fresh render
python build.py --control  # plant a stale figure and a stale source; both must be caught
```

Measured on 2026-09-29:

- `--check` passes on a fresh build.
- `--control` catches both plants: a stale ABI in page A (caught at line 122),
  and cft-fp256 re-pinned to its first commit (refused, naming cft-fp256).
- A stale ABI planted by hand in a written page made `--check` exit 1, and
  exit 0 again after a rebuild.
- At 375 px wide, no page scrolls sideways (scrollWidth equals clientWidth,
  375). A planted 600 px element was caught (scrollWidth 616), so that check
  can fail.
- After E was added, the check and both controls were re-run and pass. A to D
  hashed identical before and after the change that made E's paths break only
  at `/`. All six pages were re-measured at 375 px: scrollWidth equals
  clientWidth on every one (360 each, because of the frame's scrollbar).

### Known limits

- Only Home exists. The other eight navigation entries do nothing.
- Every page but D loads fonts from Google Fonts. The site would serve its own.
- E keeps D's inline sources, which make the ledger heavy to read. Logan
  accepted E as it is on 2026-09-29 ("E looks good as it is"), so the inline
  sources stay.
- On a phone the map opens at its left edge, on the sparse 2025 stretch. It
  needs a narrow layout of its own, and that is not built.
- The *agent-written* column counts Co-Authored-By trailers. It does not count
  lines, and it cannot see help that was never credited in a trailer.
- The spec's `shares-workers` edge type is not drawn, because no file was
  found to support any instance of it.
