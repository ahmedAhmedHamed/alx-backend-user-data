#!/usr/bin/env python3
""" Module of authentication class
"""
import os
from typing import List, TypeVar
from flask import request


class Auth:
    """ class for authentication handling
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns True if the path is not
        in the list of strings excluded_paths """
        if path is None or not excluded_paths:
            return True
        path_cpy = path[:]
        if path_cpy[-1] != '/':
            path_cpy += '/'
        for path in excluded_paths:
            if path[-1] == '*':
                temp_path = path[:-1]
                if path_cpy.startswith(temp_path):
                    return False
            else:
                if path == path_cpy:
                    return False
        return True

    def authorization_header(self, request: request = None) -> str:
        """ authorization header """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request: request = None) -> TypeVar('User'):
        """ current user """
        return None

    def session_cookie(self, request=None):
            """ returns a cookie value from a request """
            if request is None:
                return None
            cookie_name = os.getenv('SESSION_NAME', '_my_session_id')
            return request.cookies.get(cookie_name)
