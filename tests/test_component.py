import pytest
from typing import Iterator, Iterable

from generate_html import component, contents, fragment, render_html, tag
from generate_html.components import InvalidHTML


@component
def double_component() -> Iterator:
    yield contents(1)
    yield '@'
    yield contents(2)


@fragment
def use_double_component() -> Iterator:
    for i in double_component():
        yield i
        yield ','


@fragment
def use_double_component_wrong() -> Iterator:
    with double_component() as i:
        yield i
        yield ','


@component
def simple_ul(iterable: Iterable) -> Iterator:
    with tag.ul():
        for item in iterable:
            with tag.li():
                yield contents(item + 1)


@fragment
def use_simple_ul() -> Iterator:
    for item in simple_ul(range(3)):
        yield tag.strong(item)


@component
def contextmanager_component() -> Iterator:
    with tag.super():
        yield '['
        yield contents()
        yield ']'


@fragment
def use_contextmanager_component() -> Iterator:
    with contextmanager_component():
        yield 3


@component
def invalid_component() -> Iterator:
    yield tag.p()


@fragment
def use_invalid_component() -> Iterator:
    with invalid_component():
        yield 'OK'


@fragment
def pass_through_errors() -> Iterator:
    with contextmanager_component():
        raise FileNotFoundError


@fragment
def use_component_wrong() -> Iterator:
    yield contextmanager_component()


def test_double() -> None:
    assert render_html(use_double_component()) == '1,@2,'


def test_double_2() -> None:
    with pytest.raises(InvalidHTML):
        render_html(use_double_component_wrong())


def test_simple_ul() -> None:
    assert (render_html(use_simple_ul()) ==
            '<ul><li><strong>1</strong></li><li><strong>2</strong></li><li><strong>3</strong></li></ul>')


def test_contextmanager() -> None:
    assert render_html(use_contextmanager_component()) == '<super>[3]</super>'


def test_contextmanager_2() -> None:
    with pytest.raises(TypeError):
        render_html(use_component_wrong())


def test_invalid() -> None:
    with pytest.raises(InvalidHTML):
        render_html(use_invalid_component())


def test_pass_through_errors() -> None:
    with pytest.raises(FileNotFoundError):
        render_html(pass_through_errors())
