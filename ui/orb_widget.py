from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, Qt, QPointF
from PySide6.QtGui import QPainter, QRadialGradient, QColor, QPen, QFont, QBrush, QPainterPath, QMovie, QImage, QPixmap
import math

class OrbWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.ai_name = "MAYA"
        self.amplitude = 0
        self.base_radius = 280  # Increased initial size even more
        self.current_radius = self.base_radius

        # Load the user-provided GIF
        self.movie = QMovie("orb.gif")
        self.movie.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)  # 60 FPS

    def update_amplitude(self, value):
        self.amplitude = value

    def set_ai_name(self, name):
        self.ai_name = name

    def animate(self):
        # Responsiveness to sound (scale up max size based on amplitude significantly)
        target = self.base_radius + self.amplitude * 180
        self.current_radius += (target - self.current_radius) * 0.4
        
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        center = self.rect().center()

        # Using HSV to smoothly transition colors for the glow/text based on sound amplitude
        current_amp = min(self.amplitude * 2, 1.0)
        
        # Idle Blue (240) to Cyan (180) for the text glow (Removed red orb tinting)
        hue = 240 - (current_amp * 60)
        
        # Draw the GIF Orb
        if self.movie.isValid():
            image = self.movie.currentImage()
            if not image.isNull():
                # Make the background color transparent natively
                bg_color = image.pixelColor(0, 0)
                mask = image.createMaskFromColor(bg_color.rgb(), Qt.MaskOutColor)
                image = image.convertToFormat(QImage.Format_ARGB32)
                image.setAlphaChannel(mask)
                
                size = int(self.current_radius * 2 * 1.2)  # Adjusted multiplier for better scaling
                
                # Convert to Pixmap and scale smoothly
                pixmap = QPixmap.fromImage(image)
                scaled_pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                
                # Draw the pixmap without the red tinting
                x = int(center.x() - scaled_pixmap.width() / 2)
                y = int(center.y() - scaled_pixmap.height() / 2)
                painter.drawPixmap(x, y, scaled_pixmap)

        # Draw AI Name
        self.draw_ai_name(painter, center, current_amp, hue)

    def draw_ai_name(self, painter, center, current_amp, hue):
        # Outer glow
        glow_color = QColor.fromHsv(int(hue), 255, 255, int(150 + 100 * current_amp))
        for i in range(3):
            offset = i * 2
            painter.setPen(QColor(glow_color.red(), glow_color.green(), glow_color.blue(), 100))
            font = QFont("Consolas", 18 + i + int(5 * current_amp))
            font.setBold(True)
            painter.setFont(font)
            text_rect = self.rect().adjusted(-offset, -offset, offset, offset)
            painter.drawText(text_rect, Qt.AlignCenter, self.ai_name)

        # Solid main text
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Consolas", 20 + int(5 * current_amp))
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, self.ai_name)
