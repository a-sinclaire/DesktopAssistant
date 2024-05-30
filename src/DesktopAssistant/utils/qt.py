from shutil import which
import subprocess


def qrcForFile(path: str, alias: str | None = None) -> str:
    PRE_TEXT = '<RCC><qresource prefix="/">'
    POST_TEXT= '</qresource></RCC>\n'
    if alias:
        return f'{PRE_TEXT}<file alias="{alias}">{path}</file>{POST_TEXT}'
    else:
        return f'{PRE_TEXT}<file>{path}</file>{POST_TEXT}'


def rcc(path: str, alias: str | None = None) -> bytes:
    pyside6rcc = which('pyside6-rcc')
    if pyside6rcc is None:
        raise RuntimeError('Could not find pyside6-rcc')
    rcc = subprocess.Popen([pyside6rcc, '--binary', '-'],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    qrc = qrcForFile(path, alias).encode('utf-8')

    stdout, stderr = rcc.communicate(qrc)
    if rcc.poll() != 0:
        raise RuntimeError(f'Error generating resource at path {path} with '
                           f'alias {alias}: {stderr}')

    return stdout
