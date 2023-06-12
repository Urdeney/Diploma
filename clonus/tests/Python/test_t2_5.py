

import math
def factorial(n):
    if n <= 0:
        return 1
    return n * factorial(n-1)
def m_sqrt(number):
    return math.sqrt(number)


def main():
    
    number = int(input("Введите число: "))
    a =  int(input("Введите число: "))
    b =  int(input("Введите число: "))
    a=m_sqrt(a)
    b += b
    res = factorial(number)
    print("Факториал числа", number, "равен", res)
    print(a+b)


# Вызов главной функции
main()