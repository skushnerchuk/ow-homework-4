# -*- coding: utf-8 -*-


def get_mysql_url():
    return 'mysql://root:12345@127.0.0.1/airtradex_protect'


def get_root_mysql_url():
    return 'mysql://root:12345@127.0.0.1'


SQLALCHEMY_DATABASE_URI = get_mysql_url()
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = '1234567890'
