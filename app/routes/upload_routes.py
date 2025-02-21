from flask import Blueprint, request, jsonify, redirect, url_for, current_app
import os
import pandas as pd
from app.database import create_db_connection
import psycopg2  # Necesario para psycopg2.Binary

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload_excel', methods=['POST'])
def upload_excel():
    file = request.files['file']
    if file and file.filename.endswith('.xlsx'):
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Procesar el archivo con pandas (si es necesario)
        df = pd.read_excel(file_path)

        # Leer el contenido binario del archivo guardado
        with open(file_path, "rb") as f:
            file_data = f.read()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()

            insert_query = "INSERT INTO excel_files (file_name, file_data) VALUES (%s, %s)"
            cursor.execute(insert_query, (file.filename, psycopg2.Binary(file_data)))
            connection.commit()

            return redirect(url_for('dashboard'))
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    return jsonify({'message': 'Invalid file format. Please upload an Excel file.'}), 400
