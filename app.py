from flask import Flask
from flask_migrate import Migrate
from models import db, User, Post, Role

app = Flask(__name__)
app.secret_key = b'Y].D\xa3\x1e\xf9\xc40\xc5\x8e9\xce\x1d\x81\xedF/\xef\xd8\xed:\xef\xff'
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)