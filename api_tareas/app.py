from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de base de datos para las tareas
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    completed = db.Column(db.Boolean, default=False)

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({"message": "Bienvenido a la API de gestión de tareas"}), 200

# Obtener todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    } for task in tasks]), 200

# Obtener una tarea por ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        abort(404, description="Tarea no encontrada")
    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }), 200

# Crear una nueva tarea
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400, description="El título de la tarea es obligatorio")
    new_task = Task(
        title=request.json['title'],
        description=request.json.get('description', ''),
        completed=False
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({
        "message": "Tarea creada con éxito",
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "completed": new_task.completed
        }
    }), 201

# Actualizar una tarea existente
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        abort(404, description="Tarea no encontrada")
    data = request.json
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify({
        "message": "Tarea actualizada con éxito",
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }
    }), 200

# Eliminar una tarea
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        abort(404, description="Tarea no encontrada")
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Tarea eliminada con éxito"}), 200

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error)}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400

if __name__ == '__main__':
    app.run(debug=True)
