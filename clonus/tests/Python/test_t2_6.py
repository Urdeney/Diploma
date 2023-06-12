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
    
    # Ввод 1
    num = int(input("Введите число: "))



    # Ввод 2
    a =  int(input("Введите число: "))


    # Ввод 3
    b_124 =  int(input("Введите число: "))

    a=m_sqrt(a)
    b_124 += b_124

    result = factorial(num)



    print("Факториал числа", num, "равен", result)



    
    print(a+b_124)


# Вызов главной функции
main()