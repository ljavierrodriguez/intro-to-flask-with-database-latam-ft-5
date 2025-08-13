import os
import datetime
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from models import db, Task, User, Profile, Course
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db.init_app(app) # vinculando el archivo models.py con mi app
Migrate(app, db) # db init, db migrate, db upgrade, db downgrade 
jwt = JWTManager(app)
CORS(app)

@app.route('/todos', methods=['GET'])
@jwt_required() # estamos indicando que esta ruta es privada y solo puede ser accedida por un usuario valido
def get_todos():
    # Buscamos todas las tareas existentes
    todos = Task.query.all() # SELECT * FROM todos => [<Task 1>, <Task 2>]

    # Convertir a diccionario cada uno de los objetos en la lista de tareas
    todos = [task.serialize() for task in todos]
    #todos = list(map(lambda task: task.convertir_a_dict(), todos))

    return jsonify(todos), 200

@app.route('/todos', methods=['POST'])
@jwt_required() # estamos indicando que esta ruta es privada y solo puede ser accedida por un usuario valido
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
@jwt_required() # estamos indicando que esta ruta es privada y solo puede ser accedida por un usuario valido
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

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    if not email:
        return jsonify({"error": "El email es requerido"}), 400
    if not password:
        return jsonify({"error": "El password es requerido"}), 400
    
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({ "error": "El email/password son incorrectos"}), 401

    if not check_password_hash(user.password, password):
        return jsonify({ "error": "El email/password son incorrectos"}), 401

    expires = datetime.timedelta(minutes=60)

    access_token = create_access_token(identity=str(user.id), expires_delta=expires)

    data = {
        "access_token": access_token,
        "user": user.serialize()
    }

    return jsonify({ "status": "success", "data": data }), 200
    
@app.route('/register', methods=['POST'])
def register():
    
    email = request.json.get("email")
    password = request.json.get("password")

    if not email:
        return jsonify({"error": "El email es requerido"}), 400
    if not password:
        return jsonify({"error": "El password es requerido"}), 400
    
    found = User.query.filter_by(email=email).first() # SELECT * FROM users WHERE email="" => <User 1>
    
    if found:
        return jsonify({ "error": "El email ya esta siendo utilizado"}), 400
    
    # Configuramos los datos del usuario
    user = User()
    user.email = email
    user.password = generate_password_hash(password) # Encripta la constraseña

    # Configuramos los datos del perfil
    profile = Profile()

    # Asociamos el perfil al usuario a traves del relationship
    user.profile = profile

    # Guardamos el usuario
    db.session.add(user)
    db.session.commit()

    return jsonify({ "success":"Registro exitoso"}), 200

@app.route('/profile', methods=['GET'])
@jwt_required() # estamos indicando que esta ruta es privada y solo puede ser accedida por un usuario valido
def profile():
    id = get_jwt_identity() # Obtenemos el id del usuario que esta haciendo la petision
    user = User.query.get(id) # Buscamos al usuario
    return jsonify(user.serialize_complete_info()), 200


if __name__ == '__main__':
    app.run()