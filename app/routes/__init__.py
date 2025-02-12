from flask import Blueprint

# Importar los Blueprints
from app.routes.auth_routes import auth_bp
from app.routes.data_routes import data_bp
from app.routes.upload_routes import upload_bp
from app.routes.dashboard_routes import dashboard_bp 
from app.routes.reports_routes import reports_bp 


# Lista de Blueprints
blueprints = [auth_bp, data_bp, upload_bp, dashboard_bp, reports_bp]
