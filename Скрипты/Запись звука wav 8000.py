import sys
import sounddevice as sd
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from scipy.io.wavfile import write
import numpy as np

class AudioRecorder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.recording = False
        self.fs = 8000  # Sample rate
        self.recorded_data = []

    def initUI(self):
        self.setWindowTitle('Диктофон')
        self.setGeometry(100, 100, 200, 100)

        layout = QVBoxLayout()
        self.btn_record = QPushButton('Запись', self)
        self.btn_record.clicked.connect(self.toggle_recording)
        layout.addWidget(self.btn_record)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def toggle_recording(self):
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.recorded_data = []
        self.recording = True
        self.btn_record.setText('Стоп')
        print("Запись началась...")
        # Начинаем асинхронную запись
        self.stream = sd.InputStream(callback=self.audio_callback, samplerate=self.fs, channels=1, dtype='int16')
        self.stream.start()

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.btn_record.setText('Запись')
            print("Запись остановлена...")
            self.stream.stop()
            self.save_recording()

    def audio_callback(self, indata, frames, time, status):
        self.recorded_data.append(indata.copy())

    def save_recording(self):
        if self.recorded_data:
            recording_array = np.concatenate(self.recorded_data, axis=0)
            write('output.wav', self.fs, recording_array)
            print("Аудио сохранено как output.wav")

def main():
    app = QApplication(sys.argv)
    ex = AudioRecorder()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
