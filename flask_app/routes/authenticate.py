from datetime import datetime, timedelta

import jwt
from flask import Blueprint, jsonify, make_response, render_template, request, session

from flask_app import app, mysqldb
from flask_app.models.mysql.user import User


@app.route('/api/register', methods=('POST',))
def register():
    user = User.find_user(id=session.get('user_id'))
    if user:
        app.logger.info(f'User is already registered and logged in {user}')
        return make_response('Already authenticated.', 304)

    data = request.get_json()
    user = User.find_user(**data)

    if not user:
        user = User(**data)
        mysqldb.session.add(user)
        mysqldb.session.commit()

        app.logger.info(f'Created new user {user}')
        return make_response('User created.', 201)
    else:
        app.logger.info(f'User already exists {user}')
        return make_response('User already exists.', 304)


@app.route('/api/login', methods=('POST',))
def login():
    user = User.find_user(id=session.get('user_id'))
    if user:
        app.logger.info(f'User is already logged in {user}')
        return make_response('Already authenticated.', 304)

    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        app.logger.info(f'Failed to authenticate user')
        return make_response('Failed to authenticate.', 401)
    else:
        session.pop('spotify_id')
        session['user_id'] = user.id
        app.logger.info(f'Authenticated user {user}')
        return make_response('Authenticated.', 200)


@app.route('/api/logout', methods=('GET',))
def logout():
    user = User.find_user(id=session.get('user_id'))
    if not user:
        app.logger.info(f'User is not logged in')
        return make_response('Unauthenticated.', 401)

    app.logger.info(f'Logging out user {user}')
    session.clear()
    return make_response('Logged out.', 200)



@app.route('/api/user', methods=('GET',))
def current_user():
    user = User.find_user(id=session.get('user_id'))
    if not user:
        return make_response('Unauthenticated.', 401)

    app.logger.info(user)
    return make_response(jsonify({
        'user_id': user.id,
        'username': user.username,
        'email': user.email
    }), 200)
