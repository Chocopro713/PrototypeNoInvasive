from flask import Blueprint, jsonify
import pandas as pd

data_bp = Blueprint('data', __name__)

@data_bp.route('/data_relajado')
def data_relajado():
    df = pd.read_excel("data/Lectura_relajado.xlsx")
    return jsonify({'segundos': df['Segundos'].tolist(), 'valor_gsr': df['Valor_GSR'].tolist()})

@data_bp.route('/data_agitado')
def data_agitado():
    df = pd.read_excel("data/Lectura_agitado.xlsx")
    return jsonify({'segundos': df['Segundos'].tolist(), 'valor_gsr': df['Valor_GSR'].tolist()})

@data_bp.route('/data_mind_monitor')
def data_mind_monitor():
    df = pd.read_csv('data/mindMonitor.csv')
    return jsonify({
        'timestamp': df['TimeStamp'].tolist(),
        'delta_tp9': df['Delta_TP9'].tolist(),
        'theta_tp9': df['Theta_TP9'].tolist(),
        'beta_af7': df['Beta_AF7'].tolist()
    })
