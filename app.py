from flask import Flask, render_template, request, redirect, url_for
from fnclass import *   

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()

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
            return render_template('index.html', result="Invalid operation.")

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
            result = pa.inverse(input_data)

        print(f"Debug: Result before handling: {result}")

        if result is not None:
            if input_type == 'hexadecimal':
                result = hex(int(result, 2))[2:].zfill(int(pa.deg/4))
            print(f"Debug: Result after conversion: {result}")

        else:
            result = "Error: Calculation result is None."
            print("Debug: Result is None.")

        pa.record_operation(operation, input_data, key, result)

        return render_template('index.html', result=result, poly=poly)
    except Exception as e:
        print(f"Debug: Exception - {str(e)}")
        return render_template('index.html', result=str(e))
    
@app.route('/history')
def history():
    operations = Operation.query.all()
    return render_template('history.html', operations=operations)

@app.route('/perform_operation/<int:operation_id>')
def perform_operation(operation_id):
    operation = Operation.query.get_or_404(operation_id)

    pa = PolynomialArithmetic(len(operation.input_data) - 1)
    result = None

    if operation.operation_type == 'add':
        result = pa.add(operation.input_data, operation.key)
    elif operation.operation_type == 'subtract':
        result = pa.subtract(operation.input_data, operation.key)
    elif operation.operation_type == 'multiply':
        result = pa.multiply(operation.input_data, operation.key)
    elif operation.operation_type == 'divide':
        result = pa.divide(operation.input_data, operation.key)
    elif operation.operation_type == 'modred':
        result = pa.modulo_reduction(operation.input_data)
    elif operation.operation_type == 'inverse':
        result = pa.inverse(operation.input_data)

    pa.record_operation(operation.operation_type, operation.input_data, operation.key, result)

    return redirect(url_for('history'))

@app.route('/clear_history', methods=['POST'])
def clear_history():
    pa = PolynomialArithmetic(0)
    pa.clear_history()
    return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True)