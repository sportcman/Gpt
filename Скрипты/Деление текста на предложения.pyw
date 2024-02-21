import re
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Создание метки и поля ввода для выбора файла
        input_label = QLabel(self)
        input_label.setText("Выберите входной файл:")
        input_label.move(10, 10)
        input_label.adjustSize()

        self.input_entry = QLineEdit(self)
        self.input_entry.setGeometry(10, 30, 380, 20)

        input_button = QPushButton('Просмотр', self)
        input_button.setGeometry(400, 28, 80, 25)
        input_button.clicked.connect(self.browse_input_file)

        output_label = QLabel(self)
        output_label.setText("Выберите выходной файл:")
        output_label.move(10, 60)
        output_label.adjustSize()

        self.output_entry = QLineEdit(self)
        self.output_entry.setGeometry(10, 80, 380, 20)

        output_button = QPushButton('Просмотр', self)
        output_button.setGeometry(400, 78, 80, 25)
        output_button.clicked.connect(self.browse_output_file)

        # Создание кнопки для запуска обработки текста
        process_button = QPushButton('Обработать текст', self)
        process_button.setGeometry(240, 110, 130, 40)
        process_button.clicked.connect(self.process_text)

        # Создание метки для отображения статуса обработки
        self.status_label = QLabel(self)
        self.status_label.setGeometry(10, 160, 470, 20)

        self.setGeometry(100, 100, 490, 200)
        self.setWindowTitle('Разделение предложений в файле')
        self.show()

    def browse_input_file(self):
        input_filename, _ = QFileDialog.getOpenFileName(self, "Выберите входной файл", "", "Text files (*.txt)")
        self.input_entry.setText(input_filename)

    def browse_output_file(self):
        output_filename, _ = QFileDialog.getSaveFileName(self, "Выберите выходной файл", "", "Text files (*.txt)")
        self.output_entry.setText(output_filename)

    def save_to_file(self, sentences, output_filename):
        with open(output_filename, "w", encoding="utf-8") as output_file:
            for sentence in sentences:
                if sentence.strip():
                    output_file.write(sentence + '\n')

    def process_file(self, input_filename, output_filename):
        with open(input_filename, "r", encoding="utf-8") as input_file:
            text = input_file.read()

        # Разделение текста на предложения по знакам препинания (.?!) за исключением точки в конце строки и точки после одного символа в конце строки
        sentences = re.split(r"([.?!]+(?:\s+(?!\.{1,2}$)|(?<=\S)[\.]))\s*", text)

        # Запись предложений в выходной файл, каждое на новой строке
        with open(output_filename, "w", encoding="utf-8") as output_file:
            for sentence in sentences:
                if sentence.strip():
                    output_file.write(sentence + '\n')

    def process_text(self):
        input_filename = self.input_entry.text()
        output_filename = self.output_entry.text()

        if not input_filename or not output_filename:
            QMessageBox.warning(self, "Ошибка", "Выберите входной и выходной файлы")
            return

        try:
            self.process_file(input_filename, output_filename)
            self.status_label.setText("Предложения разделены успешно.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", "Произошла ошибка при разделении предложений: {}".format(str(e)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
