# module imports
from flask_sqlalchemy import SQLAlchemy

# create an instance of database to be used in the models
db = SQLAlchemy()


class User(db.Model):
    """
    The User model (table)
    """
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    last_name = db.Column('last_name', db.String(100))
    first_name = db.Column('first_name', db.String(100))

    def __init__(self, last_name, first_name):
        self.last_name = last_name
        self.first_name = first_name


class Email(db.Model):
    """
    The Email model (table)
    """
    __tablename__ = 'email'
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, mail, user_id):
        self.mail = mail
        self.user_id = user_id


class PhoneNumber(db.Model):
    """
    The PhoneNumber model (table)
    """
    __tablename__ = 'phone_number'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, number, user_id):
        self.phone = number
        self.user_id = user_id