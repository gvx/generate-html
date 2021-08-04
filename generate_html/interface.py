from functools import partial, update_wrapper
from typing import Any, Callable, Dict, Iterable, Iterator, Type, TypeVar

from .components import Component, ComponentContents
from .context import get_stack
from .html import HTML, RAW_TEXT_ELEMENTS, convert_identifier, into_html
from .nodes import (CommentNode, DocumentElement, Element, ElementCollection,
                    Node)

__all__ = ['tag', 'comment', 'contents', 'document', 'fragment', 'component']


def create_element(tagname: str, children: Iterable, attributes: Dict[str, Any]) -> Element:
    '''Create a new HTML element.

    The following are equivalent::

        create_element('a', ['text'], {'href': '/'})
        tag('a', 'text', href='/')
        tag['a']('text', href='/')
        tag.a('text', href='/')

    When Python identifiers are used to represent tag names or
    attribute names, trailing underscores are removed and any remaining
    underscores are converted to dashes. This means that the following
    are equivalent as well::

        tag.import_(class_='test', data_accept='y')
        create_element('import', [], {'class': 'test', 'data-accept': 'y'})
    '''
    if tagname in RAW_TEXT_ELEMENTS:
        children_fix = [child if isinstance(child, HTML) else HTML(child) for child in children]
    else:
        children_fix = [into_html(child) for child in children]
    return Element(children_fix, tagname, attributes)


class TagHelper:
    'See :func:`create_element`'
    def __call__(self, tagname: str, /, *children: Any, **attributes: Any) -> Element:
        return create_element(tagname, children, attributes)

    def __getattr__(self, key: str) -> Callable[..., Element]:
        return partial(self, convert_identifier(key))
    __getitem__ = __getattr__


tag = TagHelper()


def comment(*args: Any) -> CommentNode:
    '''Create an HTML comment'''
    return CommentNode([into_html(piece) for piece in args])


def contents(*args: Any) -> ComponentContents:
    '''Create a marker to insert component contents, giving back control to the component user.'''
    if len(args) == 1:
        return ComponentContents(args[0])
    return ComponentContents(args)


def _construct_node(f: Callable[..., Iterator], top_level: Type[Node], /, *args: Any, **kwargs: Any) -> HTML:
    stack = get_stack()
    with stack.yield_element(top_level([])) as top_el:
        for thing in f(*args, **kwargs):
            stack.add(thing)
    return top_el


T = TypeVar('T', HTML, Component)


def _signature_fix(decorated: Callable, original: Callable[..., Iterator],
                   return_annotation: Type[T]) -> Callable[..., T]:
    update_wrapper(decorated, original)
    decorated.__annotations__['return'] = return_annotation
    return decorated


def document(f: Callable[..., Iterator]) -> Callable[..., HTML]:
    """Decorator for full HTML documents.

    Converts a function that returns an interator. :func:`generate_html.into_html` is used """
    return _signature_fix(lambda *args, **kwargs: _construct_node(f, DocumentElement, *args, **kwargs), f, HTML)


def fragment(f: Callable[..., Iterator]) -> Callable[..., HTML]:
    """Decorator for HTML fragments"""
    return _signature_fix(lambda *args, **kwargs: _construct_node(f, ElementCollection, *args, **kwargs), f, HTML)


def component(f: Callable[..., Iterator]) -> Callable[..., Component]:
    """Decorator for components"""
    return _signature_fix(lambda *args, **kwargs: Component(f, *args, **kwargs), f, Component)
