import sys
from timeit import default_timer as timer
import time


def log(fileName="std"):
    def log_decorator(func):
        def func_wrapper(*args, **kwargs):
            original_stdout = sys.stdout
            temp = fileName
            std = True
            if fileName != "std":
                try:
                    open(fileName, 'w')
                    std = False
                except:
                    std = True
            if std is False:
                sys.stdout = open(fileName, 'w')

            print("∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗")
            print("Calling function ", func.__name__, ".", sep="")

            # Arguments
            types = [(0, 0)]
            counter = 0
            if len(args) != 0:
                print("Arguments: ")
                for i in range(0, len(args)):
                    if any(str(type(args[i])) in subl for subl in types):
                        for x, y in types:
                            if y == str(type(args[i])):
                                types[counter][0] = types[counter][0] + 1
                            counter = counter + 1
                    else:
                        types.append([int(1), str(type(args[i]))])
                types.pop(0)
                for i in range(0, len(types)):
                    print("\t- ", types[i][0], " arguments of ", types[i][1], ".", sep="")
            else:
                print("No arguments provided.")

            # Output, Time
            print("Output:")
            start = timer()
            y = func(*args, **kwargs)
            end = timer()
            print("Execution time: %.5f s." % (end - start))

            # Return value
            print("Return value: ", y, " of type ", str(type(y)), ".", sep="")
            print("∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗∗\n")
            sys.stdout = original_stdout
        return func_wrapper
    return log_decorator

@log()
def factorial(*num_list):
    results = []
    for number in num_list:
        res = number
        for i in range(number-1,0,-1):
            res = i*res
        results.append(res)
        return results

@log("logger.txt")
def waste_time(a, b, c):
    print("Wasting time.")
    time.sleep(5)
    return a, b, c

@log("logger.txt")
def gcd(a, b):
    print("The GCD of ", a, " and ", b, " is ", end="")
    while a!=b:
        if a > b:
            a -= b
        else:
            b -= a
    print(abs(a))
    return abs(a)

@log()
def print_hello():
    print("Hello!")

@log(10)
def print_goodbye():
    print("Goodbye!")


if __name__ == "__main__":
    factorial(4, 5)
    waste_time("one", 2, "3")
    gcd(15,9)
    print_hello()
    print_goodbye()
