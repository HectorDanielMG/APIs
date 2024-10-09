from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Servicios simulados (ejemplo de URLs de servicios de seguimiento)
TRACKING_SERVICES = {
    "dhl": "https://api.dhl.com/track?tracking_number={}",
    "ups": "https://onlinetools.ups.com/track?tracking_number={}",
    "fedex": "https://www.fedex.com/tracking?tracknumber={}"
}

@app.route('/track', methods=['GET'])
def track_package():
    tracking_number = request.args.get('tracking_number')
    service = request.args.get('service')

    if not tracking_number or not service:
        return jsonify({"error": "Faltan parámetros 'tracking_number' o 'service'."}), 400

    if service not in TRACKING_SERVICES:
        return jsonify({"error": "El servicio no es compatible."}), 400

    # Llamada a la API del servicio de seguimiento
    try:
        tracking_url = TRACKING_SERVICES[service].format(tracking_number)
        response = requests.get(tracking_url)

        if response.status_code == 200:
            return jsonify({"status": response.json()})
        else:
            return jsonify({"error": "No se pudo obtener información del paquete."}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
