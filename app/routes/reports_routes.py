from flask import Blueprint, render_template

reports_bp = Blueprint('reports', __name__)  # Asegúrate de que el nombre del Blueprint sea 'reports'

@reports_bp.route('/reports')
def reports():
    return render_template('reports.html')
