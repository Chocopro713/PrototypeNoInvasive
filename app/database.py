import psycopg2
from flask import current_app

def create_db_connection():
    return psycopg2.connect(
        host=current_app.config['POSTGRES_HOST'],
        database=current_app.config['POSTGRES_DB'],
        user=current_app.config['POSTGRES_USER'],
        password=current_app.config['POSTGRES_PASSWORD']
    )
