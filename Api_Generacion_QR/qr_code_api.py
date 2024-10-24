from flask import Flask, render_template, request, make_response
import qrcode
from io import BytesIO
import validators

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener los datos del formulario
        url = request.form.get('url')
        fill_color = request.form.get('fill_color') or 'black'
        back_color = request.form.get('back_color') or 'white'
        
        # Validar la URL
        if not validators.url(url):
            return render_template('index.html', error="URL inválida. Por favor, introduce una URL válida.")

        # Generar el código QR con colores personalizados
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill=fill_color, back_color=back_color)

        # Guardar el código QR en un objeto BytesIO
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        # Devolver el código QR como una imagen en la respuesta para visualizar y descargar
        response = make_response(img_io.read())
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition', 'attachment', filename='qr_code.png')
        return response
    
    # Mostrar la página de inicio con el formulario
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
