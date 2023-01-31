from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

# create Models based off our ERD

wishlist = db.Table('wishlist',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('books_id', db.Integer, db.ForeignKey('books.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False, unique=True)
    email = db.Column(db.String(250), nullable = False, unique = True)
    password = db.Column(db.String(250), nullable=False)
    wishing = db.relationship('Books',
        primaryjoin = (wishlist.columns.user_id==id),
        secondaryjoin = (wishlist.columns.books_id==id),
        secondary=wishlist,
        backref='wishlists',
        lazy='dynamic'
        )

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def add(self,wishing, books_id):
        self.wishing.append(books_id)
        db.session.commit()


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cover_edition_key = db.Column(db.Integer)
    title = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String)
    cover_img = db.Column(db.String)

    def __init__(self, id, cover_edition_key, title, author, cover_img):
        self.id = id
        self.cover_edition_key = cover_edition_key
        self.title = title
        self.author = author
        self.cover_img = cover_img

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()



    