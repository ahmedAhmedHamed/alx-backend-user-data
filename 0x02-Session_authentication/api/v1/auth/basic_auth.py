#!/usr/bin/env python3
""" Module of basic authentication class
"""
import base64
from typing import TypeVar
from models.user import User
from models.base import DATA
from .auth import Auth


class BasicAuth(Auth):
    """ Basic authentication class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ extracts the base64 part of a basic authorization header """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           b64_auth_header: str) -> str:
        """ decodes the base64 part of a basic authorization header """
        if b64_auth_header is None:
            return None
        if not isinstance(b64_auth_header, str):
            return None
        try:
            b64_auth_header = b64_auth_header.encode('utf-8')
            decodedb64 = base64.b64decode(b64_auth_header)
        except Exception as e:
            return None
        try:
            return decodedb64.decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str) -> (
                                    str, str):
        """returns the user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password."""
        if user_email is None or user_pwd is None:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            users: User = User.search({"email": user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ gets the current user from authorization header """
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None
        authorization_header = (
            self.extract_base64_authorization_header(authorization_header))
        if authorization_header is None:
            return None
        authorization_header = (
            self.decode_base64_authorization_header(authorization_header))
        if authorization_header is None:
            return None
        username, password = (
            self.extract_user_credentials(authorization_header))
        if username is None or password is None:
            return None
        user = self.user_object_from_credentials(username, password)
        return user
