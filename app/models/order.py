"""
Modelos de pedidos para a aplicação E-commerce
"""
from datetime import datetime
from app import db


class Order(db.Model):
    """
    Modelo para pedidos
    
    Attributes:
        id (int): Identificador único do pedido
        user_id (int): ID do usuário que fez o pedido
        total (decimal): Valor total do pedido
        status (str): Status do pedido
        created_at (datetime): Data de criação do pedido
        updated_at (datetime): Data de última atualização
        items (relationship): Relacionamento com itens do pedido
    """
    __tablename__ = 'orders'
    
    # Status possíveis do pedido
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0.0)
    status = db.Column(db.String(50), default=PENDING, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relacionamentos
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Order {self.id} - {self.status}>'
    
    @property
    def items_count(self):
        """Retorna a quantidade total de itens no pedido"""
        return sum(item.quantity for item in self.items)
    
    def to_dict(self):
        """
        Converte o objeto Order para dicionário
        
        Returns:
            dict: Dados do pedido
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'total': float(self.total),
            'status': self.status,
            'items_count': self.items_count,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def calculate_total(self):
        """
        Calcula o total do pedido baseado nos itens
        
        Returns:
            float: Valor total do pedido
        """
        total = sum(item.get_total_price() for item in self.items)
        self.total = total
        return total


class OrderItem(db.Model):
    """
    Modelo para itens de um pedido
    
    Attributes:
        id (int): Identificador único do item
        order_id (int): ID do pedido
        product_id (int): ID do produto
        quantity (int): Quantidade do produto
        price (decimal): Preço unitário no momento do pedido
    """
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Preço no momento do pedido

    def __repr__(self):
        return f'<OrderItem Order:{self.order_id} Product:{self.product_id}>'
    
    def to_dict(self):
        """
        Converte o objeto OrderItem para dicionário
        
        Returns:
            dict: Dados do item do pedido
        """
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'quantity': self.quantity,
            'price': float(self.price),
            'total_price': self.get_total_price()
        }
    
    def get_total_price(self):
        """
        Calcula o preço total do item (preço unitário * quantidade)
        
        Returns:
            float: Preço total do item
        """
        return float(self.price) * self.quantity
