from flask import Blueprint, render_template, jsonify, session
from app.database import create_db_connection  # Asegúrate de tener la conexión directa a PostgreSQL

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports')
def reports():
    return render_template('reports.html')


# ✅ Ruta que devuelve los datos en JSON
@reports_bp.route('/report_data')
def report_data():
    connection = None
    cursor = None

    # user_id = session.get('user_id')  # Opcional: Si quieres filtrar por usuario logueado
    user_id = 2  # Opcional: Si quieres filtrar por usuario logueado

    try:
        connection = create_db_connection()
        cursor = connection.cursor()

        # ⚙️ Consulta para obtener las emociones y fechas, agrupadas por sesión
        query = """
            SELECT MIN(created_at) as fecha, emotion
            FROM gsr_readings
            WHERE user_id = %s
            GROUP BY session_id, emotion
            ORDER BY fecha DESC
        """
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

        # Preparar datos para enviar como JSON
        report_list = []
        for row in rows:
            report = {
                'date': row[0].strftime('%Y-%m-%d %H:%M:%S'),  # Formato de fecha bonito
                'emotion': row[1]
            }
            report_list.append(report)

        return jsonify(report_list)

    except Exception as e:
        print(f"Error al obtener reportes: {e}")
        return jsonify({'error': 'Error al obtener reportes'}), 500

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
