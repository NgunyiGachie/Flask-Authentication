from random import randint, choice as rc
from faker import Faker
from app import app
from models import db, User, Post

faker = Faker()

with app.app_context():
    print("Deleting all records...")
    User.query.delete()
    Post.query.delete()

    fake = Faker()

    print("Creating users....")
    users = []
    usernames = []
    emails = []

    for i in range(25):
        username = fake.first_name()
        
