import mysql.connector
from flask import current_app

def create_db_connection():
    return mysql.connector.connect(
        host=current_app.config['MYSQL_HOST'],
        database=current_app.config['MYSQL_DATABASE'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD']
    )
