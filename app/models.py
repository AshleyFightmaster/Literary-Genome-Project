from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

# create Models based off our ERD
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False, unique=True)
    email = db.Column(db.String(250), nullable = False, unique = True)
    password = db.Column(db.String(250), nullable=False)
    favorites = db.relationship('Favorites', backref = 'user', lazy=True)
    wishlist = db.relationship('Wishlist', backref = 'user', lazy=True)
    dislikes = db.relationship('Dislikes', backref = 'user', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    books_id = db.Column(db.String(50), db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# favorites = db.Table(
#     'favorites',
#     db.Column(db.String(50), db.ForeignKey('books.id'), nullable=False)
#     db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# )

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    books_id = db.Column(db.String(50), db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

# wishlist = db.Table(
#     'wishlist',
#     db.Column(db.String(50), db.ForeignKey('books.id'), nullable=False)
#     db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# )

class Dislikes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    books_id = db.Column(db.String(50), db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# dislikes = db.Table(
#     'dislikes',
#     db.Column(db.String(50), db.ForeignKey('books.id'), nullable=False)
#     db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# )


class Books(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    key = db.Column(db.Integer)
    title = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String)
    cover_img = db.Column(db.String)
    favorites = db.relationship('Favorites', lazy=True)
    wishlist = db.relationship('Wishlist', lazy=True)
    dislikes = db.relationship('Dislikes', lazy=True)

    def __init__(self, id, key, title, author, cover_img):
        self.id = id
        self.key = key
        self.title = title
        self.author = author
        self.cover_img = cover_img

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    