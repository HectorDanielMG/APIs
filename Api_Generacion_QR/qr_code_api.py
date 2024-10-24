from flask import Flask, render_template, request, make_response, redirect, url_for, send_file
import qrcode
from io import BytesIO
import validators
import base64
import zipfile
import os

app = Flask(__name__)

# Historial de QR generados
qr_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        urls = request.form.getlist('urls')
        fill_color = request.form.get('fill_color') or 'black'
        back_color = request.form.get('back_color') or 'white'
        
        # Limitar la cantidad de URLs que se pueden enviar
        if len(urls) > 5:
            return render_template('index.html', error="No puedes generar más de 5 códigos QR a la vez.")
        
        qr_images = []
        for url in urls:
            if not validators.url(url):
                return render_template('index.html', error=f"URL inválida: {url}. Por favor, introduce URLs válidas.")

            # Generar el código QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            img = qr.make_image(fill=fill_color, back_color=back_color)

            # Guardar el código QR en un objeto BytesIO para previsualización
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)

            # Convertir la imagen a base64 para previsualización en HTML
            img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

            # Guardar la imagen y URL en la lista para previsualización
            qr_images.append({'url': url, 'img_base64': img_base64})

            # Agregar al historial
            qr_history.append({'url': url, 'image': img_base64})

        return render_template('index.html', qr_images=qr_images, qr_history=qr_history)

    # Mostrar la página de inicio con el formulario
    return render_template('index.html', qr_history=qr_history)


@app.route('/download_zip', methods=['POST'])
def download_zip():
    urls = request.form.getlist('urls')
    fill_color = request.form.get('fill_color') or 'black'
    back_color = request.form.get('back_color') or 'white'

    # Crear un archivo ZIP en memoria
    zip_io = BytesIO()
    with zipfile.ZipFile(zip_io, 'w') as zip_file:
        for i, url in enumerate(urls):
            # Generar el código QR para cada URL
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

            # Guardar cada imagen en el archivo ZIP
            file_name = f"qr_code_{i+1}.png"
            zip_file.writestr(file_name, img_io.read())

    zip_io.seek(0)

    # Enviar el archivo ZIP para descargar
    return send_file(zip_io, mimetype='application/zip', as_attachment=True, download_name='qr_codes.zip')


if __name__ == '__main__':
    app.run(debug=True)
