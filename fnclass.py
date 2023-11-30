from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
db = SQLAlchemy(app)

class Operation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation_type = db.Column(db.String(20), nullable=False)
    input_data = db.Column(db.String(255), nullable=False)
    key = db.Column(db.String(255), nullable=False)
    result = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class PolynomialArithmetic:
    
    def __init__(self, deg):
        self.deg = deg
        self.m = self.generate_irreducible_polynomial()
    
    def generate_irreducible_polynomial(self):
        deg = self.deg
        
        s=""
        if deg==113:
            for i in range(0,114):
                if i==113 or i==15 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s
        
        if deg==131:
            for i in range(0,132):
                if i==131 or i==99 or i==97 or i==95 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s
        
        if deg==163:
            for i in range(0,164):
                if i==163 or i==99 or i==97 or i==3 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s
        
        if deg==193:
            for i in range(0,194):
                if i==193 or i==73 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s
        
        if deg==233:
            for i in range(0,234):
                if i==233 or i==159 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s
        
        if deg==239:
            for i in range(0,240):
                if i==239 or i==203 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s
        
        if deg==283:
            for i in range(0,284):
                if i==283 or i==249 or i==219 or i==27 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s
        
        if deg==409:
            for i in range(0,410):
                if i==409 or i==87 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s
        
        if deg==571:
            for i in range(0,572):
                if i==571 or i==507 or i==475 or i==417 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s
    
    
    def generate_x_polynomial(self):
        x = ''
        m = self.m
        plus = False
        for i in range(len(m)-1,-1,-1):
            if i!= 0:
                if m[i]=='1':
                    if plus==False:
                        x = x + 'x^(' + str(i) + ')' 
                        plus=True
                    else:
                        x = x + ' + ' + 'x^(' + str(i) + ')'
            else:
                if m[i]=='1':
                    x = x + ' + 1'
        return x
    
    def modulo_reduction(self, s):
        s=bin(int(s,2))[2:]
        m = self.generate_irreducible_polynomial()
        m_l = len(m)-1
        m = int(m,2)
        while len(s)-1>m_l:
            l=len(s)-1
            s = int(s,2)
            s ^= (m << (l-m_l))
            s = bin(s)[2:]
            s = s.zfill(m_l)
        return s
    
    def inverse(self, b):
        m = self.generate_irreducible_polynomial()       
        (a1, a2, a3) = ('1', '0', m)
        (b1, b2, b3) = ('0', '1', b)
        while int(b3,2) != 1:
            if b3 == '0':
                return "no inverse"
            q = self.divide(a3, b3)
            t1 = self.subtract(a1, self.multiply(q, b1))
            t2 = self.subtract(a2, self.multiply(q, b2))
            t3 = self.subtract(a3, self.multiply(q, b3))
            (a1, a2, a3) = (b1, b2, b3)
            (b1, b2, b3) = (t1, t2, t3)
        return b2  
    
    def add(self, a, b):
        inta = int(a, 2)
        intb = int(b, 2)
        intresult = inta ^ intb
        result = bin(intresult)
        result = result[2:]
        result = result.zfill(self.deg)
        return result
    
    def subtract(self, a, b):
        inta = int(a, 2)
        intb = int(b, 2)
        intresult = inta ^ intb
        result = bin(intresult)
        result = result[2:]
        result = result.zfill(self.deg)
        return result
    
    def multiply(self, multiplicand, multiplier):
        result= '0' * (len(multiplicand)+len(multiplier)-1)
        for i in range(len(multiplier)-1,-1, -1):
            if multiplier[i]=='1':
                result = int(result,2)
                result ^= (int(multiplicand,2)<<(len(multiplier)-1-i))
                result = bin(result)[2:]
                result = self.modulo_reduction(result)
        return result
 
    def divide(self, dividend, divisor):
    
        dividend_int = int(dividend, 2)
        divisor_int = int(divisor, 2)
    
        quotient = 0
        remainder = dividend_int
    
        while divisor_int <= remainder:
            shift = remainder.bit_length() - divisor_int.bit_length()
    
            quotient |= 1 << shift
            remainder ^= divisor_int << shift
    
        quotient_str = bin(quotient)[2:]
    
        return quotient_str
    
    def record_operation(self, operation_type, input_data, key, result):
        operation = Operation(operation_type=operation_type, input_data=input_data, key=key, result=result)
        db.session.add(operation)
        db.session.commit()

    def clear_history(self):
        Operation.query.delete()
        db.session.commit()