# Это программа для вычисления факториала числа

def factorial(n):
    if n <= 0:
        return 1

    # Рекурсивное вычисление факториала
    return n * factorial(n-1)


# Главная функция
def main():
    # Ввод числа от пользователя
    num = int(input("Введите число: "))

    # Вызов функции factorial и вывод результата
    result = factorial(num)
    print("Факториал числа", num, "равен", result)


# Вызов главной функции
main()