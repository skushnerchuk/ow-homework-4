# -*- coding: utf-8 -*-

from os import environ as env

db_host = env.get('DB_HOST', '127.0.0.1')
db_password = env.get('DB_PASSWORD', '12345')
register_token = env.get('REGISTER_TOKEN', 'qjdfhqwldjf83902ydpawjedhf984')

SQLALCHEMY_DATABASE_URI = f'mysql://root:{db_password}@{db_host}/airtradex_protect'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = '1234567890'
