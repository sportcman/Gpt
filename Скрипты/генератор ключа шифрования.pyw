import os
from cryptography.fernet import Fernet
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
import pyperclip


class KeyGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Генератор ключей шифрования')
        self.layout = QVBoxLayout()

        self.key_label = QLabel('Сгенерированный ключ:')
        self.key_label.setWordWrap(True)

        self.generate_button = QPushButton('Сгенерировать ключ')
        self.generate_button.clicked.connect(self.generate_key)

        self.copy_button = QPushButton('Скопировать ключ')
        self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(self.copy_key)

        self.layout.addWidget(self.key_label)
        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.copy_button)

        self.setLayout(self.layout)

    def generate_key(self):
        key = Fernet.generate_key()
        key_base64 = key.decode()
        self.key_label.setText(f'Сгенерированный ключ:\n{key_base64}')
        self.copy_button.setEnabled(True)
        QMessageBox.information(self, 'Успех', 'Ключ шифрования успешно сгенерирован и отображен.')

    def copy_key(self):
        key = self.key_label.text().split('\n')[1]
        pyperclip.copy(key)
        QMessageBox.information(self, 'Успех', 'Ключ шифрования успешно скопирован в буфер обмена.')


if __name__ == '__main__':
    app = QApplication([])
    key_generator_app = KeyGeneratorApp()
    key_generator_app.show()
    app.exec()
