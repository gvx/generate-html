from __future__ import annotations

from html import escape as html_escape
from typing import Any

VOID_ELEMENTS = frozenset({'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'menuitem', 'meta', 'param', 'source', 'track', 'wbr'})
RAW_TEXT_ELEMENTS = frozenset({'script', 'style'})
ESCAPABLE_RAW_TEXT_ELEMENTS = frozenset({'textarea', 'title'})


class HTML:
    '''Represents some HTML fragment or document.

    This can be either a simple value like ``HTML('<img>')``
    or it can be a subclass. Subclasses might calculate the
    actual HTML lazily.

    Use :func:`render_html` to get the HTML as a string.
    '''
    def __init__(self, value: Any) -> None:
        self.value = str(value)

    def __repr__(self) -> str:
        return f'HTML({self.value!r})'

    def __html__(self) -> str:
        return self.value


def escape(thing: Any) -> str:
    '''Convert to string and escape special characters.

    This function is called automatically where relevant, you usually
    do not need to call this yourself.'''
    return html_escape(str(thing))


def render_html(thing: Any) -> str:
    '''Render something as an HTML string, escaping special characters if necessary

    ::

        render_html(HTML('<img>')) == '<img>'
        render_html(42) == '42'
        render_html('<img>') == '&lt;img&gt;'
    '''
    return into_html(thing).__html__()


def into_html(thing: Any) -> HTML:
    """Convert an object to HTML, escaping special characters if necessary

    ::

        into_html(HTML('<img>')) == HTML('<img>')
        into_html(42) == HTML('42')
        into_html('<img>') == HTML('&lt;img&gt;')
    """
    if isinstance(thing, HTML):
        return thing
    return HTML(escape(thing))


def convert_identifier(key: str) -> str:
    return key.rstrip('_').replace('_', '-')
