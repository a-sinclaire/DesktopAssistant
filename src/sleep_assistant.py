#!/bin/env python3
import argparse
from datetime import datetime, timedelta
import sys

from PySide6 import QtCore

import assistant


class SleepApplication(assistant.Application):
    '''
    nightStart:  'HH:MM'
    nightLength: int (minutes)
    '''
    def __init__(self, nightStart, nightLengthMins):
        super().__init__(iconName='bnuuy.png',
                         spriteName='sleepy_claire_smaller.gif')

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(60000)  # update once a minute

        self.nightStart = nightStart
        self.nightLengthMins = nightLengthMins

        self.lock = self.isNight()

        if not self.isNight():
            self.hide()

    def isNight(self):
        now = datetime.now()
        t = datetime.strptime(self.nightStart, '%H:%M')
        tonightStart = now.replace(hour=t.hour, minute=t.minute)
        delta = timedelta(minutes=self.nightLengthMins)
        tonightEnd = tonightStart + delta
        fullDay = timedelta(hours=24)
        yesterdayStart = tonightStart - fullDay
        yesterdayEnd = yesterdayStart + delta
        return ((now >= tonightStart and now < tonightEnd) or
                (now >= yesterdayStart and now < yesterdayEnd))

    def hide(self):
        if self.widget.isVisible():
            self.toggleVisibility()

    def unhide(self):
        if not self.widget.isVisible():
            self.toggleVisibility()

    def update(self):
        if self.isNight():
            if self.lock:
                self.lock = False
                self.unhide()
        else:
            if not self.lock:
                self.lock = True
                self.hide()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser_args = {
        ('-s', '--nightStart'): {
            'help': 'Time sleep assistant will appear in format "HH:MM"',
            'type': str,
            'default': '22:00'
        },
        ('-t', '--nightLength'): {
            'help': 'Duration sleep assistant will stay on screen in minutes',
            'type': int,
            'default': 8 * 60
        }
    }
    for args, kwargs in parser_args.items():
        parser.add_argument(*args, **kwargs)
    args = parser.parse_args()

    app = SleepApplication(args.nightStart, args.nightLength)
    sys.exit(app.exec())
