from flask import Flask, render_template, redirect, request, url_for, jsonify, send_file
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Cambia el backend a Agg
import io
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
# Ruta para generar la gráfica "relajado"
@app.route('/plot_relajado')
def plot_relajado():
    df = pd.read_excel("data/Lectura_relajado.xlsx")

    plt.figure(figsize=(10, 6))
    plt.plot(df['Segundos'], df['Valor_GSR'], label='Onda Alfa')
    plt.xlabel('Tiempo (Segundos)')
    plt.ylabel('Amplitud')
    plt.title('Ondas de recepción - Relajado')
    plt.legend()

    # Guardar el gráfico en memoria
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

# Ruta para generar la gráfica "agitado"
@app.route('/plot_agitado')
def plot_agitado():
    df = pd.read_excel("data/Lectura_agitado.xlsx")

    plt.figure(figsize=(10, 6))
    plt.plot(df['Segundos'], df['Valor_GSR'], label='Onda Alfa')
    plt.xlabel('Tiempo (Segundos)')
    plt.ylabel('Amplitud')
    plt.title('Ondas de recepción - Agitado')
    plt.legend()

    # Guardar el gráfico en memoria
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png') 

# Ruta para generar la gráfica de Mind Monitor
@app.route('/plot_mind_monitor')
def plot_mind_monitor():
    df = pd.read_excel("data/mindMonitor.xlsx")

    plt.figure(figsize=(10, 6))
    plt.plot(df['TimeStamp'], df['Delta_TP9'], label='Onda Delta')
    # Si quieres agregar más ondas cerebrales, puedes descomentar las siguientes líneas:
    # plt.plot(df['TimeStamp'], df['Delta_AF7'], label='Onda Beta')
    # plt.plot(df['TimeStamp'], df['Theta_TP9'], label='Onda Theta')
    plt.xlabel('Tiempo (TimeStamp)')
    plt.ylabel('Frecuencia en Hz')
    plt.title('Ondas Cerebrales - Mind Monitor')
    plt.legend()

    # Guardar el gráfico en memoria
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

# Ruta para la página de registro
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

# # Ruta para generar la gráfica "relajado"
# @app.route('/plot_relajado')
# def plot_relajado():
#     df = pd.read_excel("data/Lectura_relajado.xlsx")  # Cambia por la ruta correcta

#     plt.figure(figsize=(10, 6))
#     plt.plot(df['Segundos'], df['Valor_GSR'], label='Onda Alfa')
#     plt.xlabel('Tiempo')
#     plt.ylabel('Amplitud')
#     plt.title('Ondas de recepción - Relajado')
#     plt.legend()

#     # Guardar el gráfico en memoria
#     img = io.BytesIO()
#     plt.savefig(img, format='png')
#     img.seek(0)
#     plt.close()

#     return send_file(img, mimetype='image/png')

# # Ruta para generar la gráfica "agitado"
# @app.route('/plot_agitado')
# def plot_agitado():
#     df = pd.read_excel("data/Lectura_agitado.xlsx")  # Cambia por la ruta correcta

#     plt.figure(figsize=(10, 6))
#     plt.plot(df['Segundos'], df['Valor_GSR'], label='Onda Alfa')
#     plt.xlabel('Tiempo')
#     plt.ylabel('Amplitud')
#     plt.title('Ondas de recepción - Agitado')
#     plt.legend()

#     # Guardar el gráfico en memoria
#     img = io.BytesIO()
#     plt.savefig(img, format='png')
#     img.seek(0)
#     plt.close()

#     return send_file(img, mimetype='image/png')

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