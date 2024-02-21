import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit
from PyQt6.QtCore import Qt
from bs4 import BeautifulSoup


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Конвертер FB2 в TXT")
        self.setGeometry(100, 500, 300, 50)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.convert_button = QPushButton("Конвертировать")

        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.convert_button)

        self.central_widget.setLayout(self.layout)

        self.convert_button.clicked.connect(self.convert_file)

    def convert_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Выберите файл FB2", "", "FB2 Файлы (*.fb2)")

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    soup = BeautifulSoup(file, "xml")
                    text = soup.get_text()

                save_dialog = QFileDialog()
                save_path, _ = save_dialog.getSaveFileName(self, "Сохранить как TXT", "", "TXT Файлы (*.txt)")

                if save_path:
                    with open(save_path, "w", encoding="utf-8") as save_file:
                        save_file.write(text)

                    self.text_edit.clear()
                    self.text_edit.append("Конвертация завершена!")
            except Exception as e:
                self.text_edit.clear()
                self.text_edit.append(f"Ошибка: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
