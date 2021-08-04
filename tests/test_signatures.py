from inspect import Parameter, Signature, isfunction, signature
from typing import Iterator

from generate_html import HTML, component, contents, document, fragment, Component


@component
def my_component(arg1: str) -> Iterator:
    yield contents(arg1)


@fragment
def my_fragment() -> Iterator:
    yield ''


@document
def my_document(one: int, /, two: str = '2', *, three: None) -> Iterator:
    yield ''


def test_component_signature() -> None:
    assert isfunction(my_component)
    assert my_component.__name__ == 'my_component'
    assert signature(my_component) == Signature(
        [Parameter('arg1', Parameter.POSITIONAL_OR_KEYWORD, annotation=str)],
        return_annotation=Component)


def test_fragment_signature() -> None:
    assert isfunction(my_fragment)
    assert my_fragment.__name__ == 'my_fragment'
    assert signature(my_fragment) == Signature([], return_annotation=HTML)


def test_document_signature() -> None:
    assert isfunction(my_document)
    assert my_document.__name__ == 'my_document'
    assert signature(my_document) == Signature(
        [Parameter('one', Parameter.POSITIONAL_ONLY, annotation=int),
         Parameter('two', Parameter.POSITIONAL_OR_KEYWORD, default='2', annotation=str),
         Parameter('three', Parameter.KEYWORD_ONLY, annotation=None)],
        return_annotation=HTML)
