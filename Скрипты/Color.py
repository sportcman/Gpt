from PyQt6.QtWidgets import QApplication, QColorDialog, QPushButton

class CustomColorDialog(QColorDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.copy_button = QPushButton('Копировать', self)
        self.copy_button.clicked.connect(self.copyColor)
        self.layout().addWidget(self.copy_button)

    def copyColor(self):
        selected_color = self.currentColor()
        QApplication.clipboard().setText(selected_color.name())
        print(f"Цвет {selected_color.name()} скопирован в буфер обмена.")

if __name__ == '__main__':
    app = QApplication([])

    color_dialog = CustomColorDialog()
    color_dialog.exec()

    app.exec()
