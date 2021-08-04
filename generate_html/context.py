from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterator, List

if TYPE_CHECKING:
    from .nodes import Node


@dataclass
class NodeStack:
    stack: List[Node]

    def push(self, item: Node) -> None:
        self.stack.append(item)

    def pop(self, item: Node) -> None:
        top = self.stack.pop()
        assert top is item

    def add(self, item: Node) -> None:
        self.stack[-1].add(item)

    @contextmanager
    def yield_element(self, item: Node) -> Iterator[Node]:
        self.push(item)
        try:
            yield item
        finally:
            self.pop(item)


current_node_stack: ContextVar[NodeStack] = ContextVar('current_node_stack')


def get_stack() -> NodeStack:
    try:
        return current_node_stack.get()
    except LookupError:
        stack = NodeStack([])
        current_node_stack.set(stack)
        return stack
