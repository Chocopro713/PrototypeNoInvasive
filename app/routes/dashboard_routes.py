from datetime import datetime
from flask import Blueprint, render_template, request, session, jsonify
import os
import pandas as pd
from flask import current_app
from app.database import create_db_connection
from app.middleware import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
# @login_required
def dashboard():
    filename = request.args.get('filename')

    if filename:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        df = pd.read_excel(file_path)

        data = {
            'segundos': df['Segundos'].tolist(),
            'valor_gsr': df['Valor_GSR'].tolist()
        }

        return render_template('dashboard.html', user_name=session.get('user_name'), data=data, filename=filename)

    return render_template('dashboard.html', user_name=session.get('user_name'))

@dashboard_bp.route('/save_gsr_data', methods=['POST'])
def save_gsr_data():
    data = request.json
    gsr_average = data.get('gsr_average')  # Promedio de las 10 lecturas
    emotion = data.get('emotion')  # Estado emocional

    # user_id = session.get('user_id')  # Obtener el user_id desde la sesión
    user_id = 2  # Obtener el user_id desde la sesión

    if gsr_average is None or not emotion:
        return jsonify({'status': 'error', 'message': 'Datos incompletos.'}), 400

    if not user_id:
        return jsonify({'status': 'error', 'message': 'Usuario no autenticado.'}), 401

    connection = None
    cursor = None
    session_id = str(datetime.utcnow().timestamp())  # ID único de la sesión
    created_at = datetime.utcnow()

    try:
        connection = create_db_connection()
        cursor = connection.cursor()

        # ⚠️ INSERTA SOLO UN REGISTRO CON EL PROMEDIO
        insert_query = """
            INSERT INTO gsr_readings (user_id, value, emotion, created_at, session_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (user_id, gsr_average, emotion, created_at, session_id)
        cursor.execute(insert_query, values)
        connection.commit()

        return jsonify({'status': 'success', 'message': 'Datos guardados correctamente.'}), 200

    except Exception as e:
        print(f"Error al guardar datos GSR: {e}")
        return jsonify({'status': 'error', 'message': f'Error al guardar datos: {e}'}), 500

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
