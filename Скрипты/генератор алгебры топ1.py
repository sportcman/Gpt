import random
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QLineEdit, QMessageBox

def evaluate_equation(equation, x, y, z):
    try:
        return eval(equation)
    except ZeroDivisionError:
        return None

def generate_equation():
    operators = ['+', '-', '*', '/']
    operator = random.choice(operators)

    if operator == '/':
        divisor = random.randint(1, 5000)
        dividend = divisor * random.randint(1, 5000)
        equation = f"({dividend}{operator}{divisor})"
    else:
        operands = ['x', 'y', 'z']
        operand1 = random.choice(operands)
        operand2 = random.choice(operands)

        if random.random() < 0.00005:
            equation = f"({operand1}{operator}{operand2})"
        else:
            inner_equation = generate_equation()
            equation = f"{operand1}{operator}{inner_equation}"

    return equation

class ExampleGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генератор примеров")
        self.setGeometry(100, 100, 400, 200)

        self.num_examples_label = QLabel("Количество примеров:", self)
        self.num_examples_label.setGeometry(20, 20, 150, 30)

        self.num_examples_input = QLineEdit(self)
        self.num_examples_input.setGeometry(160, 20, 150, 30)

        self.generate_button = QPushButton("Сгенерировать примеры", self)
        self.generate_button.setGeometry(20, 70, 300, 30)
        self.generate_button.clicked.connect(self.generate_examples)

    def generate_examples(self):
        num_examples = self.num_examples_input.text()
        if not num_examples.isdigit() or int(num_examples) <= 0:
            QMessageBox.critical(self, "Ошибка", "Введите положительное целое число.")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Выберите файл для сохранения", "", "TXT файлы (*.txt)")
        if not save_path:
            return

        with open(save_path, 'w') as file:
            for _ in range(int(num_examples)):
                x, y, z = random.randint(1, 5000), random.randint(1, 5000), random.randint(1, 5000)
                equation = generate_equation()
                answer = evaluate_equation(equation, x, y, z)
                if answer is not None:
                    example_str = f"{equation}={answer}  (x={x}, y={y}, z={z})"
                    file.write(example_str + '\n')

        QMessageBox.information(self, "Готово", f"Примеры сохранены в файл: {save_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExampleGeneratorApp()
    ex.show()
    sys.exit(app.exec())
