import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QMessageBox
import yt_dlp
import ffmpeg

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube загрузка аудио stereo mono')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.url_line_edit = QLineEdit(self)
        self.url_line_edit.setPlaceholderText("Вставьте ссылку на YouTube видео или плейлист здесь...")
        layout.addWidget(self.url_line_edit)

        self.download_button = QPushButton('Выбрать папку и сохранить', self)
        self.download_button.clicked.connect(self.download_audio)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def download_audio(self):
        url = self.url_line_edit.text()
        if not url:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, введите URL видео или плейлиста.')
            return

        save_directory = QFileDialog.getExistingDirectory(self, 'Выбрать папку для сохранения')
        if not save_directory:
            return

        try:
            # Загрузка аудио с использованием yt-dlp
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': save_directory + '/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '192'
                }],
                'progress_hooks': [self.post_download],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))

    def post_download(self, d):
        if d['status'] == 'finished':
            file_path = d['filename']
            output_path = file_path.rsplit('.', 1)[0] + '_mono.wav'  # Исправлено для создания уникального имени файла
            self.convert_to_mono(file_path, output_path)

    def convert_to_mono(self, input_file, output_file):
        try:
            (
                ffmpeg
                .input(input_file)
                .output(output_file, ac=1)  # ac=1 устанавливает количество аудиоканалов равным 1, что соответствует моно
                .global_args('-y')  # Автоматически подтверждаем перезапись файла
                .run()
            )
            QMessageBox.information(self, 'Преобразование завершено', f'Файл {output_file} был успешно сохранен в моно.')
        except ffmpeg.Error as e:
            QMessageBox.critical(self, 'Ошибка при преобразовании', f'Произошла ошибка при преобразовании файла: {e.stderr}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YouTubeDownloader()
    ex.show()
    sys.exit(app.exec())
