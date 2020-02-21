from datetime import datetime, timedelta

import jwt
from flask import Blueprint, jsonify, make_response, render_template, request, session

from flask_app import app, mysqldb
from flask_app.models.mysql.user import User


@app.route('/api/register', methods=('POST',))
def register():
    data = request.get_json()
    user = User.find_user(**data)

    # TODO: ensure use is authenticated in session    

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

    # TODO: ensure use is authenticated in session

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
        user = User.find_user(**session)
        app.logger.info(f'Logging out user {user}')

        session['authenticated'] = False
        session.pop('username', None)
        session.pop('email', None)
    else:
        app.logger.info(f'User is not logged in')
    
    return 'Logged out.', 200

@app.route('/api/info', methods=('GET',))
def info():
    response = {
        'username': session.get('username'),
        'email': session.get('email'),
        'authenticated': session.get('authenticated')
    }

    return make_response(jsonify(response), 200)
