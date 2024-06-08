#!/bin/env python3
import argparse
from datetime import datetime, timedelta
import sys

from PySide6.QtCore import QTimer
from PySide6.QtGui import QMouseEvent

from DesktopAssistant import assistant


class SleepWidget(assistant.Widget):
    CLAIRE_DRAG_NECK_X = 32
    CLAIRE_DRAG_NECK_Y = 45
    CLAIRE_DROP_DISPLACEMENT = 7

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)

        self.setSprite('sleepy_claire_drag')
        self.mouseMoveEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)

        self.move(event.globalX() - self.CLAIRE_DRAG_NECK_X,
                  event.globalY() - self.CLAIRE_DRAG_NECK_Y)

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)

        self.setSprite('sleepy_claire')
        self.move(self.x(), self.y() + self.CLAIRE_DROP_DISPLACEMENT)


class SleepApplication(assistant.Application):
    def __init__(self, nightStart: str, nightLengthMins: int):
        '''
        :param nightStart: when night is assumed to start (HH:MM, 24hr format)
        :param nightLength: how long the night is assumed to be
        :param widgetArgs: other positional args to be passed to the widget
        :param widgetKwrgs: other keyword args to be passed to the widget
        '''
        sprites = {
            'sleepy_claire': ':/sprites/sleepy_claire_crop.gif',
            'sleepy_claire_drag': ':/sprites/sleepy_claire_drag_crop.gif'
        }
        super().__init__(iconPath=':/icons/bnuuy.png',
                         sprites=sprites,
                         widgetClass=SleepWidget,
                         initialSprite='sleepy_claire')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(60000)  # update once a minute

        if nightLengthMins < 0:
            raise ValueError('night length cannot be negative')
        if nightLengthMins > 1440:
            raise ValueError('night length cannot exceed 1 day (1440 mins)')
        self.nightLength = timedelta(minutes=nightLengthMins)
        self.nightStart = datetime.strptime(nightStart, '%H:%M')
        self.nightEnd = self.nightStart + self.nightLength
        # reset the day value in case adding self.nightLength causes the time
        # to pass midnight, incrementing the day value
        self.nightEnd = self.nightEnd.replace(day=self.nightStart.day)

        self.lock = self.isNight()
        if not self.isNight():
            self.hide()

    def isNight(self) -> bool:
        now = datetime.now()
        tonightStart = now.replace(hour=self.nightStart.hour,
                                   minute=self.nightStart.minute)
        tonightEnd = now.replace(hour=self.nightEnd.hour,
                                 minute=self.nightEnd.minute)
        if self.nightStart < self.nightEnd:
            return tonightStart <= now < tonightEnd
        if self.nightStart > self.nightEnd:
            return now >= tonightStart or now < tonightEnd
        return False

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
    parserArgs = {
        ('-s', '--nightStart'): {
            'help': 'Time the assistant will appear at (HH:MM, 24hr format)',
            'type': str,
            'default': '22:00'
        },
        ('-t', '--nightLength'): {
            'help': 'Duration the assistant will stay on screen (in minutes)',
            'type': int,
            'default': 8 * 60
        }
    }
    for args, kwargs in parserArgs.items():
        parser.add_argument(*args, **kwargs)
    args = parser.parse_args()

    app = SleepApplication(args.nightStart, args.nightLength)
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
