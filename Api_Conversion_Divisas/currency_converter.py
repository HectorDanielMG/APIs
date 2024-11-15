from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración de la base de datos SQLite
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'currency_converter.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Currency (Moneda)
class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), nullable=False, unique=True)  # Código de moneda (ejemplo: USD)
    name = db.Column(db.String(50), nullable=False)  # Nombre de la moneda
    exchange_rate = db.Column(db.Float, nullable=False)  # Tasa de cambio respecto a una moneda base (por defecto, USD)

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "exchange_rate": self.exchange_rate
        }

# Inicialización de la base de datos
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({"message": "Bienvenido a la API de Conversión de Divisas"}), 200

# Listar todas las monedas y tasas de cambio
@app.route('/currencies', methods=['GET'])
def list_currencies():
    currencies = Currency.query.all()
    return jsonify({"currencies": [currency.to_dict() for currency in currencies]}), 200

# Agregar una nueva moneda
@app.route('/currencies', methods=['POST'])
def add_currency():
    try:
        data = request.get_json()
        code = data.get('code')
        name = data.get('name')
        exchange_rate = data.get('exchange_rate')

        if not code or not name or exchange_rate is None:
            return jsonify({"error": "Todos los campos (code, name, exchange_rate) son obligatorios"}), 400

        # Verificar si ya existe la moneda
        if Currency.query.filter_by(code=code.upper()).first():
            return jsonify({"error": "La moneda ya existe"}), 400

        new_currency = Currency(code=code.upper(), name=name, exchange_rate=float(exchange_rate))
        db.session.add(new_currency)
        db.session.commit()

        return jsonify({"message": "Moneda agregada con éxito", "currency": new_currency.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": f"Error al agregar la moneda: {str(e)}"}), 500

# Actualizar la tasa de cambio de una moneda
@app.route('/currencies/<string:code>', methods=['PUT'])
def update_currency(code):
    try:
        currency = Currency.query.filter_by(code=code.upper()).first()
        if not currency:
            return jsonify({"error": "Moneda no encontrada"}), 404

        data = request.get_json()
        exchange_rate = data.get('exchange_rate')

        if exchange_rate is None:
            return jsonify({"error": "La tasa de cambio es obligatoria"}), 400

        currency.exchange_rate = float(exchange_rate)
        db.session.commit()

        return jsonify({"message": "Tasa de cambio actualizada", "currency": currency.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar la tasa de cambio: {str(e)}"}), 500

# Convertir entre dos monedas
@app.route('/convert', methods=['POST'])
def convert_currency():
    try:
        data = request.get_json()
        from_currency_code = data.get('from_currency')
        to_currency_code = data.get('to_currency')
        amount = data.get('amount')

        if not from_currency_code or not to_currency_code or amount is None:
            return jsonify({"error": "Los campos from_currency, to_currency y amount son obligatorios"}), 400

        from_currency = Currency.query.filter_by(code=from_currency_code.upper()).first()
        to_currency = Currency.query.filter_by(code=to_currency_code.upper()).first()

        if not from_currency or not to_currency:
            return jsonify({"error": "Moneda no encontrada"}), 404

        # Calcular la conversión
        result = (amount / from_currency.exchange_rate) * to_currency.exchange_rate
        return jsonify({
            "from_currency": from_currency.to_dict(),
            "to_currency": to_currency.to_dict(),
            "amount": amount,
            "converted_amount": round(result, 2)
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error al realizar la conversión: {str(e)}"}), 500

# Eliminar una moneda
@app.route('/currencies/<string:code>', methods=['DELETE'])
def delete_currency(code):
    try:
        currency = Currency.query.filter_by(code=code.upper()).first()
        if not currency:
            return jsonify({"error": "Moneda no encontrada"}), 404

        db.session.delete(currency)
        db.session.commit()

        return jsonify({"message": "Moneda eliminada con éxito"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar la moneda: {str(e)}"}), 500

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ruta no encontrada"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Solicitud inválida"}), 400

if __name__ == '__main__':
    app.run(debug=True)
