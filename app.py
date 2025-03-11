from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, User, Post, Role

app = Flask(__name__)
app.secret_key = b'Y].D\xa3\x1e\xf9\xc40\xc5\x8e9\xce\x1d\x81\xedF/\xef\xd8\xed:\xef\xff'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

class Login(Resource):

    def post(self):
        user = User.query.filter(User.username == request.get_json()['username'])
        session['user_id'] = user.id
        return user.to_dict()

class Logout(Resource):

    def delete(self):
        session['user_id'] = None
        return {'message': '204: No content'}, 204
