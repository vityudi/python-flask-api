"""
Modelos de dados para a aplicação E-commerce
"""
from flask_login import UserMixin
from app import db


class User(db.Model, UserMixin):
    """
    Modelo para usuários do sistema
    
    Attributes:
        id (int): Identificador único do usuário
        username (str): Nome de usuário único
        email (str): Email único do usuário
        password (str): Senha do usuário (deve ser hasheada em produção)
        cart (relationship): Relacionamento com itens do carrinho
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    
    # Relacionamentos
    cart = db.relationship('CartItem', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """
        Converte o objeto User para dicionário
        
        Returns:
            dict: Dados do usuário (sem senha)
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }


class Product(db.Model):
    """
    Modelo para produtos do e-commerce
    
    Attributes:
        id (int): Identificador único do produto
        name (str): Nome do produto
        price (float): Preço do produto
        description (str): Descrição do produto
    """
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        """
        Converte o objeto Product para dicionário
        
        Returns:
            dict: Dados do produto
        """
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description
        }


class CartItem(db.Model):
    """
    Modelo para itens no carrinho de compras
    
    Attributes:
        id (int): Identificador único do item no carrinho
        user_id (int): ID do usuário proprietário do carrinho
        product_id (int): ID do produto no carrinho
        quantity (int): Quantidade do produto (padrão: 1)
    """
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    
    # Relacionamentos
    product = db.relationship('Product', backref='cart_items')

    def __repr__(self):
        return f'<CartItem User:{self.user_id} Product:{self.product_id}>'
    
    def to_dict(self):
        """
        Converte o objeto CartItem para dicionário
        
        Returns:
            dict: Dados do item do carrinho
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'product': self.product.to_dict() if self.product else None
        }
