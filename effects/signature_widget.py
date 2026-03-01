from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPainter, QColor, QFont, QLinearGradient
import math


class SignatureWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.text = "HunterIsLive"
        # No animation timer - static text

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Simple dark background
        painter.fillRect(self.rect(), QColor(20, 20, 40, 180))

        # Simple bold white text - no animations
        painter.setPen(QColor(200, 200, 200))  # Dark white for subtle look
        font = QFont("Consolas", 14)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignRight | Qt.AlignVCenter, self.text)
        
        # Simple underline - no animation
        underline_y = self.height() - 5
        underline_width = painter.fontMetrics().horizontalAdvance(self.text)
        underline_x = self.width() - underline_width - 5
        
        painter.setPen(QColor(100, 100, 100))  # Dark gray underline
        painter.drawLine(underline_x, underline_y, underline_x + underline_width, underline_y)
