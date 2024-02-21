with open('numbers.txt', 'w') as file:
    for i in range(50001):
        file.write(str(i) + '\n')