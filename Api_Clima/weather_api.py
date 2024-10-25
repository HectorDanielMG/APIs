from flask import Flask, request, render_template, session, jsonify
import requests
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Clave de la API de OpenWeatherMap
API_KEY = 'tu_clave_de_openweathermap'

def get_location_from_ip():
    try:
        # Obtener IP pública y consultar ubicación
        ip_response = requests.get('https://ipinfo.io')
        location_data = ip_response.json()
        return location_data.get('city')
    except Exception as e:
        print(f"Error obteniendo la ubicación: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    forecast_data = None
    error_message = None
    city = None

    # Obtener ciudad automáticamente desde IP si no se proporciona
    if request.method == 'POST':
        city = request.form.get('city')
        units = request.form.get('units', 'metric')  # Elegir unidades (métricas por defecto)

        if not city:
            city = get_location_from_ip()
            if not city:
                error_message = "No se pudo detectar tu ubicación automáticamente."

        if city:
            # Solicitar el clima actual
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}&lang=es"
            response = requests.get(weather_url)

            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed']
                }

                # Guardar búsqueda en historial
                if 'history' not in session:
                    session['history'] = []
                session['history'].append(weather_data)
                if len(session['history']) > 5:
                    session['history'].pop(0)

                # Solicitar previsión del clima a 5 días
                forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={units}&lang=es"
                forecast_response = requests.get(forecast_url)
                if forecast_response.status_code == 200:
                    forecast_data = forecast_response.json()['list'][:5]
            else:
                error_message = "No se pudo encontrar la ciudad. Por favor, intenta nuevamente."

    return render_template('index.html', weather_data=weather_data, forecast_data=forecast_data, 
                           error_message=error_message, history=session.get('history'))


if __name__ == '__main__':
    app.run(debug=True)
