#! /bin/env python3
import sys

import assistant


def main():
    app = assistant.Application()
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
