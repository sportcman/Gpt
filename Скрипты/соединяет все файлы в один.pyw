import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTextEdit, QPushButton, QVBoxLayout, QWidget


class TextMerger(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Слияние текста")
        
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("font-size: 16px;")
        
        self.button_select = QPushButton("Выбрать файлы")
        self.button_select.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                padding: 10px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
            }
            
            QPushButton:hover {
                background-color: #2980b9;
            }
            """
        )
        self.button_select.clicked.connect(self.select_files)
        
        self.button_merge = QPushButton("Объединить файлы")
        self.button_merge.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                padding: 10px;
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 5px;
            }
            
            QPushButton:hover {
                background-color: #27ae60;
            }
            """
        )
        self.button_merge.clicked.connect(self.merge_files)
        
        self.button_save = QPushButton("Сохранить файл")
        self.button_save.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                padding: 10px;
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
            }
            
            QPushButton:hover {
                background-color: #c0392b;
            }
            """
        )
        self.button_save.clicked.connect(self.save_file)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.button_select)
        layout.addWidget(self.button_merge)
        layout.addWidget(self.button_save)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def select_files(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            self.files = filenames

    def merge_files(self):
        text = ""
        for file in self.files:
            with open(file, "r", encoding="utf-8") as f:
                text += f.read()
        
        self.text_edit.setPlainText(text)

    def save_file(self):
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setDefaultSuffix("txt")
        if file_dialog.exec_():
            filename = file_dialog.selectedFiles()[0]
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.text_edit.toPlainText())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextMerger()
    window.show()
    sys.exit(app.exec_())
