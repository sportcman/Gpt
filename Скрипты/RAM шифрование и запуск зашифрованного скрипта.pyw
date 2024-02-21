import os
import subprocess
import io
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox

class EncryptionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Шифрование файлов')
        self.layout = QVBoxLayout()

        self.file_label = QLabel('Выберите файл для шифрования/расшифрования:')
        self.file_line_edit = QLineEdit()
        self.file_button = QPushButton('Обзор')
        self.file_button.clicked.connect(self.browse_file)

        self.key_label = QLabel('Введите ключ шифрования:')
        self.key_line_edit = QLineEdit()

        self.encrypt_button = QPushButton('Зашифровать')
        self.encrypt_button.clicked.connect(self.encrypt_file)

        self.decrypt_button = QPushButton('Расшифровать и запустить')
        self.decrypt_button.clicked.connect(self.decrypt_and_execute_file)

        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.file_line_edit)
        self.layout.addWidget(self.file_button)
        self.layout.addWidget(self.key_label)
        self.layout.addWidget(self.key_line_edit)
        self.layout.addWidget(self.encrypt_button)
        self.layout.addWidget(self.decrypt_button)

        self.setLayout(self.layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл')
        self.file_line_edit.setText(file_path)

    def encrypt_file(self):
        file_path = self.file_line_edit.text()
        if not os.path.isfile(file_path):
            QMessageBox.warning(self, 'Ошибка', 'Файл не найден.')
            return

        key = self.key_line_edit.text().encode()
        if len(key) != 44:
            QMessageBox.warning(self, 'Ошибка', 'Неправильная длина ключа шифрования.')
            return

        cipher_suite = Fernet(key)

        with open(file_path, 'rb') as file:
            original_data = file.read()

        encrypted_data = cipher_suite.encrypt(original_data)

        encrypted_file_path = os.path.splitext(file_path)[0] + '.enc'
        with open(encrypted_file_path, 'wb') as file:
            file.write(encrypted_data)

        QMessageBox.information(self, 'Успех', f'Файл успешно зашифрован и сохранен в {encrypted_file_path}')

    def decrypt_and_execute_file(self):
        file_path = self.file_line_edit.text()
        if not os.path.isfile(file_path):
            QMessageBox.warning(self, 'Ошибка', 'Файл не найден.')
            return

        key = self.key_line_edit.text().encode()
        if len(key) != 44:
            QMessageBox.warning(self, 'Ошибка', 'Неправильная длина ключа шифрования.')
            return

        cipher_suite = Fernet(key)

        with open(file_path, 'rb') as file:
            encrypted_data = file.read()

        try:
            decrypted_data = cipher_suite.decrypt(encrypted_data)
        except:
            QMessageBox.warning(self, 'Ошибка', 'Неверный ключ шифрования или файл поврежден.')
            return

        temp_file = io.BytesIO(decrypted_data)

        subprocess.run(['python'], input=temp_file.getvalue())

    def closeEvent(self, event):
        # Удаляем временный файл при закрытии программы
        file_path = self.file_line_edit.text()
        if file_path.endswith('.enc'):
            temp_file_path = file_path + '.dec'
            if os.path.isfile(temp_file_path):
                os.remove(temp_file_path)
        event.accept()

if __name__ == '__main__':
    app = QApplication([])
    encryption_app = EncryptionApp()
    encryption_app.show()
    app.exec_()
