"""
Rotas para gerenciamento de produtos
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required
from app import db
from app.models import Product

# Criar Blueprint para produtos
products_bp = Blueprint('products', __name__, url_prefix='/api/products')


@products_bp.route('', methods=['GET'])
def get_products():
    """
    Endpoint para listar todos os produtos
    
    Returns:
        JSON: Lista de produtos
    """
    try:
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching products: {str(e)}"}), 500


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    """
    Endpoint para obter detalhes de um produto específico
    
    Args:
        product_id (int): ID do produto
    
    Returns:
        JSON: Detalhes do produto
    """
    try:
        product = Product.query.get(product_id)
        if product:
            return jsonify(product.to_dict()), 200
        return jsonify({"message": "Product not found"}), 404
    except Exception as e:
        return jsonify({"message": f"Error fetching product: {str(e)}"}), 500


@products_bp.route('/add', methods=['POST'])
@login_required
def add_product():
    """
    Endpoint para adicionar um novo produto
    
    Request JSON:
        {
            "name": "string",
            "price": float,
            "description": "string" (opcional)
        }
    
    Returns:
        JSON: Resposta com status da operação
    """
    try:
        data = request.get_json()
        
        if not data or 'name' not in data or 'price' not in data:
            return jsonify({"message": "Name and price are required"}), 400
        
        if not isinstance(data['price'], (int, float)) or data['price'] <= 0:
            return jsonify({"message": "Price must be a positive number"}), 400
        
        product = Product(
            name=data['name'],
            price=float(data['price']),
            description=data.get('description', '')
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            "message": "Product added successfully",
            "product": product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error adding product: {str(e)}"}), 500


@products_bp.route('/update/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    """
    Endpoint para atualizar um produto existente
    
    Args:
        product_id (int): ID do produto
    
    Request JSON:
        {
            "name": "string" (opcional),
            "price": float (opcional),
            "description": "string" (opcional)
        }
    
    Returns:
        JSON: Resposta com status da operação
    """
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"message": "Product not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        # Atualizar campos fornecidos
        if 'name' in data:
            product.name = data['name']
        
        if 'price' in data:
            if not isinstance(data['price'], (int, float)) or data['price'] <= 0:
                return jsonify({"message": "Price must be a positive number"}), 400
            product.price = float(data['price'])
        
        if 'description' in data:
            product.description = data['description']
        
        db.session.commit()
        
        return jsonify({
            "message": "Product updated successfully",
            "product": product.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating product: {str(e)}"}), 500


@products_bp.route('/delete/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    """
    Endpoint para deletar um produto
    
    Args:
        product_id (int): ID do produto
    
    Returns:
        JSON: Resposta com status da operação
    """
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"message": "Product not found"}), 404
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({"message": "Product deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting product: {str(e)}"}), 500


@products_bp.route('/search', methods=['GET'])
def search_products():
    """
    Endpoint para buscar produtos por nome
    
    Query Parameters:
        q (str): Termo de busca
    
    Returns:
        JSON: Lista de produtos que correspondem à busca
    """
    try:
        search_term = request.args.get('q', '').strip()
        
        if not search_term:
            return jsonify({"message": "Search term is required"}), 400
        
        products = Product.query.filter(
            Product.name.ilike(f'%{search_term}%')
        ).all()
        
        return jsonify([product.to_dict() for product in products]), 200
        
    except Exception as e:
        return jsonify({"message": f"Error searching products: {str(e)}"}), 500
