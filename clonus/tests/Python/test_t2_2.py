import math

#Функция факториала
def factorial(number):
    if number <= 0:
        return 1
    return number * factorial(number-1)

#Функция квадратного корня
def m_sqrt(number):
    return math.sqrt(number)


# Главная функция
def main():
    
    num = int(input("Введите число: "))
    a1 =  int(input("Введите число: "))
    b =  int(input("Введите число: "))

    # Главная функция
    # Главная функция
    # Главная функция
    # Главная функция
    # Главная функция
    a1=m_sqrt(a1)
    b += b

    result = factorial(num)
    print("Факториал числа", num, "равен", result)
    print(a1+b)


# Вызов главной функции
main()