import random

def Print(array):
    print('Array: ', end=' ')
    for number in array:
        print(number, end=' ')
    print()


def sort_massive(array):
    for i in range(1, len(array)):
        t = array[i]
        j = i - 1
        while (j >= 0 and t < array[j]):
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = t

def GenerateMasive(size):
    a = []
    for i in range(size):
        a.append(random.randint(1, 99))
    return a

 
def main():
    size = int(input('Input n:'))
    massive = GenerateMasive(size)
    sort_massive(massive)
    Print(massive)

main()

