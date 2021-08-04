from generate_html import HTML, fragment, render_html, tag
from typing import Iterator


@fragment
def simple_fragment() -> Iterator:
    yield tag.p('Hello')


def test_html_repr() -> None:
    assert repr(HTML('ok')) == "HTML('ok')"
