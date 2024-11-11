#!/usr/bin/env python3
""" Module of authentication class
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """ class for authentication handling
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require auth """
        return False

    def authorization_header(self, request: request=None) -> str:
        """ authorization header """
        return None

    def current_user(self, request: request=None) -> TypeVar('User'):
        """ current user """
        return None
