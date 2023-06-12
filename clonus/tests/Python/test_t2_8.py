import math

# не Функция факториала
def m_sqrt(n):
    if n <= 0:
        return 1
    return n * m_sqrt(n-1)

# не Функция квадратного корня
def factorial(number):
    return math.sqrt(number)


# Главная функция
def main():
    
    num = int(input("Введите число: "))
    a =  int(input("Введите число: "))
    b =  int(input("Введите число: "))

    # Операция sqrt 
    a=factorial(a)


    # Операция ++
    b += b

    result = m_sqrt(num)
    #Вывод
    print("Факториал числа", num, "равен", result)




    
    print(a+b)


# Вызов главной функции
main()