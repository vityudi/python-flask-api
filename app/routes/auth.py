"""
Rotas de autenticação da API

Este módulo contém todas as rotas relacionadas à autenticação de usuários,
incluindo registro, login, logout e gerenciamento de sessões.
"""
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from app import db, get_models

# Criar blueprint para rotas de autenticação
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registra um novo usuário no sistema
    
    Body (JSON):
        - username (str): Nome de usuário único
        - email (str): Email único do usuário
        - password (str): Senha do usuário
    
    Returns:
        JSON: Dados do usuário criado ou erro
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Validações
        if not username or len(username) < 3:
            return jsonify({'error': 'Username deve ter pelo menos 3 caracteres'}), 400
        
        if not email or '@' not in email:
            return jsonify({'error': 'Email inválido'}), 400
        
        if not password or len(password) < 6:
            return jsonify({'error': 'Senha deve ter pelo menos 6 caracteres'}), 400
        
        models = get_models()
        User = models['User']
        
        # Verificar se usuário já existe
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username já existe'}), 409
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email já está em uso'}), 409
        
        # Criar novo usuário
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuário criado com sucesso',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erro no registro: {str(e)}')
        return jsonify({'error': 'Erro interno do servidor'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Realiza login do usuário
    
    Body (JSON):
        - username (str): Nome de usuário ou email
        - password (str): Senha do usuário
    
    Returns:
        JSON: Dados do usuário logado ou erro
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': 'Username e senha são obrigatórios'}), 400
        
        models = get_models()
        User = models['User']
        
        # Buscar usuário por username ou email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Credenciais inválidas'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Conta desativada'}), 403
        
        # Fazer login
        login_user(user)
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Erro no login: {str(e)}')
        return jsonify({'error': 'Erro interno do servidor'}), 500


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Realiza logout do usuário atual
    
    Returns:
        JSON: Mensagem de confirmação
    """
    try:
        logout_user()
        return jsonify({'message': 'Logout realizado com sucesso'}), 200
        
    except Exception as e:
        current_app.logger.error(f'Erro no logout: {str(e)}')
        return jsonify({'error': 'Erro interno do servidor'}), 500


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """
    Retorna dados do usuário atual
    
    Returns:
        JSON: Dados do usuário logado
    """
    try:
        return jsonify({
            'user': current_user.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Erro ao buscar usuário atual: {str(e)}')
        return jsonify({'error': 'Erro interno do servidor'}), 500


@auth_bp.route('/users', methods=['GET'])
@login_required
def list_users():
    """
    Lista todos os usuários (apenas para demonstração)
    
    Returns:
        JSON: Lista de usuários
    """
    try:
        models = get_models()
        User = models['User']
        
        users = User.query.all()
        
        return jsonify({
            'users': [user.to_dict() for user in users],
            'total': len(users)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Erro ao listar usuários: {str(e)}')
        return jsonify({'error': 'Erro interno do servidor'}), 500
