from flask import Flask, render_template, request
from fnclass import PolynomialArithmetic   

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        deg = request.form['deg']
        input_type = request.form['input_type']
        input_data = request.form['input_data']
        operation = request.form['operation']
        key = request.form['key']

        if operation not in ['add', 'subtract', 'multiply', 'divide', 'modred', 'inverse']:
            return render_template('index.html', result="Invalid operation")

        pa = PolynomialArithmetic(int(deg)) # Set the appropriate degree
        poly = pa.generate_x_polynomial()

        # Convert input_data to binary if it's in hexadecimal
        if input_type=='hexadecimal':
            input_data = bin(int(input_data, 16))[2:].zfill(pa.deg + 1)
            key = bin(int(key, 16))[2:].zfill(pa.deg + 1)

        result = None

        if operation == 'add':
            result = pa.add(input_data, key)
        elif operation == 'subtract':
            result = pa.subtract(input_data, key)
        elif operation == 'multiply':
            result = pa.multiply(input_data, key)
        elif operation == 'divide':
            result = pa.divide(input_data, key)
        elif operation == 'modred':
            result = pa.modulo_reduction(input_data)
        elif operation == 'inverse':
            result = pa.find_inverse(input_data)

        if input_type=='hexadecimal':
            result = hex(int(result, 2))[2:].zfill(int(pa.deg/4))

        return render_template('index.html', result=result, poly=poly)
    except Exception as e:
        return render_template('index.html', result=str(e))

if __name__ == '__main__':
    app.run(debug=True)