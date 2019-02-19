from datetime import timedelta
from functools import wraps

from flask import request
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError, OperationalError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request

from application import app, db
from database_manager import prepare_database
from models import User, Exchange
from responses import make_response


prepare_database()


def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except:
            return make_response({'error': 'Auth required'}, 403)
        return fn(*args, **kwargs)
    return wrapper


def get_user_id(email, password):
    user = User.query.filter_by(email=email, active=True).first()
    if not user:
        return None
    if not check_password_hash(user.password, password):
        return None
    return user.id


def user_exists(user_id):
    user = User.query.filter_by(id=user_id, active=True).first()
    if not user:
        return False
    return True


@app.route('/register_user', methods=['POST'])
def register_user():
    try:
        user_info = request.json
        register_token = user_info.get('token', None)
        if register_token != 'qjdfhqwldjf83902ydpawjedhf984':
            return make_response({'status': 'ok'}, 200)
        user = User()
        user.email = user_info.get('email', None)
        user.password = generate_password_hash(user_info.get('password', None))
        db.session.add(user)
        db.session.commit()
        return make_response({'status': 'ok'}, 200)
    except (IntegrityError, OperationalError) as ex:
        if ex.orig.args[0] == 1062:
            return make_response({'error': 'Email already registered'}, 500)
        return make_response({'error': '{}'.format(ex)}, 500)


@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user_id = get_user_id(email, password)
    if not user_id:
        return make_response({'error': 'User not exists or not active'}, 404)
    expires = timedelta(days=365)
    ret = {'access_token': create_access_token(identity=user_id, fresh=True, expires_delta=expires)}
    return make_response(ret, 200)


@app.route('/get_exchange_keys', methods=['GET'])
@auth_required
def get_exchange_key():
    user_id = get_jwt_identity()
    if not user_exists(user_id):
        return make_response({'error': 'User not found.'}, 404)
    exchanges = Exchange.query.filter_by(user_id=user_id).all()
    result = []
    for exchange in exchanges:
        result.append(
            {
                'exchange_id': exchange.exchange_id,
                'api_key': exchange.api_key
            }
        )
    return make_response(result, 200)


@app.route('/register_exchange', methods=['POST'])
@auth_required
def register_exchange():
    exchange_id = request.json.get('exchange_id', None)
    api_key = request.json.get('api_key', None)
    if not exchange_id or not api_key:
        return make_response({'error': 'Incorrect request'}, 400)
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return make_response({'error': 'User not exists or not active'}, 404)
    exchange = Exchange.query.filter(and_(Exchange.user_id == user_id, Exchange.exchange_id == exchange_id)).first()
    if not exchange:
        exchange = Exchange()
    exchange.user_id = user_id
    exchange.exchange_id = exchange_id
    exchange.api_key = api_key
    if not exchange.exchange_id or not exchange.api_key:
        return make_response({'error': 'Incorrect request'}, 400)
    try:
        db.session.add(exchange)
        db.session.commit()
    except (IntegrityError, OperationalError) as ex:
        if ex.orig.args[0] == 1062:
            return make_response({'error': 'Exchange already exists for this user'}, 500)
        return make_response({'error': '{}'.format(ex)}, 500)
    return make_response({'status': 'ok'}, 200)


@app.route('/delete_exchange', methods=['POST'])
@auth_required
def delete_exchange():
    exchange_id = request.json.get('exchange_id', None)
    if not exchange_id:
        return make_response({'error': 'Incorrect request'}, 400)
    try:
        user_id = get_jwt_identity()
        Exchange.query.filter(and_(Exchange.user_id == user_id, Exchange.exchange_id == exchange_id)).delete()
        db.session.commit()
    except (IntegrityError, OperationalError) as ex:
        if ex.orig.args[0] == 1062:
            return make_response({'error': 'Exchange delete error'}, 500)
        return make_response({'error': '{}'.format(ex)}, 500)
    return make_response({'status': 'ok'}, 200)


if __name__ == '__main__':
    app.run(debug=True)
