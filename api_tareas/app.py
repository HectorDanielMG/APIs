from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista de tareas simulada
tareas = [
    {'id': 1, 'titulo': 'Estudiar para examen', 'completada': False},
    {'id': 2, 'titulo': 'Ir al supermercado', 'completada': False}
]

# Obtener todas las tareas
@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    return jsonify(tareas)

# Obtener una tarea por su ID
@app.route('/tareas/<int:tarea_id>', methods=['GET'])
def obtener_tarea(tarea_id):
    tarea = next((tarea for tarea in tareas if tarea['id'] == tarea_id), None)
    if tarea:
        return jsonify(tarea)
    return jsonify({'mensaje': 'Tarea no encontrada'}), 404

# Crear una nueva tarea
@app.route('/tareas', methods=['POST'])
def crear_tarea():
    nueva_tarea = {
        'id': len(tareas) + 1,
        'titulo': request.json['titulo'],
        'completada': False
    }
    tareas.append(nueva_tarea)
    return jsonify(nueva_tarea), 201

# Actualizar una tarea
@app.route('/tareas/<int:tarea_id>', methods=['PUT'])
def actualizar_tarea(tarea_id):
    tarea = next((tarea for tarea in tareas if tarea['id'] == tarea_id), None)
    if tarea:
        tarea['titulo'] = request.json.get('titulo', tarea['titulo'])
        tarea['completada'] = request.json.get('completada', tarea['completada'])
        return jsonify(tarea)
    return jsonify({'mensaje': 'Tarea no encontrada'}), 404

# Eliminar una tarea
@app.route('/tareas/<int:tarea_id>', methods=['DELETE'])
def eliminar_tarea(tarea_id):
    tarea = next((tarea for tarea in tareas if tarea['id'] == tarea_id), None)
    if tarea:
        tareas.remove(tarea)
        return jsonify({'mensaje': 'Tarea eliminada'})
    return jsonify({'mensaje': 'Tarea no encontrada'}), 404

if __name__ == '__main__':
    app.run(debug=True)
