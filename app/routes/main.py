"""
Rotas principais da aplicação
"""
from flask import Blueprint, jsonify

# Criar Blueprint para rotas principais
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def hello_world():
    """
    Endpoint principal da aplicação
    
    Returns:
        JSON: Mensagem de boas-vindas e informações da API
    """
    return jsonify({
        "message": "Welcome to E-commerce API",
        "version": "1.0.0",
        "endpoints": {
            "auth": {
                "login": "POST /login",
                "logout": "POST /logout", 
                "register": "POST /api/user/register"
            },
            "products": {
                "list": "GET /api/products",
                "get": "GET /api/products/{id}",
                "search": "GET /api/products/search?q={term}",
                "add": "POST /api/products/add",
                "update": "PUT /api/products/update/{id}",
                "delete": "DELETE /api/products/delete/{id}"
            },
            "cart": {
                "view": "GET /api/cart",
                "add": "POST /api/cart/add/{product_id}",
                "remove": "DELETE /api/cart/remove/{product_id}",
                "update": "PUT /api/cart/update/{product_id}",
                "clear": "POST /api/cart/clear",
                "checkout": "POST /api/cart/checkout",
                "total": "GET /api/cart/total"
            }
        }
    }), 200


@main_bp.route('/health')
def health_check():
    """
    Endpoint para verificação de saúde da aplicação
    
    Returns:
        JSON: Status da aplicação
    """
    return jsonify({
        "status": "healthy",
        "message": "E-commerce API is running"
    }), 200
