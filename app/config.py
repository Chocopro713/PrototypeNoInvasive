import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables desde .env

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")  # Clave de seguridad
    UPLOAD_FOLDER = 'uploads/'

    # Configuración de la base de datos
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
