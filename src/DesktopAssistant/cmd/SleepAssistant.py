#!/bin/env python3
import argparse
from datetime import datetime, timedelta
import sys

from PySide6 import QtCore, QtGui

from DesktopAssistant import assistant


class SleepWidget(assistant.Widget):
    CLAIRE_DRAG_NECK_X = 32
    CLAIRE_DRAG_NECK_Y = 45

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        super().mousePressEvent(event)

        self.setSprite('sleepy_claire_drag')
        self.mouseMoveEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        super().mouseMoveEvent(event)

        self.move(event.globalX() - self.CLAIRE_DRAG_NECK_X,
                  event.globalY() - self.CLAIRE_DRAG_NECK_Y)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        super().mouseReleaseEvent(event)

        CLAIRE_DROP_DISPLACEMENT = 7
        self.setSprite('sleepy_claire')
        self.move(self.x(), self.y() + CLAIRE_DROP_DISPLACEMENT)


class SleepApplication(assistant.Application):
    def __init__(self, nightStart: str, nightLengthMins: int):
        '''
        :param nightStart:  when night is assumed to start
        :param nightLength: how long the night is assumed to be
        :param widgetArgs: other positional args to be passed to the widget
        :param widgetKwrgs: other keyword args to be passed to the widget
        '''
        sprites = {
            'sleepy_claire': ':/sprites/sleepy_claire_crop.gif',
            'sleepy_claire_drag': ':/sprites/sleepy_claire_drag_crop.gif'
        }
        sprites = [assistant.Sprite(k, v) for k, v in sprites.items()]
        super().__init__(iconPath=':/icons/bnuuy.png',
                         sprites=sprites,
                         widgetClass=SleepWidget,
                         initialSprite='sleepy_claire')

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


def main():
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
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())

