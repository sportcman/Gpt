import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit


class FileConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Converter')

        # Создание кнопки выбора файла
        self.file_btn = QPushButton('Выбрать файл', self)
        self.file_btn.clicked.connect(self.selectFile)

        # Создание кнопки преобразования файла
        self.convert_btn = QPushButton('Преобразовать', self)
        self.convert_btn.clicked.connect(self.convertFile)
        self.convert_btn.setEnabled(False)

        # Создание виджета для отображения содержимого файла
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        # Создание вертикального слоя и добавление виджетов
        layout = QVBoxLayout()
        layout.addWidget(self.file_btn)
        layout.addWidget(self.convert_btn)
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

    def selectFile(self):
        # Открытие диалогового окна выбора файла
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Текстовые файлы (*.txt)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            if filenames:
                self.selected_file = filenames[0]
                self.convert_btn.setEnabled(True)
                self.text_edit.clear()

                # Отображение содержимого файла в QTextEdit
                with open(self.selected_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.text_edit.setPlainText(content)

    def convertFile(self):
        if hasattr(self, 'selected_file'):
            # Удаление пустых строк
            with open(self.selected_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            lines = [line.strip() for line in lines if line.strip()]

            with open(self.selected_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

            self.text_edit.clear()
            self.text_edit.setPlainText("Файл успешно преобразован!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = FileConverter()
    converter.show()
    sys.exit(app.exec_())
