"""
Rotas de gerenciamento de produtos

Este módulo contém todas as rotas relacionadas aos produtos,
incluindo listagem, criação, atualização, exclusão e busca.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required
from app import db, get_models

# Criar blueprint para rotas de produtos
products_bp = Blueprint('products', __name__)


@products_bp.route('/', methods=['GET'])
def get_all_products():
    """
    Lista todos os produtos disponíveis
    
    Query Parameters:
        - category_id (int): Filtrar por categoria (opcional)
        - active_only (bool): Apenas produtos ativos (padrão: true)
    
    Returns:
        JSON: Lista de produtos
    """
    try:
        models = get_models()
        Product = models['Product']
        
        # Parâmetros de consulta
        category_id = request.args.get('category_id', type=int)
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        # Construir consulta
        query = Product.query
        
        if active_only:
            query = query.filter_by(is_active=True)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        products = query.all()
        
        return jsonify({
            'success': True,
            'data': [product.to_dict() for product in products]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar produtos: {str(e)}'
        }), 500


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    """
    Obtém detalhes de um produto específico
    
    Args:
        product_id (int): ID do produto
    
    Returns:
        JSON: Detalhes do produto
    """
    try:
        models = get_models()
        Product = models['Product']
        
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({
                'success': False,
                'message': 'Produto não encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': product.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar produto: {str(e)}'
        }), 500


@products_bp.route('/', methods=['POST'])
@login_required
def create_product():
    """
    Cria um novo produto
    
    Body (JSON):
        - name (str): Nome do produto
        - description (str): Descrição do produto (opcional)
        - price (float): Preço do produto
        - stock (int): Quantidade em estoque (opcional, padrão: 0)
        - category_id (int): ID da categoria (opcional)
    
    Returns:
        JSON: Dados do produto criado
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados não fornecidos'
            }), 400
        
        # Validações
        name = data.get('name', '').strip()
        if not name:
            return jsonify({
                'success': False,
                'message': 'Nome do produto é obrigatório'
            }), 400
        
        try:
            price = float(data.get('price', 0))
            if price < 0:
                return jsonify({
                    'success': False,
                    'message': 'Preço deve ser um valor positivo'
                }), 400
        except (TypeError, ValueError):
            return jsonify({
                'success': False,
                'message': 'Preço deve ser um número válido'
            }), 400
        
        models = get_models()
        Product = models['Product']
        
        product = Product(
            name=name,
            description=data.get('description', ''),
            price=price,
            stock=data.get('stock', 0),
            category_id=data.get('category_id')
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Produto criado com sucesso',
            'data': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao criar produto: {str(e)}'
        }), 500


@products_bp.route('/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    """
    Atualiza um produto existente
    
    Args:
        product_id (int): ID do produto
    
    Body (JSON):
        - name (str): Nome do produto (opcional)
        - description (str): Descrição do produto (opcional)
        - price (float): Preço do produto (opcional)
        - stock (int): Quantidade em estoque (opcional)
        - category_id (int): ID da categoria (opcional)
        - is_active (bool): Status do produto (opcional)
    
    Returns:
        JSON: Dados do produto atualizado
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados não fornecidos'
            }), 400
        
        models = get_models()
        Product = models['Product']
        
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({
                'success': False,
                'message': 'Produto não encontrado'
            }), 404
        
        # Atualizar campos fornecidos
        if 'name' in data:
            name = data['name'].strip()
            if not name:
                return jsonify({
                    'success': False,
                    'message': 'Nome do produto não pode estar vazio'
                }), 400
            product.name = name
        
        if 'description' in data:
            product.description = data['description']
        
        if 'price' in data:
            try:
                price = float(data['price'])
                if price < 0:
                    return jsonify({
                        'success': False,
                        'message': 'Preço deve ser um valor positivo'
                    }), 400
                product.price = price
            except (TypeError, ValueError):
                return jsonify({
                    'success': False,
                    'message': 'Preço deve ser um número válido'
                }), 400
        
        if 'stock' in data:
            try:
                stock = int(data['stock'])
                if stock < 0:
                    return jsonify({
                        'success': False,
                        'message': 'Estoque deve ser um valor não negativo'
                    }), 400
                product.stock = stock
            except (TypeError, ValueError):
                return jsonify({
                    'success': False,
                    'message': 'Estoque deve ser um número inteiro válido'
                }), 400
        
        if 'category_id' in data:
            product.category_id = data['category_id']
        
        if 'is_active' in data:
            product.is_active = bool(data['is_active'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Produto atualizado com sucesso',
            'data': product.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao atualizar produto: {str(e)}'
        }), 500


@products_bp.route('/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    """
    Exclui um produto (soft delete - marca como inativo)
    
    Args:
        product_id (int): ID do produto
    
    Returns:
        JSON: Confirmação da exclusão
    """
    try:
        models = get_models()
        Product = models['Product']
        
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({
                'success': False,
                'message': 'Produto não encontrado'
            }), 404
        
        # Soft delete - apenas marcar como inativo
        product.is_active = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Produto removido com sucesso'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao remover produto: {str(e)}'
        }), 500


@products_bp.route('/search', methods=['GET'])
def search_products():
    """
    Busca produtos por nome
    
    Query Parameters:
        - q (str): Termo de busca
        - category_id (int): Filtrar por categoria (opcional)
    
    Returns:
        JSON: Lista de produtos encontrados
    """
    try:
        search_term = request.args.get('q', '').strip()
        category_id = request.args.get('category_id', type=int)
        
        if not search_term:
            return jsonify({
                'success': False,
                'message': 'Termo de busca é obrigatório'
            }), 400
        
        models = get_models()
        Product = models['Product']
        
        # Construir consulta de busca
        query = Product.query.filter(
            Product.name.ilike(f'%{search_term}%'),
            Product.is_active == True
        )
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        products = query.all()
        
        return jsonify({
            'success': True,
            'data': [product.to_dict() for product in products],
            'search_term': search_term,
            'results_count': len(products)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro na busca: {str(e)}'
        }), 500


@products_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Lista todas as categorias de produtos
    
    Returns:
        JSON: Lista de categorias
    """
    try:
        models = get_models()
        Category = models['Category']
        
        categories = Category.query.all()
        
        return jsonify({
            'success': True,
            'data': [category.to_dict() for category in categories]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar categorias: {str(e)}'
        }), 500
