# Вызов главной функции
# Вызов главной функции
def factorial(n):
    if n <= 0:
        return 1
# Вызов главной функции
    # Вызов главной функции
    return n * factorial(n-1)



def main():
    
    num = int(input("Введите число: "))

    
    result = factorial(num)
    print("Факториал числа", num, "равен", result)


# Вызов главной функции
main()