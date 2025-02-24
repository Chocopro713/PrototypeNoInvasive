import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables desde .env

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")  # Clave de seguridad
    UPLOAD_FOLDER = 'uploads/'

    # Configuración de la base de datos para PostgreSQL
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
