

def factorial(n):
    if n <= 0:
        return 1

    
    return n * factorial(n-1)



def main():
    
    num = int(
        input("Введите число: "))

    
    result = factorial(num)
    print("Факториал числа", num, "равен", result)


# Вызов главной функции
main()