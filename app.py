from flask import Flask, render_template, redirect, request, url_for, jsonify, send_file
import mysql.connector
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Cambia el backend a Agg
import io
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
	
def create_db_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        database='PrototypeNoInvasive',
        user='roo1',
        password='PrototypeNoInvasive'
    )

@app.route('/data_relajado')
def data_relajado():
    df = pd.read_excel("data/Lectura_relajado.xlsx")
    data = {
        'segundos': df['Segundos'].tolist(),
        'valor_gsr': df['Valor_GSR'].tolist()
    }
    return jsonify(data)

# Ruta para los datos de Lectura Agitado
@app.route('/data_agitado')
def data_agitado():
    df = pd.read_excel("data/Lectura_agitado.xlsx")
    data = {
        'segundos': df['Segundos'].tolist(),
        'valor_gsr': df['Valor_GSR'].tolist()
    }
    return jsonify(data)

# Ruta para los datos del Mind Monitor
@app.route('/data_mind_monitor')
def data_mind_monitor():
    df = pd.read_excel("data/mindMonitor.xlsx")
    data = {
        'timestamp': df['TimeStamp'].tolist(),
        'delta_tp9': df['Delta_TP9'].tolist(),
        'theta_tp9': df['Theta_TP9'].tolist(),
        'beta_af7': df['Beta_AF7'].tolist()
    }
    return jsonify(data)

# Ruta para los datos comparativos Relajado vs Agitado
@app.route('/data_comparativo')
def data_comparativo():
    df_relajado = pd.read_excel("data/Lectura_relajado.xlsx")
    df_agitado = pd.read_excel("data/Lectura_agitado.xlsx")
    data = {
        'segundos_relajado': df_relajado['Segundos'].tolist(),
        'valor_gsr_relajado': df_relajado['Valor_GSR'].tolist(),
        'segundos_agitado': df_agitado['Segundos'].tolist(),
        'valor_gsr_agitado': df_agitado['Valor_GSR'].tolist()
    }
    return jsonify(data)

# Ruta para los datos agrupados por intervalos de tiempo (Relajado vs Agitado)
@app.route('/data_barras_intervalos')
def data_barras_intervalos():
    df_relajado = pd.read_excel("data/Lectura_relajado.xlsx")
    df_agitado = pd.read_excel("data/Lectura_agitado.xlsx")

    df_relajado['Intervalo'] = df_relajado['Segundos'] // 10 * 10
    df_agitado['Intervalo'] = df_agitado['Segundos'] // 10 * 10

    relajado_promedio = df_relajado.groupby('Intervalo')['Valor_GSR'].mean()
    agitado_promedio = df_agitado.groupby('Intervalo')['Valor_GSR'].mean()

    data = {
        'intervalos': relajado_promedio.index.tolist(),
        'relajado': relajado_promedio.tolist(),
        'agitado': agitado_promedio.tolist()
    }
    return jsonify(data)

@app.route('/data_scatter_relajado_agitado')
def data_scatter_relajado_agitado():
    df_relajado = pd.read_excel("data/Lectura_relajado.xlsx")
    df_agitado = pd.read_excel("data/Lectura_agitado.xlsx")
    data = {
        'segundos_relajado': df_relajado['Segundos'].tolist(),
        'valor_gsr_relajado': df_relajado['Valor_GSR'].tolist(),
        'segundos_agitado': df_agitado['Segundos'].tolist(),
        'valor_gsr_agitado': df_agitado['Valor_GSR'].tolist()
    }
    return jsonify(data)

@app.route('/data_radar_mind_monitor')
def data_radar_mind_monitor():
    df = pd.read_excel("data/mindMonitor.xlsx")
    # Tomar promedios para comparar cada onda cerebral
    avg_delta = df['Delta_TP9'].mean()
    avg_theta = df['Theta_TP9'].mean()
    avg_beta = df['Beta_AF7'].mean()

    data = {
        'labels': ['Delta', 'Theta', 'Beta'],
        'values': [avg_delta, avg_theta, avg_beta]
    }
    return jsonify(data)

@app.route('/data_stacked_mind_monitor')
def data_stacked_mind_monitor():
    df = pd.read_excel("data/mindMonitor.xlsx")
    data = {
        'timestamp': df['TimeStamp'].tolist(),
        'delta_tp9': df['Delta_TP9'].tolist(),
        'theta_tp9': df['Theta_TP9'].tolist(),
        'beta_af7': df['Beta_AF7'].tolist()
    }
    return jsonify(data)


@app.route('/data_donut_mind_monitor')
def data_donut_mind_monitor():
    df = pd.read_excel("data/mindMonitor.xlsx")
    # Sumar los valores de cada tipo de onda para obtener la distribución total
    total_delta = df['Delta_TP9'].sum()
    total_theta = df['Theta_TP9'].sum()
    total_beta = df['Beta_AF7'].sum()
    
    data = {
        'labels': ['Delta', 'Theta', 'Beta'],
        'values': [total_delta, total_theta, total_beta]
    }
    return jsonify(data)

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

# Ruta para la página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
 
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        correo = request.form['correo']
        password = request.form['password']
        fecha_nacimiento = request.form['fecha_nacimiento']
 
        try:
            connection = create_db_connection()
            if connection.is_connected():
                cursor = connection.cursor()
            
                insert_query = """
                    INSERT INTO `users` (`NOMBRE`, `APELLIDOS`, `CORREO`, `CONTRASENA`, `FECHA_NACIMIENTO`)
                    VALUES (%s, %s, %s, %s, %s);
                """
                values = (nombres, apellidos, correo, password, fecha_nacimiento)
                cursor.execute(insert_query, values)
                connection.commit()
 
                return redirect(url_for('dashboard'))
 
        except mysql.connector.Error as e:
            return f"Error al insertar los datos: {e}"
 
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
 
    return render_template('register.html')

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
    # app.run(host='85.31.235.126/', port=80) 
    # Cambia el puerto 5000 a 80