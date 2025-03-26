from flask import Blueprint, request, session, render_template, jsonify, redirect, url_for, current_app
import pandas as pd
from datetime import datetime
from app.database import create_db_connection
import psycopg2  # Necesario para psycopg2.Binary

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload_excel', methods=['GET'])
def upload_excel_form():
    return render_template('upload_excel.html')

@upload_bp.route('/upload_excel', methods=['POST'])
def upload_excel():
    file = request.files['file']
    if file and file.filename.endswith('.xlsx'):
        # Leer el archivo directamente desde la solicitud
        df = pd.read_excel(file)

        # Calcular el promedio de la columna 'gsr'
        promedio_gsr = df['gsr'].mean()

        # Determinar la emoción basada en el promedio_gsr
        def determine_emotion(average_value):
            if average_value < 100:
                return 'Relajado'
            elif average_value < 200:
                return 'Triste'
            else:
                return 'Enojado'

        emotion = determine_emotion(promedio_gsr)

        try:
            connection = create_db_connection()
            cursor = connection.cursor()

            # Insertar los datos en la tabla existente
            insert_query = """
            INSERT INTO gsr_readings (user_id, value, emotion, created_at, session_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            # Aquí debes proporcionar los valores para user_id, emotion y session_id
            user_id = session.get('user_id')  # Obtener el user_id desde la sesión
            # user_id = 2  # Obtener el user_id desde la sesión
            session_id = str(datetime.now().timestamp())  # ID único de la sesión
            created_at = datetime.now()

            cursor.execute(insert_query, (user_id, float(promedio_gsr), emotion, created_at, session_id))
            connection.commit()

            return render_template('reports.html')
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    return jsonify({'message': 'Invalid file format. Please upload an Excel file.'}), 400