"""
Modelo de categoria para a aplicação E-commerce
"""
from datetime import datetime
from app import db


class Category(db.Model):
    """
    Modelo para categorias de produtos
    
    Attributes:
        id (int): Identificador único da categoria
        name (str): Nome da categoria
        description (str): Descrição da categoria
        created_at (datetime): Data de criação
        products (relationship): Relacionamento com produtos da categoria
    """
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relacionamentos
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self):
        """
        Converte o objeto Category para dicionário
        
        Returns:
            dict: Dados da categoria
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'products_count': len(self.products)
        }
