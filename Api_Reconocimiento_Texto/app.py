from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image

app = Flask(__name__)

# Configuración de la ruta para guardar imágenes
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuración de Tesseract (asegúrate de que esté instalado en tu sistema)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Cambia según tu sistema operativo

@app.route('/')
def home():
    return jsonify({"message": "Bienvenido a la API de Reconocimiento de Texto"}), 200

# Ruta para subir imágenes y realizar reconocimiento de texto
@app.route('/recognize', methods=['POST'])
def recognize_text():
    if 'image' not in request.files:
        return jsonify({"error": "No se encontró el archivo de imagen en la solicitud"}), 400

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({"error": "No se proporcionó un archivo válido"}), 400

    try:
        # Guardar el archivo de imagen
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path)

        # Abrir la imagen y realizar reconocimiento de texto
        img = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(img)

        # Eliminar la imagen después de procesarla (opcional)
        os.remove(image_path)

        return jsonify({
            "message": "Reconocimiento de texto realizado con éxito",
            "extracted_text": extracted_text.strip()
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error al procesar la imagen: {str(e)}"}), 500

# Ruta para listar todos los archivos subidos (opcional)
@app.route('/uploads', methods=['GET'])
def list_uploads():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({"uploaded_files": files}), 200

# Ruta para eliminar imágenes subidas (opcional)
@app.route('/uploads/<filename>', methods=['DELETE'])
def delete_upload(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": f"Archivo {filename} eliminado con éxito"}), 200
    return jsonify({"error": "Archivo no encontrado"}), 404

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ruta no encontrada"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Solicitud inválida"}), 400

if __name__ == '__main__':
    app.run(debug=True)
