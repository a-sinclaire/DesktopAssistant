import random
import sys

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt


class Application(QtWidgets.QApplication):
    def __init__(self):
        super().__init__([])

        self.icon = QtGui.QIcon('res/bnuuy.png')
        self.tray = QtWidgets.QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)

        self.menu = QtWidgets.QMenu()
        self.quitAction = QtGui.QAction('Quit')
        self.quitAction.triggered.connect(self.quit)
        self.hideAction = QtGui.QAction('Hide')
        self.hideAction.triggered.connect(self.toggle_visibility)
        self.actions = [self.hideAction, self.quitAction]
        for action in self.actions:
            self.menu.addAction(action)
        self.tray.setContextMenu(self.menu)

        self.widget = Widget()
        self.widget.show()

    @QtCore.Slot()
    def toggle_visibility(self):
        if self.widget.isVisible():
            self.widget.setVisible(False)
            self.hideAction.setText('Show')
        else:
            self.widget.setVisible(True)
            self.hideAction.setText('Hide')


class Widget(QtWidgets.QWidget):
    def __init__(self):
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

        self.avatar = QtWidgets.QLabel(alignment=Qt.AlignCenter)
        self.movie = QtGui.QMovie('res/sleepy_claire_smaller.gif')
        self.avatar.setMovie(self.movie)
        self.movie.start()

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
