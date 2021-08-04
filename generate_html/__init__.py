__version__ = '1.0.0'

from .html import HTML, escape, into_html, render_html
from .components import Component
from .interface import comment, component, contents, document, fragment, tag, create_element

__all__ = ['HTML', 'escape', 'into_html', 'render_html', 'Component', 'comment', 'component', 'contents', 'document',
           'fragment', 'tag', 'create_element']
