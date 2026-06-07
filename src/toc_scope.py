"""Scope the table of contents.

Adds two rules on top of python-markdown's ``toc`` extension:

* Headings that appear *before* the ``[TOC]`` marker are excluded from the
  table of contents (so a cheat-sheet above the marker is skipped).
* Any heading carrying the ``toc-omit`` class (via ``attr_list``) is excluded
  individually, e.g. ``## Internal { .toc-omit }``.

Both rules work by hiding the heading from the ``toc`` collector and restoring
it afterwards, so excluded headings still render normally; they simply get no
ToC entry and no anchor id.
"""

import xml.etree.ElementTree as etree

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

from src.constants import TOC_MARKER, TOC_OMIT_CLASS

HEADER_TAGS = frozenset({"h1", "h2", "h3", "h4", "h5", "h6"})
ORIG_TAG_ATTR = "data-orig-tag"

# Run before toc (priority 5) to hide, after toc to restore.
HIDE_PRIORITY = 6
RESTORE_PRIORITY = 4


def _is_marker(el: etree.Element) -> bool:
    """Match a paragraph whose only content is the ToC marker.

    Mirrors the check used by the ``toc`` extension; ``len(el) == 0`` keeps it
    correct when ``nl2br`` introduces child ``<br>`` elements elsewhere.
    """
    return el.tag == "p" and el.text is not None and el.text.strip() == TOC_MARKER and len(el) == 0


def _has_omit_class(el: etree.Element) -> bool:
    return TOC_OMIT_CLASS in el.get("class", "").split()


class HideHeadersTreeprocessor(Treeprocessor):
    """Retag headings that must not appear in the ToC so ``toc`` skips them."""

    def run(self, doc: etree.Element) -> None:
        has_marker = any(_is_marker(el) for el in doc.iter())
        # Without a marker, do no positional hiding (only explicit opt-outs).
        before_marker = has_marker

        for el in doc.iter():
            if _is_marker(el):
                before_marker = False
                continue
            if el.tag in HEADER_TAGS and (before_marker or _has_omit_class(el)):
                el.set(ORIG_TAG_ATTR, el.tag)
                el.tag = "p"


class RestoreHeadersTreeprocessor(Treeprocessor):
    """Restore headings hidden by :class:`HideHeadersTreeprocessor`."""

    def run(self, doc: etree.Element) -> None:
        for el in doc.iter():
            orig = el.get(ORIG_TAG_ATTR)
            if orig:
                el.tag = orig
                del el.attrib[ORIG_TAG_ATTR]


class TocScopeExtension(Extension):
    def extendMarkdown(self, md) -> None:  # noqa: ANN001 - markdown API type
        md.treeprocessors.register(HideHeadersTreeprocessor(md), "toc_scope_hide", HIDE_PRIORITY)
        md.treeprocessors.register(RestoreHeadersTreeprocessor(md), "toc_scope_restore", RESTORE_PRIORITY)


def makeExtension(**kwargs) -> TocScopeExtension:
    return TocScopeExtension(**kwargs)
