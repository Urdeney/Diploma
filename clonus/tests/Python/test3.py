import math

def f(number):
    return math.sqrt(number)

def g():
    z = [i for i in range(1,10)]
    return z

def main():
    x = 5
    y = 2
    x = x * y
    x = x * x
    res = f(x)

    k = g()
    print(k)

main()