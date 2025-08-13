import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Task, User, Profile, Course
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app) # vinculando el archivo models.py con mi app
Migrate(app, db) # db init, db migrate, db upgrade, db downgrade 
CORS(app)

@app.route('/todos', methods=['GET'])
def get_todos():
    # Buscamos todas las tareas existentes
    todos = Task.query.all() # SELECT * FROM todos => [<Task 1>, <Task 2>]

    # Convertir a diccionario cada uno de los objetos en la lista de tareas
    todos = [task.serialize() for task in todos]
    #todos = list(map(lambda task: task.convertir_a_dict(), todos))

    return jsonify(todos), 200

@app.route('/todos', methods=['POST'])
def add_task():
    # Obtener los datos a guardar 
    datos = request.get_json() # {"label": "Task", "done": false }
    
    # Preparamos los datos de la tarea a guardar
    task = Task()
    task.label = datos["label"]
    task.done = datos["done"]

    # INSERT INTO todos (label, done) VALUES (?,?)
    db.session.add(task)
    db.session.commit() # Guardamos en la base de datos definitivamente

    return jsonify(task.serialize()), 201

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_task(id):

    task = Task.query.get(id) # SELECT * FROM todos WHERE id = ? => <Task 1>

    if not task:
        return jsonify({ "error": "La tarea a eliminar no existe"}), 404
    
    db.session.delete(task) # DELETE FROM todos WHERE id=1
    db.session.commit() # Guardamos la eliminacion permanentemente

    return jsonify({ "success": "Tarea eliminada correctamente"}), 200

@app.route('/info/<int:user_id>', methods=['GET'])
def info_usuario(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "Usuario no existe"}), 404

    return jsonify(user.serialize()), 200


if __name__ == '__main__':
    app.run()