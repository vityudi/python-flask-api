"""
Rotas de autenticação (login/logout)
"""
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from app import db, login_manager
from app.models import User

# Criar Blueprint para autenticação
auth_bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    """
    Carrega usuário pelo ID para o Flask-Login
    
    Args:
        user_id (str): ID do usuário
        
    Returns:
        User: Objeto do usuário ou None
    """
    return User.query.get(int(user_id))


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint para fazer login
    
    Request JSON:
        {
            "username": "string",
            "password": "string"
        }
    
    Returns:
        JSON: Resposta com status do login
    """
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"message": "Username and password are required"}), 400
        
        user = User.query.filter_by(
            username=data['username'], 
            password=data['password']
        ).first()
        
        if user:
            login_user(user)
            return jsonify({
                "message": "Login successful", 
                "user_id": user.id,
                "username": user.username
            }), 200
        
        return jsonify({"message": "Invalid credentials"}), 401
        
    except Exception as e:
        return jsonify({"message": f"Error during login: {str(e)}"}), 500


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Endpoint para fazer logout
    
    Returns:
        JSON: Resposta confirmando logout
    """
    try:
        logout_user()
        return jsonify({"message": "Logout successful"}), 200
    except Exception as e:
        return jsonify({"message": f"Error during logout: {str(e)}"}), 500


@auth_bp.route('/api/user/register', methods=['POST'])
def register():
    """
    Endpoint para registrar novo usuário
    
    Request JSON:
        {
            "username": "string",
            "email": "string",
            "password": "string"
        }
    
    Returns:
        JSON: Resposta com status do registro
    """
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['username', 'email', 'password']):
            return jsonify({"message": "Username, email and password are required"}), 400
        
        # Verificar se usuário já existe
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"message": "Username already exists"}), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"message": "Email already exists"}), 409
        
        # Criar novo usuário
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']  # Em produção, usar hash da senha
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            "message": "User registered successfully",
            "user_id": user.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error during registration: {str(e)}"}), 500
