from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Tu API key de Fixer o ExchangeRate-API
API_KEY = 'tu_api_key_aqui'

# URL para la API de Fixer (o usa la URL del servicio que prefieras)
BASE_URL = 'http://data.fixer.io/api/latest'

@app.route('/convert', methods=['GET'])
def convert_currency():
    base_currency = request.args.get('base')
    target_currency = request.args.get('target')
    amount = request.args.get('amount', type=float)

    if not base_currency or not target_currency or not amount:
        return jsonify({'error': 'Faltan parámetros. Necesitas base, target y amount'}), 400

    # Hacer una solicitud a la API de tasas de cambio
    url = f"{BASE_URL}?access_key={API_KEY}&base={base_currency}&symbols={target_currency}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({'error': 'No se pudo obtener las tasas de cambio'}), response.status_code

    data = response.json()

    if 'error' in data:
        return jsonify(data), 400

    # Obtener la tasa de cambio y calcular la conversión
    exchange_rate = data['rates'].get(target_currency)
    if not exchange_rate:
        return jsonify({'error': f'No se encontró la tasa de cambio para {target_currency}'}), 400

    converted_amount = amount * exchange_rate

    return jsonify({
        'base_currency': base_currency,
        'target_currency': target_currency,
        'exchange_rate': exchange_rate,
        'amount': amount,
        'converted_amount': converted_amount
    })

if __name__ == '__main__':
    app.run(debug=True)
