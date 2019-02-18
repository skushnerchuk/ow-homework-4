from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from application import app, db
from database_manager import prepare_database
from models import User, Exchange


prepare_database()


@app.route('/register_user', methods=['POST'])
def register_user():
    try:
        user_info = request.json
        user = User()
        user.email = user_info['email']
        user.password = generate_password_hash(user_info['password'])
        db.session.add(user)
        db.session.commit()
        return 'Registered', 200
    except Exception as ex:
        return 'Register error:{}'.format(ex), 500


@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(email=email).first()
    if not user:
        return "User not exists", 404
    if not check_password_hash(user.password, password):
        return "Incorrect password", 400
    ret = {'access_token': create_access_token(identity=user.id, fresh=True)}
    return jsonify(ret), 200


@app.route('/get_exchange_keys', methods=['POST'])
@jwt_required
def get_exchange_key():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return 'User not found.', 404
    exchanges = Exchange.query.filter_by(user_id=user_id).all()
    result = []
    for exchange in exchanges:
        result.append(
            {
                'id': exchange.id,
                'api_key': exchange.api_key
            }
        )
    return jsonify(result), 200


@app.route('/register_exchange', methods=['POST'])
@jwt_required
def register_exchange():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return 'User not found.', 404
    exchange = Exchange()
    exchange.user_id = user_id
    exchange.exchange_id = request.json.get('exchange_id', None)
    exchange.api_key = request.json.get('api_key', None)
    try:
        db.session.add(exchange)
        db.session.commit()
    except IntegrityError as ex:
        if ex.orig.args[0] == 1062:
            return 'Exchange already exists for this user'.format(ex), 500
        return '{}'.format(ex), 500
    return 'OK', 200


if __name__ == '__main__':
    app.run(debug=True)
