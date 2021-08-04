from dataclasses import dataclass
from functools import partial
from types import TracebackType
from typing import (Any, Callable, ContextManager, Iterable, Iterator,
                    Optional, Type)

from .context import get_stack


@dataclass
class ComponentContents:
    args: Any


class InvalidHTML(Exception):
    pass


class Component(ContextManager, Iterable):
    def __init__(self, f: Callable[..., Iterator], /, *args: Any, **kwargs: Any):
        self.it = f(*args, **kwargs)

    def __iter__(self) -> Iterator:
        stack = get_stack()
        for item in self.it:
            if isinstance(item, ComponentContents):
                yield item.args
            else:
                stack.add(item)

    def __enter__(self) -> None:
        stack = get_stack()
        for item in self.it:
            if isinstance(item, ComponentContents):
                return item.args
            stack.add(item)
        raise InvalidHTML('component does not contain an instance of contents()')

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException], traceback: Optional[TracebackType]) -> None:
        stack = get_stack()
        if exc_type is not None:
            return
        for item in self.it:
            if isinstance(item, ComponentContents):
                raise InvalidHTML('component invoked as as a context manager, but has multiple instances of contents()')
            stack.add(item)
