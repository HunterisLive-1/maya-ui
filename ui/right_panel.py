from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer, QTime, Qt
from PySide6.QtGui import QFont, QPainter, QColor, QLinearGradient
import datetime


class RightPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(250)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title = QLabel("AI STATUS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #00ff88;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Consolas';
                padding: 8px;
                background: rgba(0, 100, 50, 30);
                border: 1px solid #00ff88;
                border-radius: 5px;
            }
        """)
        layout.addWidget(title)

        # Clock with futuristic style
        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignCenter)
        self.clock.setFont(QFont("Consolas", 20))
        self.clock.setStyleSheet("""
            QLabel {
                color: #00ffff;
                font-weight: bold;
                padding: 10px;
                background: rgba(0, 50, 100, 40);
                border: 2px solid #00ffff;
                border-radius: 8px;
            }
        """)

        # Date display
        self.date = QLabel()
        self.date.setAlignment(Qt.AlignCenter)
        self.date.setFont(QFont("Consolas", 12))
        self.date.setStyleSheet("""
            QLabel {
                color: #88ccff;
                padding: 5px;
            }
        """)

        # Status indicator
        self.status = QLabel("● MAYA ONLINE")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setFont(QFont("Consolas", 14))
        self.status.setStyleSheet("""
            QLabel {
                color: #00ff00;
                font-weight: bold;
                padding: 8px;
                background: rgba(0, 50, 0, 50);
                border: 1px solid #00ff00;
                border-radius: 5px;
            }
        """)

        # Performance indicator
        self.performance = QLabel("PERFORMANCE: OPTIMAL")
        self.performance.setAlignment(Qt.AlignCenter)
        self.performance.setFont(QFont("Consolas", 11))
        self.performance.setStyleSheet("""
            QLabel {
                color: #ffaa00;
                padding: 5px;
            }
        """)

        # AI CORE Section
        self.ai_core = QLabel("MODEL: NEURAL ENGINE v4.2")
        self.ai_core.setAlignment(Qt.AlignCenter)
        self.ai_core.setFont(QFont("Consolas", 10))
        self.ai_core.setStyleSheet("""
            QLabel {
                color: #0088ff;
                padding: 10px;
                background: rgba(0, 30, 60, 40);
                border: 1px dashed #0088ff;
                border-radius: 5px;
            }
        """)

        # Thread count display
        self.threads = QLabel("CPU THREADS: --")
        self.threads.setAlignment(Qt.AlignCenter)
        self.threads.setFont(QFont("Consolas", 10))
        self.threads.setStyleSheet("""
            QLabel {
                color: #88ffcc;
                padding: 5px;
            }
        """)

        layout.addWidget(self.clock)
        layout.addWidget(self.date)
        layout.addWidget(self.status)
        layout.addWidget(self.performance)
        layout.addWidget(self.ai_core)
        layout.addWidget(self.threads)
        layout.addStretch()

        # Update timers
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

        status_timer = QTimer(self)
        status_timer.timeout.connect(self.update_status)
        status_timer.start(3000)

        self.update_time()
        self.status_messages = [
            "● MAYA ONLINE",
            "● SYSTEM READY", 
            "● MONITORING ACTIVE",
            "● AI OPERATIONAL"
        ]
        self.status_index = 0

    def update_time(self):
        current_time = QTime.currentTime()
        self.clock.setText(current_time.toString("hh:mm:ss"))
        
        current_date = datetime.date.today()
        self.date.setText(current_date.strftime("%B %d, %Y"))
        
        # Update thread count from system
        import psutil
        try:
            p = psutil.Process()
            thread_count = p.num_threads()
            self.threads.setText(f"APP THREADS: {thread_count}")
        except:
            pass

    def update_status(self):
        self.status_index = (self.status_index + 1) % len(self.status_messages)
        self.status.setText(self.status_messages[self.status_index])

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
        pen = QColor(0, 150, 255, 100)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(1, 1, self.width() - 2, self.height() - 2)
