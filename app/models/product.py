"""
Modelo de produto para a aplicação E-commerce
"""
from datetime import datetime
from app import db


class Product(db.Model):
    """
    Modelo para produtos do e-commerce
    
    Attributes:
        id (int): Identificador único do produto
        name (str): Nome do produto
        price (decimal): Preço do produto
        description (str): Descrição do produto
        stock (int): Quantidade em estoque
        category_id (int): ID da categoria do produto
        is_active (bool): Status ativo do produto
        created_at (datetime): Data de criação
        updated_at (datetime): Data de última atualização
        cart_items (relationship): Relacionamento com itens do carrinho
        order_items (relationship): Relacionamento com itens de pedidos
    """
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relacionamentos
    cart_items = db.relationship('CartItem', backref='product', lazy=True, cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

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
            'description': self.description,
            'price': float(self.price),
            'stock': self.stock,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def is_available(self, quantity=1):
        """
        Verifica se o produto está disponível na quantidade solicitada
        
        Args:
            quantity (int): Quantidade desejada
            
        Returns:
            bool: True se disponível
        """
        return self.stock >= quantity and self.is_active
    
    def reduce_stock(self, quantity):
        """
        Reduz o estoque do produto
        
        Args:
            quantity (int): Quantidade a ser reduzida
            
        Returns:
            bool: True se a operação foi bem-sucedida
        """
        if self.is_available(quantity):
            self.stock -= quantity
            return True
        return False
