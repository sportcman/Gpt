import os
import sys
import chardet
from PyQt5.QtWidgets import QApplication, QFileDialog, QComboBox, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget, QLabel, QListWidget, QListWidgetItem, QHBoxLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конвертер кодировки")
        self.setGeometry(100, 100, 500, 300)

        self.layout = QVBoxLayout()

        self.file_button = QPushButton("Выбрать файлы", self)
        self.file_button.clicked.connect(self.select_files)

        self.convert_button = QPushButton("Конвертировать", self)
        self.convert_button.clicked.connect(self.convert_files)

        self.selected_files_list = QListWidget()

        self.encoding_label = QLabel("Выберите кодировку:", self)
        self.encoding_combo = QComboBox(self)
        self.encoding_combo.addItem("utf-8")
        self.encoding_combo.addItem("utf-16")
        self.encoding_combo.addItem("cp1251")

        self.layout.addWidget(self.file_button)

        info_layout = QHBoxLayout()
        info_layout.addWidget(self.selected_files_list)
        info_layout.addWidget(self.encoding_label)
        info_layout.addWidget(self.encoding_combo)

        self.layout.addLayout(info_layout)
        self.layout.addWidget(self.convert_button)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def select_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        options |= QFileDialog.ExistingFiles
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы", "", "Text Files (*.txt)", options=options)
        self.selected_files_list.clear()
        for file_path in files:
            item = QListWidgetItem(file_path)
            self.selected_files_list.addItem(item)

    def convert_files(self):
        if self.selected_files_list.count() == 0:
            QMessageBox.warning(self, "Ошибка", "Файлы не выбраны!")
            return

        selected_encoding = self.encoding_combo.currentText()

        for i in range(self.selected_files_list.count()):
            file_item = self.selected_files_list.item(i)
            file_path = file_item.text()
            try:
                with open(file_path, 'rb') as file:
                    raw_data = file.read()
                    detected_encoding = chardet.detect(raw_data)['encoding']
                    content = raw_data.decode(detected_encoding)

                with open(file_path, 'w', encoding=selected_encoding) as file:
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
