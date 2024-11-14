import os

import flask
from flask import request

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
