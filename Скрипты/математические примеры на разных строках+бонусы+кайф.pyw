import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit, QFileDialog, QHBoxLayout, QSpinBox, QCheckBox


class MathProblemGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Генератор математических примеров")
        self.setGeometry(200, 200, 500, 400)
        self.layout = QVBoxLayout()

        self.problem_label = QLabel("Задача:")
        self.layout.addWidget(self.problem_label)

        self.answer_label = QLabel("")
        self.layout.addWidget(self.answer_label)

        self.include_answer_checkbox = QCheckBox("Включить ответ на той же строке что и пример")
        self.layout.addWidget(self.include_answer_checkbox)

        self.spin_box_layout = QHBoxLayout()
        self.spin_box_layout.addWidget(QLabel("Количество примеров:"))
        self.spin_box = QSpinBox()
        self.spin_box.setRange(1, 100000)
        self.spin_box.setValue(1)
        self.spin_box_layout.addWidget(self.spin_box)
        self.layout.addLayout(self.spin_box_layout)

        self.generate_button = QPushButton("Сгенерировать пример(ы)")
        self.generate_button.clicked.connect(self.generate_problems)
        self.layout.addWidget(self.generate_button)

        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear_problems)
        self.layout.addWidget(self.clear_button)

        self.save_button = QPushButton("Сохранить в файл")
        self.save_button.clicked.connect(self.save_to_file)
        self.layout.addWidget(self.save_button)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)

        self.setLayout(self.layout)
        self.generated_problems = []

    def generate_problems(self):
        operators = ["+", "-", "*", "/"]
        count = self.spin_box.value()
        include_answer_on_same_line = self.include_answer_checkbox.isChecked()

        for i in range(count):
            operator = random.choice(operators)

            if operator == "+" or operator == "-":
                a = random.randint(1, 100)
                b = random.randint(1, 100)
                problem = f"{a} {operator} {b}"
                answer = str(eval(problem))

                if include_answer_on_same_line:
                    problem += " = " + answer
                    self.generated_problems.append(problem)
                else:
                    problem += " ="
                    self.generated_problems.append(problem)
                    self.generated_problems.append(answer)

            elif operator == "*":
                a = random.randint(1, 20)
                b = random.randint(1, 10)
                problem = f"{a} {operator} {b}"
                answer = str(eval(problem))

                if include_answer_on_same_line:
                    problem += " = " + answer
                    self.generated_problems.append(problem)
                else:
                    problem += " ="
                    self.generated_problems.append(problem)
                    self.generated_problems.append(answer)

            elif operator == "/":
                a = random.randint(1, 100)
                b = random.randint(1, 10)
                a = a * b
                problem = f"{a} {operator} {b}"
                answer = str(eval(problem))

                if include_answer_on_same_line:
                    problem += " = " + answer
                    self.generated_problems.append(problem)
                else:
                    problem += " ="
                    self.generated_problems.append(problem)
                    self.generated_problems.append(answer)

        # Обновление текстового поля с примерами и ответами
        self.text_edit.setPlainText("\n".join(self.generated_problems))

        # Обновление метки с текущим примером и ответом
        current_problem_index = -1 if include_answer_on_same_line else -2
        if current_problem_index >= 0 and current_problem_index < len(self.generated_problems):
            current_problem = self.generated_problems[current_problem_index]
            self.problem_label.setText(f"Задача: {current_problem}")

        if include_answer_on_same_line:
            self.answer_label.setText("")

    def clear_problems(self):
        self.generated_problems = []
        self.problem_label.setText("Задача:")
        self.answer_label.setText("")
        self.text_edit.setPlainText("")

    def save_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Текстовые файлы (*.txt)")

        if file_path:
            with open(file_path, "w") as f:
                f.write("\n".join(self.generated_problems))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    generator = MathProblemGenerator()
    generator.show()

    sys.exit(app.exec_())
