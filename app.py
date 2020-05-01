import os

from flask import Flask, jsonify, request
from passlib.hash import sha256_crypt
from marshmallow import ValidationError

import models
from models import User
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

db = models.init_app(app)
engine = models.create_tables(app)

jwt = JWTManager(app)

user_schema = models.UserSchema()


@app.route("/")
def status():
    connection_info = False
    try:
        db.engine.connect()
        connection_info = True
    except BaseException as e:
        app.logger.info(e)
    finally:
        if connection_info:
            database = 'Connected'
        else:
            database = 'Please check database connection'
        data = {
            'status': 'OK',
            'database': database
        }
        return jsonify(data), 200


@app.route('/api/user/<username>', methods=['GET'])
def get_username(username):
    item = User.query.filter_by(username=username).first()
    if item is not None:
        response = jsonify({'result': True})
    else:
        response = jsonify({'result': False}), 404
    return response


def check_username(username):
    item = User.query.filter_by(username=username).first()
    if item is not None:
        return True
    else:
        return False


def check_email(email):
    item = User.query.filter_by(email=email).first()
    if item is not None:
        return True
    else:
        return False


@app.route('/api/register', methods=['POST'])
def add_register():
    json_data = request.get_json(force=True)
    if not json_data:
        return {'message': 'No input data provided'}, 400

    try:
        data = user_schema.load(json_data)
    except ValidationError as errors:
        return jsonify({'ok': False, 'message': 'Bad request: {}'.format(errors)}), 422

    name = data['name']
    email = data['email']
    username = data['username']
    password = sha256_crypt.hash((data['password']))

    if check_email(email):
        return jsonify({'message': 'ops ! you already have an account with this email'})

    if check_username(username):
        return jsonify({'message': 'ops ! username has been taken'})

    try:
        user = User(
            email=email,
            name=name,
            password=password,
            username=username,
        )
        db.session.add(user)
        db.session.commit()
        response = jsonify({'message': 'User added', 'result': user_schema.dump(user)})
    except Exception as e:
        response = jsonify({'message': str(e)})

    return response


@app.route('/api/users', methods=['GET'])
def get_users():
    data = []
    for row in User.query.all():
        data.append(row.to_json())

    response = jsonify(data)

    return response


@app.route('/api/login', methods=['POST'])
def login():
    if request.is_json:
        username = request.json['username']
        password = request.json['password']
    else:
        username = request.form['username']
        password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user:
        if sha256_crypt.verify(password, user.password):
            token = create_access_token(identity=username)
            return jsonify(message='login completed', access_token=token)
        else:
            return jsonify(message='password doesn\'t match')
    else:
        return jsonify(message='no user found with this username')


@app.route('/api/profile', methods=['GET'])
@jwt_required
def get_profile():
    if request.is_json:
        username = request.json['username']
    else:
        username = request.form['username']
    item = User.query.filter_by(username=username).first()
    if item is not None:
        response = jsonify({'result': True})
    else:
        response = jsonify({'result': False}), 404

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
