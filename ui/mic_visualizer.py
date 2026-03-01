from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QPainterPath, QBrush, QPen
import math
import random


class MicVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(120)
        self.level = 0
        self.smoothed_level = 0
        self.time_phase = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)  # 60 FPS

    def update_level(self, value):
        self.level = value

    def animate(self):
        # Progress time for wave animation
        self.time_phase += 0.08 + (self.smoothed_level * 0.1)
        
        # Smooth out the incoming volume level
        target_level = self.level
        
        # Jitter the idle baseline slightly so it always feels "alive"
        if target_level < 0.02:
            target_level = 0.05 + math.sin(self.time_phase * 0.5) * 0.02

        self.smoothed_level += (target_level - self.smoothed_level) * 0.2
        self.update()

    def get_wave_path(self, width, height, y_offset, amplitude_multiplier, phase_offset, frequency, points_count=60):
        path = QPainterPath()
        
        # Start at bottom left
        path.moveTo(0, height)
        path.lineTo(0, y_offset)

        step = width / (points_count - 1)
        
        # Create a smooth, flowing curve
        points = []
        for i in range(points_count):
            x = i * step
            # Combine multiple sine waves for a more natural, fluid motion
            wave1 = math.sin((i / points_count) * math.pi * frequency + self.time_phase + phase_offset)
            wave2 = math.cos((i / points_count) * math.pi * frequency * 1.5 - self.time_phase * 1.2 + phase_offset)
            
            # Taper the ends so it grounds smoothly to the edges
            edge_taper = math.sin((i / (points_count - 1)) * math.pi)
            
            # Base amplitude and audio-reactive amplitude
            base_wobble = (wave1 + wave2) * 5 * edge_taper * amplitude_multiplier
            audio_wobble = (wave1 * 1.5 + wave2 * 0.5) * self.smoothed_level * height * 0.6 * edge_taper * amplitude_multiplier
            
            y = y_offset - base_wobble - audio_wobble
            
            # Don't let it go below the bottom
            y = min(y, height)
            
            points.append(QPointF(x, y))

        path.lineTo(points[0])
        # Smooth curve through the points
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]
            ctrl_pt = QPointF((p1.x() + p2.x()) / 2, p1.y())
            path.quadTo(ctrl_pt, p2)

        # Close the path on the right side and bottom
        path.lineTo(width, height)
        path.closeSubpath()
        return path

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        
        # Draw multiple layered waves for depth
        
        # Layer 1: Background dark blue, tall & slow
        bg_path = self.get_wave_path(w, h, h - 10, amplitude_multiplier=0.6, phase_offset=0, frequency=2)
        bg_gradient = QLinearGradient(0, 0, 0, h)
        bg_gradient.setColorAt(0, QColor(10, 50, 150, 100))
        bg_gradient.setColorAt(1, QColor(0, 10, 50, 20))
        painter.setBrush(QBrush(bg_gradient))
        painter.setPen(Qt.NoPen)
        painter.drawPath(bg_path)
        
        # Layer 2: Mid cyan, offset and wavy
        mid_path = self.get_wave_path(w, h, h - 5, amplitude_multiplier=0.8, phase_offset=1.5, frequency=3)
        mid_gradient = QLinearGradient(0, 0, 0, h)
        mid_gradient.setColorAt(0, QColor(0, 150, 220, 140))
        mid_gradient.setColorAt(1, QColor(0, 50, 100, 30))
        painter.setBrush(QBrush(mid_gradient))
        painter.drawPath(mid_path)
        
        # Layer 3: Foreground bright cyan/white core
        fg_path = self.get_wave_path(w, h, h, amplitude_multiplier=1.2, phase_offset=3.14, frequency=2.5)
        fg_gradient = QLinearGradient(0, 0, 0, h)
        
        # Brighten gradient significantly when audio is loud
        loudness = min(self.smoothed_level * 2, 1.0)
        top_color = QColor(int(50 + 200 * loudness), 255, 255, 220)
        fg_gradient.setColorAt(0, top_color)
        fg_gradient.setColorAt(0.5, QColor(0, 200, 255, 180))
        fg_gradient.setColorAt(1, QColor(0, 100, 150, 50))
        
        painter.setBrush(QBrush(fg_gradient))
        
        # Add a bright border to the top edge of the foreground wave
        border_pen = QPen(QColor(150 + int(loudness * 100), 255, 255, 255), 2)
        painter.setPen(border_pen)
        
        painter.drawPath(fg_path)

    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        return self.size()
