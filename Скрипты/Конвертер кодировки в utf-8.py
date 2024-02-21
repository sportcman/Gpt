import os
import sys
import chardet
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конвертер кодировки")
        self.setGeometry(100, 100, 400, 150)

        self.file_button = QPushButton("Выбрать файлы", self)
        self.file_button.setGeometry(120, 40, 160, 30)
        self.file_button.clicked.connect(self.select_files)

        self.convert_button = QPushButton("Конвертировать", self)
        self.convert_button.setGeometry(120, 80, 160, 30)
        self.convert_button.clicked.connect(self.convert_files)

        self.selected_files = []

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

        for file_path in self.selected_files:
            try:
                with open(file_path, 'rb') as file:
                    raw_data = file.read()
                    detected_encoding = chardet.detect(raw_data)['encoding']
                    content = raw_data.decode(detected_encoding)

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
