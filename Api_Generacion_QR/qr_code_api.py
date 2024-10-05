from flask import Flask, render_template, make_response
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    # URL a convertir en QR
    url = "https://github.com/HectorDanielMG"

    # Generar el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Guardar el código QR en un objeto BytesIO
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Devolver el código QR como una imagen en la respuesta
    response = make_response(img_io.read())
    response.headers.set('Content-Type', 'image/png')
    response.headers.set('Content-Disposition', 'inline', filename='qr_code.png')
    return response

if __name__ == '__main__':
    app.run(debug=True)
