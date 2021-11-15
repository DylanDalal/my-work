# Dylan Dalal
# dmd19e
# 01.20.21
# The program in this file is the individual work of Dylan Dalal.

def calculate(top, bot):
    diff = top - bot
    bottom = factorial(bot) * factorial(diff)
    total = int(factorial(top)) / int(bottom)
    return int(total)

def factorial(x):
    total = 1
    for z in range(1, x+1):
        total *= z
    if total > 0:
        return total
    else:
        return 1

def printTriangle(N):
    triangle = list()
    row = int(N)
    for x in range(row):  #x is current row
        for y in range(x):
            entry = calculate(x, y)
            triangle.append(entry)
    triangle.append(1)

    #actually print
    total = 0
    for i in range(0, row):
        for o in range(0, i+1):
            print(triangle[o+total], end=' ')
        print()
        total += i

def main():
    N = input('Input the number of rows: ')
    printTriangle(N)

if __name__ == "__main__":
    main()