from flask import Flask, render_template, redirect, request, url_for, jsonify
import json
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

# Ruta para la subida de archivos
@app.route('/upload_excel', methods=['GET', 'POST'])
def upload_excel():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            # Leer el archivo de Excel usando pandas
            df = pd.read_excel(file_path)
            # Aquí puedes hacer algo con los datos, como guardarlos en la base de datos
            return jsonify({'message': 'File uploaded successfully', 'data': df.to_dict()}), 200
        else:
            return jsonify({'message': 'Invalid file format. Please upload an Excel file.'}), 400
    return render_template('upload_excel.html')

@app.route('/logout')
def logout():
    # Aquí puedes añadir la lógica de cierre de sesión
    return redirect(url_for('login'))

@app.route('/data')
def data():
    with open('data/data.json') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/report_data')
def report_data():
    with open('data/reports.json') as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
