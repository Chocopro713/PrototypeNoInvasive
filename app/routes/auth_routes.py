from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from app.database import create_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import mysql

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']

        try:
            connection = create_db_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute("SELECT * FROM users WHERE correo = %s", (correo,))
            user = cursor.fetchone()

            if user and check_password_hash(user['contrasena'], password):
                # Guardar sesión
                session['user_id'] = user['id']
                session['user_name'] = user['nombres']
                flash("Inicio de sesión exitoso.", "success")  # ✅ Agrega mensaje flash
                return redirect(url_for('dashboard.dashboard'))  # Redirige al dashboard
            else:
                flash("Correo o contraseña incorrectos.", "danger")  # ✅ Mensaje de error

        except Exception as e:
            flash(f"Error en el login: {e}", "danger")  # ✅ Muestra errores

        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        correo = request.form['correo']
        password = request.form['password']
        fecha_nacimiento = request.form['fecha_nacimiento']

        hashed_password = generate_password_hash(password)  # Hash de contraseña

        try:
            connection = create_db_connection()
            cursor = connection.cursor()

            insert_query = """
                INSERT INTO users (nombres, apellidos, correo, contrasena, fecha_nacimiento)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (nombres, apellidos, correo, hashed_password, fecha_nacimiento)
            cursor.execute(insert_query, values)
            connection.commit()

            flash("Registro exitoso. Inicia sesión.", "success")
            return redirect(url_for('auth.login'))

        except mysql.connector.Error as e:
            flash(f"Error al registrar: {e}", "danger")
        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for('auth.login'))
