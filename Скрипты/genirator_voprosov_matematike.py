import random

# Генерация математического вопроса и ответа
def generate_question_and_answer():
    num1 = random.randint(-150, 150)
    num2 = 0
    while num2 == 0:
        num2 = random.randint(-150, 150)
    operator = random.choice(['+', '-', '*', '/'])
    question = f"{num1} {operator} {num2} ="
    if operator == '+':
        answer = num1 + num2
    elif operator == '-':
        answer = num1 - num2
    elif operator == '*':
        answer = num1 * num2
    else:
        answer = num1 / num2
    return question, str(answer)

# Создание текстового документа с вопросами и ответами
def create_question_file(num_questions, file_path):
    with open(file_path, 'w') as file:
        for _ in range(num_questions):
            question, answer = generate_question_and_answer()
            file.write(question + '\n')
            file.write(answer + '\n')

# Пример использования
num_questions = 100000  # Количество вопросов
file_path = r'D:\matematika\math_questions.txt'  # Путь к файлу (используйте 'r' перед строкой для обработки слэшей)

create_question_file(num_questions, file_path)
print(f"Сгенерированные вопросы и ответы сохранены в файл '{file_path}'.")
