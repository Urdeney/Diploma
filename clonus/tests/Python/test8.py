import random

def Print(alist):
    for i in range(len(alist)):
        print(alist[i], end=' ')
    print()

def create_array(size, mmin = 0, mmax = 10):
    return [random.randint(mmin, mmax) for i in range(size)]

def insertion_sort(alist):
    for i in range(1, len(alist)):
        temp = alist[i]
        j = i - 1
        while (j >= 0 and temp < alist[j]):
            alist[j + 1] = alist[j]
            j = j - 1
        alist[j + 1] = temp
    return alist
 
def main():
    alist = input('Enter the list of numbers: ').split()
    alist = [int(x) for x in alist]
    Print(alist)
    alist = insertion_sort(alist)
    Print(alist)

    blist = create_array(10)
    Print(blist)
    blist = insertion_sort(blist)
    Print(blist)

main()