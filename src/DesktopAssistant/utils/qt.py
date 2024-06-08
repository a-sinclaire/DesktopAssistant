from shutil import which
import subprocess


def qrcForFile(path: str, alias: str | None = None) -> str:
    classText = f' alias="{alias}"' if alias else ''
    return ('<RCC><qresource prefix="/">'
            f'<file{classText}>{path}</file>'
            '</qresource></RCC>\n')


def rcc(path: str, alias: str | None = None) -> bytes:
    pyside6rcc = which('pyside6-rcc')
    if pyside6rcc is None:
        raise RuntimeError('Could not find pyside6-rcc')

    with subprocess.Popen(
            [pyside6rcc, '--binary', '-'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            ) as rccProc:
        qrc = qrcForFile(path, alias).encode('utf-8')
        stdout, stderr = rccProc.communicate(qrc)
        if rccProc.poll() != 0:
            raise RuntimeError(f'Error generating resource at path {path} '
                               f'with alias {alias}: {stderr}')

    return stdout
