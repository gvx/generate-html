from generate_html import document, render_html, tag
from typing import Iterator


@document
def simple_document() -> Iterator:
    with tag.html(lang='en'):
        yield tag.head()
        yield tag.body()


def test_simple_document() -> None:
    assert render_html(simple_document()) == '<!doctype html><html lang="en"><head></head><body></body></html>'


def test_document_repr() -> None:
    assert repr(simple_document()) == "DocumentElement([Element(children=[Element(children=[], tagname='head', attributes={}), Element(children=[], tagname='body', attributes={})], tagname='html', attributes={'lang': 'en'})])"
