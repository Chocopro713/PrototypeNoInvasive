from flask import Blueprint, render_template, request, session
import os
import pandas as pd
from flask import current_app
from app.middleware import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
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
