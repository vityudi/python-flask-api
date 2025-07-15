# E-commerce API

Uma API REST completa para e-commerce desenvolvida com Flask, incluindo autenticação, gerenciamento de produtos, carrinho de compras e sistema de pedidos.

## 🚀 Funcionalidades

- **Autenticação**: Login, logout e registro de usuários com hash de senhas
- **Produtos**: CRUD completo com categorias, busca e gerenciamento de estoque
- **Carrinho**: Adicionar, remover, atualizar quantidades e validação de estoque
- **Pedidos**: Sistema completo de pedidos com status e histórico
- **Categorias**: Organização de produtos por categorias
- **Documentação**: Endpoints autodocumentados com Swagger

## 📁 Estrutura do Projeto

```
python-flask-api/
├── app/                          # Pacote principal da aplicação
│   ├── __init__.py              # Factory da aplicação Flask
│   ├── models/                  # Modelos de dados separados
│   │   ├── __init__.py         # Centralização das importações
│   │   ├── user.py             # Modelo de usuário
│   │   ├── category.py         # Modelo de categoria
│   │   ├── product.py          # Modelo de produto
│   │   ├── cart.py             # Modelo de carrinho
│   │   └── order.py            # Modelos de pedidos
│   └── routes/                  # Blueprints das rotas
│       ├── main.py             # Rotas principais e health check
│       ├── auth.py             # Autenticação (login/logout/register)
│       ├── products.py         # Gerenciamento de produtos e categorias
│       ├── cart.py             # Carrinho de compras
│       └── orders.py           # Sistema de pedidos
├── instance/                    # Arquivos de instância (banco de dados)
│   └── ecommerce.db            # Banco SQLite
├── config.py                   # Configurações da aplicação
├── requirements.txt            # Dependências do projeto
├── run.py                     # Ponto de entrada da aplicação
├── swagger.yaml               # Documentação OpenAPI
└── .gitignore                 # Arquivos ignorados pelo Git
```

## 🏗️ Arquitetura Modular

### Separação de Responsabilidades

#### Modelos (app/models/)
Cada modelo está em seu próprio arquivo para melhor manutenibilidade:
- **user.py**: Usuário com autenticação e hash de senhas
- **category.py**: Categorias de produtos
- **product.py**: Produtos com estoque e relacionamentos
- **cart.py**: Itens do carrinho com validações
- **order.py**: Pedidos e itens de pedidos

#### Rotas (app/routes/)
Blueprints organizados por funcionalidade:
- **main.py**: Endpoints principais e health check
- **auth.py**: Autenticação e gerenciamento de usuários
- **products.py**: CRUD de produtos e categorias
- **cart.py**: Gerenciamento do carrinho
- **orders.py**: Sistema de pedidos

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

## 📋 Dados Iniciais

A aplicação cria automaticamente:
- **Usuário Admin**: username: `admin`, password: `admin123`
- **Categorias**: Eletrônicos, Roupas, Casa, Livros, Esportes
- **Produtos de Exemplo**: Smartphone, Notebook, Camiseta, Jeans

## 📊 Formato de Resposta

Todas as respostas da API seguem um padrão estruturado:

### Sucesso
```json
{
  "success": true,
  "data": {
    // dados solicitados
  },
  "message": "Operação realizada com sucesso" // opcional
}
```

### Erro
```json
{
  "success": false,
  "message": "Descrição do erro",
  "error_code": "ERROR_TYPE" // opcional
}
```

## 🎯 Exemplo de Uso

### Fluxo Completo de E-commerce

1. **Registrar usuário**:
```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "joao", "email": "joao@email.com", "password": "senha123"}'
```

2. **Fazer login**:
```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "joao", "password": "senha123"}'
```

3. **Listar produtos**:
```bash
curl -X GET http://127.0.0.1:5000/api/products
```

4. **Adicionar ao carrinho**:
```bash
curl -X POST http://127.0.0.1:5000/api/cart/add/1 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 2}'
```

5. **Criar pedido**:
```bash
curl -X POST http://127.0.0.1:5000/api/orders
```

6. **Verificar pedidos**:
```bash
curl -X GET http://127.0.0.1:5000/api/orders
```

## 📈 Resumo das Melhorias Implementadas

### 🔧 Reestruturação Completa
- **Modelos Separados**: Cada modelo agora tem seu próprio arquivo (user.py, product.py, category.py, cart.py, order.py)
- **Rotas Organizadas**: Sistema de blueprints melhorado com separação clara de responsabilidades
- **Sistema de Importação**: Centralização das importações através do `__init__.py` dos modelos

### 🆕 Novas Funcionalidades
- **Sistema de Pedidos**: Completo com status, histórico e gestão
- **Categorias de Produtos**: Organização hierárquica dos produtos
- **Validação de Estoque**: Verificação automática antes de adicionar ao carrinho
- **Soft Delete**: Produtos podem ser desativados sem perder dados históricos

### 🔒 Segurança Aprimorada
- **Hash de Senhas**: Implementação segura com Werkzeug
- **Validação Robusta**: Entrada de dados validada em todas as rotas
- **Transações Seguras**: Rollback automático em caso de erro

### 📊 Melhoria na Estrutura de Dados
- **Timestamps Automáticos**: Rastreamento de criação e atualização
- **Relacionamentos Complexos**: Mapeamento completo entre entidades
- **Constraints de Integridade**: Prevenção de dados inconsistentes
- **Preços Históricos**: Manutenção do preço no momento da compra
```

## 📖 Documentação da API

### Autenticação

#### Registrar Usuário
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "string",
  "email": "string", 
  "password": "string"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

#### Logout
```http
POST /api/auth/logout
Authorization: Required (logged in user)
```

#### Perfil do Usuário
```http
GET /api/auth/profile
Authorization: Required
```

### Produtos

#### Listar Produtos
```http
GET /api/products
Query Parameters:
  - category_id: int (opcional) - Filtrar por categoria
  - active_only: bool (opcional, padrão: true) - Apenas produtos ativos
```

#### Obter Produto
```http
GET /api/products/{id}
```

#### Buscar Produtos
```http
GET /api/products/search
Query Parameters:
  - q: string (obrigatório) - Termo de busca
  - category_id: int (opcional) - Filtrar por categoria
```

#### Criar Produto
```http
POST /api/products
Authorization: Required
Content-Type: application/json

{
  "name": "string",
  "description": "string (opcional)",
  "price": number,
  "stock": number (opcional, padrão: 0),
  "category_id": number (opcional)
}
```

#### Atualizar Produto
```http
PUT /api/products/{id}
Authorization: Required
Content-Type: application/json

{
  "name": "string (opcional)",
  "description": "string (opcional)",
  "price": number (opcional),
  "stock": number (opcional),
  "category_id": number (opcional),
  "is_active": boolean (opcional)
}
```

#### Deletar Produto (Soft Delete)
```http
DELETE /api/products/{id}
Authorization: Required
```

#### Listar Categorias
```http
GET /api/products/categories
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

#### Total do Carrinho
```http
GET /api/cart/total
Authorization: Required
```

### Pedidos

#### Listar Pedidos
```http
GET /api/orders
Authorization: Required
Query Parameters:
  - status: string (opcional) - Filtrar por status
  - page: int (opcional, padrão: 1) - Página
  - per_page: int (opcional, padrão: 10) - Itens por página
```

#### Obter Pedido
```http
GET /api/orders/{id}
Authorization: Required
```

#### Criar Pedido (a partir do carrinho)
```http
POST /api/orders
Authorization: Required
```

#### Cancelar Pedido
```http
PUT /api/orders/{id}/cancel
Authorization: Required
```

#### Atualizar Status do Pedido
```http
PUT /api/orders/{id}/status
Authorization: Required
Content-Type: application/json

{
  "status": "pending|confirmed|shipped|delivered|cancelled"
}
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

## 🏗️ Recursos Técnicos

### Design Patterns
- **Factory Pattern**: Função `create_app()` para instâncias configuráveis
- **Blueprint Pattern**: Organização modular das rotas
- **Repository Pattern**: Separação clara entre modelos e lógica de negócio

### Blueprints Organizados
- `main_bp`: Rotas principais e health check
- `auth_bp`: Autenticação e registro (`/api/auth`)
- `products_bp`: Gerenciamento de produtos (`/api/products`)
- `cart_bp`: Carrinho de compras (`/api/cart`)
- `orders_bp`: Sistema de pedidos (`/api/orders`)

### Modelos de Dados Relacionais

#### Relacionamentos
- **User** → **CartItem** (1:N)
- **User** → **Order** (1:N)
- **Category** → **Product** (1:N)
- **Product** → **CartItem** (1:N)
- **Product** → **OrderItem** (1:N)
- **Order** → **OrderItem** (1:N)

#### Características dos Modelos
- **Timestamps automáticos**: created_at, updated_at
- **Soft delete**: Produtos marcados como inativos
- **Validações de estoque**: Verificação automática de disponibilidade
- **Preços históricos**: OrderItem mantém preço no momento da compra
- **Constraints de unicidade**: Evita duplicação de itens no carrinho

### Recursos de Segurança
- **Hash de senhas**: Werkzeug para hash seguro
- **Validação de entrada**: Sanitização de dados
- **Rollback automático**: Transações seguras
- **Session management**: Flask-Login integrado

### Tratamento de Erros
- **Códigos HTTP apropriados**: 200, 201, 400, 401, 404, 500
- **Mensagens de erro estruturadas**: JSON padronizado
- **Logging de erros**: Para debug e monitoramento
- **Validação robusta**: Entrada e tipos de dados

## 🧪 Testes

### Executar testes (quando implementados):
```bash
python -m pytest tests/
```

## 📝 Melhorias Implementadas

### ✅ Estrutura Modular
- [x] Separação de modelos em arquivos individuais
- [x] Organização clara de rotas por funcionalidade
- [x] Sistema de importação centralizado
- [x] Factory pattern para configuração

### ✅ Funcionalidades Avançadas
- [x] Hash seguro de senhas (Werkzeug)
- [x] Sistema completo de pedidos
- [x] Categorias de produtos
- [x] Validação de estoque em tempo real
- [x] Soft delete para produtos
- [x] Timestamps automáticos
- [x] Relacionamentos complexos entre modelos

### ✅ Melhorias de Segurança
- [x] Validação robusta de entrada
- [x] Tratamento de erros estruturado
- [x] Transações seguras com rollback
- [x] Sessões seguras com Flask-Login

## 🔮 Melhorias Futuras

### 🚀 Performance e Escalabilidade
- [ ] Implementar cache (Redis)
- [ ] Paginação em todas as listagens
- [ ] Indexação otimizada do banco
- [ ] Compressão de respostas

### 🔐 Segurança e Autenticação
- [ ] Autenticação JWT
- [ ] Rate limiting
- [ ] CORS configurável
- [ ] Auditoria de ações

### 📊 Funcionalidades de Negócio
- [ ] Sistema de avaliações e comentários
- [ ] Cupons de desconto
- [ ] Sistema de favoritos
- [ ] Histórico de preços
- [ ] Notificações de estoque baixo

### 🛠️ DevOps e Monitoramento
- [ ] Logging estruturado
- [ ] Métricas e monitoramento
- [ ] Testes unitários e de integração
- [ ] CI/CD pipeline
- [ ] Containerização (Docker)

### 🎨 Interface e Experiência
- [ ] Upload de imagens para produtos
- [ ] API de busca avançada
- [ ] Filtros dinâmicos
- [ ] Exportação de dados

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
