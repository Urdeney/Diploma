def sum(number1,number2):
    return number1 + number2 #just a comment 1

def gen_arr(): 
    return [i for i in range(1,10)] #just a comment 2

def main():
    x = 10
    arr = gen_arr()
    for i in range(len(arr)):
        arr[i] = sum(x,arr[i])

    print(arr) #just a comment 3

main()
