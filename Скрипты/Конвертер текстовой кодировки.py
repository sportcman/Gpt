import os
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget, QLabel, QComboBox
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конвертер кодировки")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.file_button = QPushButton("Выбрать файлы", self)
        self.file_button.clicked.connect(self.select_files)

        self.convert_button = QPushButton("Конвертировать", self)
        self.convert_button.clicked.connect(self.convert_files)

        self.selected_files = []

        self.encoding_label = QLabel("Выберите кодировку:", self)
        self.encoding_combo = QComboBox(self)
        self.encoding_combo.addItem("ANSI")
        self.encoding_combo.addItem("UTF-8")
        self.encoding_combo.addItem("UTF-16")
        self.encoding_combo.addItem("KOI8-R")

        self.layout.addWidget(self.file_button)
        self.layout.addWidget(self.encoding_label)
        self.layout.addWidget(self.encoding_combo)
        self.layout.addWidget(self.convert_button)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def select_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        options |= QFileDialog.ExistingFiles
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы", "", "Text Files (*.txt)", options=options)
        self.selected_files = files

    def convert_files(self):
        if not self.selected_files:
            QMessageBox.warning(self, "Ошибка", "Файлы не выбраны!")
            return

        selected_encoding = self.encoding_combo.currentText()

        for file_path in self.selected_files:
            try:
                with open(file_path, 'r', encoding=selected_encoding) as file:
                    content = file.read()

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось конвертировать файл: {file_path}\n\n{str(e)}")
                return

        QMessageBox.information(self, "Успех", "Файлы успешно конвертированы!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
