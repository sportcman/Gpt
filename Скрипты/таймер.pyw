import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSpinBox, QPushButton, QHBoxLayout, QMessageBox, QAction
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, QTimer, QSize, QPropertyAnimation
import subprocess

class ShutdownTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('   ')
        self.setGeometry(100, 100, 330, 200)
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("""
        QWidget {
            font-family: 'Segoe UI', sans-serif;
            font-size: 16px;
            background-color: #FFFFFF;
            color: #333333;
        }
        
        QLabel {
            font-size: 20px;
        }
        
        QPushButton {
            background-color: #2196F3;
            border: none;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            min-width: 100px;
        }
        
        QPushButton#stop_button {
            background-color: #4CAF50;
        }
        
        QPushButton:hover {
            background-color: #0D47A1;
        }
        
        QSpinBox {
            font-size: 18px;
            padding: 5px;
            border-radius: 5px;
        }
        
        QSpinBox::hover {
            background-color: #E0E0E0;
        }
        
        QLabel#countdown_label {
            font-size: 24px;
            margin-top: 20px;
        }
        """)
        
        self.timer_label = QLabel('Таймер 120 минут максимум.')
        self.timer_spinbox = QSpinBox()
        self.timer_spinbox.setMinimum(1)
        self.timer_spinbox.setMaximum(120)
        
        self.start_button = QPushButton('Старт')
        self.start_button.clicked.connect(self.start_timer)
        
        self.stop_button = QPushButton('Стоп')
        self.stop_button.setObjectName('stop_button')
        self.stop_button.clicked.connect(self.stop_timer)
        
        self.countdown_label = QLabel('')
        self.countdown_label.setObjectName('countdown_label')
        
        top_layout = QVBoxLayout()
        top_layout.addWidget(self.timer_label)
        top_layout.addWidget(self.timer_spinbox)
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.start_button)
        bottom_layout.addWidget(self.stop_button)
        bottom_layout.addStretch()
        
        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addLayout(bottom_layout)
        layout.addWidget(self.countdown_label)
        
        self.setLayout(layout)
    
    def start_timer(self):
        minutes = self.timer_spinbox.value()
        seconds = minutes * 60
        
        # Запускаем таймер
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)  # 1 секунда
    
        self.remaining_seconds = seconds
        self.update_countdown()

        # Добавляем анимацию
        self.animation = QPropertyAnimation(self.countdown_label, b"size")
        self.animation.setDuration(500)
        self.animation.setStartValue(QSize(0, 0))
        self.animation.setEndValue(QSize(200, 50))
        self.animation.start()
    
    def update_countdown(self):
        self.remaining_seconds -= 1
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        self.countdown_label.setText(f'Осталось времени: {minutes:02d}:{seconds:02d}')
        
        if self.remaining_seconds <= 0:
            self.shutdown()
    
    def stop_timer(self):
        reply = QMessageBox.question(self, 'Выключение компьютера', 'Вы действительно хотите остановить таймер?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.timer.stop()
            self.countdown_label.setText('')
            self.timer_spinbox.setValue(1)
    
    def shutdown(self):

            # Выключаем компьютер с помощью команды "shutdown"
            try:
                subprocess.call(['shutdown', '/s', '/t', '0'])
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Не удалось выключить компьютер: {e}')
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShutdownTimer()
    window.show()
    sys.exit(app.exec_())
