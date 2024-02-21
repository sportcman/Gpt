import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit


class TextProcessor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('¥')

        # Создание виджета для ввода символов
        self.symbol_input = QLineEdit(self)

        # Создание кнопки выбора файла
        self.file_btn = QPushButton('Выбрать файл', self)
        self.file_btn.clicked.connect(self.selectFile)

        # Создание кнопки удаления символов
        self.process_btn = QPushButton('Удалить символы', self)
        self.process_btn.clicked.connect(self.processText)
        self.process_btn.setEnabled(False)

        # Создание вертикального слоя и добавление виджетов
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Введите символы для удаления:'))
        layout.addWidget(self.symbol_input)
        layout.addWidget(self.file_btn)
        layout.addWidget(self.process_btn)

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
                self.process_btn.setEnabled(True)

    def processText(self):
        if hasattr(self, 'selected_file'):
            # Удаление выбранных символов
            symbols_to_remove = self.symbol_input.text()
            with open(self.selected_file, 'r', encoding='utf-8') as f:
                text = f.read()

            processed_text = ''.join(ch for ch in text if ch not in symbols_to_remove)

            with open(self.selected_file, 'w', encoding='utf-8') as f:
                f.write(processed_text)

            self.symbol_input.clear()
            self.process_btn.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    processor = TextProcessor()
    processor.show()
    sys.exit(app.exec_())
