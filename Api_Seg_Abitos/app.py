from flask import Flask, jsonify, request
from models import db, Habit, init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def setup():
    init_db()

# Obtener todos los hábitos
@app.route('/habits', methods=['GET'])
def get_habits():
    habits = Habit.query.all()
    return jsonify([habit.to_dict() for habit in habits])

# Crear un nuevo hábito
@app.route('/habits', methods=['POST'])
def create_habit():
    data = request.get_json()
    new_habit = Habit(name=data['name'], description=data['description'])
    db.session.add(new_habit)
    db.session.commit()
    return jsonify(new_habit.to_dict()), 201

# Marcar un hábito como completado
@app.route('/habits/<int:habit_id>/complete', methods=['POST'])
def complete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    habit.complete()
    db.session.commit()
    return jsonify(habit.to_dict())

# Actualizar un hábito
@app.route('/habits/<int:habit_id>', methods=['PUT'])
def update_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    data = request.get_json()
    habit.name = data.get('name', habit.name)
    habit.description = data.get('description', habit.description)
    db.session.commit()
    return jsonify(habit.to_dict())

# Eliminar un hábito
@app.route('/habits/<int:habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    db.session.delete(habit)
    db.session.commit()
    return jsonify({'message': 'Hábito eliminado'})

if __name__ == '__main__':
    app.run(debug=True)
