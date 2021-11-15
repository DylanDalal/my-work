def encrypted_decorator(func):
    def inner(a, b):
        print("The encrypted", end=" ")
        func(a, b)
    return inner


def decrypted_decorator(func):
    def inner(a, b):
        print("The decrypted", end=" ")
        func(a, b)
    return inner


class RSA:
    e = 0
    d = 0
    lst = []

    def __init__(self):
        self.e = 0
        self.d = 0
        self.phiN = 0
        self.lst = []
        self.N = 0
        self.p = 0
        self.q = 0

    def inputFunc(self):
        num = int(input("Enter the number of entries: "))
        for i in range(0, num):
            entry = input()
            self.lst.append(entry)
        print(self.lst)

    @encrypted_decorator
    @decrypted_decorator
    def printFunc(self, num):
        print("message is", num)

    def primeGen(self, minVal):  # error check for minVal < 1
        maxVal = int(minVal) + 100000
        prime1 = 0
        prime2 = 0
        for i in range(minVal, maxVal):
            if prime1 == 0 or prime2 == 0:
                for o in range(2, i):
                    if (i % o) == 0:
                        break
                else:
                    if prime1 == 0:
                        prime1 = i
                    else:
                        prime2 = i
            else:
                break
        self.p = prime1
        self.q = prime2

    def keyGen(self):
        minVal = int(input("Enter a minimum value: "))
        self.primeGen(minVal)
        self.N = self.p * self.q
        self.phiN = (self.p - 1) * (self.q - 1)
        print("N is", self.N)
        start = 2
        if self.phiN/60 > 3:
            start = self.phiN/60
        if self.phiN/6000 > 3:
            start = self.phiN/6000
        if self.phiN/60000 > 3:
            start = self.phiN/60000
        if self.phiN/1000000 > 3:
            start = self.phiN/1000000
        for e in range(int(start), self.phiN):
            gcd, d, garbo = self.gcd(e, self.phiN)
            if gcd == 1:
                self.e = e
                self.d = d
                break
        print("e is", self.e)
        while self.d > 0:
            self.d = self.d - self.phiN
        while self.d < 0:
            self.d = self.d + self.phiN

    def gcd(self, a, b):
        if a == 0:
            return b, 0, 1

        gcd, x, y = self.gcd(b % a, a)
        d = y - (b // a) * x
        return gcd, d, x

    def encrypt(self, given):
        num = int(given)
        if num > self.N:
            #padding
            print("Value too large")
        encrypt = num**self.e
        #encrypt = self.exponentiate(num, self.e)
        encrypt = encrypt % self.N
        return encrypt

    def decrypt(self, given):
        num = int(given)
        decrypt = self.exponentiate(num, self.d, self.N)
        return decrypt

    def exponentiate(self, base, exp, mod):
        res = 1
        while exp > 0:
            if exp % 2 == 0:
                base = (base * base) % mod
                exp = exp / 2
            else:
                res = (base * res) % mod
                exp = exp - 1
        return res

    def messages(self):
        init = iter(self.lst)
        encrypted = []
        decrypted = []

        self.inputFunc()
        self.keyGen()

        for x in init:
            a = self.encrypt(x)
            encrypted.append(a)
        for x in encrypted:
            self.printFunc(x)
            a = self.decrypt(x)
            decrypted.append(a)
        for x in decrypted:
            self.printFunc(x)


def main():
    test = RSA()
    test.messages()

if __name__ == "__main__":
    main()