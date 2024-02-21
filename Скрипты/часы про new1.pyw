import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QTimer, QTime

class HelloApp(QWidget):
    def __init__(self):
        super().__init__()

        # Создание виджетов на главном окне
        self.clock_label = QLabel("", self)
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Размещение виджетов на layout
        layout = QVBoxLayout()
        layout.addWidget(self.clock_label)  # Добавляем метку часов в layout
        self.setLayout(layout)

        # Создание анимации для метки
        self.label_animation = QPropertyAnimation(self)
        self.label_animation.setTargetObject(self.clock_label)
        self.label_animation.setPropertyName(b"font")
        self.label_animation.setStartValue(QFont("Arial", 24))
        self.label_animation.setEndValue(QFont("Arial", 24))
        self.label_animation.setDuration(1000)
        self.label_animation.setLoopCount(-1)
        self.label_animation.start()

        # Создание анимации для окна
        self.window_animation = QPropertyAnimation(self)
        self.window_animation.setTargetObject(self)
        self.window_animation.setPropertyName(b"windowOpacity")
        self.window_animation.setStartValue(0.1)
        self.window_animation.setEndValue(1.7)
        self.window_animation.setDuration(2000)
        self.window_animation.start()

        # Создаем таймер для обновления времени
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Обновление каждую секунду

    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.clock_label.setText(current_time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HelloApp()
    
    window.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Установка флага FramelessWindowHint
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
    
    window.clock_label.setStyleSheet("font-size: 26px; font-family: Arial; color: #37b2b8;")
    window.move(620, 921)  # Перемещение окна в левый верхний угол экрана
    
    app.setWindowIcon(QIcon('icon.png'))  # Установка иконки приложения
    
    window.show()
    sys.exit(app.exec())
