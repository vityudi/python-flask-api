"""
Rotas para gerenciamento de pedidos da API

Este módulo contém todas as rotas relacionadas ao gerenciamento de pedidos,
incluindo criação, listagem, atualização de status e detalhes dos pedidos.
"""
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from decimal import Decimal
from datetime import datetime

from app import db, get_models

# Criar blueprint para rotas de pedidos
orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/', methods=['GET'])
@login_required
def get_orders():
    """
    Lista todos os pedidos do usuário logado
    
    Query Parameters:
        - status (str): Filtrar por status (opcional)
        - page (int): Número da página (padrão: 1)
        - per_page (int): Itens por página (padrão: 10)
    
    Returns:
        JSON: Lista de pedidos do usuário
    """
    try:
        models = get_models()
        Order = models['Order']
        
        # Parâmetros de consulta
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)  # Máximo 100 por página
        
        # Construir consulta
        query = Order.query.filter_by(user_id=current_user.id)
        
        if status:
            query = query.filter_by(status=status)
        
        # Ordenar por data de criação (mais recente primeiro)
        query = query.order_by(Order.created_at.desc())
        
        # Paginação
        orders = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': {
                'orders': [order.to_dict() for order in orders.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': orders.total,
                    'pages': orders.pages,
                    'has_next': orders.has_next,
                    'has_prev': orders.has_prev
                }
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar pedidos: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@orders_bp.route('/<int:order_id>', methods=['GET'])
@login_required
def get_order(order_id):
    """
    Obtém detalhes de um pedido específico
    
    Args:
        order_id (int): ID do pedido
    
    Returns:
        JSON: Detalhes do pedido
    """
    try:
        models = get_models()
        Order = models['Order']
        
        order = Order.query.filter_by(
            id=order_id, 
            user_id=current_user.id
        ).first()
        
        if not order:
            return jsonify({
                'success': False,
                'message': 'Pedido não encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': order.to_dict()
        })
        
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar pedido {order_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@orders_bp.route('/', methods=['POST'])
@login_required
def create_order():
    """
    Cria um novo pedido a partir dos itens do carrinho
    
    Returns:
        JSON: Dados do pedido criado
    """
    try:
        models = get_models()
        Order = models['Order']
        OrderItem = models['OrderItem']
        CartItem = models['CartItem']
        Product = models['Product']
        
        # Buscar itens do carrinho do usuário
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        
        if not cart_items:
            return jsonify({
                'success': False,
                'message': 'Carrinho vazio'
            }), 400
        
        # Verificar estoque dos produtos
        for cart_item in cart_items:
            if not cart_item.product.is_in_stock(cart_item.quantity):
                return jsonify({
                    'success': False,
                    'message': f'Produto "{cart_item.product.name}" não possui estoque suficiente'
                }), 400
        
        # Criar novo pedido
        order = Order(
            user_id=current_user.id,
            total=Decimal('0.00'),
            status='pending'
        )
        db.session.add(order)
        db.session.flush()  # Para obter o ID do pedido
        
        total = Decimal('0.00')
        
        # Criar itens do pedido
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
            
            # Reduzir estoque
            cart_item.product.reduce_stock(cart_item.quantity)
            
            # Calcular total
            total += cart_item.product.price * cart_item.quantity
        
        # Atualizar total do pedido
        order.total = total
        
        # Limpar carrinho
        CartItem.query.filter_by(user_id=current_user.id).delete()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Pedido criado com sucesso',
            'data': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar pedido: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@orders_bp.route('/<int:order_id>/cancel', methods=['PUT'])
@login_required
def cancel_order(order_id):
    """
    Cancela um pedido (apenas se estiver pendente)
    
    Args:
        order_id (int): ID do pedido
    
    Returns:
        JSON: Confirmação do cancelamento
    """
    try:
        models = get_models()
        Order = models['Order']
        Product = models['Product']
        
        order = Order.query.filter_by(
            id=order_id, 
            user_id=current_user.id
        ).first()
        
        if not order:
            return jsonify({
                'success': False,
                'message': 'Pedido não encontrado'
            }), 404
        
        if order.status != 'pending':
            return jsonify({
                'success': False,
                'message': 'Apenas pedidos pendentes podem ser cancelados'
            }), 400
        
        # Restaurar estoque dos produtos
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock += item.quantity
        
        # Atualizar status do pedido
        order.status = 'cancelled'
        order.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Pedido cancelado com sucesso',
            'data': order.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao cancelar pedido {order_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@orders_bp.route('/<int:order_id>/status', methods=['PUT'])
@login_required
def update_order_status(order_id):
    """
    Atualiza o status de um pedido (apenas para administradores)
    
    Args:
        order_id (int): ID do pedido
    
    Body (JSON):
        - status (str): Novo status do pedido
    
    Returns:
        JSON: Dados do pedido atualizado
    """
    try:
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({
                'success': False,
                'message': 'Status é obrigatório'
            }), 400
        
        new_status = data['status']
        valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
        
        if new_status not in valid_statuses:
            return jsonify({
                'success': False,
                'message': f'Status inválido. Valores válidos: {", ".join(valid_statuses)}'
            }), 400
        
        models = get_models()
        Order = models['Order']
        
        # Por enquanto, qualquer usuário pode atualizar o status
        # Em uma implementação real, verificaria se é admin
        order = Order.query.get(order_id)
        
        if not order:
            return jsonify({
                'success': False,
                'message': 'Pedido não encontrado'
            }), 404
        
        order.status = new_status
        order.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Status do pedido atualizado com sucesso',
            'data': order.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao atualizar status do pedido {order_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500
