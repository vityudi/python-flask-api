"""
Configurações da aplicação Flask
"""
import os
from datetime import timedelta


class Config:
    """
    Configuração base da aplicação
    """
    # Configurações básicas do Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave123'
    
    # Configurações do banco de dados
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///ecommerce.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de sessão
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    
    # Configurações de CORS
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]


class DevelopmentConfig(Config):
    """
    Configuração para desenvolvimento
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Log de queries SQL


class ProductionConfig(Config):
    """
    Configuração para produção
    """
    DEBUG = False
    
    # Use variáveis de ambiente para configurações sensíveis
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    def __init__(self):
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable must be set for production")


class TestingConfig(Config):
    """
    Configuração para testes
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
