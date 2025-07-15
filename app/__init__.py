"""
Inicialização da aplicação Flask E-commerce API

Este módulo configura e inicializa a aplicação Flask com todas as suas extensões,
blueprints e configurações necessárias.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
import os
import sys

# Adicionar o diretório pai ao path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Inicializar extensões
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name=None):
    """
    Factory function para criar e configurar a aplicação Flask
    
    Args:
        config_name (str): Nome da configuração a ser usada
        
    Returns:
        Flask: Instância configurada da aplicação
    """
    app = Flask(__name__)
    
    # Carregar configurações
    if config_name is None:
        config_name = 'development'
    
    from config import config
    app.config.from_object(config[config_name])
    
    # Inicializar extensões com a aplicação
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app)
    
    # Criar modelos após inicializar o db
    from app.models import get_all_models
    
    # Configurar Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # Registrar blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.cart import cart_bp
    from app.routes.orders import orders_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    
    # Criar tabelas do banco de dados
    with app.app_context():
        db.create_all()
        
        # Criar dados iniciais se necessário
        create_initial_data()
    
    return app


def create_initial_data():
    """
    Cria dados iniciais no banco de dados se ele estiver vazio
    """
    from app.models import Category, Product, User
    
    # Verificar se já existem categorias
    if Category.query.count() == 0:
        # Criar categorias padrão
        categories = [
            Category(name='Eletrônicos', description='Produtos eletrônicos e gadgets'),
            Category(name='Roupas', description='Vestuário e acessórios'),
            Category(name='Casa', description='Itens para casa e decoração'),
            Category(name='Livros', description='Livros e materiais educativos'),
            Category(name='Esportes', description='Equipamentos esportivos e fitness')
        ]
        
        for category in categories:
            db.session.add(category)
        
        db.session.commit()
        
        # Criar produtos de exemplo
        electronics = Category.query.filter_by(name='Eletrônicos').first()
        clothes = Category.query.filter_by(name='Roupas').first()
        
        products = [
            Product(
                name='Smartphone XYZ',
                description='Smartphone com 128GB de armazenamento',
                price=899.99,
                stock=50,
                category_id=electronics.id
            ),
            Product(
                name='Notebook ABC',
                description='Notebook para trabalho e estudos',
                price=2499.99,
                stock=25,
                category_id=electronics.id
            ),
            Product(
                name='Camiseta Básica',
                description='Camiseta 100% algodão',
                price=29.99,
                stock=100,
                category_id=clothes.id
            ),
            Product(
                name='Jeans Premium',
                description='Calça jeans de alta qualidade',
                price=89.99,
                stock=75,
                category_id=clothes.id
            )
        ]
        
        for product in products:
            db.session.add(product)
        
        db.session.commit()
    
    # Criar usuário admin se não existir
    if User.query.filter_by(username='admin').first() is None:
        admin_user = User(
            username='admin',
            email='admin@example.com'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()


def get_models():
    """Retorna os modelos da aplicação"""
    from app.models import get_all_models
    return get_all_models()
