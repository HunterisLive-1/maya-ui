from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer, QRectF, QSize, QPointF
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QPen, QFont, QRadialGradient, QPainterPath
from PySide6.QtGui import QShortcut, QKeySequence
import math

from ui.orb_widget import OrbWidget
from ui.left_panel import LeftPanel
from ui.right_panel import RightPanel
from ui.mic_visualizer import MicVisualizer
from effects.particle_engine import ParticleEngine
from effects.signature_widget import SignatureWidget

from workers.audio_worker import AudioWorker
from workers.system_worker import SystemWorker
from workers.mic_worker import MicWorker


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Maya AI HUD")

        # Floating Window with glow border
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowMinimizeButtonHint
        )

        self.resize(1400, 800)

        # Main Horizontal Layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # Left Panel - System Info
        self.left_panel = LeftPanel()
        main_layout.addWidget(self.left_panel)

        # Center Layout (Orb + Mic Visualizer)
        center_layout = QVBoxLayout()
        center_layout.setSpacing(20)

        self.orb = OrbWidget()
        center_layout.addWidget(self.orb, 2)

        self.mic_visualizer = MicVisualizer()
        center_layout.addWidget(self.mic_visualizer, 1)

        main_layout.addLayout(center_layout, 2)

        # Right Panel
        self.right_panel = RightPanel()
        main_layout.addWidget(self.right_panel)

        # We are going back to custom rendering for a clean look, so we won't use bg_label
        # (keeping Particle Engine on top)

        # Particle Engine Background (keep particles on top of GIF if desired, or we can remove it. Let's keep it overlayed)
        self.particle_engine = ParticleEngine(self)
        self.particle_engine.setGeometry(0, 0, self.width(), self.height())
        # To make particle engine overlay the gif properly without drawing its own solid bg, we just insert it above bg_label
        # (This assumes ParticleEngine supports transparent background, which it normally handles via paintEvent)

        # Signature Widget
        self.signature = SignatureWidget(self)
        self.signature.setGeometry(self.width() - 220, self.height() - 40, 200, 30)

        # Background Animation Timer (60 FPS) for the glowing border
        self.bg_offset = 0
        self.bg_timer = QTimer()
        self.bg_timer.timeout.connect(self.animate_overlay)
        self.bg_timer.start(16)

        # ========================
        # THREADS
        # ========================

        # Speaker Audio → Orb
        self.audio_worker = AudioWorker()
        self.audio_worker.amplitude_signal.connect(self.orb.update_amplitude)
        self.audio_worker.start()

        # Mic → Bottom Visualizer
        self.mic_worker = MicWorker()
        self.mic_worker.mic_signal.connect(self.mic_visualizer.update_level)
        self.mic_worker.start()

        # System Monitor → Left Panel
        self.system_worker = SystemWorker()
        self.system_worker.system_signal.connect(self.left_panel.update_stats)
        self.system_worker.start()

        self.old_pos = None

        # ========================
        # Shortcut to Close
        # ========================

        self.exit_shortcut = QShortcut(QKeySequence("Esc"), self)
        self.exit_shortcut.setContext(Qt.ApplicationShortcut)
        self.exit_shortcut.activated.connect(self.close)

        self.ctrlq_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.ctrlq_shortcut.setContext(Qt.ApplicationShortcut)
        self.ctrlq_shortcut.activated.connect(self.close)

    def closeEvent(self, event):
        print("Closing Maya HUD...")

        # Stop timers first
        self.bg_timer.stop()

        # Request interruption for all workers
        for worker in [self.audio_worker, self.mic_worker, self.system_worker]:
            if worker.isRunning():
                worker.requestInterruption()
                worker.quit()
                worker.wait(3000)  # Wait up to 3 seconds

        # Force close if still running
        for worker in [self.audio_worker, self.mic_worker, self.system_worker]:
            if worker.isRunning():
                worker.terminate()
                worker.wait(1000)

        event.accept()

    # ========================
    # Overlay Animation
    # ========================

    def animate_overlay(self):
        self.bg_offset += 1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dynamic clean futuristic background
        time = self.bg_offset * 0.01
        
        # Base deep dark space
        painter.fillRect(self.rect(), QColor(5, 5, 10))

        # Animated wide sweeping cyan/blue gradient
        sweeping_grad = QLinearGradient(
            0, self.height() / 2 + math.sin(time) * 200, 
            self.width(), self.height() / 2 + math.cos(time * 0.8) * 200
        )
        sweeping_grad.setColorAt(0, QColor(0, 50, 100, 40))
        sweeping_grad.setColorAt(0.5, QColor(0, 100, 150, 70))
        sweeping_grad.setColorAt(1, QColor(0, 20, 50, 30))
        painter.fillRect(self.rect(), sweeping_grad)

        # High quality smooth dark vignette over the corners
        vignette = QRadialGradient(self.width() / 2, self.height() / 2, self.width() / 1.2)
        vignette.setColorAt(0, QColor(0, 0, 0, 0))
        vignette.setColorAt(0.7, QColor(0, 0, 0, 150))
        vignette.setColorAt(1, QColor(0, 0, 0, 240))
        painter.fillRect(self.rect(), vignette)

        # Enhanced glow border with animated effects
        self.draw_enhanced_glow_border(painter)

    def draw_enhanced_glow_border(self, painter):
        # Multi-layer glow border with animation
        time = self.bg_offset * 0.02
        
        # Outer glow with pulse
        pulse = (math.sin(time) + 1) / 2
        outer_glow = QPen(QColor(0, 200, 255, int(50 + pulse * 50)), 4)
        painter.setPen(outer_glow)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(0, 0, self.width(), self.height())
        
        # Middle glow with color shift
        hue_shift = (math.sin(time * 0.5) + 1) / 2
        mid_color = QColor(
            int(0 + hue_shift * 100),
            int(200 - hue_shift * 50),
            255
        )
        mid_glow = QPen(mid_color, 2)
        painter.setPen(mid_glow)
        painter.drawRect(2, 2, self.width() - 4, self.height() - 4)
        
        # Inner sharp border
        inner_border = QPen(QColor(0, 150, 255, 150), 1)
        painter.setPen(inner_border)
        painter.drawRect(5, 5, self.width() - 10, self.height() - 10)
        
        # Corner accents
        corner_size = 20
        corner_color = QColor(0, 255, 200, int(100 + pulse * 100))
        painter.setPen(QPen(corner_color, 2))
        
        # Top-left corner
        painter.drawLine(0, 0, corner_size, 0)
        painter.drawLine(0, 0, 0, corner_size)
        
        # Top-right corner
        painter.drawLine(self.width() - corner_size, 0, self.width(), 0)
        painter.drawLine(self.width(), 0, self.width(), corner_size)
        
        # Bottom-left corner
        painter.drawLine(0, self.height(), corner_size, self.height())
        painter.drawLine(0, self.height() - corner_size, 0, self.height())
        
        # Bottom-right corner
        painter.drawLine(self.width() - corner_size, self.height(), self.width(), self.height())
        painter.drawLine(self.width(), self.height() - corner_size, self.width(), self.height())

    # ========================
    # Drag Window
    # ========================

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        self.particle_engine.setGeometry(0, 0, self.width(), self.height())
        self.signature.setGeometry(self.width() - 220, self.height() - 40, 200, 30)
