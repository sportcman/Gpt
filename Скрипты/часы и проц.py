import sys
import platform
import psutil
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QTimer, QDateTime

class HelloApp(QWidget):
    def __init__(self):
        super().__init__()

        # Создание виджетов на главном окне
        self.clock_label = QLabel("", self)
        self.date_label = QLabel("", self)
        self.cpu_label = QLabel("", self)


        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cpu_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Размещение виджетов на layout
        layout = QVBoxLayout()
        layout.addWidget(self.cpu_label)  # Добавляем метку процессора в layout
        layout.addWidget(self.clock_label)  # Добавляем метку часов в layout
        layout.addWidget(self.date_label)  # Добавляем метку даты в layout
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

        # Создаем таймер для обновления времени и даты
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)  # Обновление каждую секунду

    # В методе update_info класса HelloApp
    def update_info(self):
        cpu_info = f"{psutil.cpu_percent()}%"
        self.cpu_label.setText(cpu_info)
        current_time = QDateTime.currentDateTime().toString("hh:mm:ss")
        current_date = QDateTime.currentDateTime().toString("dd-MM-yyyy")
        datetime_str = f"{current_time}  {current_date}"
        self.clock_label.setText(datetime_str)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HelloApp()
    
    window.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Установка флага FramelessWindowHint
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
    window.cpu_label.setStyleSheet("font-size: 16px; font-family: Arial; color: #37b2b8;")
    window.clock_label.setStyleSheet("font-size: 16px; font-family: Arial; color: #37b2b8;")
    window.date_label.setStyleSheet("font-size: 16px; font-family: Arial; color: #37b2b8;")
    window.move(750, 1100)  # Перемещение окна в левый верхний угол экрана
    
    app.setWindowIcon(QIcon('icon.png'))  # Установка иконки приложения
    
    window.show()
    sys.exit(app.exec())
