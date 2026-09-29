"""One module per page. build.py finds them by glob; nothing lists them.

A page module defines PAGE = {"file", "nav", "title", "description"}, a
render_page(ctx) that returns the page's body HTML, and optionally ASSETS, a
list of (published path, repository, path at its pin) for files copied byte
for byte. ctx["built"] maps each built page's navigation label to its file.
"""
