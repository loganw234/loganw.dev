"""Shared helper for P5's two pages (Method, About). A leading underscore
keeps this out of pages.discover(), as _dossier.py's does for P3.
"""
from render import L


def page_link(ctx, section, file, text):
    """A link to file, if it is one of the pages this build produced for
    section (ctx["pages"][section], from render_all()); otherwise text,
    unlinked, with a note that it isn't built yet. The links check refuses a
    link to a file that isn't published, so a page never links one it can't
    see in ctx."""
    if file in ctx.get("pages", {}).get(section, []):
        return L(file, text)
    return text + ", not yet built"
