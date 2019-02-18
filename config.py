# -*- coding: utf-8 -*-


def get_mysql_url():
    return 'mysql://root:12345@database/airtradex_protect'


SQLALCHEMY_DATABASE_URI = get_mysql_url()
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = '1234567890'
