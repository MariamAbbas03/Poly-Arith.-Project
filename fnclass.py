# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 00:14:47 2023

@author: USER
"""

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
        m = ""
        for i in range(0, 9):
            if i == 0 or i==1 or i == 3 or i == 4 or i == 8:
                m += '1'
            else:
                m += '0'
        return m[::-1]
    
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
        s = int(s, 2)
        m = self.generate_irreducible_polynomial()       
        m = int(m,2)
        remainder = s % m
        remainder_binary = bin(remainder)[2:]
        return remainder_binary

    def inverse(self, b):

        m = self.generate_irreducible_polynomial()       
        (a1, a2, a3) = ('1', '0', m)
        (b1, b2, b3) = ('0', '1', b)
        while b3 != '1':
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
    
    def multiply(self, multiplicand, multiplier):
        
        multiplicand = int(multiplicand, 2)
        multiplier = int(multiplier, 2)
        partial_products = []
    
        multiplier_str = bin(multiplier)[2:]
    
        for i in range(len(multiplier_str) - 1, -1, -1):
            digit_multiplier = int(multiplier_str[i])
            partial_product = multiplicand * digit_multiplier
    
            partial_product <<= (len(multiplier_str) - 1 - i)
            partial_products.append(bin(partial_product)[2:])
        
        result = '0'
        for x in partial_products:
            result = self.add(result, x)
    
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
    

