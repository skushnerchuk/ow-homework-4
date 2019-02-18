# -*- coding: utf-8 -*-

from application import db


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)


class Exchange(db.Model):

    __tablename__ = 'exchanges'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exchange_id = db.Column(db.Integer, nullable=False)
    api_key = db.Column(db.String(255), nullable=False)


class Token(db.Model):

    __tablename__ = 'tokens'

    def __init__(self):
        pass

    token_id = db.Column(db.String(50), primary_key=True)
    status = db.Column(db.SmallInteger)
