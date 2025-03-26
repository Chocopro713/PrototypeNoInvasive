from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from app.database import create_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']

        connection = None
        cursor = None
        try:
            connection = create_db_connection()
            cursor = connection.cursor(cursor_factory=RealDictCursor)

            cursor.execute("SELECT * FROM users WHERE correo = %s", (correo,))
            user = cursor.fetchone()

            if user and check_password_hash(user['contrasena'], password):
                # Guardar sesión
                session['user_id'] = user['id']
                session['user_name'] = user['nombres']
                session['user_lastname'] = user['apellidos']
                flash("Inicio de sesión exitoso.", "success")
                return redirect(url_for('dashboard.dashboard'))
            else:
                flash("Correo o contraseña incorrectos.", "danger")

        except Exception as e:
            flash(f"Error en el login: {e}", "danger")
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
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

        connection = None
        cursor = None
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

        except Exception as e:
            flash(f"Error al registrar: {e}", "danger")
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for('auth.login'))

@auth_bp.route('/test_db_connection')
def test_db_connection():
    connection = None
    cursor = None
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("SET search_path TO public;")
        cursor.execute("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)
        tables = cursor.fetchall()
        return str(tables)
        # tables = cursor.fetchall()
        # table_names = [table[0] for table in tables]
        # return f"Conexión exitosa a la base de datos. Tablas: {', '.join(table_names)}"
    except Exception as e:
        return f"Error al conectar a la base de datos: {e}"
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()