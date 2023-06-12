import math

#Функция факториала
def factorial(n):
    if n <= 0:
        return 1
    return n * factorial(n-1)

#Функция квадратного корня
def sqrt_m(number):
    return math.sqrt(number)


# Главная функция
def main():
    
    a_num = int(input("Введите число: "))
    a_num =  int(input("Введите число: "))
    b_num =  int(input("Введите число: "))

    a_num=sqrt_m(a_num)
    b_num += b_num

    result = factorial(a_num)
    print("Факториал числа", a_num, "равен", result)
    print(a_num+b_num)
    # Главная функция
    # Главная функция
    # Главная функция
    # Главная функция
    # Главная функция
    # Главная функция

# Вызов главной функции
main()