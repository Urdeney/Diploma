import math

#calculate sqrt from number
def sqrt(number):
    return math.sqrt(number)

def main():
    array = [4, 9, 25, 36, 49]
    s = 0
    for number in array:
        s = s + sqrt(number)
    print('Result: {0}'.format(s))

main()
