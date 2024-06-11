#!/bin/env python3
import sys

from DesktopAssistant import assistant


def main():
    sprites = {
        'sleepy_claire': ':/sprites/sleepy_claire_crop.gif',
        'sleepy_claire_drag': ':/sprites/sleepy_claire_drag_crop.gif'
    }
    app = assistant.Application(iconPath=':/icons/bnuuy.png', sprites=sprites,
                                initialSprite='sleepy_claire')
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
