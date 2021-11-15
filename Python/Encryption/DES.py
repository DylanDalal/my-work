def printBothSides(left, right):
    lft = False
    counter = lcounter = rcounter = 0

    print()
    for x in range(0, 64):
        if counter % 4 == 0 and lft is True:
            lft = False
        elif counter % 4 == 0 and lft is False:
            lft = True
        if lft is True:
            print(left[lcounter], end=" ")
            lcounter = lcounter + 1
        elif lft is False:
            print(right[rcounter], end=" ")
            rcounter = rcounter + 1
        counter = counter + 1
        if counter % 8 == 0:
            print()

def encrypt(ptext, key):
    times = len(ptext) / 8
    counter = 0
    total = ""
    binary = []
    encrypted = []

    for char in ptext:
        if counter < 8:
            binVal = format((ord(char)), 'b').zfill(8)
            total = total + binVal
            counter = counter + 1
        else:
            binary.append(total)
            total = ""
            binary = 0

    if total != "":
        total = total.zfill(64)
        binary.append(total)

    for value in binary:
        ctext = DES((value), key)
        encrypted.append(ctext)


    return encrypted


def DES(val, key):
    print("Val:", val)
    num = str(val).zfill(64)
    left = right = initial = ""


    # ----initial permutation-----
    for a in range(0, 4):
        start = 58 + (2 * a)
        for y in range(0, 8):
            start = start - 8
            initial = initial + num[start]
    for a in range(0, 4):
        start = 57 + (2 * a)
        for y in range(0, 8):
            start = start - 8
            initial = initial + num[start]
    print(initial)

    # ---split-the-value-in-half---
    lft = False
    counter = 0
    for x in num:
        if counter % 4 == 0 and lft is True:
            lft = False
        elif counter % 4 == 0 and lft is False:
            lft = True
        if lft is True:
            left = left + x
        elif lft is False:
            right = right + x
        counter = counter + 1
    printBothSides(left, right)
    print(left)
    print(right)

    encrypted = ""
    return encrypted

def main():
    k = ptext = ""
    while ptext != "Exit":
        ptext = input("Enter text to encrypt (\"Exit\" to quit) ")
        if ptext == "Exit":
            break
        test = encrypt(ptext, k)


if __name__ == "__main__":
    main()