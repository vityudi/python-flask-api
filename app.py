from flask import Flask, request, jsonify # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_cors import CORS # type: ignore
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user # type: ignore

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    cart = db.relationship('CartItem', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Product {self.name}>'

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))     

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user and data.get('password') == user.password:
        login_user(user)  # This will set the user in the session
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200

@app.route('/api/products/add', methods=['POST'])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(
            name=data['name'],
            price=data['price'],
            description=data.get('description', '')
        )
        db.session.add(product) 
        db.session.commit()
        return jsonify({"message": "Product added successfully", "product_id": product.id}), 201
    
    return jsonify({"message": "Invalid data"}), 400

@app.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    return jsonify({"message": "Product not found"}), 404

@app.route('/api/produts/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        }), 200
    return jsonify({"message": "Product not found"}), 404

@app.route('/api/products/update/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    data = request.json
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'description' in data:
        product.description = data['description']
    
    db.session.commit()
    return jsonify({"message": "Product updated successfully"}), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description
    } for product in products]), 200

@app.route('/api/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    cart_item = CartItem(user_id=current_user.id, product_id=product.id)
    db.session.add(cart_item)
    db.session.commit()
    return jsonify({"message": "Product added to cart"}), 201

@app.route('/api/card/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_cart(product_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if not cart_item:
        return jsonify({"message": "Cart item not found"}), 404
    
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Product removed from cart"}), 200

@app.route('/api/cart', methods=['GET'])
@login_required
def get_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        "id": item.id,
        "product_id": item.product_id,
        "user_id": item.user_id
    } for item in cart_items]), 200

@app.route('/api/cart/clear', methods=['POST'])
@login_required
def clear_cart():
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({"message": "Cart cleared"}), 200

@app.route('/api/cart/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400
    
    db.session.delete(cart_items)
    db.session.commit()
    
    return jsonify({"message": "Checkout successful"}), 200

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)