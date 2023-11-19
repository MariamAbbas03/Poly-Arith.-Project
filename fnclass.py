class PolynomialArithmetic:
    
    def __init__(self, deg):
        self.deg = deg
        self.m = self.generate_primitive_polynomial()
    
    def generate_primitive_polynomial(self):
        m = ""
        for i in range(0, 164):
            if i == 0 or i == 6 or i == 7 or i == 163:
                m += '1'
            else:
                m += '0'
        return m

    def generate_x_polynomial(self):
        x = ''
        m = self.m
        for i in range(len(m)):
            if i!= len(m)-1:
                if m[i]=='1':
                    x = x + 'x^(' + str(i) + ')' + '+'
            else:
                if m[i]=='1':
                    x = x + 'x^(' + str(i) + ')'
        return x
    
    def mod2(self, s):
        for i in range(0, len(s) - 1):
            if int(s[i]) % 2 == 0:
                s[i] = '0'
            else:
                s[i] = '1'
                
    def modulo_reduction(self, s):
        l = len(s)
        i = l - 1
        while i > self.deg - 1:
            if s[i] == '1':
                intm = int(self.m, 2)
                intm = intm << (i - self.deg)
                ints = int(s, 2)
                ints = ints ^ intm
                s = bin(ints)
                s = s[2:]
                s.zfill(l)
            i -= 1
        return s
    
    def inverse(self, b):
        (a1, a2, a3) = (1, 0, self.deg)
        (b1, b2, b3) = (0, 1, b)
        while b3 != 1:
            if b3 == 0:
                return "no inverse"
            q = self.divide(a3, b3)
            t1 = self.subtract(a1, self.multiply(q, b1), self.deg)
            t2 = self.subtract(a2, self.multiply(q, b2), self.deg)
            t3 = self.subtract(a3, self.multiply(q, b3), self.deg)
            (a1, a2, a3) = (b1, b2, b3)
            (b1, b2, b3) = (t1, t2, t3)
        return b2  
    
    def add(self, a, b):
        inta = int(a, 2)
        intb = int(b, 2)
        intresult = inta ^ intb
        result = bin(intresult)
        result = result[2:]
        result.zfill(self.deg + 1)
        return result
    
    def subtract(self, a, b):
        inta = int(a, 2)
        intb = int(b, 2)
        intresult = inta ^ intb
        result = bin(intresult)
        result = result[2:]
        result.zfill(self.deg + 1)
        return result
    
    def multiply(self, a, b):
        a = str(a)
        b = str(b)
        mul = int(a, 2) * int(b, 2)
        answer = bin(mul)
        answer = self.modulo_reduction(answer, self.deg)
        return answer

    def divide(self, a, b):
        if b == '0':
            raise ValueError("Division by zero")
    
        a = int(a, 2)
        b = int(b, 2)
    
        quotient = 0
        while a >= b:
            shift = len(bin(a)) - len(bin(b))
            a ^= (b << shift)
            quotient |= (1 << shift)
    
        quotient_str = bin(quotient)[2:].zfill(self.deg + 1)
        return quotient_str
        