from importlib import resources
import io
from os import path
import random
import sys
from typing import BinaryIO

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt

import DesktopAssistant.assets
from DesktopAssistant.utils import filetype


class Application(QtWidgets.QApplication):
    def __init__(self, spritePath: str, iconPath: str):
        """
        :param spritePath: QResource path of the desktop assistant sprite
        :param spritePath: QResource path of the system tray icon
        """
        super().__init__([])

        self.icon = QtGui.QIcon(iconPath)
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
        self.widget = Widget(spritePath)
        self.widget.show()

    def toggleVisibility(self):
        if self.widget.isVisible():
            self.widget.setVisible(False)
            self.hideAction.setText('Show')
        else:
            self.widget.setVisible(True)
            self.hideAction.setText('Hide')


class Widget(QtWidgets.QWidget):
    def __init__(self, spritePath: str):
        """
        :param spritePath: QResource path of the desktop assistant sprite
        """
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

        resource = QtCore.QResource(spritePath)
        fpSprite = io.BytesIO(resource.data())
        spriteIsAnimated = filetype.isAnimated(fpSprite)
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

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        self.click_x = event.x()
        self.click_y = event.y()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        self.move(event.globalX() - self.click_x,
                  event.globalY() - self.click_y)

