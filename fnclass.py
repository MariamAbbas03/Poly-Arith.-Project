from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask

# Initialize Flask app
app = Flask(__name__)
# Configure the database URI for SQLAlchemy (using SQLite in this case)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
db = SQLAlchemy(app)


class Operation(db.Model):
    """
    A database model representing an operation in the polynomial arithmetic system.
    """
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each operation
    operation_type = db.Column(db.String(20), nullable=False)  # Type of operation (e.g., 'add', 'multiply')
    input_data = db.Column(db.String(255), nullable=False)  # Input data for the operation
    key = db.Column(db.String(255), nullable=False)  # Key used in the operation (e.g., polynomial degree)
    result = db.Column(db.String(255), nullable=True)  # Result of the operation
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp when the operation was performed
    
class PolynomialArithmetic:
    
    def __init__(self, deg):
        try:
            self.deg = deg # Degree of the polynomial
            if not isinstance(deg, int) or deg < 1:
                raise ValueError("Degree must be a positive integer.")
            self.m = self.generate_irreducible_polynomial() # Generate the irreducible polynomial
        except ValueError as ve:
            print(f"Initialization error: {ve}")
        except Exception as e:
            print(f"Unexpected error during initialization: {e}")
    
    def generate_irreducible_polynomial(self):
      try:
        deg = self.deg
        supported_degrees = [113, 131, 163, 193, 233, 239, 283, 409, 571]
        if self.deg not in supported_degrees:
            raise ValueError(f"Unsupported polynomial degree: {self.deg}")
        s=""
        # Dictionary to store irreducible polynomials for specific degrees
        if deg==113:
            for i in range(0,114):
                if i==113 or i==15 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s[::-1]
        
        if deg==131:
            for i in range(0,132):
                if i==131 or i==99 or i==97 or i==95 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s[::-1]
        
        if deg==163:
            for i in range(0,164):
                if i==163 or i==99 or i==97 or i==3 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s[::-1]
        
        if deg==193:
            for i in range(0,194):
                if i==193 or i==73 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s[::-1]
        
        if deg==233:
            for i in range(0,234):
                if i==233 or i==159 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s[::-1]
        
        if deg==239:
            for i in range(0,240):
                if i==239 or i==203 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s[::-1]
        
        if deg==283:
            for i in range(0,284):
                if i==283 or i==249 or i==219 or i==27 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s[::-1]
        
        if deg==409:
            for i in range(0,410):
                if i==409 or i==87 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s[::-1]
        
        if deg==571:
            for i in range(0,572):
                if i==571 or i==507 or i==475 or i==417 or i==0:
                    s+='1'
                else:
                    s+='0'
            return s[::-1]
        return "Please enter another common power"
      except ValueError as ve:
        return f"Unsupported polynomial degree: {self.deg}"
      except Exception as e:
            return f"Unexpected error in generate_irreducible_polynomial: Please try another input."

    
    
    def generate_x_polynomial(self):
      try:

        x = '' # Initialize an empty string to represent the x polynomial
        m = self.m # Retrieve the irreducible polynomial
        if m[0]!='1' and m[0]!='0':
            return m
        plus = False # Flag to track whether a 'plus' symbol should be added
        for i in range(len(m)-1,-1,-1): # Iterate over the irreducible polynomial bits in reverse order
            if i!= 0:
                if m[i]=='1':
                    if plus==False: # If it's the first term, no need to add 'plus'
                        x = x + 'x^(' + str(i) + ')' # Add the term to the polynomial
                        plus=True # Set the flag to True for subsequent terms
                    else:
                        x = x + ' + ' + 'x^(' + str(i) + ')' # Add the term with a 'plus' symbol
            else:
                if m[i]=='1':
                    x = x + ' + 1' # Add a constant term if the last bit is 1
        return x  # Return the generated x polynomial as a string
      except Exception as e:
            return f"Error in generating polynomial: Please try another input."
    
    def modulo_reduction(self, s):
      try:
        s=bin(int(s,2))[2:] # Convert the binary string to an integer, then back to binary
        m = self.generate_irreducible_polynomial() # Retrieve the irreducible polynomial
        m_l = len(m)-1 # Calculate the degree of the irreducible polynomial
        m = int(m,2) # Convert the irreducible polynomial to an integer
        while len(s)-1 >= m_l: # Perform modulo reduction until the length is less than the irreducible polynomial degree
            l=len(s)-1 # Calculate the current length of the binary string
            s = int(s,2) # Convert the binary string to an integer
            s ^= (m << (l-m_l)) # XOR operation to perform modulo reduction
            s = bin(s)[2:] # Convert the result back to a binary string
            s = s.zfill(m_l) # Fill with zeros to match the irreducible polynomial degree -1
        return s # Return the result after modulo reduction
      except Exception as e:
            return f"Error in modulo reduction: Please try another input."
    
    def inverse(self, b):
      try:
        m = self.generate_irreducible_polynomial()       
        (a1, a2, a3) = ('1', '0', m)
        (b1, b2, b3) = ('0', '1', b)
        while int(b3,2) != 1: # Perform extended Euclidean algorithm until the remainder is 1
            if b3 == '0':
                return "no inverse" # If the remainder is 0, no inverse exists
            q = self.divide(a3, b3)
            t1 = self.subtract(a1, self.multiply(q, b1))
            t2 = self.subtract(a2, self.multiply(q, b2))
            t3 = self.subtract(a3, self.multiply(q, b3))
            (a1, a2, a3) = (b1, b2, b3)
            (b1, b2, b3) = (t1, t2, t3)
        return b2  # Return the multiplicative inverse
      except Exception as e:
            return f"Error in finding inverse: Please try another input."
    
    def add(self, a, b):
      try:
        # Check if inputs are strings
        # Convert binary strings to integers
        inta = int(a, 2)
        intb = int(b, 2)
        intresult = inta ^ intb # XOR operation for addition
        result = bin(intresult) # Convert the result back to binary
        result = result[2:] # Remove the '0b' prefix from binary representation
        result = result.zfill(self.deg) # Fill with leading zeros to match the polynomial degree
        return result # Return the result of addition
      except ValueError as ve:
        return f"Error in addition: Please try another input."
        
      except Exception as e:
            return f"Error in addition: {e}"
    
    def subtract(self, a, b):
      try:
        # Check if inputs are strings
        if not isinstance(a, str) or not isinstance(b, str):
            raise ValueError("Inputs must be binary strings for subtraction.")
        # Convert binary strings to integers
        inta = int(a, 2)
        intb = int(b, 2)
        intresult = inta ^ intb # XOR operation for addition
        result = bin(intresult) # Convert the result back to binary
        result = result[2:] # Remove the '0b' prefix from binary representation
        result = result.zfill(self.deg) # Fill with leading zeros to match the polynomial degree
        return result # Return the result of addition
      except ValueError as ve:
        return f"Error in subtraction: Please try another input."
      except Exception as e:
            return f"Error in subtraction: {e}"
    
    def multiply(self, multiplicand, multiplier):
      try:
        # Check if inputs are strings
        if not isinstance(multiplicand, str) or not isinstance(multiplier, str):
              raise ValueError("Inputs must be binary strings for multiplication.")
        # Initialize result with zeros
        result= '0' * (len(multiplicand)+len(multiplier)-1)
        # Iterate over the multiplier bits
        for i in range(len(multiplier)-1,-1, -1):
            if multiplier[i]=='1':
                result = int(result,2)
                result ^= (int(multiplicand,2)<<(len(multiplier)-1-i)) # Perform XOR operation for multiplication
                result = bin(result)[2:]
                result = self.modulo_reduction(result)
        return result # Return the result of multiplication
      except ValueError as ve:
            return f"Error in multiplication: Please try another input."
      except Exception as e:
            return f"Unexpected error in multiplication: {e}"


    def divide(self, dividend, divisor): 
        try:
            # Check if inputs are strings
            if not isinstance(dividend, str) or not isinstance(divisor, str):
                raise ValueError("Inputs must be binary strings for division.")
            # Convert binary strings to integers
            dividend_int = int(dividend, 2)
            divisor_int = int(divisor, 2)
            # Initialize quotient and remainder
            quotient = 0
            remainder = 0
            # Iterate for the polynomial degree
            for _ in range(self.deg):
                # Shift remainder to the left
                remainder <<= 1
                remainder |= (dividend_int >> (self.deg - 1)) & 1
                # Check if remainder is greater than or equal to divisor
                if remainder >= divisor_int:
                    remainder -= divisor_int
                    quotient |= 1
                # Shift quotient to the lef
                quotient <<= 1
                dividend_int <<= 1
            quotient_str = bin(quotient >> 1)[2:]  # Convert quotient to binary and remove extra 0
            return quotient_str # Return the result of division
    
        except ValueError as ve:
            return f"Error in division: Please try another input."
        except Exception as e:
            return f"Unexpected error in division: {e}"
  

    def record_operation(self, operation_type, input_data, key, result):
        """
        Records an operation to the database.
        Args:
        operation_type (str): The type of the operation (e.g., 'add', 'multiply').
        input_data (str): The input data for the operation.
        key (str): The key used in the operation (e.g., polynomial degree).
        result (str): The result of the operation.
        """
        try:
            if not isinstance(operation_type, str) or not isinstance(input_data, str) or not isinstance(key, str) or not isinstance(result, str):
                raise ValueError("Operation details must be strings for recording.")
            operation = Operation(operation_type=operation_type, input_data=input_data, key=key, result=result) # Create a new Operation instance with provided parameters
            db.session.add(operation)  # Add the operation to the database session
            db.session.commit()  # Commit the session to save the operation in the database
        except ValueError as ve:
            print(f"Error recording operation: {ve}")
        except Exception as e:
            print(f"Unexpected error recording operation: {e}")

    def clear_history(self):
        """
        Clears the operation history from the database.
        """
        try:
            Operation.query.delete() # Delete all records from the Operation table
            db.session.commit() # Commit the session to apply changes to the database
        except ValueError as ve:
            print(f"Error clearing history: {ve}")
        except Exception as e:
            print(f"Error clearing history: {e}")



