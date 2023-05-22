import random

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
    massive = [random.random.randint(1,10) for i in range(n)] # Генерируем рандомно массив


    my_sort_insert(massive) # Сортируем
    print('Отсортированный массив: ', end='') # Вывод массива
    print(massive)

main()
