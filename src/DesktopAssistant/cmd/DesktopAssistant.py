#!/bin/env python3
import sys

from DesktopAssistant import assistant


def main():
    app = assistant.Application(
        spritePath=':/sprites/sleepy_claire_smaller.gif',
        iconPath=':/icons/bnuuy.png'
    )
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())

