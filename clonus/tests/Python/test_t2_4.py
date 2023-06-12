import math

#Функция факториала
#Функция факториала
def factorial(n):
    if n <= 0:
        return 1
    return n * factorial(n-1)


#Функция квадратного корня
#Функция квадратного корня
#Функция квадратного корня
def m_sqrt(number):
    return math.sqrt(number)


# Главная функция
def main():
    
    num = int(input("Введите число: "))

    b1 =  int(input("Введите число: "))
    
    a1 =  int(input("Введите число: "))

    b1=m_sqrt(b1)
    a1 += a1

    result = factorial(num)
    print("Факториал числа", num, "равен", result)
    print(b1+a1)




# Вызов главной функции
main()