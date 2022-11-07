from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20), nullable=False,  unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    favorites =db.relationship("Favorites", backref="user", cascade="all, delete-orphan")

    @classmethod
    def register(cls, username, email, password):
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = cls(username=username, password=hashed_pwd, email=email)
        db.session.add(user)

        return user

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        else:
            return False

class Favorites(db.Model):

     __tablename__ = "favorites"
     id = db.Column(db.Integer,primary_key=True,autoincrement=True)
     user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
     parkcode = db.Column(db.Text, nullable=False)
