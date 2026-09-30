"""One module per page. build.py finds them by glob; nothing lists them.

A page module defines:

  PAGE = {"file", "nav", "title", "description"} and, in a section of more
      than one page, "index": True on the one page the navigation links to.
      "file" is a flat, lower-case .html name; every page is published beside
      index.html, so one set of relative links works on both hosts.
  render_page(ctx) -> the page's body HTML. ctx["built"] maps each navigation
      label to the file it links to; ctx["pages"] maps each label to every
      file in its section. Every figure goes through render.render() or
      render.fig(), and so carries its fact's id: the numbers stage refuses a
      numeral anywhere else on the page.
  ASSETS (optional): [(published path, repository, path at its pin)], copied
      byte for byte from the pin. An asset is an image: a lower-case .png,
      .jpg or .webp under assets/, that is what its name says by its bytes.
  extra_files(ctx) (optional) -> {flat .txt name: text}: a dossier's
      plain-text twin, for instance. Its figures go through render.plain(),
      which writes each as `text [fact N]`, and the numbers stage holds a
      text file to the same rule as a page.

A name with a numeral in it that is not a figure, such as "Mercenaries 2", is
allowed only through site/data/numeral_names.json, which is the lead's, and
only if some fact's text holds it. A page module that defines NUMERAL_NAMES
is refused.

A stylesheet under site/styles/ may not hide what it styles in any of the
ways the README's "Styles" list gives (build.hiding_problems is the rule),
since that could hide a figure or its source while every page check passes. A layout
that must hide one view for another names each selector, the declaration it
may use (display:none, say), and why, in site/data/css_hides.json, which is
the lead's.

The module also defines:
  controls() (optional) -> [(name, caught, how)]: the page's own negative
      controls, run by `build.py --control`. Each plants a fault the page's
      own checks must catch; caught is True only when the check said no. A
      control that needs every pinned clone raises facts.Unavailable on a
      machine without them, and is skipped by name.
"""
import importlib
import pathlib


def discover():
    """Every page module, in file-name order."""
    here = pathlib.Path(__file__).resolve().parent
    return [importlib.import_module("pages." + f.stem)
            for f in sorted(here.glob("*.py")) if not f.stem.startswith("_")]
