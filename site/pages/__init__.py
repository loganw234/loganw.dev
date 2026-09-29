"""One module per page. build.py finds them by glob; nothing lists them.

A page module defines:

  PAGE = {"file", "nav", "title", "description"} and, in a section of more
      than one page, "index": True on the one page the navigation links to.
      "file" is a flat, lower-case .html name; every page is published beside
      index.html, so one set of relative links works on both hosts.
  render_page(ctx) -> the page's body HTML. ctx["built"] maps each navigation
      label to the file it links to; ctx["pages"] maps each label to every
      file in its section.
  ASSETS (optional): [(published path, repository, path at its pin)], copied
      byte for byte from the pin.
  extra_files(ctx) (optional) -> {flat .txt name: text}: a dossier's
      plain-text twin, for instance.
  controls() (optional) -> [(name, caught, how)]: the page's own negative
      controls, run by `build.py --control`. Each plants a fault the page's
      own checks must catch; caught is True only when the check said no.

"""
