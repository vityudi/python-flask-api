"""
Modelo de carrinho para a aplicação E-commerce
"""
from datetime import datetime
from app import db


class CartItem(db.Model):
    """
    Modelo para itens no carrinho de compras
    
    Attributes:
        id (int): Identificador único do item no carrinho
        user_id (int): ID do usuário proprietário do carrinho
        product_id (int): ID do produto no carrinho
        quantity (int): Quantidade do produto (padrão: 1)
        created_at (datetime): Data de criação
    """
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Constraint para evitar duplicatas
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_user_product'),)

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
            'product_name': self.product.name if self.product else None,
            'product_price': float(self.product.price) if self.product else 0,
            'quantity': self.quantity,
            'total_price': self.get_total_price(),
            'created_at': self.created_at.isoformat()
        }
    
    def get_total_price(self):
        """
        Calcula o preço total do item (preço unitário * quantidade)
        
        Returns:
            float: Preço total do item
        """
        if self.product:
            return float(self.product.price) * self.quantity
        return 0.0
