import pytest
from typing import Iterator

from generate_html import HTML, fragment, render_html, tag


@fragment
def simple_fragment() -> Iterator:
    yield tag.p('Hello')


@fragment
def empty_fragment() -> Iterator:
    if False:
        yield


@fragment
def nested_fragment() -> Iterator:
    with tag.p('pre'):
        yield tag.em('infix')
        yield 'post'


@fragment
def instrumented_fragment(tagname: str) -> Iterator:
    yield tag[tagname]('OK')


@fragment
def clashing_ids() -> Iterator:
    with tag.p(class_='aclass'):
        yield tag.def_()
        yield tag.fake_tag()


@fragment
def void_elems() -> Iterator:
    yield tag.input(type='submit')
    yield tag.link(rel='stylesheet', href='/static/style.css')
    yield tag.br()
    yield tag.hr()


@fragment
def escaping_strings_and_numbers() -> Iterator:
    yield tag.p('<3', data_id=42)
    yield tag.textarea('<3')


@fragment
def nonescaping() -> Iterator:
    yield HTML('<x>')
    yield tag.script('1 < 2')
    with tag.style('p > a '):
        yield '{ '
        yield HTML('}')


@fragment
def use_fragment_in_fragment() -> Iterator:
    yield simple_fragment()


@fragment
def use_fragment_as_contextmanger() -> Iterator:
    with simple_fragment():  # type: ignore
        yield 'unreachable'


@fragment
def attributes() -> Iterator:
    yield tag.p(class_=['large', 'blue'], disabled=False)


@fragment
def void_children_1() -> Iterator:
    yield tag.br('no')


@fragment
def void_children_2() -> Iterator:
    with tag.br():
        yield 'no'


def test_simple1() -> None:
    assert render_html(simple_fragment()) == '<p>Hello</p>'


def test_empty() -> None:
    assert render_html(empty_fragment()) == ''


def test_nested() -> None:
    assert render_html(nested_fragment()) == '<p>pre<em>infix</em>post</p>'


def test_instrumented() -> None:
    assert render_html(instrumented_fragment('p')) == '<p>OK</p>'
    assert render_html(instrumented_fragment('span')) == '<span>OK</span>'
    assert render_html(instrumented_fragment('title')) == '<title>OK</title>'


def test_id_clashes() -> None:
    assert render_html(clashing_ids()) == '<p class="aclass"><def></def><fake-tag></fake-tag></p>'


def test_void_elems() -> None:
    assert render_html(void_elems()) == '<input type="submit"><link rel="stylesheet" href="/static/style.css"><br><hr>'


def test_escaping() -> None:
    assert render_html(escaping_strings_and_numbers()) == '<p data-id="42">&lt;3</p><textarea>&lt;3</textarea>'


def test_nonescaping() -> None:
    assert render_html(nonescaping()) == '<x><script>1 < 2</script><style>p > a { }</style>'


def test_fragment_in_fragment() -> None:
    assert render_html(use_fragment_in_fragment()) == '<p>Hello</p>'


def test_contextmanager() -> None:
    with pytest.raises(TypeError):
        render_html(use_fragment_as_contextmanger())


def test_attributes() -> None:
    assert render_html(attributes()) == '<p class="large blue"></p>'


def test_void_children() -> None:
    with pytest.raises(TypeError):
        render_html(void_children_1())
    with pytest.raises(TypeError):
        render_html(void_children_2())
