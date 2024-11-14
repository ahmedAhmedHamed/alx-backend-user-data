#!/usr/bin/env python3
""" Module of session authentication class
"""
import os
import uuid

import flask
from flask import request

from models.user import User
from .auth import Auth


class SessionAuth(Auth):
    """ Session authentication class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a unique session for a user """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns user id based on session id """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns a User instance based on a cookie value """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None):
        if request is None:
            return False
        cookie = self.session_cookie(request)
        if not cookie:
            return False
        if not self.user_id_for_session_id(cookie):
            return False
        del SessionAuth.user_id_by_session_id[cookie]
        return True
