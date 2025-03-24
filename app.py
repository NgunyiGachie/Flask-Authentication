from functools import wraps
from flask import Flask, make_response, jsonify, request, session
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import (JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
from models import db, User, Post, Role

app = Flask(__name__)
app.secret_key = b'Y].D\xa3\x1e\xf9\xc40\xc5\x8e9\xce\x1d\x81\xedF/\xef\xd8\xed:\xef\xff'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
db.init_app(app)

def require_role(role_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user or not user.has_role(role_name):
                return jsonify({"message": "Access denied. Insufficient permissions"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

class Register(Resource):

    def post(self):
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if User.query.filter_by(email=email).first():
            return {"message": "Email already exists"}, 400

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()

class Login(Resource):

    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return {"message": "Invalid credentials"}, 401

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return {"access_token": access_token, "refresh_token": refresh_token}, 200

class Profile(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return {"id": user.id, "username": user.username, "email": user.email}, 200

    @jwt_required()
    @require_role("admin")
    def patch(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        data = request.get_json()
        if "username" in data:
            user.username = data["username"]
        if "email" in data:
            user.email = data["email"]

        db.session.commit()
        return {"message": "Profile updated successfully"}, 200

class Logout(Resource):

    def delete(self):
        session['user_id'] = None
        return {'message': '204: No content'}, 204

class PostResource(Resource):

    def get(self):
        posts = Post.query.all()
        return jsonify([post.to_dict() for post in posts])

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.has_permission("write"):
            return jsonify({"message": "You do not have permission to create posts"}), 403
        data = request.get_json()
        new_post = Post(
            title=data["title"],
            content=data["content"],
            author_id=user.id
        )
        db.session.add(new_post)
        return jsonify({"message": "Post created successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)
