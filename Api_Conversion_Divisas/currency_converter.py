from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "YOUR_API_KEY"  # Reemplaza con tu API Key de ExchangeRate-API
BASE_URL = "https://v6.exchangerate-api.com/v6/"

# Ruta para convertir una cantidad de una moneda a otra
@app.route('/convertir', methods=['GET'])
def convertir():
    de_moneda = request.args.get('de')
    a_moneda = request.args.get('a')
    cantidad = request.args.get('cantidad', type=float)

    if not de_moneda or not a_moneda or cantidad is None:
        return jsonify({"error": "Por favor proporciona los parámetros 'de', 'a' y 'cantidad'."}), 400

    try:
        response = requests.get(f"{BASE_URL}{API_KEY}/pair/{de_moneda}/{a_moneda}")
        data = response.json()

        if response.status_code != 200:
            return jsonify({"error": data.get("error", "Error desconocido")}), response.status_code

        tasa_conversion = data['conversion_rate']
        resultado = cantidad * tasa_conversion

        return jsonify({
            "de_moneda": de_moneda,
            "a_moneda": a_moneda,
            "cantidad": cantidad,
            "tasa_conversion": tasa_conversion,
            "resultado": resultado
        })
    except Exception as e:
        return jsonify({"error": "Hubo un problema al realizar la conversión de divisas"}), 500

# Ruta de error 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Recurso no encontrado"}), 404

# Iniciar la API
if __name__ == '__main__':
    app.run(debug=True)
