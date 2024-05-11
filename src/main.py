#!/bin/env python3
import sys

import assistant


def main():
    app = assistant.Application(spriteName='sleepy_claire_smaller.gif',
                                iconName='bnuuy.png')
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
