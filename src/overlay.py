import sys
import random
import psutil

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QRect, QTimer, QPropertyAnimation
from PyQt5.QtGui import QPainter, QColor, QPen


class Overlay(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setGeometry(QApplication.primaryScreen().geometry())
        self.setMouseTracking(True)

        # Square sizes
        self.green_square_size = (200, 50)
        self.red_square_size = (50, 50)

        # Initial positions
        self.green_square_x = 0
        self.green_square_y = 0
        self.red_square_x = 0
        self.red_square_y = 0

        # Animation
        self.animation = QPropertyAnimation(self, b"geometry")

        self.randomize_squares()
        self.show()

    def randomize_squares(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        
        # Randomize green square
        self.green_square_x = random.randint(0, screen_geometry.width() - self.green_square_size[0])
        self.green_square_y = random.randint(0, screen_geometry.height() - self.green_square_size[1])
        
        # Randomize red square
        self.red_square_x = random.randint(0, screen_geometry.width() - self.red_square_size[0])
        self.red_square_y = random.randint(0, screen_geometry.height() - self.red_square_size[1])
        
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw green square
        painter.setPen(QPen(QColor(0, 255, 0, 255), 2))
        painter.setBrush(QColor(0, 255, 0, 50))
        green_rect = QRect(self.green_square_x, self.green_square_y, *self.green_square_size)
        painter.drawRect(green_rect)

        # Draw red square
        painter.setPen(QPen(QColor(255, 0, 0, 255), 2))
        painter.setBrush(QColor(255, 0, 0, 50))
        red_rect = QRect(self.red_square_x, self.red_square_y, *self.red_square_size)
        painter.drawRect(red_rect)

    def mousePressEvent(self, event):
        # Check if green square is clicked
        if (self.green_square_x <= event.x() <= self.green_square_x + self.green_square_size[0] and
            self.green_square_y <= event.y() <= self.green_square_y + self.green_square_size[1]):
            self.randomize_squares()

        # Check if red square is clicked
        if (self.red_square_x <= event.x() <= self.red_square_x + self.red_square_size[0] and
            self.red_square_y <= event.y() <= self.red_square_y + self.red_square_size[1]):
            self.close()


def is_vscode_running():
    """Check if Visual Studio Code is running."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'Code.exe' or proc.info['name'] == 'code':  # Windows and macOS/Linux process names
            return True
    return False


def main():
    app = QApplication(sys.argv)
    overlay = Overlay()

    # Timer to check if Visual Studio Code is running
    timer = QTimer()
    timer.timeout.connect(lambda: overlay.close() if not is_vscode_running() else None)
    timer.start(1000)  # Check every second

    # Run only if Visual Studio Code is running at start
    if is_vscode_running():
        sys.exit(app.exec_())
    else:
        print("Visual Studio Code is not running.")
        sys.exit()