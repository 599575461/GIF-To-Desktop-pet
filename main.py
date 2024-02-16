import sys
import os
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QAction, QMenu, QSystemTrayIcon, QWidget, QMessageBox
from PyQt5.QtGui import QMovie, QIcon, QCursor
from PyQt5.QtCore import Qt


class GifWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.icon = QIcon(os.path.join('Elaina.jpg'))
        if not os.path.isfile(gif_path):
            msg = QMessageBox()
            msg.information(self, "错误", f"未找到GIF文件{gif_path}")
            self.quit()
        self.initUI()

    def quit(self):
        QApplication.quit()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowIcon(self.icon)
        self.repaint()
        layout = QVBoxLayout()
        self.label = QLabel()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.movie = QMovie(gif_path)
        self.movie.setSpeed(400)
        self.label.setMovie(self.movie)
        self.movie.start()
        quit_action = QAction('退出', self)
        quit_action.setIcon(self.icon)
        quit_action.triggered.connect(self.quit)
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.icon)
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gif_path = 'gif.gif'
    widget = GifWidget()
    widget.show()
    sys.exit(app.exec_())
