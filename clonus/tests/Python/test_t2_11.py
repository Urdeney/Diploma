import math

#Функция факториала
def factorial(n):
    if n <= 0:
        return 1
    return n * factorial(n-1)

#Функция квадратного корня
def m_sqrt(number):
    return math.sqrt(number)


# Главная функция
def main():
    
    num = int(input("Введите число: "))
    a =  int(input("Введите число: "))
    b =  int(input("Введите число: "))

    a=m_sqrt(a)
    b += b

    result = factorial(num)
    print("Факториал числа", num, "равен", result)
    print("Сумма числа",a+b)
    # Главная функция
    # Главная функция
    # Главная функция
    # Главная функция
    # Главная функция
    # Главная функция
    # Главная функция
    #Закончилась


# Вызов главной функции
main()