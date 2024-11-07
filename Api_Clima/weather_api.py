from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Reemplaza 'YOUR_API_KEY' con tu clave de API de OpenWeatherMap
API_KEY = 'YOUR_API_KEY'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'Please provide a city parameter'}), 400

    # Llamada a la API de OpenWeatherMap
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Cambiar a 'imperial' para grados Fahrenheit
    }

    response = requests.get(BASE_URL, params=params)

    # Verifica si la respuesta es válida
    if response.status_code != 200:
        return jsonify({'error': 'City not found or API error occurred'}), response.status_code

    # Procesa y estructura los datos en un JSON sencillo
    data = response.json()
    weather_data = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed']
    }

    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)
