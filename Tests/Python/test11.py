import random

def CreateArray(size):
    a = []
    for i in range(size):
        a.append(random.randint(1, 99))
    return a

def PrintArray(array):
    print('Array: ', end=' ')
    for number in array:
        print(number, end=' ')
    print()


def my_sort_insert(array):
    for i in range(1, len(array)):
        t = array[i]
        j = i - 1
        while (j >= 0 and t < array[j]):
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = t
 
def main():
    n = int(input('Введите число n:')) # Вводим число n для генерации массива
    massive = CreateArray(n)


    my_sort_insert(massive) # Сортируем
    PrintArray(massive)

main()