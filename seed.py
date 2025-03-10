from random import randint, choice as rc
from faker import Faker
from app import app
from models import db, User, Post, Role

faker = Faker()

with app.app_context():
    print("Deleting all records...")
    User.query.delete()
    Post.query.delete()
    Role.query.delete()

    fake = Faker()

    print("Creating roles....")
    roles = ['Admin', "Editor", "User"]
    role_objects = [Role(name=role) for role in roles]
    db.session.add_all(role_objects)
    db.session.commit()

    print("Creating users....")
    users = []
    usernames = set()
    emails = set()

    for _ in range(25):
        username = faker.unique.first_name()
        email = faker.unique.email()
        role = rc(role_objects)

        user = User(
            username=username,
            email=email,
            password_hash=faker.password(),
            role_id=role.id
        )
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    print("Creating posts...")
    posts = []

    for _ in range(50):
        post = Post(
            title=faker.sentence(),
            content=faker.text(),
            author_id=rc(users).id
        )
        posts.append(post)

    db.session.add_all(posts)
    db.session.commit()

    print("seedinf complete!")
