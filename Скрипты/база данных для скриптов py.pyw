import os
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QWidget,
    QListWidget,
)


class ScriptManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scripts = []
        self.current_script = None
        self.script_text = ""
        self.directory = os.path.dirname(os.path.realpath(__file__))
        self.history_file = os.path.join(self.directory, "История.txt")

        self.init_ui()

    def init_ui(self):
        # Создаем окно
        self.setWindowTitle("Менеджер скриптов")

        # Создаем виджеты
        self.scripts_list = QListWidget()
        self.scripts_list.currentItemChanged.connect(self.script_selected)

        self.script_text_edit = QTextEdit()
        self.script_text_edit.setReadOnly(False)

        new_script_button = QPushButton("Новый скрипт")
        new_script_button.clicked.connect(self.new_script)

        save_script_button = QPushButton("Сохранить скрипт")
        save_script_button.clicked.connect(self.save_script)

        load_script_button = QPushButton("Загрузить скрипт")
        load_script_button.clicked.connect(self.load_script)

        delete_script_button = QPushButton("Удалить скрипт")
        delete_script_button.clicked.connect(self.delete_script)

        # Создаем вертикальный контейнер для кнопок
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(new_script_button)
        buttons_layout.addWidget(save_script_button)
        buttons_layout.addWidget(load_script_button)
        buttons_layout.addWidget(delete_script_button)

        # Создаем горизонтальный контейнер для виджетов скриптов
        scripts_layout = QHBoxLayout()
        scripts_layout.addWidget(self.scripts_list)
        scripts_layout.addWidget(self.script_text_edit)

        # Создаем вертикальный контейнер для всех виджетов
        main_layout = QVBoxLayout()
        main_layout.addLayout(scripts_layout)
        main_layout.addLayout(buttons_layout)

        # Устанавливаем главный виджет
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Загружаем скрипты из папки
        self.load_scripts()

    def load_scripts(self):
        self.scripts = []
        self.scripts_list.clear()
        for filename in os.listdir(self.directory):
            if filename.endswith(".py"):
                with open(os.path.join(self.directory, filename), "r", encoding="utf-8") as f:
                    text = f.read()
                self.scripts.append({"filename": filename, "text": text})
                self.scripts_list.addItem(os.path.basename(filename))

        # Загружаем историю из файла
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as f:
                history = f.read()
            self.script_text_edit.setPlainText(history)

    def script_selected(self, current_item, previous_item):
        # Сохраняем текущий скрипт
        if self.current_script:
            self.current_script["text"] = self.script_text_edit.toPlainText()

        # Загружаем выбранный скрипт
        if current_item:
            filename = current_item.text()
            for script in self.scripts:
                if os.path.basename(script["filename"]) == filename:
                    self.current_script = script
                    self.script_text_edit.setPlainText(script["text"])

    def new_script(self):
        # Сохраняем текущий скрипт
        if self.current_script:
            self.current_script["text"] = self.script_text_edit.toPlainText()

        # Создаем новый скрипт
        filename, _ = QFileDialog.getSaveFileName(self, "Создать новый скрипт", self.directory, "Python files (*.py)")
        if filename:
            self.current_script = {"filename": filename, "text": ""}
            self.scripts.append(self.current_script)
            self.scripts_list.addItem(os.path.basename(filename))
            self.script_text_edit.setPlainText("")

    def save_script(self):
        if self.current_script:
            with open(self.current_script["filename"], "w", encoding="utf-8") as f:
                f.write(self.script_text_edit.toPlainText())
                self.statusBar().showMessage("Скрипт сохранен.")

            # Сохраняем историю в файл
            with open(self.history_file, "w", encoding="utf-8") as f:
                f.write(self.script_text_edit.toPlainText())

    def load_script(self):
        # Сохраняем текущий скрипт
        if self.current_script:
            self.current_script["text"] = self.script_text_edit.toPlainText()

        # Загружаем скрипт
        filename, _ = QFileDialog.getOpenFileName(self, "Загрузить скрипт", self.directory, "Python files (*.py)")
        if filename:
            with open(filename, "r", encoding="utf-8") as f:
                text = f.read()
            self.current_script = {"filename": filename, "text": text}
            self.scripts.append(self.current_script)
            self.scripts_list.addItem(os.path.basename(filename))
            self.script_text_edit.setPlainText(text)

            # Сохраняем историю в файл
            with open(self.history_file, "w", encoding="utf-8") as f:
                f.write(text)

    def delete_script(self):
        if self.current_script:
            filename = self.current_script["filename"]
            self.scripts.remove(self.current_script)
            self.scripts_list.takeItem(self.scripts_list.currentIndex().row())

            if os.path.exists(filename):
                os.remove(filename)

            self.script_text_edit.setPlainText("")
            self.current_script = None

    def closeEvent(self, event):
        # Сохраняем текущий скрипт перед выходом
        if self.current_script:
            self.current_script["text"] = self.script_text_edit.toPlainText()
            self.save_script()

        super().closeEvent(event)

 # QT6 заменить
if __name__ == "__main__":
    app = QApplication([])
    manager = ScriptManager()
    manager.show()
    app.exec()

