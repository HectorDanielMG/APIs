from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Configuración de la base de datos SQLite
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'habit_tracker.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Habit (Hábito)
class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    streak = db.Column(db.Integer, default=0)  # Racha de días completados

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "creation_date": self.creation_date.strftime('%Y-%m-%d %H:%M:%S'),
            "streak": self.streak
        }

# Inicialización de la base de datos
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({"message": "Bienvenido a la API de Seguimiento de Hábitos"}), 200

# Crear un nuevo hábito
@app.route('/habits', methods=['POST'])
def create_habit():
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')

        if not name:
            return jsonify({"error": "El nombre del hábito es obligatorio"}), 400

        new_habit = Habit(name=name, description=description)
        db.session.add(new_habit)
        db.session.commit()

        return jsonify({"message": "Hábito creado con éxito", "habit": new_habit.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear el hábito: {str(e)}"}), 500

# Listar todos los hábitos
@app.route('/habits', methods=['GET'])
def list_habits():
    habits = Habit.query.all()
    return jsonify({"habits": [habit.to_dict() for habit in habits]}), 200

# Obtener un hábito por ID
@app.route('/habits/<int:habit_id>', methods=['GET'])
def get_habit(habit_id):
    habit = Habit.query.get(habit_id)
    if not habit:
        return jsonify({"error": "Hábito no encontrado"}), 404

    return jsonify({"habit": habit.to_dict()}), 200

# Actualizar un hábito (nombre o descripción)
@app.route('/habits/<int:habit_id>', methods=['PUT'])
def update_habit(habit_id):
    try:
        habit = Habit.query.get(habit_id)
        if not habit:
            return jsonify({"error": "Hábito no encontrado"}), 404

        data = request.get_json()
        habit.name = data.get('name', habit.name)
        habit.description = data.get('description', habit.description)

        db.session.commit()
        return jsonify({"message": "Hábito actualizado con éxito", "habit": habit.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el hábito: {str(e)}"}), 500

# Marcar un hábito como completado (incrementar racha)
@app.route('/habits/<int:habit_id>/complete', methods=['POST'])
def complete_habit(habit_id):
    try:
        habit = Habit.query.get(habit_id)
        if not habit:
            return jsonify({"error": "Hábito no encontrado"}), 404

        habit.streak += 1
        db.session.commit()
        return jsonify({"message": "Hábito marcado como completado", "habit": habit.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": f"Error al marcar el hábito como completado: {str(e)}"}), 500

# Reiniciar la racha de un hábito
@app.route('/habits/<int:habit_id>/reset', methods=['POST'])
def reset_habit_streak(habit_id):
    try:
        habit = Habit.query.get(habit_id)
        if not habit:
            return jsonify({"error": "Hábito no encontrado"}), 404

        habit.streak = 0
        db.session.commit()
        return jsonify({"message": "Racha del hábito reiniciada", "habit": habit.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": f"Error al reiniciar la racha del hábito: {str(e)}"}), 500

# Eliminar un hábito
@app.route('/habits/<int:habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    habit = Habit.query.get(habit_id)
    if not habit:
        return jsonify({"error": "Hábito no encontrado"}), 404

    db.session.delete(habit)
    db.session.commit()
    return jsonify({"message": "Hábito eliminado con éxito"}), 200

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ruta no encontrada"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Solicitud inválida"}), 400

if __name__ == '__main__':
    app.run(debug=True)
