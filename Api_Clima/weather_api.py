from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "YOUR_API_KEY"  # Reemplaza con tu API Key de OpenWeatherMap
BASE_URL = "http://api.openweathermap.org/data/2.5/"

# Ruta para obtener el clima actual de una ciudad
@app.route('/clima/actual', methods=['GET'])
def clima_actual():
    ciudad = request.args.get('ciudad')
    if not ciudad:
        return jsonify({"error": "Por favor proporciona una ciudad"}), 400

    try:
        response = requests.get(f"{BASE_URL}weather", params={
            'q': ciudad,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'es'
        })
        data = response.json()
        
        if response.status_code != 200:
            return jsonify({"error": data.get("message", "Error desconocido")}), response.status_code

        clima = {
            "ciudad": data['name'],
            "temperatura": data['main']['temp'],
            "descripcion": data['weather'][0]['description'],
            "humedad": data['main']['humidity'],
            "viento": data['wind']['speed']
        }
        return jsonify(clima)
    except Exception as e:
        return jsonify({"error": "Hubo un problema al obtener el clima actual"}), 500


# Ruta para obtener el pronóstico extendido (por 5 días)
@app.route('/clima/pronostico', methods=['GET'])
def pronostico():
    ciudad = request.args.get('ciudad')
    if not ciudad:
        return jsonify({"error": "Por favor proporciona una ciudad"}), 400

    try:
        response = requests.get(f"{BASE_URL}forecast", params={
            'q': ciudad,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'es'
        })
        data = response.json()

        if response.status_code != 200:
            return jsonify({"error": data.get("message", "Error desconocido")}), response.status_code

        pronostico = []
        for item in data['list']:
            pronostico.append({
                "fecha": item['dt_txt'],
                "temperatura": item['main']['temp'],
                "descripcion": item['weather'][0]['description'],
                "humedad": item['main']['humidity'],
                "viento": item['wind']['speed']
            })

        return jsonify({"ciudad": data['city']['name'], "pronostico": pronostico})
    except Exception as e:
        return jsonify({"error": "Hubo un problema al obtener el pronóstico"}), 500


# Ruta de error 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Recurso no encontrado"}), 404


# Iniciar la API
if __name__ == '__main__':
    app.run(debug=True)
