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
      byte for byte from the pin.
  extra_files(ctx) (optional) -> {flat .txt name: text}: a dossier's
      plain-text twin, for instance. Its figures go through render.plain(),
      which writes each as `text [fact N]`, and the numbers stage holds a
      text file to the same rule as a page.
  NUMERAL_NAMES (optional): names that have a numeral in them and are not
      figures, such as "Mercenaries 2". The numbers stage allows exactly these
      phrases, and prints how many it allowed.
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
