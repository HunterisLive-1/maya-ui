from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, QPointF, Qt
from PySide6.QtGui import QPainter, QColor, QRadialGradient, QPen
import random
import math


class Particle:
    def __init__(self, width, height):
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        self.vx = random.uniform(-1, 1)  # Reduced from ±2 to ±1 for less movement
        self.vy = random.uniform(-1, 1)  # Reduced from ±2 to ±1 for less movement
        self.size = random.uniform(1, 3)  # Reduced from 1-4 to 1-3
        self.life = random.uniform(0.5, 1.0)
        self.max_life = self.life
        self.color = random.choice([
            QColor(255, 100, 200, 200),  # Pink
            QColor(100, 200, 255, 200),  # Cyan
            QColor(200, 100, 255, 200),  # Purple
            QColor(255, 255, 255, 200),  # White (AI data)
            QColor(100, 255, 200, 200),  # Mint
            QColor(0, 255, 255, 200),    # Neon Aqua
        ])

    def update(self, width, height):
        self.x += self.vx
        self.y += self.vy
        self.life -= 0.01

        # Wrap around edges
        if self.x < 0:
            self.x = width
        elif self.x > width:
            self.x = 0
        
        if self.y < 0:
            self.y = height
        elif self.y > height:
            self.y = 0

        # Respawn if dead
        if self.life <= 0:
            self.life = self.max_life
            self.x = random.uniform(0, width)
            self.y = random.uniform(0, height)

    def draw(self, painter):
        # Glow rendering
        alpha = int((self.life / self.max_life) * 200)
        color = QColor(self.color)
        color.setAlpha(alpha)
        
        glow = QRadialGradient(self.x, self.y, self.size * 2)
        glow.setColorAt(0, color)
        glow.setColorAt(1, QColor(0, 0, 0, 0))
        
        painter.setBrush(glow)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(self.x, self.y), self.size * 2, self.size * 2)


class ParticleEngine(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = []
        self.init_particles(150)  # Increased for richer background
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(33)  # Reduced from 16ms to 33ms (30 FPS instead of 60 FPS)

    def init_particles(self, count):
        width = self.width() if self.width() > 0 else 1400
        height = self.height() if self.height() > 0 else 800
        
        for _ in range(count):
            self.particles.append(Particle(width, height))

    def update_particles(self):
        width = self.width()
        height = self.height()
        
        for particle in self.particles:
            particle.update(width, height)
        
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setPen(QColor(0, 150, 255, 30))
        connection_count = 0
        max_connections = 100  # More connections for "AI network" look
        
        for i, p1 in enumerate(self.particles):
            if connection_count >= max_connections:
                break
            for p2 in self.particles[i+1:]:
                if connection_count >= max_connections:
                    break
                distance = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
                if distance < 150:
                    alpha = int((1 - distance / 150) * 40)
                    painter.setPen(QPen(QColor(0, 150, 255, alpha), 1))
                    painter.drawLine(QPointF(p1.x, p1.y), QPointF(p2.x, p2.y))
                    connection_count += 1
        
        # Draw scanlines for futuristic effect
        painter.setPen(QColor(0, 200, 255, 10))
        for y in range(0, self.height(), 4):
            painter.drawLine(0, y, self.width(), y)
        
        # Draw particles with simplified rendering
        for particle in self.particles:
            particle.draw(painter)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Reinitialize particles if size changes significantly
        if len(self.particles) == 0 or self.width() == 0:
            self.init_particles(100)
