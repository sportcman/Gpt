import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPlainTextEdit, QPushButton, QMessageBox, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class SentenceExtractor(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        # Создаем label и plain text edit для отображения текста и результата
        self.input_label = QLabel('Введите текст:')
        self.input_text = QPlainTextEdit()
        self.output_label = QLabel('Результат:')
        self.output_text = QPlainTextEdit()
        self.output_text.setReadOnly(True)
        
        # Создаем кнопку для запуска процесса извлечения предложений
        self.extract_button = QPushButton('Извлечь предложения')
        self.extract_button.clicked.connect(self.extractSentences)
        
        # Создаем кнопку для сохранения результата в файл
        self.save_button = QPushButton('Сохранить результат')
        self.save_button.clicked.connect(self.saveResult)
        
        # Создаем layout и добавляем элементы на форму
        vbox = QVBoxLayout()
        vbox.addWidget(self.input_label)
        vbox.addWidget(self.input_text)
        vbox.addWidget(self.output_label)
        vbox.addWidget(self.output_text)
        vbox.addWidget(self.extract_button)
        vbox.addWidget(self.save_button)
        self.setLayout(vbox)
        
        # Устанавливаем заголовок окна, размеры и отображаем его
        self.setWindowTitle('Извлечение предложений')
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(100, 100, 500, 500)
        self.show()
        
    def extractSentences(self):
        # Получаем текст из plain text edit
        text = self.input_text.toPlainText()
        
        # Разделяем текст на предложения
        sentences = text.split('.')
        
        # Очищаем результат от пробелов и пустых строк
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Преобразуем список предложений в одну строку с разделителями
        result = '\n'.join(sentences)
        
        # Выводим результат в output text edit
        self.output_text.setPlainText(result)
        
    def saveResult(self):
        # Открываем диалог для выбора файла для сохранения
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self,"Сохранить файл", "","Text Files (*.txt)", options=options)
        
        # Если пользователь выбрал файл - сохраняем результат в него
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.output_text.toPlainText())
                    QMessageBox.information(self, 'Успешно', 'Результат сохранен в файл')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SentenceExtractor()
    sys.exit(app.exec_())
