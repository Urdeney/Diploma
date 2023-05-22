import random

def my_sort(array):
    for i in range(1, len(array)):
        t = array[i]
        j = i - 1
        while (j >= 0 and t < array[j]):
            array[j + 1] = array[j]
            j = j - 1
        array[j + 1] = t
    return array
    
def print_array(array):
    for i in range(len(array)):
        print(array[i], end=' ')
    print()

def create_array(n):
    array = []
    for i in range(n):
        x = random.randint(0, 10)
        array.append(x)
    return array

 
def main():
    n = int(input('Введите размер массива: '))
    array = create_array(n)
    print_array(array)
    array = my_sort(array)
    print_array(array)

main()

