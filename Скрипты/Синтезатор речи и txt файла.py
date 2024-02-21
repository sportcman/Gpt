import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel
import pyttsx3
import threading

class TextToSpeechGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        # Инициализация движка синтеза речи
        self.engine = pyttsx3.init()
        # Установка языка речи
        voices = self.engine.getProperty('voices')
        for voice in voices:
            # Проверяем, не пуст ли список languages
            if voice.languages:
                # Проверяем наличие подстроки 'ru' с учетом возможного формата байтовой строки
                if any('ru' in lang.decode() if isinstance(lang, bytes) else 'ru' in lang for lang in voice.languages):
                    self.engine.setProperty('voice', voice.id)
                    break

        # Флаги состояния воспроизведения
        self.isPlaying = False
        self.isPaused = False

    def initUI(self):
        self.setWindowTitle("Текст в Речь")
        self.setGeometry(0, 0, 100, 100)

        self.setStyleSheet("background-color: #f0f0f0;")

        layout = QVBoxLayout()

        self.label = QLabel("Выберите текстовый файл", self)
        self.label.setStyleSheet("font-size: 11px;")
        layout.addWidget(self.label)

        self.btnOpenFile = QPushButton("Открыть файл", self)
        self.btnOpenFile.setStyleSheet("background-color: #008577; color: white; font-weight: bold;")
        self.btnOpenFile.clicked.connect(self.openFileDialog)
        layout.addWidget(self.btnOpenFile)

        self.btnStart = QPushButton("Старт", self)
        self.btnStart.setStyleSheet("background-color: #0057d8; color: white; font-weight: bold;")
        self.btnStart.clicked.connect(self.startReading)
        layout.addWidget(self.btnStart)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def openFileDialog(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Text Files (*.txt)")
        if filePath:
            self.filePath = filePath
            self.label.setText(f"Файл: {filePath}")

    def readText(self):
        with open(self.filePath, 'r', encoding='utf-8') as file:
            text = file.read()
            self.engine.say(text)
            self.engine.runAndWait()

    def startReading(self):
        if not self.isPlaying:
            self.isPlaying = True
            self.thread = threading.Thread(target=self.readText)
            self.thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = TextToSpeechGUI()
    mainWin.show()
    sys.exit(app.exec())
