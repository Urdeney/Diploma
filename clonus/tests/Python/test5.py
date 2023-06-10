import math
import random

def gen(x):
    r = random.randint(0, 10)
    return [x for i in range(r)]

def main():
    x = int(input())
    arr = gen(x)
    print(arr)

    for i in range(len(arr)):
        arr[i] = arr[i] * 2
    
    print(arr)

main()

