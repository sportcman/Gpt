import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

class ImageConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ICO')
        self.setGeometry(300, 300, 300, 150)
        self.setStyleSheet("background-color: #f5f5f5;")

        self.layout = QVBoxLayout()

        self.label = QLabel(self)
        self.label.setStyleSheet("border: 2px solid black;")
        self.layout.addWidget(self.label)

        self.browse_button = QPushButton('Выбрать', self)
        self.browse_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;")
        self.browse_button.clicked.connect(self.browse_image)
        self.layout.addWidget(self.browse_button)

        self.convert_button = QPushButton('Конвертировать', self)
        self.convert_button.setStyleSheet("background-color: #008CBA; color: white; border-radius: 5px;")
        self.convert_button.clicked.connect(self.convert_image)
        self.layout.addWidget(self.convert_button)

        self.setLayout(self.layout)

    def browse_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select PNG Image')
        if file_path:
            pixmap = QPixmap(file_path)
            self.label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))

            self.png_image_path = file_path

    def convert_image(self):
        if hasattr(self, 'png_image_path'):
            ico_file_path, _ = QFileDialog.getSaveFileName(self, 'Save ICO File', '', 'ICO Files (*.ico)')
            if ico_file_path:
                image = Image.open(self.png_image_path)
                image.save(ico_file_path, format='ICO')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = ImageConverter()
    converter.show()
    sys.exit(app.exec_())
