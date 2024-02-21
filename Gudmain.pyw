import sys
import re
import torch
import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit,
    QVBoxLayout, QHBoxLayout, QSlider, QSpinBox, QFileDialog, QMessageBox
)
from transformers import GPT2LMHeadModel, GPT2Tokenizer


class GPT2Generator:
    def __init__(self, model_path):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        self.model = GPT2LMHeadModel.from_pretrained(model_path)

    def generate_text(
        self, input_text, temperature_value, length_value, num_results,
        no_repeat_ngram_size
    ):
        input_ids = self.tokenizer.encode(input_text, return_tensors='pt')
        attention_mask = torch.ones(
            input_ids.shape, dtype=torch.long, device=input_ids.device
        )

        outputs = self.model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=length_value,
            num_return_sequences=num_results,
            no_repeat_ngram_size=no_repeat_ngram_size,
            repetition_penalty=1.5,
            temperature=temperature_value,
            do_sample=True
        )

        result_text = ""
        for i, output in enumerate(outputs):
            generated_text = self.tokenizer.decode(output, skip_special_tokens=True)
            if i == 0:
                generated_text = generated_text.replace(input_text, "")

            lexer = get_lexer_by_name("python", stripall=True)
            formatter = HtmlFormatter(linenos=False, cssclass="code")
            highlighted_code = pygments.highlight(generated_text, lexer, formatter)
            generated_text = re.sub(r'(?<=[.])(?=[^\s])', '\n', generated_text)
            result_text += f"<style>{formatter.get_style_defs('.code')}</style>"
            result_text += f"<pre>{highlighted_code}</pre>\n\n"

        return result_text


class GPT2App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.model_path = "C://Users//GpT//Desktop//GPT//model"
        self.temperature_value = 0.1 

    def initUI(self):
        self.setWindowTitle('Генератор ответов.')
        self.resize(800, 800) 

        self.input_label = QLabel('Введите вопрос:')
        self.input_text = QLineEdit()

        self.temperature_label = QLabel('Температура от 0.1 до 10.0:')
        self.temperature_slider = QSlider(Qt.Orientation.Horizontal)
        self.temperature_slider.setMinimum(1)
        self.temperature_slider.setMaximum(100)
        self.temperature_slider.setValue(1)
        self.temperature_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.temperature_slider.setTickInterval(10)
        self.temperature_display = QLabel('0.01')

        self.length_label = QLabel('Длина текста до 2048 символов:')
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setMinimum(10)
        self.length_spinbox.setMaximum(2048)
        self.length_spinbox.setValue(64)

        self.num_results_label = QLabel('Количество вариантов от 1 до 100:')
        self.num_results_spinbox = QSpinBox()
        self.num_results_spinbox.setMinimum(1)
        self.num_results_spinbox.setMaximum(100)
        self.num_results_spinbox.setValue(1)

        self.generate_button = QPushButton('Сгенерировать ответ.')
        self.generate_button.clicked.connect(self.generateText)

        vbox = QVBoxLayout()
        vbox.addWidget(self.input_label)
        vbox.addWidget(self.input_text)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.temperature_slider)
        vbox.addWidget(self.temperature_display)
        vbox.addWidget(self.length_label)
        vbox.addWidget(self.length_spinbox)
        vbox.addWidget(self.num_results_label)
        vbox.addWidget(self.generate_button)

        self.result_text = QTextEdit()
        vbox.addWidget(self.result_text)

        self.setLayout(vbox)
        self.show()

        self.temperature_slider.valueChanged.connect(self.updateTemperatureDisplay)

    def generateText(self):
        input_text = self.input_text.text()
        length_value = self.length_spinbox.value()
        num_results = self.num_results_spinbox.value()
        ngram_value = 2

        gpt2_generator = GPT2Generator(self.model_path)
        result_text = gpt2_generator.generate_text(
            input_text, self.temperature_value, length_value, num_results, ngram_value
        )
        self.result_text.setHtml(result_text)

    def updateTemperatureDisplay(self, value):
        self.temperature_value = value / 10.0
        self.temperature_display.setText(str(self.temperature_value))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GPT2App()
    sys.exit(app.exec())
