# loganw.dev

Logan W.'s projects, and the record behind every figure about them. The site
is served at <https://loganw.dev> and <https://loganw234.github.io/loganw.dev/>.

**Nothing on the site is typed.** Every figure comes from one of two places:

- a repository in [pins.json](pins.json), read at the commit pinned there;
- the GitHub snapshot that pins.json names.

What no file can back is marked *stated*. [public/facts.json](public/facts.json)
lists every figure with where it was read. A figure the build can't read from
its source stops the build, naming the figure.

## Does it still hold?

```bash
bash verify/run.sh --require-all
```

That runs all 7 stages and takes about 15 seconds on the desktop, which has
every pinned repository cloned, private ones included. On any other machine,
leave out `--require-all`: a stage that needs a private repository is skipped
by name, never passed.

To check the published figures yourself, from a clone of this repository:

```bash
LOGANW_FETCH=1 python site/build.py --verify-facts
```

That reads every figure again at its pin. It fetches the public repositories
it needs, and names each private one it can't read.

## Layout

| path | what it is |
|---|---|
| [pins.json](pins.json) | Every repository the site reads, and the commit it reads it at. |
| [site/](site/) | The generator. [facts.py](site/facts.py) reads the figures, [render.py](site/render.py) holds the page shell, [pages/](site/pages/) has one module per page, [mapgen.py](site/mapgen.py) draws the map from [data/relations.json](site/data/relations.json), and [build.py](site/build.py) builds and checks. |
| [public/](public/) | The built site, committed and deployed exactly as it stands, including `MANIFEST` (a hash of every file) and `facts.json`. |
| [sources/](sources/) | GitHub snapshots, each taken once by `site/snapshot_github.py`. |
| [verify/run.sh](verify/run.sh) | The one command above. |
| [docs/SPEC.md](docs/SPEC.md) | The spec as given, the decisions made about it, and where the repositories corrected it. |
| [docs/VALIDATION.md](docs/VALIDATION.md) | The ledger. It is append-only: every run, failures included. |
| [docs/ROUND1.md](docs/ROUND1.md) | The plan for the parcel round that builds the rest of the site. |
| [design/](design/) | The design experiments, and the one that was chosen. |

## Licence

MIT ([LICENSE](LICENSE)). The fonts are under the SIL Open Font License 1.1;
see [site/fonts/](site/fonts/).
