from flask import Flask, render_template, redirect, url_for, jsonify
import json

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

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
