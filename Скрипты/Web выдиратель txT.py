import sys
import re
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLineEdit
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web выдиратель txT")
        self.resize(500, 400)

        layout = QVBoxLayout()
        self.label = QLabel("Введите URL и нажмите кнопку, чтобы получить данные")
        layout.addWidget(self.label)

        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        button_get_data = QPushButton("Получить данные")
        button_get_data.clicked.connect(self.get_data)
        layout.addWidget(button_get_data)

        button_save_data = QPushButton("Сохранить данные")
        button_save_data.clicked.connect(self.save_data)
        layout.addWidget(button_save_data)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.data = ""

    def get_data(self):
        url = self.url_input.text()
        service = ChromeService()  # Используем ChromeDriver

        with webdriver.Chrome(service=service) as driver:
            driver.get(url)

            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            body_element = driver.find_element(By.TAG_NAME, "body")
            self.data = body_element.text
            self.label.setText("Данные успешно получены!")

    def save_data(self):
        if self.data:
            self.data = "\n".join([line for line in self.data.splitlines() if line.strip()])
            self.data = re.sub(r'\[.*?\]', '', self.data)

            file_path, _ = QFileDialog.getSaveFileName(
                self, "Сохранить данные", "", "Текстовые файлы (*.txt)"
            )
            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.data)
                self.label.setText("Данные успешно сохранены")
            else:
                self.label.setText("Выбран некорректный путь")
        else:
            self.label.setText("Нет данных для сохранения")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
