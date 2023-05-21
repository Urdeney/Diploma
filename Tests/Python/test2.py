import random

def BubbleSort(array):
    n = len(array)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
    return array

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

def main():
    N = 10
    a = CreateArray(N)

    a = BubbleSort(a)

    PrintArray(a)

main()