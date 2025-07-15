"""
Rotas de gerenciamento do carrinho de compras

Este módulo contém todas as rotas relacionadas ao carrinho de compras,
incluindo adicionar, remover, atualizar e finalizar compra.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db, get_models

# Criar blueprint para rotas do carrinho
cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/', methods=['GET'])
@login_required
def get_cart():
    """
    Obtém todos os itens do carrinho do usuário atual
    
    Returns:
        JSON: Lista de itens no carrinho com detalhes dos produtos
    """
    try:
        models = get_models()
        CartItem = models['CartItem']
        
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        return jsonify({
            'success': True,
            'data': [item.to_dict() for item in cart_items]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar carrinho: {str(e)}'
        }), 500


@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """
    Adiciona um produto ao carrinho
    
    Args:
        product_id (int): ID do produto
    
    Body (JSON) (opcional):
        - quantity (int): Quantidade (padrão: 1)
    
    Returns:
        JSON: Resposta com status da operação
    """
    try:
        models = get_models()
        Product = models['Product']
        CartItem = models['CartItem']
        
        product = Product.query.get(product_id)
        if not product:
            return jsonify({
                'success': False,
                'message': 'Produto não encontrado'
            }), 404
        
        data = request.get_json() or {}
        quantity = data.get('quantity', 1)
        
        if not isinstance(quantity, int) or quantity <= 0:
            return jsonify({
                'success': False,
                'message': 'Quantidade deve ser um número inteiro positivo'
            }), 400
        
        # Verificar estoque
        if not product.is_available(quantity):
            return jsonify({
                'success': False,
                'message': 'Produto sem estoque suficiente'
            }), 400
        
        # Verificar se o item já existe no carrinho
        existing_item = CartItem.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first()
        
        if existing_item:
            # Se já existe, verificar se a nova quantidade total não excede o estoque
            new_total_quantity = existing_item.quantity + quantity
            if not product.is_available(new_total_quantity):
                return jsonify({
                    'success': False,
                    'message': 'Quantidade total excede o estoque disponível'
                }), 400
            
            existing_item.quantity = new_total_quantity
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Quantidade do produto atualizada no carrinho',
                'data': existing_item.to_dict()
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
                'success': True,
                'message': 'Produto adicionado ao carrinho',
                'data': cart_item.to_dict()
            }), 201
            
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao adicionar ao carrinho: {str(e)}'
        }), 500


@cart_bp.route('/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_cart(product_id):
    """
    Remove um produto do carrinho
    
    Args:
        product_id (int): ID do produto
    
    Returns:
        JSON: Resposta com status da operação
    """
    try:
        models = get_models()
        CartItem = models['CartItem']
        
        cart_item = CartItem.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first()
        
        if not cart_item:
            return jsonify({
                'success': False,
                'message': 'Item não encontrado no carrinho'
            }), 404
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Produto removido do carrinho'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao remover do carrinho: {str(e)}'
        }), 500


@cart_bp.route('/update/<int:product_id>', methods=['PUT'])
@login_required
def update_cart_item(product_id):
    """
    Atualiza a quantidade de um item no carrinho
    
    Args:
        product_id (int): ID do produto
    
    Body (JSON):
        - quantity (int): Nova quantidade
    
    Returns:
        JSON: Resposta com status da operação
    """
    try:
        data = request.get_json()
        if not data or 'quantity' not in data:
            return jsonify({
                'success': False,
                'message': 'Quantidade é obrigatória'
            }), 400
        
        quantity = data['quantity']
        if not isinstance(quantity, int) or quantity <= 0:
            return jsonify({
                'success': False,
                'message': 'Quantidade deve ser um número inteiro positivo'
            }), 400
        
        models = get_models()
        CartItem = models['CartItem']
        Product = models['Product']
        
        cart_item = CartItem.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first()
        
        if not cart_item:
            return jsonify({
                'success': False,
                'message': 'Item não encontrado no carrinho'
            }), 404
        
        # Verificar estoque
        if not cart_item.product.is_available(quantity):
            return jsonify({
                'success': False,
                'message': 'Quantidade excede o estoque disponível'
            }), 400
        
        cart_item.quantity = quantity
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Item do carrinho atualizado com sucesso',
            'data': cart_item.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao atualizar item do carrinho: {str(e)}'
        }), 500


@cart_bp.route('/clear', methods=['POST'])
@login_required
def clear_cart():
    """
    Limpa todo o carrinho do usuário
    
    Returns:
        JSON: Resposta confirmando limpeza do carrinho
    """
    try:
        models = get_models()
        CartItem = models['CartItem']
        
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Carrinho limpo com sucesso'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao limpar carrinho: {str(e)}'
        }), 500


@cart_bp.route('/total', methods=['GET'])
@login_required
def get_cart_total():
    """
    Obtém o total do carrinho e contagem de itens
    
    Returns:
        JSON: Total do carrinho e contagem de itens
    """
    try:
        models = get_models()
        CartItem = models['CartItem']
        
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        
        total = 0
        item_count = 0
        
        for item in cart_items:
            if item.product:
                total += item.get_total_price()
                item_count += item.quantity
        
        return jsonify({
            'success': True,
            'data': {
                'total': round(total, 2),
                'item_count': item_count,
                'unique_items': len(cart_items)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao calcular total do carrinho: {str(e)}'
        }), 500
