from os import environ as env


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '!"*%*:%;lksadoufhlkbqw(^^%&*(*&'
    UPLOAD_FOLDER = 'static/uploads/'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    DEBUG = True
    db_host = env.get('DB_HOST', '172.17.0.2')
    db_password = env.get('DB_PASSWORD', '1')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:{}@{}/online_store'.format(db_password, db_host)
    DEBUG = bool(env.get('DEBUG', False))
