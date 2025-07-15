"""
Módulo de modelos da aplicação E-commerce

Este módulo centraliza a importação de todos os modelos de dados
da aplicação, facilitando o acesso e a organização.
"""

# Importar todos os modelos
from .user import User
from .category import Category
from .product import Product
from .cart import CartItem
from .order import Order, OrderItem

# Lista de todos os modelos para facilitar importação
__all__ = [
    'User',
    'Category', 
    'Product',
    'CartItem',
    'Order',
    'OrderItem'
]


def get_all_models():
    """
    Retorna um dicionário com todos os modelos da aplicação
    
    Returns:
        dict: Dicionário com nome do modelo como chave e classe como valor
    """
    return {
        'User': User,
        'Category': Category,
        'Product': Product,
        'CartItem': CartItem,
        'Order': Order,
        'OrderItem': OrderItem
    }


# Manter compatibilidade com a função create_models existente
def create_models(db):
    """
    Função para manter compatibilidade com o código existente
    
    Args:
        db: Instância do SQLAlchemy (não utilizada mais)
        
    Returns:
        dict: Dicionário com todos os modelos
    """
    return get_all_models()
