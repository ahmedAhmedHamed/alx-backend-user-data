#!/usr/bin/env python3
""" Module of SessionExpAuth authentication class
"""
import os
import uuid
from datetime import datetime, timedelta

import flask
from flask import request

from models.user import User
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session authentication class """

    def __init__(self):
        """ Constructor of SessionExpAuth class """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """overloaded session creation"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {'user_id': user_id,
                              'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ overloaded user_id for session id """
        if session_id is None:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
        if session_dictionary.get('created_at') is None:
            return None

        if (session_dictionary.get('created_at')
                + timedelta(seconds=self.session_duration)
                < datetime.now()):
            return None
        return session_dictionary.get('user_id')
