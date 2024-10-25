from flask import Flask, request, render_template, session
import requests

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para manejar sesiones

# Configurar la clave de la API de OpenWeatherMap
API_KEY = 'tu_clave_de_openweathermap'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    forecast_data = None
    error_message = None
    city = None

    if request.method == 'POST':
        city = request.form.get('city')

        # Realizar la solicitud de clima actual
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=es"
        response = requests.get(weather_url)

        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],  # Icono de clima
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }

            # Guardar búsqueda en historial
            if 'history' not in session:
                session['history'] = []
            session['history'].append(weather_data)
            if len(session['history']) > 5:
                session['history'].pop(0)  # Mantener solo las últimas 5 búsquedas

            # Realizar la solicitud de previsión del clima a 5 días
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=es"
            forecast_response = requests.get(forecast_url)
            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()['list'][:5]  # Obtener solo las primeras 5 previsiones
        else:
            error_message = "No se pudo encontrar la ciudad. Por favor, inténtalo de nuevo."

    return render_template('index.html', weather_data=weather_data, forecast_data=forecast_data, 
                           error_message=error_message, history=session.get('history'))


if __name__ == '__main__':
    app.run(debug=True)
