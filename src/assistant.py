from os import path
import random
import sys

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt

import utils.filetype


def assetPath(filename=None):
    directory = path.dirname(__file__)
    return path.join(directory, '../assets', filename)


class Application(QtWidgets.QApplication):
    def __init__(self, spriteName, iconName):
        super().__init__([])

        self.icon = QtGui.QIcon(assetPath(iconName))
        self.tray = QtWidgets.QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)

        self.menu = QtWidgets.QMenu()
        self.quitAction = QtGui.QAction('Quit')
        self.quitAction.triggered.connect(self.quit)
        self.hideAction = QtGui.QAction('Hide')
        self.hideAction.triggered.connect(self.toggleVisibility)
        self.actions = [self.hideAction, self.quitAction]
        for action in self.actions:
            self.menu.addAction(action)
        self.tray.setContextMenu(self.menu)

        self.widget = Widget(spriteName)
        self.widget.show()

    @QtCore.Slot()
    def toggleVisibility(self):
        if self.widget.isVisible():
            self.widget.setVisible(False)
            self.hideAction.setText('Show')
        else:
            self.widget.setVisible(True)
            self.hideAction.setText('Hide')


class Widget(QtWidgets.QWidget):
    def __init__(self, spriteName):
        super().__init__()

        attributes = [Qt.WA_TranslucentBackground]
        for attr in attributes:
            self.setAttribute(attr)

        windowFlags = [Qt.BypassWindowManagerHint,
                       Qt.FramelessWindowHint,
                       Qt.NoDropShadowWindowHint,
                       Qt.WindowStaysOnTopHint]
        for flag in windowFlags:
            self.setWindowFlag(flag)

        spritePath = assetPath(spriteName)
        spriteIsAnimated = utils.filetype.isAnimated(spritePath)
        self.avatar = QtWidgets.QLabel(alignment=Qt.AlignCenter)
        if spriteIsAnimated:
            self.sprite = QtGui.QMovie(spritePath)
            self.avatar.setMovie(self.sprite)
            self.sprite.start()
        else:
            self.sprite = QtGui.QPixmap(spritePath)
            self.avatar.setPixmap(self.sprite)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.avatar)

        self.click_x = None
        self.click_y = None

    def mousePressEvent(self, event):
        self.click_x = event.x()
        self.click_y = event.y()

    def mouseMoveEvent(self, event):
        self.move(event.globalX() - self.click_x,
                  event.globalY() - self.click_y)


if __name__ == '__main__':
    app = Application()

    widget = DesktopAssistant()
    widget.show()

    sys.exit(app.exec())
