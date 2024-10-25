from flask import Flask, request, render_template, session, jsonify
import requests
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Clave de la API de OpenWeatherMap
API_KEY = 'tu_clave_de_openweathermap'

# Historial de búsquedas almacenado en el servidor
search_history = []

def get_weather_by_coordinates(lat, lon, units='metric'):
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units={units}&lang=es"
    response = requests.get(weather_url)
    return response.json() if response.status_code == 200 else None

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    forecast_data = None
    error_message = None

    if request.method == 'POST':
        lat = request.form.get('latitude')
        lon = request.form.get('longitude')
        units = request.form.get('units', 'metric')  # Elegir unidades (métricas por defecto)

        if lat and lon:
            # Obtener clima usando coordenadas
            data = get_weather_by_coordinates(lat, lon, units)
            if data:
                weather_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed']
                }

                # Guardar búsqueda en historial
                search_history.append(weather_data)
                if len(search_history) > 5:
                    search_history.pop(0)

                # Obtener previsión del clima
                forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units={units}&lang=es"
                forecast_response = requests.get(forecast_url)
                if forecast_response.status_code == 200:
                    forecast_data = forecast_response.json()['list'][:5]
            else:
                error_message = "No se pudo obtener el clima para las coordenadas proporcionadas."
        else:
            error_message = "Debes seleccionar una ubicación en el mapa."

    return render_template('index.html', weather_data=weather_data, forecast_data=forecast_data,
                           error_message=error_message, history=search_history)

if __name__ == '__main__':
    app.run(debug=True)
