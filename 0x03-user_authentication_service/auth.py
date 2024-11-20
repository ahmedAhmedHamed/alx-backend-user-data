#!/usr/bin/env python3
"""auth module
"""
import uuid
from typing import Union

import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hash a password and return the bytes."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ return a string representation of a new UUID """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a new user. """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        hashed_password = _hash_password(password)
        user = self._db.add_user(email, hashed_password.decode('utf-8'))
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """ checks if credentials are valid. """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if bcrypt.checkpw(password.encode('utf-8'),
                          user.hashed_password.encode('utf-8')):
            return True
        return False

    def create_session(self, email: str) -> str:
        """ creates and returns the session ID as a string """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ gets a user given session id """
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ updates the corresponding user’s session ID to None """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return

    def get_reset_password_token(self, email: str) -> str:
        """ generates a reset password token """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token
