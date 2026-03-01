from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QFont, QLinearGradient, QPen
import math

class SystemMetric(QWidget):
    def __init__(self, name, unit="", color_base=(0, 200, 255)):
        super().__init__()
        self.name = name
        self.unit = unit
        self.color_base = color_base
        self.value = 0
        self.target_value = 0
        self.animation_phase = 0
        
        self.setMinimumHeight(65)
        
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate)
        self.animation_timer.start(50)

    def update_value(self, value):
        self.target_value = value

    def animate(self):
        self.value += (self.target_value - self.value) * 0.1
        self.animation_phase += 0.1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Metric name
        painter.setPen(QColor(150, 200, 255))
        font = QFont("Consolas", 10)
        painter.setFont(font)
        painter.drawText(10, 18, self.name)

        # Large value text - positioned better
        value_color = self.get_value_color(self.value)
        painter.setPen(value_color)
        font = QFont("Consolas", 20)
        font.setBold(True)
        painter.setFont(font)
        value_text = f"{self.value:.0f}{self.unit}"
        painter.drawText(10, 45, value_text)

        # Progress bar - repositioned
        self.draw_progress_bar(painter)

    def draw_progress_bar(self, painter):
        bar_y = 52
        bar_height = 6
        bar_width = self.width() - 20
        bar_x = 10

        # Background
        painter.fillRect(bar_x, bar_y, bar_width, bar_height, QColor(20, 20, 40))

        # Animated progress
        progress_width = int(bar_width * (self.value / 100))
        if progress_width > 0:
            gradient = QLinearGradient(bar_x, 0, bar_x + progress_width, 0)
            color = self.get_value_color(self.value)
            
            # Animated glow effect
            glow_pos = (math.sin(self.animation_phase) + 1) / 2
            gradient.setColorAt(0, color.darker(150))
            gradient.setColorAt(glow_pos, color.lighter(120))
            gradient.setColorAt(1, color)

            painter.fillRect(bar_x, bar_y, progress_width, bar_height, gradient)

        # Border glow
        pen = QPen(self.get_value_color(self.value).lighter(150), 1)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(bar_x, bar_y, bar_width, bar_height)

    def get_value_color(self, value):
        if value < 50:
            return QColor(0, 255, 100)  # Green
        elif value < 80:
            return QColor(255, 200, 0)  # Yellow
        else:
            return QColor(255, 50, 50)   # Red

class LeftPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(280)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title = QLabel("SYSTEM METRICS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #00c8ff;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Consolas';
                padding: 10px;
                background: rgba(0, 50, 100, 30);
                border: 1px solid #00c8ff;
                border-radius: 5px;
            }
        """)
        layout.addWidget(title)

        # System metrics
        self.cpu_metric = SystemMetric("CPU", "%", (0, 200, 255))
        self.ram_metric = SystemMetric("RAM", "%", (255, 100, 200))
        self.temp_metric = SystemMetric("TEMP", "°C", (255, 150, 0))
        self.gpu_metric = SystemMetric("GPU", "%", (100, 255, 200))
        self.disk_metric = SystemMetric("DISK", "%", (200, 100, 255))
        metrics = [
            self.cpu_metric, self.ram_metric, self.temp_metric,
            self.gpu_metric, self.disk_metric
        ]

        for metric in metrics:
            layout.addWidget(metric)

        layout.addStretch()

        # Animation timer for visual effects
        self.glow_timer = QTimer()
        self.glow_timer.timeout.connect(self.update_glow)
        self.glow_timer.start(100)

    def update_stats(self, data):
        self.cpu_metric.update_value(data.get('cpu', 0))
        self.ram_metric.update_value(data.get('ram', 0))
        self.temp_metric.update_value(data.get('temp', 0))
        self.gpu_metric.update_value(data.get('gpu', 0))
        self.disk_metric.update_value(data.get('disk', 0))


    def update_glow(self):
        # Trigger repaint for glow animations
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Panel background with subtle gradient
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(10, 10, 30, 180))
        gradient.setColorAt(0.5, QColor(20, 20, 50, 200))
        gradient.setColorAt(1, QColor(10, 10, 30, 180))
        
        painter.fillRect(self.rect(), gradient)

        # Border glow
        pen = QPen(QColor(0, 150, 255, 100), 2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(1, 1, self.width() - 2, self.height() - 2)
