from flask import Flask, request, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    data = request.args.get('data')

    if not data:
        return {'error': 'No se proporcionó ningún dato'}, 400

    # Generar el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Guardar la imagen en memoria
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Enviar la imagen al cliente
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
