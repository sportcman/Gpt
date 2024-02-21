import sys
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Удаление квадратных скобок")
        self.setGeometry(100, 100, 400, 150)
        self.setWindowIcon(QIcon('icon.png'))

        self.label = QLabel("Выберите файл для удаления квадратных скобок:")
        self.button = QPushButton("Выбрать файл")
        self.button.clicked.connect(self.open_file_dialog)
        self.button.setStyleSheet("background-color: #4CAF50; color: white;")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Выберите файл", "", "Текстовые файлы (*.txt)")
        if file_path:
            self.remove_brackets(file_path)

    def remove_brackets(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        pattern = r'\[.*?\]'
        result = re.sub(pattern, '', content)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(result)

        self.label.setText("Квадратные скобки и их содержимое успешно удалены!")
        self.label.setStyleSheet("color: green; font-size: 16px; font-weight: bold;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    
    palette = window.palette()
    palette.setColor(window.backgroundRole(), QColor(240, 240, 240))
    palette.setColor(window.foregroundRole(), Qt.white)
    window.setPalette(palette)

    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
    window.show()
    sys.exit(app.exec_())
