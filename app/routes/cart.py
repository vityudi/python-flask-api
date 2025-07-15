"""
Rotas para gerenciamento do carrinho de compras
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Product, CartItem

# Criar Blueprint para carrinho
cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')


@cart_bp.route('', methods=['GET'])
@login_required
def get_cart():
    """
    Endpoint para obter itens do carrinho do usuário atual
    
    Returns:
        JSON: Lista de itens no carrinho com detalhes dos produtos
    """
    try:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        return jsonify([item.to_dict() for item in cart_items]), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching cart: {str(e)}"}), 500


@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """
    Endpoint para adicionar produto ao carrinho
    
    Args:
        product_id (int): ID do produto
    
    Request JSON (opcional):
        {
            "quantity": int (padrão: 1)
        }
    
    Returns:
        JSON: Resposta com status da operação
    """
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"message": "Product not found"}), 404
        
        data = request.get_json() or {}
        quantity = data.get('quantity', 1)
        
        if not isinstance(quantity, int) or quantity <= 0:
            return jsonify({"message": "Quantity must be a positive integer"}), 400
        
        # Verificar se o item já existe no carrinho
        existing_item = CartItem.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first()
        
        if existing_item:
            # Se já existe, aumentar a quantidade
            existing_item.quantity += quantity
            db.session.commit()
            return jsonify({
                "message": "Product quantity updated in cart",
                "cart_item": existing_item.to_dict()
            }), 200
        else:
            # Se não existe, criar novo item
            cart_item = CartItem(
                user_id=current_user.id, 
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
            db.session.commit()
            
            return jsonify({
                "message": "Product added to cart",
                "cart_item": cart_item.to_dict()
            }), 201
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error adding to cart: {str(e)}"}), 500


@cart_bp.route('/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_cart(product_id):
    """
    Endpoint para remover produto do carrinho
    
    Args:
        product_id (int): ID do produto
    
    Returns:
        JSON: Resposta com status da operação
    """
    try:
        cart_item = CartItem.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first()
        
        if not cart_item:
            return jsonify({"message": "Cart item not found"}), 404
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({"message": "Product removed from cart"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error removing from cart: {str(e)}"}), 500


@cart_bp.route('/update/<int:product_id>', methods=['PUT'])
@login_required
def update_cart_item(product_id):
    """
    Endpoint para atualizar quantidade de item no carrinho
    
    Args:
        product_id (int): ID do produto
    
    Request JSON:
        {
            "quantity": int
        }
    
    Returns:
        JSON: Resposta com status da operação
    """
    try:
        data = request.get_json()
        if not data or 'quantity' not in data:
            return jsonify({"message": "Quantity is required"}), 400
        
        quantity = data['quantity']
        if not isinstance(quantity, int) or quantity <= 0:
            return jsonify({"message": "Quantity must be a positive integer"}), 400
        
        cart_item = CartItem.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first()
        
        if not cart_item:
            return jsonify({"message": "Cart item not found"}), 404
        
        cart_item.quantity = quantity
        db.session.commit()
        
        return jsonify({
            "message": "Cart item updated successfully",
            "cart_item": cart_item.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating cart item: {str(e)}"}), 500


@cart_bp.route('/clear', methods=['POST'])
@login_required
def clear_cart():
    """
    Endpoint para limpar todo o carrinho do usuário
    
    Returns:
        JSON: Resposta confirmando limpeza do carrinho
    """
    try:
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        return jsonify({"message": "Cart cleared successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error clearing cart: {str(e)}"}), 500


@cart_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    """
    Endpoint para finalizar compra (checkout)
    
    Returns:
        JSON: Resposta com status do checkout
    """
    try:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        
        if not cart_items:
            return jsonify({"message": "Cart is empty"}), 400
        
        # Calcular total da compra
        total = 0
        order_items = []
        
        for item in cart_items:
            if item.product:
                item_total = item.product.price * item.quantity
                total += item_total
                order_items.append({
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "unit_price": item.product.price,
                    "total_price": item_total
                })
        
        # Remover itens do carrinho após checkout
        for item in cart_items:
            db.session.delete(item)
        
        db.session.commit()
        
        return jsonify({
            "message": "Checkout successful",
            "order_summary": {
                "items": order_items,
                "total": round(total, 2),
                "item_count": len(order_items)
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error during checkout: {str(e)}"}), 500


@cart_bp.route('/total', methods=['GET'])
@login_required
def get_cart_total():
    """
    Endpoint para obter total do carrinho
    
    Returns:
        JSON: Total do carrinho e contagem de itens
    """
    try:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        
        total = 0
        item_count = 0
        
        for item in cart_items:
            if item.product:
                total += item.product.price * item.quantity
                item_count += item.quantity
        
        return jsonify({
            "total": round(total, 2),
            "item_count": item_count
        }), 200
        
    except Exception as e:
        return jsonify({"message": f"Error calculating cart total: {str(e)}"}), 500
