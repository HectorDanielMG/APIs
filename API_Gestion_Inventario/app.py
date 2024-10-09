from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Producto
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

# Crear la base de datos
@app.before_first_request
def create_tables():
    db.create_all()

# Endpoint para agregar un nuevo producto
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        quantity=data['quantity'],
        price=data['price']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Producto agregado!'}), 201

# Endpoint para obtener todos los productos
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'quantity': p.quantity, 'price': p.price} for p in products]), 200

# Endpoint para actualizar un producto
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Producto no encontrado!'}), 404

    data = request.get_json()
    product.name = data.get('name', product.name)
    product.quantity = data.get('quantity', product.quantity)
    product.price = data.get('price', product.price)
    db.session.commit()
    return jsonify({'message': 'Producto actualizado!'}), 200

# Endpoint para eliminar un producto
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Producto no encontrado!'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Producto eliminado!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
