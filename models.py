from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from flask_security import UserMixin, RoleMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

app = Flask(__name__)
bcrypt = Bcrypt(app)
db = SQLAlchemy(metadata=metadata)

role_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

class User(db.Model, SerializerMixin, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    role = db.relationship('Role', secondary=role_users, backref='users')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles())

    def has_permission(self, required_permission):
        for role in self.roles:
            if role.permissions and required_permission in role.permissions.split(","):
                return True
        return False

    def __repr__(self):
        return f'User {self.id}'

class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    author = db.relationship('User', backref='posts')

    def __repr__(self):
        return f'Post {self.id} by {self.author.username}'

class Role(db.Model, SerializerMixin, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    permissions = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'Role {self.name}'