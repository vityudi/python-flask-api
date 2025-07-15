"""
Aplicação Flask para E-commerce API
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager

# Instâncias globais
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name=None):
    """
    Factory function para criar a aplicação Flask
    
    Args:
        config_name (str): Nome da configuração ('development', 'production', 'testing')
    
    Returns:
        Flask: Instância configurada da aplicação
    """
    app = Flask(__name__)
    
    # Carregar configurações
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    from config import config
    app.config.from_object(config.get(config_name, config['default']))
    
    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    CORS(app)
    
    # Registrar Blueprints
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.cart import cart_bp
    from app.routes.main import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(main_bp)
    
    # Criar tabelas no contexto da aplicação
    with app.app_context():
        db.create_all()
    
    return app
