from generate_html import comment, fragment, render_html, tag
from typing import Iterator


@fragment
def simple_comment() -> Iterator:
    yield comment('hi')


@fragment
def comment_doesnt_escape() -> Iterator:
    with comment():
        yield tag.input()


def test_simple_comment() -> None:
    assert render_html(simple_comment()) == '<!-- hi -->'


def test_comment_doesnt_escape() -> None:
    assert render_html(comment_doesnt_escape()) == '<!-- <input> -->'
