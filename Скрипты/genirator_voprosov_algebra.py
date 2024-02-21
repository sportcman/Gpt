import random

# Генерация вопроса и ответа по алгебре
def generate_question_and_answer():
    a = random.randint(-150, 150)
    b = random.randint(-150, 150)
    c = random.randint(-150, 150)
    operator1 = random.choice(['+', '-'])
    operator2 = random.choice(['*', '/'])
    question = f"{a}x{operator1}{b}={c}{operator2}x"

    right_side = None  # Инициализируем переменную right_side

    if operator1 == '+':
        left_side = a + b
    else:
        left_side = a - b
    
    if operator2 == '*':
        right_side = c * left_side
    else:
        if left_side != 0:  
            right_side = c / left_side

    if right_side is None:
        right_side = 0  # Устанавливаем значение по умолчанию, если right_side не был инициализирован

    answer = round(right_side, 2)
    return question, str(answer)

# Создание текстового документа с вопросами и ответами
def create_question_file(num_questions, file_path):
    with open(file_path, 'w') as file:
        for _ in range(num_questions):
            question, answer = generate_question_and_answer()
            file.write(question + '\n')
            file.write(answer + '\n')

# Пример использования
num_questions = 100000
file_path = r'D:\matematika\algebra_questions.txt'

create_question_file(num_questions, file_path)
print(f"Сгенерированные вопросы и ответы сохранены в файл '{file_path}'.")
