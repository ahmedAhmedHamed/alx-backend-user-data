#!/usr/bin/env python3
""" Module of SessionExpAuth authentication class
"""
import os
import uuid
from datetime import datetime, timedelta

import flask
from flask import request

from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """ Sessiondb authentication class """
    def create_session(self, user_id=None):
        """ creates the session and saves it to storage """
        session_id = super().create_session(user_id)
        if user_id is None:
            return None
        user_session_kwargs = {'user_id:': user_id, 'session_id': session_id}
        user_session = UserSession(**user_session_kwargs)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ uses persistent storage to find the user id from the session """
        if session_id is None:
            return None
        UserSession.load_from_file()
        try:
            users = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if not users:
            return None
        user = users[0]
        start_time = user.created_at
        if ((start_time + timedelta(seconds=self.session_duration))
                < datetime.now()):
            return None
        return user.user_id

    def destroy_session(self, request=None):
        """ Destroys the session and removes it from the storage
            given a cookie.
         """
        cookie = self.session_cookie(request)
        if cookie is None:
            return False
        if not self.user_id_for_session_id(cookie):
            return False
        try:
            user_sessions = UserSession.search({'session_id': cookie})
        except Exception:
            return False
        if not user_sessions:
            return False
        user_session = user_sessions[0]
        try:
            user_session.remove()
            UserSession.save_to_file()
        except Exception:
            return False
        return True
