from dataclasses import dataclass
from types import TracebackType
from typing import (Any, Callable, ContextManager, Dict, Iterable, Iterator,
                    List, Optional, Type)

from .components import Component
from .context import get_stack
from .html import (HTML, RAW_TEXT_ELEMENTS, VOID_ELEMENTS, convert_identifier,
                   escape, into_html, render_html)


@dataclass
class Node(HTML, ContextManager):
    children: List[HTML]

    def add(self, item: Any) -> None:
        if isinstance(item, ElementCollection):
            self.children.extend(item.children)
        elif isinstance(item, Component):
            raise TypeError('trying to use a component as a fragment, use it as a context manager or iterable instead')
        else:
            self.children.append(into_html(item))

    def generate_html(self) -> Iterator[str]:
        for item in self.children:
            if isinstance(item, Node):
                yield from item.generate_html()
            else:
                yield item.__html__()

    def __html__(self) -> str:
        return ''.join(self.generate_html())

    def __enter__(self) -> None:
        get_stack().push(self)

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        stack = get_stack()
        stack.pop(self)
        stack.add(self)


class ElementCollection(Node):
    def __enter__(self) -> None:
        raise TypeError('trying to use a fragment as a component, yield it instead')


class CommentNode(Node):
    def generate_html(self) -> Iterator[str]:
        yield '<!-- '
        yield from super().generate_html()
        yield ' -->'


@dataclass
class Element(Node):
    tagname: str
    attributes: Dict[str, Any]

    def __post_init__(self) -> None:
        if self.children and self.tagname in VOID_ELEMENTS:
            raise TypeError(f'<{self.tagname}> cannot have children')

    def has_closing_tag(self) -> bool:
        return self.tagname not in VOID_ELEMENTS

    def generate_attribute(self, key: str, value: Any) -> Iterator[str]:
        if value is False:
            return
        yield ' '
        yield convert_identifier(key)
        if value is True:
            return
        yield '="'
        yield escape(value)
        yield '"'

    def generate_html(self) -> Iterator[str]:
        yield '<'
        yield self.tagname
        for key, value in self.attributes.items():
            if isinstance(value, list):
                value = ' '.join(str(item) for item in value)
            yield from self.generate_attribute(key, value)
        yield '>'
        if self.tagname not in VOID_ELEMENTS:
            yield from super().generate_html()
        if self.has_closing_tag():
            yield '</'
            yield self.tagname
            yield '>'

    def add(self, item: Any) -> None:
        if self.tagname in VOID_ELEMENTS:
            raise TypeError(f'<{self.tagname}> cannot have children')
        if self.tagname in RAW_TEXT_ELEMENTS:
            if not isinstance(item, HTML):
                item = HTML(item)
        super().add(item)


class DocumentElement(Element):
    def __init__(self, children: List[HTML]) -> None:
        super().__init__(children, '!doctype', dict(html=True))

    def has_closing_tag(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f'DocumentElement({self.children})'
