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
    roles_data = [
        {"name": "Admin", "permissions": "create, read, update, delete"},
        {"name": "Editor", "permissions": "create, read, update"},
        {"name": "User", "permissions": "read"}
    ]
    roles = [Role(name=data["name"], permissions=data["permissions"]) for data in roles_data]
    db.session.add_all(roles)
    db.session.commit()

    print("Creating users....")
    users = []
    usernames = set()
    emails = set()

    for _ in range(25):
        username = faker.unique.first_name()
        email = faker.unique.email()
        role = rc(roles).id

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

    print("seeding complete!")
