
#all my functions are here


def generate_primitive_polynomial(m = ""):
    for i in range(164):
        if i in {0, 6, 7, 163}:
            m += '1'
        else:
            m += '0'
    return m

def mod2(s):
    s[:] = ['0' if int(bit) % 2 == 0 else '1' for bit in s]

def modulo_reduction(s, deg, primitive_poly):
    l = len(s)
    for i in range(l - 1, deg - 1, -1):
        if s[i] == '1':
            intm = int(primitive_poly, 2) << (i - deg)
            ints = int(s, 2)
            s = bin(ints ^ intm)[2:].zfill(l)
    return s

def inverse(b, deg):
    a1, a2, a3 = 1, 0, deg
    b1, b2, b3 = 0, 1, b
    while b3 != 1:
        if b3 == 0:
            return "no inverse"
        q = divide(a3, b3, deg)
        t1 = subtract(a1, multiply(q, b1, deg), deg)
        t2 = subtract(a2, multiply(q, b2, deg), deg)
        t3 = subtract(a3, multiply(q, b3, deg), deg)
        a1, a2, a3 = b1, b2, b3
        b1, b2, b3 = t1, t2, t3
    return b2

def add(a, b, deg):
    intresult = int(a, 2) ^ int(b, 2)
    result = bin(intresult)[2:].zfill(deg + 1)
    return result

def subtract(a, b, deg):
    intresult = int(a, 2) ^ int(b, 2)
    result = bin(intresult)[2:].zfill(deg + 1)
    return result

def multiply(a, b, deg, primitive_poly):
    mul = int(a, 2) * int(b, 2)
    answer = bin(mul)[2:].zfill(deg + 1)
    return modulo_reduction(answer, deg, primitive_poly)

def divide(a, b, deg):
    if b == '0':
        raise ValueError("Division by zero")
    
    a, b = int(a, 2), int(b, 2)
    
    quotient = 0
    while a >= b:
        shift = len(bin(a)) - len(bin(b))
        a ^= (b << shift)
        quotient |= (1 << shift)
    
    quotient_str = bin(quotient)[2:].zfill(deg + 1)
    return quotient_str
