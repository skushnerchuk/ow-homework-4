from datetime import timedelta
from functools import wraps

from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_required, get_jwt_identity, verify_jwt_in_request

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
        user = User()
        user.email = user_info['email']
        user.password = generate_password_hash(user_info['password'])
        db.session.add(user)
        db.session.commit()
        return make_response({'status': 'ok'}, 200)
    except Exception as ex:
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
                'id': exchange.id,
                'api_key': exchange.api_key
            }
        )
    return make_response(result, 200)


@app.route('/register_exchange', methods=['POST'])
@auth_required
def register_exchange():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return make_response({'error': 'User not exists or not active'}, 404)
    exchange = Exchange()
    exchange.user_id = user_id
    exchange.exchange_id = request.json.get('exchange_id', None)
    exchange.api_key = request.json.get('api_key', None)
    try:
        db.session.add(exchange)
        db.session.commit()
    except IntegrityError as ex:
        if ex.orig.args[0] == 1062:
            return make_response({'error': 'Exchange already exists for this user'}, 500)
        return make_response({'error': '{}'.format(ex)}, 500)
    return 'OK', 200


if __name__ == '__main__':
    app.run(debug=True)
