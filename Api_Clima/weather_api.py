from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Configurar la clave de la API de OpenWeatherMap
API_KEY = 'tu_clave_de_openweathermap'  # Reemplaza esto con tu propia clave de API de OpenWeatherMap

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error_message = None

    if request.method == 'POST':
        city = request.form.get('city')

        # Realizar la solicitud a la API de OpenWeatherMap
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=es"
        response = requests.get(weather_url)

        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
        else:
            error_message = "No se pudo encontrar la ciudad. Por favor, inténtalo de nuevo."

    return render_template('index.html', weather_data=weather_data, error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)
