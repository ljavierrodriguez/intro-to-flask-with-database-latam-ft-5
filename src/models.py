from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

users_courses = db.Table(
    "users_courses",
    db.Column("users_id", db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column("courses_id", db.Integer, db.ForeignKey('courses.id'), primary_key=True),
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    # 1-1 Un usuario tiene un perfil
    profile = db.relationship('Profile', back_populates="user", uselist=False, cascade="all, delete-orphan")

    # 1-M Un usuario tiene muchas tareas
    todos = db.relationship('Task', back_populates="user", cascade="all, delete-orphan")

    # M-N Un usuario puede estar en muchos cursos
    courses = db.relationship('Course', secondary=users_courses, back_populates="users")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
        }

    def serialize_complete_info(self):
        return {
            "id": self.id,
            "email": self.email,
            "profile": {
                "bio": self.profile.bio,
                "github": self.profile.github
            },
            "todos": [task.serialize() for task in self.todos],
            "courses": [course.serialize() for course in self.courses]
        }

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text(), default="")
    github = db.Column(db.String(100), default="")
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # relationship back con usuarios
    user = db.relationship('User', back_populates="profile")

    def serialize(self):
        return {
            "id": self.id,
            "bio": self.bio,
            "github": self.github
        }
    
class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # M-N Un curso puede estar asociado a muchos usuarios
    users = db.relationship('User', secondary=users_courses, back_populates="courses")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Task(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # relationship back con usuarios
    user = db.relationship('User', back_populates="todos")

    def serialize(self):
        return {
            "id": self.id,
            "label": self.label,
            "done": self.done
        }

    """ 
    Nota: cualquier cambio que altere alguna column se debe generar nuevamente las migraciones 
    """
