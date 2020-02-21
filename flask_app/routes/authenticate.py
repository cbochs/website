from datetime import datetime, timedelta

import jwt
from flask import Blueprint, jsonify, make_response, render_template, request, session

from flask_app import app, mysqldb
from flask_app.models.mysql.user import User


@app.route('/api/register', methods=('POST',))
def register():
    data = request.get_json()
    user = User.find_user(**data)

    # TODO: check the session that the user isn't already authenticated
    
    if user is None:
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
    data = request.get_json()
    user = User.authenticate(**data)

    # TODO: check the session that the user isn't already authenticated

    if user is None:
        app.logger.info(f'Failed to authenticate user')
        return make_response('Failed to authenticate.', 401)
    else:
        session['authenticated'] = True
        session['username'] = user.username
        session['email'] = user.email

        app.logger.info(f'Authenticated user {user}')
        return make_response('Authenticated.', 200)

@app.route('/api/logout', methods=('GET',))
def logout():
    authenticated = session.get('authenticated', False)
    if authenticated:
        session['authenticated'] = False
        session.pop('username', None)
        session.pop('email', None)
