# loganw.dev

Logan W.'s projects, and the record behind every figure about them. GitHub
Pages publishes the site from this repository at
<https://loganw234.github.io/loganw.dev/>, with <https://loganw.dev> set as
its custom domain. The domain serves the site once its DNS points to GitHub
Pages. After that, the github.io address redirects there. Every push to main
deploys, once the gate passes.

**Every figure on the site is read from a source, and a gate refuses one that
isn't.** A figure comes from one of two places:

- a repository in [pins.json](pins.json), read at the commit pinned there;
- the GitHub snapshot that pins.json names;
- for the site's own history, its own ledger,
  [docs/VALIDATION.md](docs/VALIDATION.md), read from the commit being built.

What no file can back is marked *stated*, with who said it and when.
[public/facts.json](public/facts.json) lists every figure with where it was
read. If the build can't read a figure from its source, it stops and names
the figure. The `numbers` stage refuses a numeral on a page that isn't inside
a figure's mark, and any mark whose text isn't exactly its own fact's.

What that doesn't cover:

- **Digits inside names.** Digits written straight after a letter are read
  as part of a name, like cft-fp256 or binary32.com. So a figure glued to a
  word, like "x3397", would pass.
- **Numbers in words.** The numbers stage sees only the number words it lists
  ("seven", "twenty"), not "one" or "first".
- **Snapshot figures.** These are read again from the committed snapshot, not
  from GitHub today. Their label gives the snapshot's date.
- **The site's own ledger.** This repository can't pin itself, so
  docs/VALIDATION.md is read from the tree being built. MANIFEST hashes it,
  so the gate fails if it changed after the build. A figure read there shows
  that the page quotes the ledger. It doesn't show that a run went as the
  ledger says.
- **Paraphrases.** A paraphrase prints its source's own words beside it, and
  can't add a numeral those words don't have. Whether it keeps their meaning
  is for the reader to judge.
- **Images.** An image is checked only as the bytes its pin gives. What it
  shows is not read.
- **Styles.** The gates read a page's HTML and its stylesheets' text. They
  don't render the page. The numbers stage refuses exactly the declarations
  listed below, unless `site/data/css_hides.json` names the selector and
  that declaration. `build.hiding_problems` is the rule. Property names are
  read without a vendor prefix.
  - `display:none`, `visibility:hidden` or `collapse`, and
    `content-visibility:hidden`.
  - `opacity`, `fill-opacity`, `font-size`, `scale` or `zoom` at zero or
    below, or computed with `calc()`, `min()`, `max()` or `clamp()`.
  - A `font` shorthand whose size is zero or computed.
  - A `transform` with `scale()` at zero, below zero or computed, or with
    `matrix()`.
  - An `opacity()` filter at zero or below.
  - In `color`, `fill` and `text-fill-color`:
    - the word `transparent`;
    - a hex colour with zero alpha;
    - a colour function whose alpha is zero, below zero, or computed.
  - `fill:none`.
  - `clip`, `clip-path`, `mask` and `mask-image`, other than `none` or
    `auto`.
  - `text-indent` other than zero.

  How the stylesheets are read:
  - Every block is read, at any depth: rules nested in rules, and at-rules
    such as `@media`, `@supports` and `@scope`. A nested block is named by
    its own prelude, so an entry in `css_hides.json`, which names a flat
    selector, never allows one.
  - Comments, strings and `url()` are cut as CSS cuts them, line endings and
    form feeds included.
  - A custom property is read as every value the stylesheet gives it: in a
    rule, as a `var()` fallback, or as an `@property`'s initial value.

  Local-only refuses the shapes this build knows of in which a reading of
  the text and a browser's could part:
  - an ASCII control character other than a line feed or a tab;
  - a string or a comment left open;
  - a comment marker inside a string;
  - a malformed `url()`;
  - a backslash escape.

  A control reads the published stylesheet a second time with tinycss2, a
  parser that follows the CSS specifications. It fails the gate if the two
  readings differ in any block, property or hiding verdict.

  Anything else passes, including:
  - a near-zero value;
  - text coloured like its background;
  - text placed off screen, or stacked under something else.

## Does it still hold?

```bash
bash verify/run.sh --require-all
```

That runs every stage (`bash verify/run.sh --list` prints them). Only the
desktop can run it this way. It has every pinned repository cloned, private
ones included, and it has Logan's GitHub login.

On any other machine, leave out `--require-all`. A stage or a figure that
needs something the machine can't read is then skipped by name, never passed.

The site needs only Python's standard library, except in two of the gate's
controls:
- one reads each ledger a second way, with CommonMark's own parser
  (markdown-it-py);
- the other reads the published stylesheet a second way (tinycss2).

Install both, pinned by hash, with
`python -m pip install --require-hashes --no-deps -r verify/requirements.txt`.
Otherwise each control is skipped by name.

To check the published figures yourself, from a clone of this repository:

```bash
LOGANW_FETCH=1 python site/build.py --verify-facts
```

That reads every figure again: at its pin, from the committed snapshot, or
from the site's own ledger in the clone. It
fetches the public repositories it needs, and names each figure from a
private repository, which it can't read.

## Layout

| path | what it is |
|---|---|
| [pins.json](pins.json) | Every repository the site reads, the commit it reads it at, how each of its workflows counts, and which ledger lines count as a pass. |
| [site/](site/) | The generator. [facts.py](site/facts.py) reads the figures, [render.py](site/render.py) holds the page shell, [pages/](site/pages/) has one module per page, [mapgen.py](site/mapgen.py) draws the map from [data/relations.json](site/data/relations.json), and [build.py](site/build.py) builds and checks. |
| [public/](public/) | The built site, committed and deployed exactly as it stands. It includes `facts.json` and `MANIFEST`: the sha256 of every published file except `BUILD` and `MANIFEST` itself, and of pins.json and the snapshot. |
| [sources/](sources/) | GitHub snapshots, each taken once by `site/snapshot_github.py`. |
| [verify/run.sh](verify/run.sh) | The one command above. |
| [docs/SPEC.md](docs/SPEC.md) | The spec as given, the decisions made about it, and where the repositories corrected it. |
| [docs/VALIDATION.md](docs/VALIDATION.md) | The ledger. It is append-only: every run, failures included. |
| [docs/ROUND1.md](docs/ROUND1.md) | The plan for the parcel round that builds the rest of the site. |
| [design/](design/) | The design experiments, and the one that was chosen. |

## Licence

MIT ([LICENSE](LICENSE)). The fonts are under the SIL Open Font License 1.1;
see [site/fonts/](site/fonts/).
