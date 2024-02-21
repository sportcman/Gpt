import re
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, \
    QFileDialog, QCheckBox, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        input_label = QLabel(self)
        input_label.setText("Выберите файл:")
        input_label.move(10, 10)
        input_label.adjustSize()
        self.input_entry = QLineEdit(self)
        self.input_entry.setGeometry(10, 30, 380, 20)
        input_button = QPushButton('Просмотр', self)
        input_button.setGeometry(400, 28, 80, 25)
        input_button.clicked.connect(self.browse_input_file)

        output_label = QLabel(self)
        output_label.setText("Сохранить в файл:")
        output_label.move(10, 60)
        output_label.adjustSize() # текст становится видным целиком
        self.output_entry = QLineEdit(self)
        self.output_entry.setGeometry(10, 80, 380, 20)
        output_button = QPushButton('Просмотр', self)
        output_button.setGeometry(400, 78, 80, 25)
        output_button.clicked.connect(self.browse_output_file)

        remove_chars_label = QLabel(self)
        remove_chars_label.setText("Удалить символы:")
        remove_chars_label.move(10, 110)
        remove_chars_label.adjustSize()
        self.remove_chars_entry = QLineEdit(self)
        self.remove_chars_entry.setGeometry(10, 130, 470, 20)

        remove_spaces_label = QLabel(self)
        remove_spaces_label.setText("Сделать текст в одну строку")
        remove_spaces_label.move(10, 160)
        remove_spaces_label.adjustSize()
        self.remove_spaces_checkbox = QCheckBox(self)
        self.remove_spaces_checkbox.setGeometry(10, 180, 200, 25)


        remove_brackets_label = QLabel(self)
        remove_brackets_label.setText("Удалить квадратные скобки и их содержимое")
        remove_brackets_label.move(10, 220)
        remove_brackets_label.adjustSize()
        self.remove_brackets_checkbox = QCheckBox(self)
        self.remove_brackets_checkbox.setGeometry(10, 240, 400, 25)

        process_button = QPushButton('Обработать текст', self)
        process_button.setGeometry(240, 270, 150, 40)
        process_button.clicked.connect(self.process_text)

        self.status_label = QLabel(self)
        self.status_label.setGeometry(10, 310, 470, 20) # Аргументы 10 и 310 определяют положение виджета по оси X и Y соответственно. Аргументы 470 и 20 определяют ширину и высоту виджета соответственно.

        self.setGeometry(100, 100, 490, 350) # В данном случае, первое число 100 - это позиция окна по оси X, второе число 100 - позиция окна по оси Y, третье число 490 - ширина окна, четвертое число 350 - высота окна
        self.setWindowTitle('Обработка текста')
        self.show()

    def browse_input_file(self):
        input_filename, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Text files (*.txt)")
        self.input_entry.setText(input_filename)

    def browse_output_file(self):
        output_filename, _ = QFileDialog.getSaveFileName(self, "Сохранить как", "", "Text files (*.txt)")
        self.output_entry.setText(output_filename)

    def save_to_file(self, sentences, output_filename):
        with open(output_filename, "w", encoding="utf-8") as output_file:
            for sentence in sentences:
                if sentence.strip():
                    cleaned_sentence = ' '.join(sentence.split())
                    output_file.write(cleaned_sentence + '\n')

    def process_file(self, input_filename, output_filename, remove_chars, remove_spaces, remove_brackets):
        with open(input_filename, "r", encoding="utf-8") as input_file:
            text = input_file.read()

        for char in remove_chars:
            text = text.replace(char, " ")

        if remove_brackets:
            text = re.sub(r"\[.*?\]", "", text)

        if remove_spaces:
            text = re.sub(r"\s+", " ", text.strip())

        text = text.replace("\n", " ")

        sentences = re.split(r"([.?!]+(?:\s+(?!\.{1,2}$)|(?<=\S)[\.]))\s+", text)

        cleaned_sentences = []
        for i in range(len(sentences)):
            if sentences[i].strip() and i > 0 and re.match(r"\.{1}$", sentences[i - 1]):
                cleaned_sentences[-1] += " " + sentences[i]
            else:
                cleaned_sentences.append(sentences[i])

        self.save_to_file(cleaned_sentences, output_filename)

    def process_text(self):
        input_filename = self.input_entry.text()
        output_filename = self.output_entry.text()
        remove_chars = self.remove_chars_entry.text()
        remove_spaces = self.remove_spaces_checkbox.isChecked()
        remove_brackets = self.remove_brackets_checkbox.isChecked()

        if not input_filename or not output_filename:
            QMessageBox.warning(self, "Ошибка", "Выберите входной и выходной файлы")
            return

        try:
            self.process_file(input_filename, output_filename, remove_chars, remove_spaces, remove_brackets)
            self.status_label.setText("Текст обработан.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", "Произошла ошибка при обработке текста: {}".format(str(e)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
