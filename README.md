# E-commerce API

Uma API REST completa para e-commerce desenvolvida com Flask, incluindo autenticação, gerenciamento de produtos e carrinho de compras.

## 🚀 Funcionalidades

- **Autenticação**: Login, logout e registro de usuários
- **Produtos**: CRUD completo (criar, ler, atualizar, deletar) e busca
- **Carrinho**: Adicionar, remover, atualizar quantidades e checkout
- **Documentação**: Endpoints autodocumentados

## 📁 Estrutura do Projeto

```
python-flask-api/
├── app/                          # Pacote principal da aplicação
│   ├── __init__.py              # Factory da aplicação Flask
│   ├── models/                  # Modelos de dados
│   │   └── __init__.py         # User, Product, CartItem
│   └── routes/                  # Blueprints das rotas
│       ├── auth.py             # Autenticação (login/logout/register)
│       ├── cart.py             # Carrinho de compras
│       ├── main.py             # Rotas principais
│       └── products.py         # Gerenciamento de produtos
├── instance/                    # Arquivos de instância (banco de dados)
│   └── ecommerce.db            # Banco SQLite
├── config.py                   # Configurações da aplicação
├── requirements.txt            # Dependências do projeto
├── run.py                     # Ponto de entrada da aplicação
├── swagger.yaml               # Documentação OpenAPI
└── .gitignore                 # Arquivos ignorados pelo Git
```

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- pip

### Configuração do Ambiente

1. **Clone o repositório**:
   ```bash
   git clone <repository-url>
   cd python-flask-api
   ```

2. **Crie um ambiente virtual**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # ou
   source venv/bin/activate  # Linux/Mac
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**:
   ```bash
   python run.py
   ```

A API estará disponível em `http://127.0.0.1:5000`

## 📖 Documentação da API

### Autenticação

#### Registrar Usuário
```http
POST /api/user/register
Content-Type: application/json

{
  "username": "string",
  "email": "string", 
  "password": "string"
}
```

#### Login
```http
POST /login
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

#### Logout
```http
POST /logout
Authorization: Required (logged in user)
```

### Produtos

#### Listar Produtos
```http
GET /api/products
```

#### Obter Produto
```http
GET /api/products/{id}
```

#### Buscar Produtos
```http
GET /api/products/search?q={termo}
```

#### Adicionar Produto
```http
POST /api/products/add
Authorization: Required
Content-Type: application/json

{
  "name": "string",
  "price": number,
  "description": "string"
}
```

#### Atualizar Produto
```http
PUT /api/products/update/{id}
Authorization: Required
Content-Type: application/json

{
  "name": "string",
  "price": number,
  "description": "string"
}
```

#### Deletar Produto
```http
DELETE /api/products/delete/{id}
Authorization: Required
```

### Carrinho

#### Ver Carrinho
```http
GET /api/cart
Authorization: Required
```

#### Adicionar ao Carrinho
```http
POST /api/cart/add/{product_id}
Authorization: Required
Content-Type: application/json

{
  "quantity": number (opcional, padrão: 1)
}
```

#### Atualizar Quantidade
```http
PUT /api/cart/update/{product_id}
Authorization: Required
Content-Type: application/json

{
  "quantity": number
}
```

#### Remover do Carrinho
```http
DELETE /api/cart/remove/{product_id}
Authorization: Required
```

#### Limpar Carrinho
```http
POST /api/cart/clear
Authorization: Required
```

#### Checkout
```http
POST /api/cart/checkout
Authorization: Required
```

#### Total do Carrinho
```http
GET /api/cart/total
Authorization: Required
```

### Utilitários

#### Health Check
```http
GET /health
```

#### Documentação dos Endpoints
```http
GET /
```

## 🔧 Configuração

### Variáveis de Ambiente

- `FLASK_ENV`: Ambiente de execução (`development`, `production`, `testing`)
- `SECRET_KEY`: Chave secreta para sessões (obrigatório em produção)
- `DATABASE_URL`: URL do banco de dados (opcional, padrão: SQLite local)

### Exemplo de configuração para produção:
```bash
export FLASK_ENV=production
export SECRET_KEY=sua-chave-secreta-muito-segura
export DATABASE_URL=postgresql://user:password@localhost/ecommerce
```

## 🏗️ Arquitetura

### Design Pattern: Factory Pattern
A aplicação usa o padrão Factory através da função `create_app()` para criar instâncias configuráveis da aplicação Flask.

### Blueprints
As rotas são organizadas em Blueprints modulares:
- `auth_bp`: Autenticação e registro
- `products_bp`: Gerenciamento de produtos  
- `cart_bp`: Carrinho de compras
- `main_bp`: Rotas principais e utilitários

### Modelos de Dados
- **User**: Usuários do sistema com autenticação
- **Product**: Produtos do e-commerce
- **CartItem**: Itens no carrinho com quantidade

### Tratamento de Erros
Todos os endpoints incluem tratamento de erros com:
- Validação de dados de entrada
- Mensagens de erro claras
- Rollback automático em caso de falha no banco
- Códigos HTTP apropriados

## 🧪 Testes

### Executar testes (quando implementados):
```bash
python -m pytest tests/
```

## 📝 Melhorias Futuras

- [ ] Implementar hash de senhas (bcrypt)
- [ ] Adicionar middleware de rate limiting
- [ ] Implementar sistema de pedidos (orders)
- [ ] Adicionar paginação na listagem de produtos
- [ ] Implementar cache (Redis)
- [ ] Adicionar logging estruturado
- [ ] Implementar testes unitários e de integração
- [ ] Adicionar autenticação JWT
- [ ] Implementar upload de imagens para produtos

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
