#!/usr/bin/env python3
""" Session authentication routes
"""
import os

import flask
from flask import request, abort

from api.v1.views import app_views
from models.user import User


@app_views.route('auth_session/login', methods=['POST'], strict_slashes=False)
def login_path():
    """ login path
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return flask.jsonify({"error": "email missing"}), 400
    if not password:
        return flask.jsonify({"error": "password missing"}), 400
    try:
        users: User = User.search({"email": email})
    except Exception:
        return flask.jsonify({"error": "no user found for this email"}), 404
    if not users:
        return flask.jsonify({"error": "no user found for this email"}), 404
    current_user = None
    for user in users:
        if user.is_valid_password(password):
            current_user = user
    if not current_user:
        return flask.jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(current_user.id)
    ret = flask.jsonify(current_user.to_json())
    ret.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return ret

@app_views.route('auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout_path():
    """ logout path """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return flask.jsonify({}), 200
    return False, abort(404)
