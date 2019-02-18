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
    __table_args__ = (db.UniqueConstraint('user_id', 'exchange_id', name='exchange_unique'),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
                        nullable=False)
    exchange_id = db.Column(db.Integer, nullable=False, unique=False)
    api_key = db.Column(db.String(255), nullable=False)
