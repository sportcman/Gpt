import sys
import asyncio
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from gtts import gTTS
import os
import pygame

class TextToSpeechThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, text, filename):
        super().__init__()
        self.text = text
        self.filename = filename

    def run(self):
        tts = gTTS(text=self.text, lang='ru')
        tts.save(self.filename)
        pygame.mixer.init()
        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play()
        self.finished.emit("Успешно создан.")

class GPT2Generator:
    def __init__(self, model_path):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        self.model = GPT2LMHeadModel.from_pretrained(model_path)

    def generate_text(self, input_text, temperature_value, length_value, num_results, no_repeat_ngram_size):
        input_ids = self.tokenizer.encode(input_text, return_tensors='pt')
        attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=input_ids.device)

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
            result_text += f"\n{generated_text}\n"
        return result_text

class MainWindow(QMainWindow):
    def __init__(self, gpt2_generator):
        super().__init__()
        self.gpt2_generator = gpt2_generator
        self.setWindowTitle("GPT-2 Audio")
        self.setGeometry(100, 100, 360, 170)

        self.initUI()

    def initUI(self):
        self.text_label = QLabel("Вопрос:", self)
        self.text_label.move(5, 20)

        self.text_input = QLineEdit(self)
        self.text_input.move(110, 20)

        self.filename_label = QLabel("Сохранить файл:", self)
        self.filename_label.move(5, 60)

        self.filename_input = QLineEdit(self)
        self.filename_input.move(110, 60)

        self.browse_button = QPushButton("Обзор", self)
        self.browse_button.move(220, 60)
        self.browse_button.clicked.connect(self.browse_file)

        self.convert_button = QPushButton("Ответить", self)
        self.convert_button.move(150, 100)
        self.convert_button.clicked.connect(self.convert_to_audio)

    def browse_file(self):
        dialog = QFileDialog(self)
        dialog.setDefaultSuffix(".mp3")
        dialog.setNameFilter("Audio files (*.mp3)")
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        if dialog.exec():
            selected_file = dialog.selectedFiles()[0]
            self.filename_input.setText(selected_file)

    def convert_to_audio(self):
        text = self.text_input.text()
        filename = self.filename_input.text()
        if text and filename:
            generated_text = self.gpt2_generator.generate_text(text, 0.3, 10, 1, 2)
            self.tts_thread = TextToSpeechThread(generated_text, filename)
            self.tts_thread.finished.connect(self.show_message_box)
            self.tts_thread.start()
        else:
            self.show_message_box("Ошибка", "Необходимо ввести текст и выбрать файл для сохранения.")

    def show_message_box(self, message):
        QMessageBox.information(self, "Ответ", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gpt2_generator = GPT2Generator("C://Users//GpT//Desktop//GPT//model")
    window = MainWindow(gpt2_generator)
    window.show()
    sys.exit(app.exec())
