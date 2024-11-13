from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

# Crear la base de datos y la tabla
@app.before_first_request
def create_tables():
    db.create_all()

# Obtener todos los productos
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'quantity': p.quantity, 'price': p.price} for p in products])

# Obtener un producto por ID
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({'id': product.id, 'name': product.name, 'quantity': product.quantity, 'price': product.price})

# Agregar un nuevo producto
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(name=data['name'], quantity=data['quantity'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Producto agregado exitosamente'}), 201

# Actualizar un producto
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    product.name = data['name']
    product.quantity = data['quantity']
    product.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Producto actualizado exitosamente'})

# Eliminar un producto
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Producto eliminado exitosamente'})

if __name__ == '__main__':
    app.run(debug=True)
