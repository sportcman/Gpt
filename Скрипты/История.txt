# Английский алфавит
english_alphabet = [chr(i) for i in range(ord('A'), ord('Z')+1)] + [chr(i) for i in range(ord('a'), ord('z')+1)]

# Русский алфавит
russian_alphabet = [chr(i) for i in range(ord('А'), ord('Я')+1)] + [chr(i) for i in range(ord('а'), ord('я')+1)]

with open('alphabet.txt', 'w') as file:
    file.write('\n'.join(english_alphabet) + '\n')
    file.write('\n'.join(russian_alphabet) + '\n')
