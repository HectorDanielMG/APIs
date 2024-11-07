from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import os
import uuid

app = Flask(__name__)

# Configuración de la carpeta de almacenamiento de imágenes subidas
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/ocr', methods=['POST'])
def ocr_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Guarda la imagen en la carpeta de uploads
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}.png")
    image_file.save(file_path)

    try:
        # Abre la imagen y usa Tesseract para extraer texto
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

        # Elimina la imagen después de procesar
        os.remove(file_path)

        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
