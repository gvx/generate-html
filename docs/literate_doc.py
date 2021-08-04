from pathlib import Path
import sys
import io
from contextlib import contextmanager
from typing import Iterator

BASE_PATH = Path(__file__).parent

sys.path.append(str(BASE_PATH.parent))


@contextmanager
def capture_stdout():
    original = sys.stdout
    try:
        sys.stdout = value = io.StringIO()
        yield value
    finally:
        sys.stdout = original


def process_rst(rst: str) -> Iterator[str]:
    state = 'main'
    codeblock = []
    context = {}
    for line in rst.splitlines():
        if line == '    [INSERT OUTPUT]':
            yield '    ' + last_output.replace('\n', '\n    ').rstrip()
            continue
        if line.startswith('    '):
            state = 'code'
            codeblock.append(line[4:])
        elif line and state == 'code':
            with capture_stdout() as output:
                exec('\n'.join(codeblock), context, context)
            last_output = output.getvalue()
            codeblock = []
            state = 'main'
        yield line


def main(filename):
    file = BASE_PATH / filename
    file.with_suffix('.rst').write_text('\n'.join(process_rst(file.read_text())) + '\n')


if __name__ == '__main__':
    main('tutorial.rst-src')