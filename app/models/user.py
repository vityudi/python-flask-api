"""
Modelo de usuário para a aplicação E-commerce
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db


class User(db.Model, UserMixin):
    """
    Modelo para usuários do sistema
    
    Attributes:
        id (int): Identificador único do usuário
        username (str): Nome de usuário único
        email (str): Email único do usuário
        password_hash (str): Senha hasheada do usuário
        is_active (bool): Status ativo do usuário
        created_at (datetime): Data de criação
        cart (relationship): Relacionamento com itens do carrinho
        orders (relationship): Relacionamento com pedidos do usuário
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relacionamentos
    cart = db.relationship('CartItem', backref='user', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """
        Define a senha do usuário (hasheada)
        
        Args:
            password (str): Senha em texto plano
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verifica se a senha fornecida está correta
        
        Args:
            password (str): Senha em texto plano
            
        Returns:
            bool: True se a senha estiver correta
        """
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """
        Converte o objeto User para dicionário
        
        Returns:
            dict: Dados do usuário (sem senha)
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }
