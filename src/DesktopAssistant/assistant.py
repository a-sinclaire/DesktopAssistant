from io import BytesIO

from PySide6.QtCore import QResource, Qt
from PySide6.QtGui import QAction, QIcon, QMouseEvent, QMovie, QPixmap
from PySide6.QtWidgets import (QApplication, QLabel, QMenu, QSystemTrayIcon,
                               QVBoxLayout, QWidget)

import DesktopAssistant.assets  # noqa: F401; pylint: disable=unused-import
from DesktopAssistant.utils import filetype


class Sprite:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

        resource = QResource(self.path)
        fpSprite = BytesIO(resource.data())
        self.animated = filetype.isAnimated(fpSprite)

        if self.animated:
            self.sprite = QMovie(self.path)
        else:
            self.sprite = QPixmap(self.path)


class Widget(QWidget):
    def __init__(self, sprites: dict[str, str], initialSprite: str):
        """
        :param sprites: dict that maps sprite names to QResource paths
        :param initialSprite: name of the initial sprite
        """
        super().__init__()

        self.sprites = {}
        for name, path in sprites.items():
            self.sprites[name] = Sprite(name, path)
        self.currentSprite = self.sprites[initialSprite]

        self.label = QLabel()
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

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.label)

        self.clickX = None
        self.clickY = None

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

    def mousePressEvent(self, event: QMouseEvent):
        self.clickX = event.x()
        self.clickY = event.y()

    def mouseMoveEvent(self, event: QMouseEvent):
        self.move(event.globalX() - self.clickX,
                  event.globalY() - self.clickY)


class Application(QApplication):
    def __init__(self, iconPath: str, sprites: dict[str, str],
                 *widgetArgs, widgetClass: QWidget = Widget,
                 initialSprite: str | None = None, **widgetKwargs):
        """
        :param iconPath: QResource path to the icon
        :param sprites: dict that maps sprite names to QResource paths
        :param widgetArgs: other positional args to be passed to the widget
        :param widgetClass: class of the widget
        :param initialSprite: name of the initial sprite
        :param widgetKwrgs: other keyword args to be passed to the widget
        """
        super().__init__([])

        self.icon = QIcon(iconPath)
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)

        self.menu = QMenu()
        self.quitAction = QAction('Quit')
        self.quitAction.triggered.connect(self.quit)
        self.hideAction = QAction('Hide')
        self.hideAction.triggered.connect(self.toggleVisibility)
        self.actions = [self.hideAction, self.quitAction]
        for action in self.actions:
            self.menu.addAction(action)
        self.tray.setContextMenu(self.menu)

        self.widget = widgetClass(sprites, initialSprite,
                                  *widgetArgs, **widgetKwargs)
        self.widget.show()

    def toggleVisibility(self):
        if self.widget.isVisible():
            self.widget.setVisible(False)
            self.hideAction.setText('Show')
        else:
            self.widget.setVisible(True)
            self.hideAction.setText('Hide')
