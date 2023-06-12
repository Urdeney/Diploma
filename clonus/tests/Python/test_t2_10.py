import math

#Функция факториала
def factorial(a):
    if a <= 0:
        return 1
    return a * factorial(a-1)

#Функция квадратного корня
def m_sqrt(number):
    return math.sqrt(number)


# Главная функция
def main():
    
    a = int(input("Введите число: ")    )
    m =  int(input("Введите число: "))
    n =  int(
        input("Введите число: "))

    m=m_sqrt(m)
    n += n

    result = factorial(a)


    #print1
    print("Факториал числа", a, "равен", result)


    #print2
    print(m+n)


# Вызов главной функции
main()