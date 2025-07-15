"""
Ponto de entrada principal da aplicação Flask E-commerce API

Este arquivo inicializa e executa a aplicação Flask.
Execute este arquivo para iniciar o servidor de desenvolvimento.

Usage:
    python run.py
"""
from app import create_app

# Criar instância da aplicação
app = create_app()

if __name__ == '__main__':
    print("🚀 Starting E-commerce API...")
    print("📖 API Documentation available at: http://127.0.0.1:5000/")
    print("🏥 Health check available at: http://127.0.0.1:5000/health")
    
    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000
    )
