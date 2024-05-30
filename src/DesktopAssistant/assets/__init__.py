from pathlib import Path

from PySide6 import QtCore

from DesktopAssistant.utils.filetype import fileType
from DesktopAssistant.utils.qt import rcc


ASSETS_DIR = Path(__file__).parent


def __findFiles(path, files=[]):
    for subpath, subdirs, subfiles in path.walk():
        for f in subfiles:
            fPath = subpath / f
            with open(fPath, 'rb') as fp:
                mimeType = fileType(fp)
            if mimeType.startswith('image/') or mimeType.startswith('video/'):
                files.append(fPath.relative_to(ASSETS_DIR))

        if subdirs and subpath != path:
            for d in subdirs:
                files += __find_files(path / d, files)

    return files


for file in __findFiles(ASSETS_DIR):
    resourceData = rcc(str(ASSETS_DIR / file), str(file))
    rccFilePath = str(ASSETS_DIR / file) + '.rcc'
    with open(rccFilePath, 'wb') as fp:
        fp.write(resourceData)
    QtCore.QResource.registerResource(rccFilePath)
