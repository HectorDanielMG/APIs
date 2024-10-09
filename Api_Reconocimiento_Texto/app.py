from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

# Ruta para subir y procesar la imagen
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegurarse de que exista la carpeta 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No se envió ninguna imagen"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    # Guardar la imagen en el servidor
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Abrir y procesar la imagen con Tesseract
    text = extract_text_from_image(filepath)

    # Eliminar el archivo después del procesamiento
    os.remove(filepath)

    return jsonify({"text": text})

def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        return f"Error procesando la imagen: {e}"

if __name__ == '__main__':
    app.run(debug=True)
