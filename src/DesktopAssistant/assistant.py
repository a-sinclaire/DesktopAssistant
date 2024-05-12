from importlib import resources
import io
from os import path
import random
import sys
from typing import BinaryIO, List

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt

import DesktopAssistant.assets
from DesktopAssistant.utils import filetype


class Sprite:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def load(self):
        resource = QtCore.QResource(self.path)
        fpSprite = io.BytesIO(resource.data())
        self.animated = filetype.isAnimated(fpSprite)

        if self.animated:
            self.sprite = QtGui.QMovie(self.path)
        else:
            self.sprite = QtGui.QPixmap(self.path)


class Widget(QtWidgets.QWidget):
    def __init__(self, sprites: List[Sprite],
                 initialSprite: str | None = None):
        """
        :param sprites: list of all the sprite objects to be used
        :param initialSprite:
            name of the initial sprite, if None this is set to the sprite at
            sprites[0]
        """
        super().__init__()

        for sprite in sprites:
            sprite.load()
        self.sprites = {sprite.name: sprite for sprite in sprites}
        self.currentSprite = (sprites[0] if initialSprite is None
                              else self.sprites[initialSprite])

        self.label = QtWidgets.QLabel()
        if self.currentSprite.animated:
            self.label.setMovie(self.currentSprite.sprite)
            self.label.movie().start()
        else:
            self.label.setPixmap(self.currentSprite.sprite)

        attributes = [Qt.WA_TranslucentBackground]
        for attr in attributes:
            self.setAttribute(attr)

        windowFlags = [Qt.BypassWindowManagerHint,
                       Qt.FramelessWindowHint,
                       Qt.NoDropShadowWindowHint,
                       Qt.WindowStaysOnTopHint]
        for flag in windowFlags:
            self.setWindowFlag(flag)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.label)

        self.click_x = None
        self.click_y = None

    def setSprite(self, spriteName: str):
        """Sets the current sprite to a given sprite

        :param spriteName: name of the sprite to set
        """
        if self.currentSprite.animated:
            self.label.movie().stop()
        self.label.clear()

        self.currentSprite = self.sprites[spriteName]
        if self.currentSprite.animated:
            self.label.setMovie(self.currentSprite.sprite)
            self.label.movie().start()
        else:
            self.label.setPixmap(self.currentSprite.sprite)
            self.label.show()

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        self.click_x = event.x()
        self.click_y = event.y()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        self.move(event.globalX() - self.click_x,
                  event.globalY() - self.click_y)


class Application(QtWidgets.QApplication):
    def __init__(self, iconPath: str, sprites: List[Sprite], *widgetArgs,
                 widgetClass = Widget, initialSprite: str | None = None,
                 **widgetKwargs):
        """
        :param iconPath: QResource path to the icon
        :param widgetClass: class of the widget
        :param sprites: list of all the sprite objects to be used
        :param initialSprite:
            name of the initial sprite, if None this is set to the sprite at
            sprites[0]
        :param widgetArgs: other positional args to be passed to the widget
        :param widgetKwrgs: other keyword args to be passed to the widget
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

        self.widget = widgetClass(sprites, initialSprite)
        self.widget.show()

    def toggleVisibility(self):
        if self.widget.isVisible():
            self.widget.setVisible(False)
            self.hideAction.setText('Show')
        else:
            self.widget.setVisible(True)
            self.hideAction.setText('Hide')

