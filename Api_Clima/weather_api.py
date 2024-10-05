from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Tu API key de OpenWeatherMap
API_KEY = 'tu_api_key_aqui'

# Ruta principal para obtener el clima por ciudad
@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'Falta el parámetro de ciudad'}), 400

    # URL para la API de OpenWeatherMap
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'

    response = requests.get(weather_url)

    if response.status_code != 200:
        return jsonify({'error': 'No se pudo obtener el clima'}), response.status_code

    data = response.json()
    return jsonify({
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed']
    })

if __name__ == '__main__':
    app.run(debug=True)
