# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
jwt = JWTManager(app)
